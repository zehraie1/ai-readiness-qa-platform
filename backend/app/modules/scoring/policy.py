"""Validation of stored scoring-policy rules_json into engine ScoringRules."""

from typing import Literal

from pydantic import BaseModel, Field, model_validator

from app.modules.scoring.engine import Band, ScoringRules


class BandV1(BaseModel):
    code: Literal["foundation", "developing", "proficient", "advanced"]
    label: str
    min: int = Field(ge=0, le=100)
    max: int = Field(ge=0, le=100)


class ScoringRulesV1(BaseModel):
    points_per_correct: int = Field(gt=0)
    expected_questions: int = Field(gt=0)
    expected_common: int = Field(ge=0)
    expected_role_specific: int = Field(ge=0)
    rounding: Literal["half_up"]
    recommendation_threshold_pct: int = Field(ge=0, le=100)
    bands: list[BandV1]

    @model_validator(mode="after")
    def _check(self) -> "ScoringRulesV1":
        if self.expected_common + self.expected_role_specific != self.expected_questions:
            raise ValueError("common + role_specific must equal expected_questions")
        if self.points_per_correct * self.expected_questions != 100:
            raise ValueError("maximum score must be 100")
        ordered = sorted(self.bands, key=lambda b: b.min)
        if not ordered or ordered[0].min != 0 or ordered[-1].max != 100:
            raise ValueError("bands must cover 0..100")
        for prev, nxt in zip(ordered, ordered[1:], strict=False):
            if nxt.min != prev.max + 1:
                raise ValueError("bands must be contiguous and non-overlapping")
        for b in ordered:
            if b.min > b.max:
                raise ValueError("band min must not exceed max")
        return self

    def to_engine(self) -> ScoringRules:
        return ScoringRules(
            points_per_correct=self.points_per_correct,
            expected_questions=self.expected_questions,
            expected_common=self.expected_common,
            expected_role_specific=self.expected_role_specific,
            recommendation_threshold_pct=self.recommendation_threshold_pct,
            bands=tuple(
                Band(code=b.code, label=b.label, min=b.min, max=b.max)
                for b in sorted(self.bands, key=lambda b: b.min)
            ),
        )


def parse_rules(rules_json: dict) -> ScoringRules:
    return ScoringRulesV1.model_validate(rules_json).to_engine()
