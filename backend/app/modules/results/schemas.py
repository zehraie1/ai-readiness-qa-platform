import uuid
from datetime import datetime

from pydantic import BaseModel

from app.modules.attempts.schemas import VersionsOut

DISCLAIMER = (
    "Internal V1 readiness classification produced by fixed, rule-based scoring. "
    "It is not an externally validated benchmark."
)


class BandOut(BaseModel):
    code: str
    label: str
    min: int
    max: int


class CompetencyResultOut(BaseModel):
    code: str
    label: str
    correct: int
    total: int
    percentage: int | None
    assessed: bool


class RecommendationOut(BaseModel):
    position: int
    competency_code: str
    competency_label: str
    title: str
    body: str


class ResultOut(BaseModel):
    attempt_id: uuid.UUID
    track_id: str
    track_name: str
    submitted_at: datetime
    overall_score: int
    max_score: int
    correct_count: int
    total_questions: int
    common_score: int
    role_specific_score: int
    readiness_band: BandOut
    competencies: list[CompetencyResultOut]
    recommendations: list[RecommendationOut]
    versions: VersionsOut
    content_provenance: str
    disclaimer: str
