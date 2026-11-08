"""Pydantic schema + invariant checks for the seed bank files (database/seed/<bank>/)."""

import json
from collections import Counter
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from app.core.config import REPO_ROOT
from app.modules.scoring.policy import ScoringRulesV1

DEFAULT_BANK_DIR = REPO_ROOT / "database" / "seed" / "placeholder_bank_v0"
Provenance = Literal["placeholder_unverified", "approved_research"]
OptionId = Literal["A", "B", "C", "D"]


class OptionIn(BaseModel):
    id: OptionId
    text: str = Field(min_length=1)


class QuestionIn(BaseModel):
    code: str = Field(min_length=1)
    competency: str
    prompt: str = Field(min_length=1)
    options: list[OptionIn] = Field(min_length=4, max_length=4)
    correct_option_id: OptionId
    explanation: str = Field(min_length=1)
    evidence_reference: str = Field(min_length=1)

    @model_validator(mode="after")
    def _options(self) -> "QuestionIn":
        if [o.id for o in self.options] != ["A", "B", "C", "D"]:
            raise ValueError(f"{self.code}: options must be A, B, C, D in order")
        return self


class QuestionFile(BaseModel):
    content_status: str
    scope: Literal["common", "role_specific"]
    track_id: str | None
    questions: list[QuestionIn]


class TrackIn(BaseModel):
    id: str
    name: str
    description: str
    sort_order: int


class CompetencyIn(BaseModel):
    code: str
    label: str
    description: str


class Manifest(BaseModel):
    version_label: str
    content_provenance: Provenance
    scoring_policy: str
    recommendation_rule_version: str
    not_for_production: bool = False


class ScoringPolicyIn(BaseModel):
    version_label: str
    status: Literal["draft", "approved", "retired"]
    rules: ScoringRulesV1


class RecommendationIn(BaseModel):
    competency: str
    title: str
    body: str


class RecommendationFile(BaseModel):
    version_label: str
    content_provenance: Provenance
    rules: list[RecommendationIn]


class Bank(BaseModel):
    manifest: Manifest
    tracks: list[TrackIn]
    competencies: list[CompetencyIn]
    scoring_policy: ScoringPolicyIn
    recommendations: RecommendationFile
    common: QuestionFile
    role_files: dict[str, QuestionFile]

    def template_order(self, track_id: str) -> list[tuple[int, QuestionIn, str]]:
        """Fixed baseline order: common 1..10, then the track's questions 11..20 (DEC-05)."""
        ordered = [(q, "common") for q in self.common.questions] + [
            (q, "role_specific") for q in self.role_files[track_id].questions
        ]
        return [(i, q, cat) for i, (q, cat) in enumerate(ordered, start=1)]


class BankInvariantError(ValueError):
    pass


def validate_invariants(bank: Bank) -> None:
    """Master §4.3: exactly 50 unique questions, 10 common + 10 exclusive per track."""
    errors: list[str] = []
    track_ids = {t.id for t in bank.tracks}
    comp_codes = {c.code for c in bank.competencies}
    if len(track_ids) != 4:
        errors.append(f"expected 4 tracks, found {len(track_ids)}")
    if bank.common.scope != "common" or bank.common.track_id is not None:
        errors.append("common file must have scope=common and track_id=null")
    if len(bank.common.questions) != 10:
        errors.append(f"expected 10 common questions, found {len(bank.common.questions)}")
    if set(bank.role_files) != track_ids:
        errors.append("role-specific files must exist for exactly the 4 tracks")
    for track_id, f in bank.role_files.items():
        if f.scope != "role_specific" or f.track_id != track_id:
            errors.append(f"{track_id}: file scope/track mismatch")
        if len(f.questions) != 10:
            errors.append(f"{track_id}: expected 10 questions, found {len(f.questions)}")
    all_q = bank.common.questions + [q for f in bank.role_files.values() for q in f.questions]
    dupes = [c for c, n in Counter(q.code for q in all_q).items() if n > 1]
    if dupes:
        errors.append(f"duplicate question codes: {dupes}")
    if len(all_q) != 50:
        errors.append(f"expected 50 questions, found {len(all_q)}")
    unknown = {q.competency for q in all_q} - comp_codes
    if unknown:
        errors.append(f"unknown competencies: {sorted(unknown)}")
    if {r.competency for r in bank.recommendations.rules} - comp_codes:
        errors.append("recommendation rules reference unknown competencies")
    if len({r.competency for r in bank.recommendations.rules}) != len(bank.recommendations.rules):
        errors.append("at most one recommendation rule per competency")
    if bank.scoring_policy.version_label != bank.manifest.scoring_policy:
        errors.append("manifest scoring_policy does not match scoring_policy.json")
    if bank.recommendations.version_label != bank.manifest.recommendation_rule_version:
        errors.append("manifest recommendation_rule_version does not match recommendations.json")
    if errors:
        raise BankInvariantError("; ".join(errors))


def load_bank(bank_dir: Path = DEFAULT_BANK_DIR) -> Bank:
    def read(name: str):
        return json.loads((bank_dir / name).read_text(encoding="utf-8"))

    tracks = [TrackIn.model_validate(t) for t in read("tracks.json")]
    bank = Bank(
        manifest=Manifest.model_validate(read("manifest.json")),
        tracks=tracks,
        competencies=[CompetencyIn.model_validate(c) for c in read("competencies.json")],
        scoring_policy=ScoringPolicyIn.model_validate({**read("scoring_policy.json")}),
        recommendations=RecommendationFile.model_validate(read("recommendations.json")),
        common=QuestionFile.model_validate(read("questions/common.json")),
        role_files={t.id: QuestionFile.model_validate(read(f"questions/{t.id}.json")) for t in tracks},
    )
    validate_invariants(bank)
    return bank
