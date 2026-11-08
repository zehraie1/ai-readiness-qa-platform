"""TC-002 composition, TC-004 no key leakage, TC-005 ownership, TC-007 validation."""

import uuid

import pytest

from tests.helpers import answer_key, find_forbidden_keys, start

TRACKS = ["manual_qa", "automation_qa", "sdet", "qa_lead"]


@pytest.mark.parametrize("track", TRACKS)
def test_start_returns_20_questions_10_common_10_track(participant, track):
    a = start(participant, track)
    qs = a["questions"]
    assert a["status"] == "in_progress" and a["total_questions"] == 20 and len(qs) == 20
    assert [q["position"] for q in qs] == list(range(1, 21))
    assert [q["category"] for q in qs] == ["common"] * 10 + ["role_specific"] * 10
    assert len({q["question_id"] for q in qs}) == 20
    assert all(len(q["options"]) == 4 and q["selected_option_id"] is None for q in qs)
    assert a["versions"] == {
        "question_bank": "placeholder-v0",
        "scoring_policy": "v1-simple",
        "recommendation_rules": "placeholder-rec-v0",
    }


def test_common_questions_shared_and_role_questions_disjoint(participant):
    sets = {t: start(participant, t)["questions"] for t in TRACKS}
    commons = {tuple(q["question_id"] for q in qs[:10]) for qs in sets.values()}
    assert len(commons) == 1
    role_ids = [q["question_id"] for qs in sets.values() for q in qs[10:]]
    assert len(role_ids) == len(set(role_ids)) == 40


def test_start_is_idempotent_while_in_progress(participant):
    first = participant.post("/api/v1/attempts", json={"track_id": "sdet"})
    second = participant.post("/api/v1/attempts", json={"track_id": "sdet"})
    assert first.status_code == 201 and second.status_code == 200
    assert first.json()["id"] == second.json()["id"]


def test_unknown_track(participant):
    r = participant.post("/api/v1/attempts", json={"track_id": "astronaut"})
    assert r.status_code == 404 and r.json()["code"] == "TRACK_NOT_FOUND"


def test_no_answer_key_fields_in_participant_responses(participant):
    a = start(participant, "sdet")
    q = a["questions"][0]
    participant.put(
        f"/api/v1/attempts/{a['id']}/answers/{q['question_id']}", json={"selected_option_id": "A"}
    )
    payloads = [
        a,
        participant.get(f"/api/v1/attempts/{a['id']}").json(),
        participant.get(f"/api/v1/attempts/{a['id']}/review").json(),
        participant.get("/api/v1/attempts").json(),
        participant.get("/api/v1/assessment-tracks").json(),
    ]
    for p in payloads:
        assert find_forbidden_keys(p) == set()


def test_save_and_change_answer_persists(participant):
    a = start(participant, "manual_qa")
    qid = a["questions"][2]["question_id"]
    url = f"/api/v1/attempts/{a['id']}/answers/{qid}"
    assert participant.put(url, json={"selected_option_id": "B"}).json()["answered_count"] == 1
    r = participant.put(url, json={"selected_option_id": "D"})
    assert r.status_code == 200 and r.json()["answered_count"] == 1
    again = participant.get(f"/api/v1/attempts/{a['id']}").json()
    assert again["questions"][2]["selected_option_id"] == "D"
    assert again["answered_count"] == 1


def test_review_lists_unanswered(participant):
    a = start(participant, "qa_lead")
    for q in a["questions"][:3]:
        participant.put(
            f"/api/v1/attempts/{a['id']}/answers/{q['question_id']}", json={"selected_option_id": "A"}
        )
    rv = participant.get(f"/api/v1/attempts/{a['id']}/review").json()
    assert rv["answered"] == 3 and rv["total"] == 20
    assert rv["unanswered_positions"] == list(range(4, 21))


@pytest.mark.parametrize("option", ["E", "a", "Z1", "AB"])
def test_invalid_option_rejected(participant, option):
    a = start(participant, "sdet")
    r = participant.put(
        f"/api/v1/attempts/{a['id']}/answers/{a['questions'][0]['question_id']}",
        json={"selected_option_id": option},
    )
    assert r.status_code == 422 and r.json()["code"] == "INVALID_OPTION"


def test_question_not_in_attempt(participant):
    a = start(participant, "sdet")
    foreign_q = next(qid for qid in answer_key() if qid not in {q["question_id"] for q in a["questions"]})
    r = participant.put(f"/api/v1/attempts/{a['id']}/answers/{foreign_q}", json={"selected_option_id": "A"})
    assert r.status_code == 404 and r.json()["code"] == "QUESTION_NOT_IN_ATTEMPT"


def test_malformed_body_and_ids(participant):
    a = start(participant, "sdet")
    qid = a["questions"][0]["question_id"]
    assert participant.put(f"/api/v1/attempts/{a['id']}/answers/{qid}", json={}).status_code == 422
    assert (
        participant.put(
            f"/api/v1/attempts/not-a-uuid/answers/{qid}", json={"selected_option_id": "A"}
        ).status_code
        == 422
    )
    assert participant.post("/api/v1/attempts", json={"track_id": ""}).status_code == 422


def test_other_participant_cannot_see_or_change_attempt(participant, participant2):
    a = start(participant, "sdet")
    qid = a["questions"][0]["question_id"]
    base = f"/api/v1/attempts/{a['id']}"
    responses = [
        participant2.get(base),
        participant2.put(f"{base}/answers/{qid}", json={"selected_option_id": "A"}),
        participant2.get(f"{base}/review"),
        participant2.post(f"{base}/submit"),
        participant2.get(f"{base}/results"),
        participant2.get(f"{base}/recommendations"),
    ]
    for r in responses:
        assert r.status_code == 404 and r.json()["code"] == "ATTEMPT_NOT_FOUND"
    # Indistinguishable from a non-existent attempt (P3)
    missing = participant2.get(f"/api/v1/attempts/{uuid.uuid4()}")
    assert missing.json()["message"] == responses[0].json()["message"]
    assert all(i["id"] != a["id"] for i in participant2.get("/api/v1/attempts").json()["items"])
