"""Read-only dashboard aggregates. Participants see only their own data; admins see aggregates only."""

import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.attempts.models import (
    STATUS_IN_PROGRESS,
    STATUS_SUBMITTED,
    AssessmentAttempt,
    AttemptAnswer,
    AttemptQuestion,
)
from app.modules.auth.models import ROLE_PARTICIPANT, User
from app.modules.content.models import (
    AssessmentTemplate,
    Competency,
    Question,
    QuestionBankVersion,
    QuestionRevision,
    TemplateQuestion,
)
from app.modules.content.repository import published_bank
from app.modules.dashboard.schemas import (
    AdminSummaryOut,
    CompetencySnapshotOut,
    CountOut,
    HistoryPointOut,
    LatestResultOut,
    ParticipantSummaryOut,
    PublishedBankOut,
    TrackAggregateOut,
    TrackStatusOut,
)
from app.modules.scoring.models import CompetencyScore, ScoreResult, ScoringPolicy
from app.modules.tracks.models import AssessmentTrack

BANDS = [
    ("foundation", "Foundation"),
    ("developing", "Developing"),
    ("proficient", "Proficient"),
    ("advanced", "Advanced"),
]


def participant_summary(db: Session, user: User) -> ParticipantSummaryOut:
    tracks = list(db.scalars(select(AssessmentTrack).order_by(AssessmentTrack.sort_order)))
    submitted = db.execute(
        select(AssessmentAttempt, ScoreResult, QuestionBankVersion.version_label, ScoringPolicy.version_label)
        .join(ScoreResult, ScoreResult.attempt_id == AssessmentAttempt.id)
        .join(QuestionBankVersion, QuestionBankVersion.id == AssessmentAttempt.bank_version_id)
        .join(ScoringPolicy, ScoringPolicy.id == ScoreResult.scoring_policy_id)
        .where(AssessmentAttempt.participant_id == user.id, AssessmentAttempt.status == STATUS_SUBMITTED)
        .order_by(AssessmentAttempt.submitted_at, AssessmentAttempt.id)
    ).all()
    in_progress = {
        a.track_id: a
        for a in db.scalars(
            select(AssessmentAttempt).where(
                AssessmentAttempt.participant_id == user.id,
                AssessmentAttempt.status == STATUS_IN_PROGRESS,
            )
        )
    }
    ip_ids = [a.id for a in in_progress.values()]
    answered: dict[uuid.UUID, int] = {}
    first_unanswered: dict[uuid.UUID, int] = {}
    if ip_ids:
        answered = dict(
            db.execute(
                select(AttemptAnswer.attempt_id, func.count())
                .where(AttemptAnswer.attempt_id.in_(ip_ids))
                .group_by(AttemptAnswer.attempt_id)
            ).all()
        )
        first_unanswered = dict(
            db.execute(
                select(AttemptQuestion.attempt_id, func.min(AttemptQuestion.position))
                .outerjoin(AttemptAnswer, AttemptAnswer.attempt_question_id == AttemptQuestion.id)
                .where(AttemptQuestion.attempt_id.in_(ip_ids), AttemptAnswer.attempt_question_id.is_(None))
                .group_by(AttemptQuestion.attempt_id)
            ).all()
        )

    names = {t.id: t.name for t in tracks}
    statuses: list[TrackStatusOut] = []
    for t in tracks:
        done = [(a, r) for a, r, _, _ in submitted if a.track_id == t.id]
        ip = in_progress.get(t.id)
        latest = done[-1] if done else None
        statuses.append(
            TrackStatusOut(
                track_id=t.id,
                track_name=t.name,
                status="in_progress" if ip else ("completed" if done else "not_started"),
                in_progress_attempt_id=ip.id if ip else None,
                resume_position=first_unanswered.get(ip.id) if ip else None,
                answered_count=answered.get(ip.id, 0) if ip else 0,
                attempts_completed=len(done),
                latest_score=latest[1].overall_score if latest else None,
                best_score=max(r.overall_score for _, r in done) if done else None,
                latest_band=latest[1].readiness_band if latest else None,
                latest_attempt_id=latest[0].id if latest else None,
            )
        )

    latest_result = None
    if submitted:
        a, r, _, _ = submitted[-1]
        comps = db.execute(
            select(CompetencyScore, Competency)
            .join(Competency, Competency.id == CompetencyScore.competency_id)
            .where(CompetencyScore.score_result_id == r.id)
            .order_by(Competency.code)
        ).all()
        latest_result = LatestResultOut(
            attempt_id=a.id,
            track_name=names[a.track_id],
            submitted_at=a.submitted_at,
            overall_score=r.overall_score,
            readiness_band=r.readiness_band,
            competencies=[
                CompetencySnapshotOut(
                    code=c.code, label=c.label, percentage=cs.percentage, assessed=cs.total_count > 0
                )
                for cs, c in comps
            ],
        )

    bank = published_bank(db)
    return ParticipantSummaryOut(
        tracks=statuses,
        latest_result=latest_result,
        score_history=[
            HistoryPointOut(
                attempt_id=a.id,
                track_id=a.track_id,
                track_name=names[a.track_id],
                submitted_at=a.submitted_at,
                overall_score=r.overall_score,
                question_bank=bank_label,
                scoring_policy=policy_label,
            )
            for a, r, bank_label, policy_label in submitted
        ],
        content_provenance=bank.content_provenance if bank else None,
    )


def admin_summary(db: Session) -> AdminSummaryOut:
    bank = published_bank(db)
    tracks = list(db.scalars(select(AssessmentTrack).order_by(AssessmentTrack.sort_order)))

    started = dict(
        db.execute(
            select(AssessmentAttempt.track_id, func.count()).group_by(AssessmentAttempt.track_id)
        ).all()
    )
    submitted_rows = db.execute(
        select(AssessmentAttempt.track_id, func.count(), func.avg(ScoreResult.overall_score))
        .join(ScoreResult, ScoreResult.attempt_id == AssessmentAttempt.id)
        .group_by(AssessmentAttempt.track_id)
    ).all()
    submitted = {tid: (n, avg) for tid, n, avg in submitted_rows}

    bands = dict(
        db.execute(
            select(ScoreResult.readiness_band, func.count()).group_by(ScoreResult.readiness_band)
        ).all()
    )
    participants_total = (
        db.scalar(select(func.count()).select_from(User).where(User.system_role == ROLE_PARTICIPANT)) or 0
    )
    participants_with_results = (
        db.scalar(
            select(func.count(func.distinct(AssessmentAttempt.participant_id))).where(
                AssessmentAttempt.status == STATUS_SUBMITTED
            )
        )
        or 0
    )

    by_scope: list[CountOut] = []
    by_competency: list[CountOut] = []
    warnings: list[str] = []
    if bank is None:
        warnings.append("No question bank is published; participants cannot start assessments.")
    else:
        # Distinct questions in the published bank's templates.
        in_bank = (
            select(Question.id, Question.scope, Question.track_id, QuestionRevision.competency_id)
            .join(QuestionRevision, QuestionRevision.question_id == Question.id)
            .join(TemplateQuestion, TemplateQuestion.question_revision_id == QuestionRevision.id)
            .join(AssessmentTemplate, AssessmentTemplate.id == TemplateQuestion.template_id)
            .where(AssessmentTemplate.bank_version_id == bank.id)
            .distinct()
            .subquery()
        )
        scope_counts = {
            (track_id or "common"): n
            for track_id, n in db.execute(
                select(in_bank.c.track_id, func.count()).group_by(in_bank.c.track_id)
            ).all()
        }
        track_names = {t.id: t.name for t in tracks}
        by_scope = [CountOut(key="common", label="Common", count=scope_counts.get("common", 0))] + [
            CountOut(key=t.id, label=track_names[t.id], count=scope_counts.get(t.id, 0)) for t in tracks
        ]
        comp_counts = db.execute(
            select(Competency.code, Competency.label, func.count(in_bank.c.id))
            .outerjoin(in_bank, in_bank.c.competency_id == Competency.id)
            .group_by(Competency.code, Competency.label)
            .order_by(Competency.code)
        ).all()
        by_competency = [CountOut(key=code, label=label, count=n) for code, label, n in comp_counts]

        total = sum(c.count for c in by_scope)
        if total != 50 or by_scope[0].count != 10 or any(c.count != 10 for c in by_scope[1:]):
            warnings.append(
                f"Published bank does not satisfy 10 common + 4×10 track questions (found {total})."
            )
        if bank.content_provenance != "approved_research":
            warnings.append(
                "Published bank is DRAFT placeholder content and is not research-backed (DEC-01)."
            )
        empty = [c.label for c in by_competency if c.count == 0]
        if empty:
            warnings.append(f"Competencies with no questions: {', '.join(empty)}.")

    return AdminSummaryOut(
        published_bank=PublishedBankOut(
            version_label=bank.version_label,
            content_provenance=bank.content_provenance,
            published_at=bank.published_at,
        )
        if bank
        else None,
        participants_total=participants_total,
        participants_with_results=participants_with_results,
        tracks=[
            TrackAggregateOut(
                track_id=t.id,
                track_name=t.name,
                attempts_started=started.get(t.id, 0),
                attempts_submitted=submitted.get(t.id, (0, None))[0],
                average_score=round(float(submitted[t.id][1]), 1) if t.id in submitted else None,
            )
            for t in tracks
        ],
        band_distribution=[CountOut(key=k, label=lbl, count=bands.get(k, 0)) for k, lbl in BANDS],
        questions_by_scope=by_scope,
        questions_by_competency=by_competency,
        warnings=warnings,
    )
