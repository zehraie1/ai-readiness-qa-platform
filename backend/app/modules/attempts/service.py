"""Attempt lifecycle: start (idempotent per P1), save answers, review, atomic idempotent submit."""

import logging
import uuid
from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.errors import AppError, ErrorCode
from app.modules.attempts.models import (
    STATUS_IN_PROGRESS,
    STATUS_SUBMITTED,
    AssessmentAttempt,
    AttemptAnswer,
    AttemptQuestion,
)
from app.modules.attempts.schemas import (
    AnswerOut,
    AttemptListOut,
    AttemptOut,
    AttemptQuestionOut,
    AttemptSummaryOut,
    OptionOut,
    ReviewItemOut,
    ReviewOut,
    VersionsOut,
)
from app.modules.auth.models import User
from app.modules.content.models import (
    Question,
    QuestionBankVersion,
    QuestionRevision,
    RecommendationRule,
    TemplateQuestion,
)
from app.modules.content.repository import published_template
from app.modules.results.schemas import ResultOut
from app.modules.results.service import compute_and_store, load_result
from app.modules.scoring.models import ScoreResult, ScoringPolicy
from app.modules.tracks.models import AssessmentTrack

logger = logging.getLogger("app.attempts")
TOTAL_QUESTIONS = 20


def _not_found() -> AppError:
    # P3: identical response for "does not exist" and "belongs to someone else".
    return AppError(404, ErrorCode.ATTEMPT_NOT_FOUND, "Attempt not found.")


def _in_progress(db: Session, user_id: uuid.UUID, track_id: str) -> AssessmentAttempt | None:
    return db.scalar(
        select(AssessmentAttempt).where(
            AssessmentAttempt.participant_id == user_id,
            AssessmentAttempt.track_id == track_id,
            AssessmentAttempt.status == STATUS_IN_PROGRESS,
        )
    )


def load_owned(db: Session, user: User, attempt_id: uuid.UUID, lock: bool = False) -> AssessmentAttempt:
    stmt = select(AssessmentAttempt).where(
        AssessmentAttempt.id == attempt_id, AssessmentAttempt.participant_id == user.id
    )
    if lock:
        stmt = stmt.with_for_update()
    attempt = db.scalar(stmt.execution_options(populate_existing=True))
    if attempt is None:
        raise _not_found()
    return attempt


def _validate_composition(rows, track_id: str) -> bool:
    positions = [r.position for r in rows]
    common = [r for r in rows if r.category == "common"]
    role = [r for r in rows if r.category == "role_specific"]
    return (
        len(rows) == TOTAL_QUESTIONS
        and positions == list(range(1, TOTAL_QUESTIONS + 1))
        and len({r.question_id for r in rows}) == TOTAL_QUESTIONS
        and len(common) == 10
        and len(role) == 10
        and all(r.scope == "common" and r.track_id is None for r in common)
        and all(r.scope == "role_specific" and r.track_id == track_id for r in role)
    )


def start_attempt(db: Session, user: User, track_id: str) -> tuple[AssessmentAttempt, bool]:
    if db.get(AssessmentTrack, track_id) is None:
        raise AppError(404, ErrorCode.TRACK_NOT_FOUND, "Assessment track not found.")
    existing = _in_progress(db, user.id, track_id)
    if existing is not None:
        return existing, False

    template = published_template(db, track_id)
    if template is None:
        raise AppError(409, ErrorCode.NO_PUBLISHED_TEMPLATE, "No published assessment for this track.")
    rows = db.execute(
        select(
            TemplateQuestion.position,
            TemplateQuestion.category,
            QuestionRevision.id.label("revision_id"),
            Question.id.label("question_id"),
            Question.scope,
            Question.track_id,
        )
        .join(QuestionRevision, QuestionRevision.id == TemplateQuestion.question_revision_id)
        .join(Question, Question.id == QuestionRevision.question_id)
        .where(TemplateQuestion.template_id == template.id)
        .order_by(TemplateQuestion.position)
    ).all()
    if not _validate_composition(rows, track_id):
        logger.error("Template %s for track %s failed 10+10 composition check", template.id, track_id)
        raise AppError(409, ErrorCode.NO_PUBLISHED_TEMPLATE, "No valid published assessment for this track.")

    policy = db.scalar(
        select(ScoringPolicy)
        .where(ScoringPolicy.status == "approved")
        .order_by(ScoringPolicy.created_at.desc())
        .limit(1)
    )
    if policy is None:
        raise AppError(409, ErrorCode.NO_SCORING_POLICY, "No approved scoring policy is available.")
    rec_version = db.scalar(
        select(RecommendationRule.version_label)
        .where(RecommendationRule.status == "active")
        .order_by(RecommendationRule.created_at.desc())
        .limit(1)
    )

    try:
        with db.begin_nested():
            attempt = AssessmentAttempt(
                participant_id=user.id,
                track_id=track_id,
                template_id=template.id,
                bank_version_id=template.bank_version_id,
                scoring_policy_id=policy.id,
                recommendation_rule_version=rec_version,
                status=STATUS_IN_PROGRESS,
            )
            db.add(attempt)
            db.flush()
            db.add_all(
                AttemptQuestion(
                    attempt_id=attempt.id,
                    position=r.position,
                    question_id=r.question_id,
                    question_revision_id=r.revision_id,
                    category=r.category,
                )
                for r in rows
            )
            db.flush()
    except IntegrityError:
        # A concurrent start won the race on the one-in-progress partial unique index.
        existing = _in_progress(db, user.id, track_id)
        if existing is None:
            raise
        return existing, False
    db.commit()
    db.refresh(attempt)
    return attempt, True


def _answered_count(db: Session, attempt_id: uuid.UUID) -> int:
    return db.scalar(select(func.count()).where(AttemptAnswer.attempt_id == attempt_id)) or 0


def attempt_detail(db: Session, attempt: AssessmentAttempt) -> AttemptOut:
    rows = db.execute(
        select(
            AttemptQuestion,
            QuestionRevision.prompt,
            QuestionRevision.options_json,
            AttemptAnswer.selected_option_id,
        )
        .join(QuestionRevision, QuestionRevision.id == AttemptQuestion.question_revision_id)
        .outerjoin(AttemptAnswer, AttemptAnswer.attempt_question_id == AttemptQuestion.id)
        .where(AttemptQuestion.attempt_id == attempt.id)
        .order_by(AttemptQuestion.position)
    ).all()
    bank = db.get(QuestionBankVersion, attempt.bank_version_id)
    policy = db.get(ScoringPolicy, attempt.scoring_policy_id)
    track = db.get(AssessmentTrack, attempt.track_id)
    questions = [
        AttemptQuestionOut(
            question_id=aq.question_id,
            position=aq.position,
            category=aq.category,
            prompt=prompt,
            options=[OptionOut(id=o["id"], text=o["text"]) for o in options],
            selected_option_id=selected,
        )
        for aq, prompt, options, selected in rows
    ]
    return AttemptOut(
        id=attempt.id,
        track_id=track.id,
        track_name=track.name,
        status=attempt.status,
        started_at=attempt.started_at,
        submitted_at=attempt.submitted_at,
        total_questions=len(questions),
        answered_count=sum(q.selected_option_id is not None for q in questions),
        content_provenance=bank.content_provenance,
        versions=VersionsOut(
            question_bank=bank.version_label,
            scoring_policy=policy.version_label,
            recommendation_rules=attempt.recommendation_rule_version,
        ),
        questions=questions,
    )


def save_answer(
    db: Session, user: User, attempt_id: uuid.UUID, question_id: uuid.UUID, option_id: str
) -> AnswerOut:
    attempt = load_owned(db, user, attempt_id, lock=True)
    if attempt.status != STATUS_IN_PROGRESS:
        raise AppError(409, ErrorCode.ATTEMPT_CLOSED, "This attempt has been submitted and cannot change.")
    row = db.execute(
        select(AttemptQuestion, QuestionRevision.options_json)
        .join(QuestionRevision, QuestionRevision.id == AttemptQuestion.question_revision_id)
        .where(AttemptQuestion.attempt_id == attempt.id, AttemptQuestion.question_id == question_id)
    ).first()
    if row is None:
        raise AppError(404, ErrorCode.QUESTION_NOT_IN_ATTEMPT, "Question is not part of this attempt.")
    aq, options = row
    valid = [o["id"] for o in options]
    if option_id not in valid:
        raise AppError(
            422,
            ErrorCode.INVALID_OPTION,
            "Selected option is not valid for this question.",
            {"allowed_option_ids": valid},
        )
    now = datetime.now(UTC)
    stmt = pg_insert(AttemptAnswer).values(
        attempt_question_id=aq.id,
        attempt_id=attempt.id,
        selected_option_id=option_id,
        created_at=now,
        updated_at=now,
    )
    db.execute(
        stmt.on_conflict_do_update(
            index_elements=[AttemptAnswer.attempt_question_id],
            set_={"selected_option_id": option_id, "updated_at": now},
        )
    )
    attempt.updated_at = now
    db.flush()
    count = _answered_count(db, attempt.id)
    db.commit()
    return AnswerOut(
        question_id=question_id, selected_option_id=option_id, answered_count=count, updated_at=now
    )


def review(db: Session, user: User, attempt_id: uuid.UUID) -> ReviewOut:
    attempt = load_owned(db, user, attempt_id)
    rows = db.execute(
        select(AttemptQuestion.position, AttemptQuestion.question_id, AttemptAnswer.attempt_question_id)
        .outerjoin(AttemptAnswer, AttemptAnswer.attempt_question_id == AttemptQuestion.id)
        .where(AttemptQuestion.attempt_id == attempt.id)
        .order_by(AttemptQuestion.position)
    ).all()
    items = [ReviewItemOut(position=p, question_id=q, answered=a is not None) for p, q, a in rows]
    return ReviewOut(
        attempt_id=attempt.id,
        status=attempt.status,
        total=len(items),
        answered=sum(i.answered for i in items),
        unanswered_positions=[i.position for i in items if not i.answered],
        items=items,
    )


def list_attempts(db: Session, user: User, status: str | None, limit: int, offset: int) -> AttemptListOut:
    base = select(AssessmentAttempt).where(AssessmentAttempt.participant_id == user.id)
    if status:
        base = base.where(AssessmentAttempt.status == status)
    total = db.scalar(select(func.count()).select_from(base.subquery())) or 0
    attempts = db.scalars(
        base.order_by(AssessmentAttempt.started_at.desc(), AssessmentAttempt.id).limit(limit).offset(offset)
    ).all()
    ids = [a.id for a in attempts]
    tracks = {t.id: t.name for t in db.scalars(select(AssessmentTrack))}
    answered: dict[uuid.UUID, int] = (
        dict(
            db.execute(
                select(AttemptAnswer.attempt_id, func.count())
                .where(AttemptAnswer.attempt_id.in_(ids))
                .group_by(AttemptAnswer.attempt_id)
            ).all()
        )
        if ids
        else {}
    )
    first_unanswered: dict[uuid.UUID, int] = (
        dict(
            db.execute(
                select(AttemptQuestion.attempt_id, func.min(AttemptQuestion.position))
                .outerjoin(AttemptAnswer, AttemptAnswer.attempt_question_id == AttemptQuestion.id)
                .where(AttemptQuestion.attempt_id.in_(ids), AttemptAnswer.attempt_question_id.is_(None))
                .group_by(AttemptQuestion.attempt_id)
            ).all()
        )
        if ids
        else {}
    )
    scores = (
        {r.attempt_id: r for r in db.scalars(select(ScoreResult).where(ScoreResult.attempt_id.in_(ids)))}
        if ids
        else {}
    )
    items = [
        AttemptSummaryOut(
            id=a.id,
            track_id=a.track_id,
            track_name=tracks.get(a.track_id, a.track_id),
            status=a.status,
            started_at=a.started_at,
            submitted_at=a.submitted_at,
            total_questions=TOTAL_QUESTIONS,
            answered_count=answered.get(a.id, 0),
            first_unanswered_position=first_unanswered.get(a.id),
            overall_score=scores[a.id].overall_score if a.id in scores else None,
            readiness_band=scores[a.id].readiness_band if a.id in scores else None,
        )
        for a in attempts
    ]
    return AttemptListOut(items=items, total=total, limit=limit, offset=offset)


def submit(db: Session, user: User, attempt_id: uuid.UUID) -> ResultOut:
    """Atomic and idempotent (P5): the row lock serialises concurrent submits; a repeat returns
    the stored result; UNIQUE(score_results.attempt_id) is the final backstop."""
    attempt = load_owned(db, user, attempt_id, lock=True)
    if attempt.status == STATUS_SUBMITTED:
        result = load_result(db, attempt)
        db.commit()
        return result
    rv = review(db, user, attempt_id)
    if rv.unanswered_positions:
        raise AppError(
            409,
            ErrorCode.ATTEMPT_INCOMPLETE,
            "All questions must be answered before submission.",
            {"unanswered_positions": rv.unanswered_positions},
        )
    compute_and_store(db, attempt)
    attempt.status = STATUS_SUBMITTED
    attempt.submitted_at = datetime.now(UTC)
    db.flush()
    result = load_result(db, attempt)
    db.commit()
    return result


def results_for(db: Session, user: User, attempt_id: uuid.UUID) -> ResultOut:
    attempt = load_owned(db, user, attempt_id)
    if attempt.status != STATUS_SUBMITTED:
        raise AppError(409, ErrorCode.RESULTS_NOT_AVAILABLE, "Results are available after submission.")
    return load_result(db, attempt)
