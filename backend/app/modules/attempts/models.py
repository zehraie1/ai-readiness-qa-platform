"""Attempts bind to immutable revisions and policy versions at creation."""

import uuid
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.types import UuidPk

STATUS_IN_PROGRESS = "in_progress"
STATUS_SUBMITTED = "submitted"


class AssessmentAttempt(Base):
    __tablename__ = "assessment_attempts"
    __table_args__ = (
        CheckConstraint("status IN ('in_progress','submitted')", name="status"),
        CheckConstraint("(status = 'submitted') = (submitted_at IS NOT NULL)", name="submitted_at_matches"),
        Index("ix_assessment_attempts_owner_status", "participant_id", "status"),
        # P1: at most one in-progress attempt per participant and track.
        Index(
            "uq_assessment_attempts_one_in_progress",
            "participant_id",
            "track_id",
            unique=True,
            postgresql_where=text("status = 'in_progress'"),
        ),
    )

    id: Mapped[UuidPk]
    participant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    track_id: Mapped[str] = mapped_column(ForeignKey("assessment_tracks.id"))
    template_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assessment_templates.id"))
    bank_version_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("question_bank_versions.id"))
    scoring_policy_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("scoring_policies.id"))
    recommendation_rule_version: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text, default=STATUS_IN_PROGRESS)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class AttemptQuestion(Base):
    __tablename__ = "attempt_questions"
    __table_args__ = (
        UniqueConstraint("attempt_id", "position"),
        UniqueConstraint("attempt_id", "question_id"),
        CheckConstraint("position BETWEEN 1 AND 20", name="position_range"),
        CheckConstraint("category IN ('common','role_specific')", name="category"),
    )

    id: Mapped[UuidPk]
    attempt_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assessment_attempts.id", ondelete="CASCADE"))
    position: Mapped[int] = mapped_column(Integer)
    question_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("questions.id"))
    question_revision_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("question_revisions.id"))
    category: Mapped[str] = mapped_column(Text)


class AttemptAnswer(Base):
    __tablename__ = "attempt_answers"
    __table_args__ = (
        CheckConstraint("selected_option_id IN ('A','B','C','D')", name="selected_option"),
        Index("ix_attempt_answers_attempt_id", "attempt_id"),
    )

    attempt_question_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("attempt_questions.id", ondelete="CASCADE"), primary_key=True
    )
    attempt_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assessment_attempts.id", ondelete="CASCADE"))
    selected_option_id: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
