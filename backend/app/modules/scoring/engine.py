"""Pure, deterministic scoring engine (DEC-02 / ADR-007). No database, no I/O.

Identical inputs always produce identical outputs, independent of input order.
"""

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from typing import Literal

Category = Literal["common", "role_specific"]


@dataclass(frozen=True)
class Band:
    code: str
    label: str
    min: int
    max: int


@dataclass(frozen=True)
class ScoringRules:
    points_per_correct: int
    expected_questions: int
    expected_common: int
    expected_role_specific: int
    recommendation_threshold_pct: int
    bands: tuple[Band, ...]


@dataclass(frozen=True)
class QuestionOutcome:
    category: Category
    competency_code: str
    is_correct: bool


@dataclass(frozen=True)
class CompetencyResult:
    code: str
    correct: int
    total: int
    percentage: int | None  # None => "Not assessed"

    @property
    def assessed(self) -> bool:
        return self.total > 0


@dataclass(frozen=True)
class RecommendationPick:
    competency_code: str
    rule_id: str
    position: int


@dataclass(frozen=True)
class ScoreOutput:
    overall_score: int
    correct_count: int
    common_score: int
    role_specific_score: int
    band: Band
    competencies: tuple[CompetencyResult, ...]
    recommendations: tuple[RecommendationPick, ...]


def percentage(correct: int, total: int) -> int | None:
    """Nearest whole percentage, half-up (12.5 -> 13). Python's round() is banker's: not used."""
    if total == 0:
        return None
    value = Decimal(correct * 100) / Decimal(total)
    return int(value.quantize(Decimal(1), rounding=ROUND_HALF_UP))


def band_for(score: int, bands: Iterable[Band]) -> Band:
    for band in bands:
        if band.min <= score <= band.max:
            return band
    raise ValueError(f"No readiness band covers score {score}")


def score(
    outcomes: Iterable[QuestionOutcome],
    rules: ScoringRules,
    recommendation_rules: Mapping[str, str] | None = None,
    competency_universe: Iterable[str] = (),
) -> ScoreOutput:
    """Score one complete attempt.

    recommendation_rules maps competency_code -> rule_id (at most one rule per competency).
    competency_universe adds competencies with zero questions so they report "Not assessed".
    """
    items = list(outcomes)
    if len(items) != rules.expected_questions:
        raise ValueError(f"Expected {rules.expected_questions} outcomes, got {len(items)}")
    common = [o for o in items if o.category == "common"]
    role = [o for o in items if o.category == "role_specific"]
    if len(common) != rules.expected_common or len(role) != rules.expected_role_specific:
        raise ValueError("Attempt composition does not match the scoring policy")

    pts = rules.points_per_correct
    correct_count = sum(o.is_correct for o in items)
    overall = correct_count * pts
    common_score = sum(o.is_correct for o in common) * pts
    role_score = sum(o.is_correct for o in role) * pts

    tallies: dict[str, list[int]] = {code: [0, 0] for code in competency_universe}
    for o in items:
        t = tallies.setdefault(o.competency_code, [0, 0])
        t[0] += int(o.is_correct)
        t[1] += 1
    competencies = tuple(
        CompetencyResult(code=c, correct=t[0], total=t[1], percentage=percentage(t[0], t[1]))
        for c, t in sorted(tallies.items())
    )

    rec_rules = recommendation_rules or {}
    below = sorted(
        (c for c in competencies if c.assessed and c.percentage < rules.recommendation_threshold_pct),
        key=lambda c: (c.percentage, c.code),
    )
    picks = tuple(
        RecommendationPick(competency_code=c.code, rule_id=rec_rules[c.code], position=i)
        for i, c in enumerate((c for c in below if c.code in rec_rules), start=1)
    )

    return ScoreOutput(
        overall_score=overall,
        correct_count=correct_count,
        common_score=common_score,
        role_specific_score=role_score,
        band=band_for(overall, rules.bands),
        competencies=competencies,
        recommendations=picks,
    )
