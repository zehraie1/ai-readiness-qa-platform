import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class TrackStatusOut(BaseModel):
    track_id: str
    track_name: str
    status: Literal["not_started", "in_progress", "completed"]
    in_progress_attempt_id: uuid.UUID | None
    resume_position: int | None
    answered_count: int
    attempts_completed: int
    latest_score: int | None
    best_score: int | None
    latest_band: str | None
    latest_attempt_id: uuid.UUID | None


class CompetencySnapshotOut(BaseModel):
    code: str
    label: str
    percentage: int | None
    assessed: bool


class LatestResultOut(BaseModel):
    attempt_id: uuid.UUID
    track_name: str
    submitted_at: datetime
    overall_score: int
    readiness_band: str
    competencies: list[CompetencySnapshotOut]


class HistoryPointOut(BaseModel):
    attempt_id: uuid.UUID
    track_id: str
    track_name: str
    submitted_at: datetime
    overall_score: int
    question_bank: str
    scoring_policy: str


class ParticipantSummaryOut(BaseModel):
    tracks: list[TrackStatusOut]
    latest_result: LatestResultOut | None
    score_history: list[HistoryPointOut]
    content_provenance: str | None


class PublishedBankOut(BaseModel):
    version_label: str
    content_provenance: str
    published_at: datetime | None


class CountOut(BaseModel):
    key: str
    label: str
    count: int


class TrackAggregateOut(BaseModel):
    track_id: str
    track_name: str
    attempts_started: int
    attempts_submitted: int
    average_score: float | None


class AdminSummaryOut(BaseModel):
    published_bank: PublishedBankOut | None
    participants_total: int
    participants_with_results: int
    tracks: list[TrackAggregateOut]
    band_distribution: list[CountOut]
    questions_by_scope: list[CountOut]
    questions_by_competency: list[CountOut]
    warnings: list[str]
