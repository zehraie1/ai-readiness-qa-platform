"""TC-009 / TC-010: deterministic scoring and stable recommendations (DEC-02)."""

import random

import pytest

from app.modules.scoring.engine import QuestionOutcome, band_for, percentage, score
from app.modules.scoring.policy import ScoringRulesV1, parse_rules

RULES_JSON = {
    "points_per_correct": 5,
    "expected_questions": 20,
    "expected_common": 10,
    "expected_role_specific": 10,
    "rounding": "half_up",
    "recommendation_threshold_pct": 60,
    "bands": [
        {"code": "foundation", "label": "Foundation", "min": 0, "max": 39},
        {"code": "developing", "label": "Developing", "min": 40, "max": 59},
        {"code": "proficient", "label": "Proficient", "min": 60, "max": 79},
        {"code": "advanced", "label": "Advanced", "min": 80, "max": 100},
    ],
}
RULES = parse_rules(RULES_JSON)


def outcomes(common_correct: int, role_correct: int, comps=("C1", "C2")) -> list[QuestionOutcome]:
    out = [QuestionOutcome("common", comps[i % len(comps)], i < common_correct) for i in range(10)]
    out += [QuestionOutcome("role_specific", comps[i % len(comps)], i < role_correct) for i in range(10)]
    return out


def test_all_correct_is_100_advanced():
    r = score(outcomes(10, 10), RULES)
    assert (r.overall_score, r.common_score, r.role_specific_score, r.band.code) == (100, 50, 50, "advanced")


def test_none_correct_is_0_foundation():
    r = score(outcomes(0, 0), RULES)
    assert (r.overall_score, r.correct_count, r.band.code) == (0, 0, "foundation")


@pytest.mark.parametrize(
    ("correct", "band"),
    [
        (7, "foundation"),
        (8, "developing"),
        (11, "developing"),
        (12, "proficient"),
        (15, "proficient"),
        (16, "advanced"),
    ],
)
def test_band_edges(correct, band):
    r = score(outcomes(min(correct, 10), max(correct - 10, 0)), RULES)
    assert r.overall_score == correct * 5
    assert r.band.code == band


@pytest.mark.parametrize(
    ("c", "t", "expected"), [(1, 8, 13), (2, 3, 67), (1, 3, 33), (1, 2, 50), (0, 4, 0), (3, 8, 38)]
)
def test_percentage_rounds_half_up(c, t, expected):
    assert percentage(c, t) == expected


def test_zero_denominator_is_not_assessed():
    r = score(outcomes(10, 10), RULES, competency_universe=["C1", "C2", "ZZ_UNUSED"])
    unused = next(c for c in r.competencies if c.code == "ZZ_UNUSED")
    assert unused.percentage is None and not unused.assessed


def test_identical_inputs_identical_output_regardless_of_order():
    items = outcomes(6, 4, comps=("C1", "C2", "C3"))
    shuffled = items[:]
    random.Random(42).shuffle(shuffled)
    rules = {"C1": "r1", "C2": "r2", "C3": "r3"}
    assert score(items, RULES, rules) == score(shuffled, RULES, rules)


def test_recommendation_threshold_strictly_below_60():
    # C1: 6/10 = 60% (no rec); C2: 4/10 = 40% (rec)
    items = [QuestionOutcome("common", "C1", i < 6) for i in range(10)]
    items += [QuestionOutcome("role_specific", "C2", i < 4) for i in range(10)]
    r = score(items, RULES, {"C1": "r1", "C2": "r2"})
    assert [p.competency_code for p in r.recommendations] == ["C2"]


def test_no_rule_means_no_fabricated_recommendation():
    r = score(outcomes(0, 0), RULES, {})
    assert r.recommendations == ()


def test_recommendations_ordered_by_percentage_then_code():
    items = [QuestionOutcome("common", "B", False) for _ in range(5)]
    items += [QuestionOutcome("common", "A", i < 1) for i in range(5)]
    items += [QuestionOutcome("role_specific", "C", False) for _ in range(10)]
    r = score(items, RULES, {"A": "ra", "B": "rb", "C": "rc"})
    assert [p.competency_code for p in r.recommendations] == ["B", "C", "A"]
    assert [p.position for p in r.recommendations] == [1, 2, 3]


def test_wrong_count_rejected():
    with pytest.raises(ValueError):
        score(outcomes(10, 10)[:19], RULES)


def test_band_lookup_rejects_out_of_range():
    with pytest.raises(ValueError):
        band_for(101, RULES.bands)


@pytest.mark.parametrize(
    "mutate",
    [
        lambda r: r["bands"].pop(),  # gap at the top
        lambda r: r["bands"][1].update(min=39),  # overlap
        lambda r: r.update(points_per_correct=4),  # max != 100
        lambda r: r.update(expected_common=9),  # composition mismatch
    ],
)
def test_policy_validation_rejects_bad_rules(mutate):
    import copy

    bad = copy.deepcopy(RULES_JSON)
    mutate(bad)
    with pytest.raises(ValueError):
        ScoringRulesV1.model_validate(bad)
