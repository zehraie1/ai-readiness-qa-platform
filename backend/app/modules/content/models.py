"""Versioned, immutable assessment content: banks, questions, revisions, templates, rules."""

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
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.types import CreatedAt, UuidPk

PROVENANCE_VALUES = "('placeholder_unverified','approved_research')"


class Competency(Base):
    __tablename__ = "competencies"

    id: Mapped[UuidPk]
    code: Mapped[str] = mapped_column(Text, unique=True)
    label: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)


class QuestionBankVersion(Base):
    __tablename__ = "question_bank_versions"
    __table_args__ = (
        CheckConstraint("status IN ('draft','review','published','retired')", name="status"),
        CheckConstraint(f"content_provenance IN {PROVENANCE_VALUES}", name="content_provenance"),
        # At most one published bank at a time.
        Index(
            "uq_question_bank_versions_one_published",
            "status",
            unique=True,
            postgresql_where=text("status = 'published'"),
        ),
    )

    id: Mapped[UuidPk]
    version_label: Mapped[str] = mapped_column(Text, unique=True)
    status: Mapped[str] = mapped_column(Text)
    content_provenance: Mapped[str] = mapped_column(Text)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[CreatedAt]


class Question(Base):
    """Logical question. Content lives in immutable revisions."""

    __tablename__ = "questions"
    __table_args__ = (
        CheckConstraint("scope IN ('common','role_specific')", name="scope"),
        CheckConstraint(
            "(scope = 'common' AND track_id IS NULL) OR (scope = 'role_specific' AND track_id IS NOT NULL)",
            name="scope_track",
        ),
    )

    id: Mapped[UuidPk]
    code: Mapped[str] = mapped_column(Text, unique=True)
    scope: Mapped[str] = mapped_column(Text)
    track_id: Mapped[str | None] = mapped_column(ForeignKey("assessment_tracks.id"))
    created_at: Mapped[CreatedAt]


class QuestionRevision(Base):
    __tablename__ = "question_revisions"
    __table_args__ = (
        UniqueConstraint("question_id", "revision_no"),
        CheckConstraint("status IN ('draft','review','published','retired')", name="status"),
        CheckConstraint(
            "jsonb_typeof(options_json) = 'array' AND jsonb_array_length(options_json) = 4",
            name="four_options",
        ),
        CheckConstraint("correct_option_id IN ('A','B','C','D')", name="correct_option"),
    )

    id: Mapped[UuidPk]
    question_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("questions.id"))
    revision_no: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(Text)
    competency_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("competencies.id"))
    prompt: Mapped[str] = mapped_column(Text)
    options_json: Mapped[list] = mapped_column(JSONB)
    # Answer-key fields: never serialised to participant-facing DTOs.
    correct_option_id: Mapped[str] = mapped_column(Text)
    explanation: Mapped[str] = mapped_column(Text)
    evidence_reference: Mapped[str] = mapped_column(Text)
    created_at: Mapped[CreatedAt]


class AssessmentTemplate(Base):
    __tablename__ = "assessment_templates"
    __table_args__ = (UniqueConstraint("bank_version_id", "track_id"),)

    id: Mapped[UuidPk]
    bank_version_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("question_bank_versions.id"))
    track_id: Mapped[str] = mapped_column(ForeignKey("assessment_tracks.id"))


class TemplateQuestion(Base):
    __tablename__ = "template_questions"
    __table_args__ = (
        UniqueConstraint("template_id", "question_revision_id"),
        CheckConstraint("position BETWEEN 1 AND 20", name="position_range"),
        CheckConstraint("category IN ('common','role_specific')", name="category"),
    )

    template_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("assessment_templates.id", ondelete="CASCADE"), primary_key=True
    )
    position: Mapped[int] = mapped_column(Integer, primary_key=True)
    question_revision_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("question_revisions.id"))
    category: Mapped[str] = mapped_column(Text)


class RecommendationRule(Base):
    __tablename__ = "recommendation_rules"
    __table_args__ = (
        UniqueConstraint("version_label", "competency_id"),
        CheckConstraint("status IN ('draft','active','retired')", name="status"),
        CheckConstraint(f"content_provenance IN {PROVENANCE_VALUES}", name="content_provenance"),
    )

    id: Mapped[UuidPk]
    version_label: Mapped[str] = mapped_column(Text)
    competency_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("competencies.id"))
    title: Mapped[str] = mapped_column(Text)
    body: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text)
    content_provenance: Mapped[str] = mapped_column(Text)
    created_at: Mapped[CreatedAt]
