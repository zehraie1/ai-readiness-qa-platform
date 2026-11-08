"""Participant-facing attempt DTOs. These models deliberately have NO answer-key fields
(correct_option_id / explanation / evidence_reference) so they can never be serialised."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class StartAttemptIn(BaseModel):
    track_id: str = Field(min_length=1, max_length=64)


class AnswerIn(BaseModel):
    selected_option_id: str = Field(min_length=1, max_length=8)


class OptionOut(BaseModel):
    id: str
    text: str


class AttemptQuestionOut(BaseModel):
    question_id: uuid.UUID
    position: int
    category: str
    prompt: str
    options: list[OptionOut]
    selected_option_id: str | None


class VersionsOut(BaseModel):
    question_bank: str
    scoring_policy: str
    recommendation_rules: str | None


class AttemptOut(BaseModel):
    id: uuid.UUID
    track_id: str
    track_name: str
    status: str
    started_at: datetime
    submitted_at: datetime | None
    total_questions: int
    answered_count: int
    content_provenance: str
    versions: VersionsOut
    questions: list[AttemptQuestionOut]


class AttemptSummaryOut(BaseModel):
    id: uuid.UUID
    track_id: str
    track_name: str
    status: str
    started_at: datetime
    submitted_at: datetime | None
    total_questions: int
    answered_count: int
    first_unanswered_position: int | None
    overall_score: int | None
    readiness_band: str | None


class AttemptListOut(BaseModel):
    items: list[AttemptSummaryOut]
    total: int
    limit: int
    offset: int


class AnswerOut(BaseModel):
    question_id: uuid.UUID
    selected_option_id: str
    answered_count: int
    updated_at: datetime


class ReviewItemOut(BaseModel):
    position: int
    question_id: uuid.UUID
    answered: bool


class ReviewOut(BaseModel):
    attempt_id: uuid.UUID
    status: str
    total: int
    answered: int
    unanswered_positions: list[int]
    items: list[ReviewItemOut]
