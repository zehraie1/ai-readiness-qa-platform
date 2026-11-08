"""Test helpers. The answer key is derived from the seed JSON — never from the API."""

from functools import lru_cache

from fastapi.testclient import TestClient

from app.seed.bank_schema import load_bank
from app.seed.seeder import sid


@lru_cache
def answer_key() -> dict[str, tuple[str, str]]:
    """question_id -> (correct_option_id, competency_code)."""
    bank = load_bank()
    qs = bank.common.questions + [q for f in bank.role_files.values() for q in f.questions]
    return {str(sid("question", q.code)): (q.correct_option_id, q.competency) for q in qs}


def wrong_option(correct: str) -> str:
    return "A" if correct != "A" else "B"


def start(client: TestClient, track: str = "sdet") -> dict:
    resp = client.post("/api/v1/attempts", json={"track_id": track})
    assert resp.status_code in (200, 201), resp.text
    return resp.json()


def answer_all(client: TestClient, attempt: dict, correct_positions: set[int] | None = None) -> None:
    """Answer every question; correct at the given positions (default: all correct)."""
    key = answer_key()
    for q in attempt["questions"]:
        correct = key[q["question_id"]][0]
        is_correct = correct_positions is None or q["position"] in correct_positions
        choice = correct if is_correct else wrong_option(correct)
        r = client.put(
            f"/api/v1/attempts/{attempt['id']}/answers/{q['question_id']}",
            json={"selected_option_id": choice},
        )
        assert r.status_code == 200, r.text


FORBIDDEN_KEYS = {"correct_option_id", "explanation", "evidence_reference", "is_correct"}


def find_forbidden_keys(payload) -> set[str]:
    found: set[str] = set()
    if isinstance(payload, dict):
        found |= FORBIDDEN_KEYS & payload.keys()
        for v in payload.values():
            found |= find_forbidden_keys(v)
    elif isinstance(payload, list):
        for v in payload:
            found |= find_forbidden_keys(v)
    return found
