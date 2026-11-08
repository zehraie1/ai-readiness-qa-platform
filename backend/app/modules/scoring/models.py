"""Scoring policy versions and immutable score snapshots."""

import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Integer, SmallInteger, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.types import CreatedAt, UuidPk


class ScoringPolicy(Base):
    __tablename__ = "scoring_policies"
    __table_args__ = (CheckConstraint("status IN ('draft','approved','retired')", name="status"),)

    id: Mapped[UuidPk]
    version_label: Mapped[str] = mapped_column(Text, unique=True)
    status: Mapped[str] = mapped_column(Text)
    rules_json: Mapped[dict] = mapped_column(JSONB)
    created_at: Mapped[CreatedAt]


class ScoreResult(Base):
    __tablename__ = "score_results"
    __table_args__ = (
        CheckConstraint("overall_score BETWEEN 0 AND 100", name="overall_range"),
        CheckConstraint("common_score BETWEEN 0 AND 50", name="common_range"),
        CheckConstraint("role_specific_score BETWEEN 0 AND 50", name="role_range"),
        CheckConstraint(
            "readiness_band IN ('foundation','developing','proficient','advanced')",
            name="readiness_band",
        ),
    )

    id: Mapped[UuidPk]
    # UNIQUE: the idempotency backstop — one result per attempt, ever.
    attempt_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assessment_attempts.id"), unique=True)
    scoring_policy_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("scoring_policies.id"))
    overall_score: Mapped[int] = mapped_column(SmallInteger)
    correct_count: Mapped[int] = mapped_column(SmallInteger)
    common_score: Mapped[int] = mapped_column(SmallInteger)
    role_specific_score: Mapped[int] = mapped_column(SmallInteger)
    readiness_band: Mapped[str] = mapped_column(Text)
    created_at: Mapped[CreatedAt]


class CompetencyScore(Base):
    __tablename__ = "competency_scores"
    __table_args__ = (
        UniqueConstraint("score_result_id", "competency_id"),
        CheckConstraint("percentage IS NULL OR percentage BETWEEN 0 AND 100", name="percentage_range"),
    )

    id: Mapped[UuidPk]
    score_result_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("score_results.id", ondelete="CASCADE"))
    competency_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("competencies.id"))
    correct_count: Mapped[int] = mapped_column(Integer)
    total_count: Mapped[int] = mapped_column(Integer)
    percentage: Mapped[int | None] = mapped_column(SmallInteger)


class ResultRecommendation(Base):
    __tablename__ = "result_recommendations"
    __table_args__ = (UniqueConstraint("score_result_id", "competency_id"),)

    id: Mapped[UuidPk]
    score_result_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("score_results.id", ondelete="CASCADE"))
    competency_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("competencies.id"))
    recommendation_rule_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("recommendation_rules.id"))
    position: Mapped[int] = mapped_column(Integer)
