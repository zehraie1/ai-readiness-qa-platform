"""Compute-and-persist scoring snapshots, and read them back (never recomputed on read)."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.attempts.models import AssessmentAttempt, AttemptAnswer, AttemptQuestion
from app.modules.attempts.schemas import VersionsOut
from app.modules.content.models import Competency, QuestionBankVersion, QuestionRevision, RecommendationRule
from app.modules.results.schemas import (
    DISCLAIMER,
    BandOut,
    CompetencyResultOut,
    RecommendationOut,
    ResultOut,
)
from app.modules.scoring import engine
from app.modules.scoring.models import CompetencyScore, ResultRecommendation, ScoreResult, ScoringPolicy
from app.modules.scoring.policy import parse_rules
from app.modules.tracks.models import AssessmentTrack


def compute_and_store(db: Session, attempt: AssessmentAttempt) -> ScoreResult:
    """Caller holds the attempt row lock and has verified all answers exist."""
    policy = db.get(ScoringPolicy, attempt.scoring_policy_id)
    rules = parse_rules(policy.rules_json)
    rows = db.execute(
        select(
            AttemptQuestion.category,
            Competency.code,
            QuestionRevision.correct_option_id,
            AttemptAnswer.selected_option_id,
        )
        .join(QuestionRevision, QuestionRevision.id == AttemptQuestion.question_revision_id)
        .join(Competency, Competency.id == QuestionRevision.competency_id)
        .join(AttemptAnswer, AttemptAnswer.attempt_question_id == AttemptQuestion.id)
        .where(AttemptQuestion.attempt_id == attempt.id)
        .order_by(AttemptQuestion.position)
    ).all()
    outcomes = [
        engine.QuestionOutcome(category=cat, competency_code=code, is_correct=sel == correct)
        for cat, code, correct, sel in rows
    ]
    competencies = {c.code: c for c in db.scalars(select(Competency))}
    rec_rules: dict[str, str] = {}
    rule_ids = {}
    if attempt.recommendation_rule_version:
        for rule in db.scalars(
            select(RecommendationRule).where(
                RecommendationRule.version_label == attempt.recommendation_rule_version,
                RecommendationRule.status == "active",
            )
        ):
            code = next(c.code for c in competencies.values() if c.id == rule.competency_id)
            rec_rules[code] = str(rule.id)
            rule_ids[str(rule.id)] = rule.id

    out = engine.score(outcomes, rules, rec_rules, competency_universe=competencies.keys())

    result = ScoreResult(
        attempt_id=attempt.id,
        scoring_policy_id=policy.id,
        overall_score=out.overall_score,
        correct_count=out.correct_count,
        common_score=out.common_score,
        role_specific_score=out.role_specific_score,
        readiness_band=out.band.code,
    )
    db.add(result)
    db.flush()
    db.add_all(
        CompetencyScore(
            score_result_id=result.id,
            competency_id=competencies[c.code].id,
            correct_count=c.correct,
            total_count=c.total,
            percentage=c.percentage,
        )
        for c in out.competencies
    )
    db.add_all(
        ResultRecommendation(
            score_result_id=result.id,
            competency_id=competencies[p.competency_code].id,
            recommendation_rule_id=rule_ids[p.rule_id],
            position=p.position,
        )
        for p in out.recommendations
    )
    db.flush()
    return result


def load_result(db: Session, attempt: AssessmentAttempt) -> ResultOut:
    result = db.scalar(select(ScoreResult).where(ScoreResult.attempt_id == attempt.id))
    policy = db.get(ScoringPolicy, result.scoring_policy_id)
    rules = parse_rules(policy.rules_json)
    band = next(b for b in rules.bands if b.code == result.readiness_band)
    bank = db.get(QuestionBankVersion, attempt.bank_version_id)
    track = db.get(AssessmentTrack, attempt.track_id)

    comp_rows = db.execute(
        select(CompetencyScore, Competency)
        .join(Competency, Competency.id == CompetencyScore.competency_id)
        .where(CompetencyScore.score_result_id == result.id)
        .order_by(Competency.code)
    ).all()
    rec_rows = db.execute(
        select(ResultRecommendation, RecommendationRule, Competency)
        .join(RecommendationRule, RecommendationRule.id == ResultRecommendation.recommendation_rule_id)
        .join(Competency, Competency.id == ResultRecommendation.competency_id)
        .where(ResultRecommendation.score_result_id == result.id)
        .order_by(ResultRecommendation.position)
    ).all()

    return ResultOut(
        attempt_id=attempt.id,
        track_id=track.id,
        track_name=track.name,
        submitted_at=attempt.submitted_at,
        overall_score=result.overall_score,
        max_score=rules.points_per_correct * rules.expected_questions,
        correct_count=result.correct_count,
        total_questions=rules.expected_questions,
        common_score=result.common_score,
        role_specific_score=result.role_specific_score,
        readiness_band=BandOut(code=band.code, label=band.label, min=band.min, max=band.max),
        competencies=[
            CompetencyResultOut(
                code=c.code,
                label=c.label,
                correct=cs.correct_count,
                total=cs.total_count,
                percentage=cs.percentage,
                assessed=cs.total_count > 0,
            )
            for cs, c in comp_rows
        ],
        recommendations=[
            RecommendationOut(
                position=rr.position,
                competency_code=c.code,
                competency_label=c.label,
                title=rule.title,
                body=rule.body,
            )
            for rr, rule, c in rec_rows
        ],
        versions=VersionsOut(
            question_bank=bank.version_label,
            scoring_policy=policy.version_label,
            recommendation_rules=attempt.recommendation_rule_version,
        ),
        content_provenance=bank.content_provenance,
        disclaimer=DISCLAIMER,
    )
