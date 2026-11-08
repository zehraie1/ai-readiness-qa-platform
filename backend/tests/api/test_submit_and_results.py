"""Submission (TC-008 sequential idempotency), results, recommendations, history."""

from tests.helpers import answer_all, answer_key, start


def test_incomplete_submit_rejected_with_positions(participant):
    a = start(participant, "sdet")
    answer_all(participant, {**a, "questions": a["questions"][:18]})
    r = participant.post(f"/api/v1/attempts/{a['id']}/submit")
    assert r.status_code == 409 and r.json()["code"] == "ATTEMPT_INCOMPLETE"
    assert r.json()["details"]["unanswered_positions"] == [19, 20]


def test_results_unavailable_before_submit(participant):
    a = start(participant, "sdet")
    r = participant.get(f"/api/v1/attempts/{a['id']}/results")
    assert r.status_code == 409 and r.json()["code"] == "RESULTS_NOT_AVAILABLE"


def test_all_correct_scores_100(participant):
    a = start(participant, "automation_qa")
    answer_all(participant, a)
    r = participant.post(f"/api/v1/attempts/{a['id']}/submit")
    assert r.status_code == 200
    res = r.json()
    assert res["overall_score"] == 100 and res["correct_count"] == 20
    assert res["common_score"] == 50 and res["role_specific_score"] == 50
    assert res["readiness_band"] == {"code": "advanced", "label": "Advanced", "min": 80, "max": 100}
    assert res["recommendations"] == []
    assert res["content_provenance"] == "placeholder_unverified"
    assert "not an externally validated benchmark" in res["disclaimer"]


def test_known_pattern_gives_exact_expected_result(participant):
    """Common positions 1-6 correct, role positions 11-13 correct => 9 correct => 45 Developing."""
    a = start(participant, "sdet")
    correct_positions = {1, 2, 3, 4, 5, 6, 11, 12, 13}
    answer_all(participant, a, correct_positions)
    res = participant.post(f"/api/v1/attempts/{a['id']}/submit").json()
    assert (res["overall_score"], res["common_score"], res["role_specific_score"]) == (45, 30, 15)
    assert res["readiness_band"]["code"] == "developing"

    # Independently compute expected competency percentages from the seed answer key.
    key = answer_key()
    tallies: dict[str, list[int]] = {}
    for q in a["questions"]:
        comp = key[q["question_id"]][1]
        t = tallies.setdefault(comp, [0, 0])
        t[0] += q["position"] in correct_positions
        t[1] += 1
    by_code = {c["code"]: c for c in res["competencies"]}
    for comp, (c, t) in tallies.items():
        assert (by_code[comp]["correct"], by_code[comp]["total"]) == (c, t)
    assert by_code["PH_QUALITY_LEADERSHIP"]["assessed"] is False
    assert by_code["PH_QUALITY_LEADERSHIP"]["percentage"] is None
    below = sorted(
        (c for c in res["competencies"] if c["assessed"] and c["percentage"] < 60),
        key=lambda c: (c["percentage"], c["code"]),
    )
    assert [r["competency_code"] for r in res["recommendations"]] == [c["code"] for c in below]
    assert [r["position"] for r in res["recommendations"]] == list(range(1, len(below) + 1))
    recs = participant.get(f"/api/v1/attempts/{a['id']}/recommendations").json()
    assert recs == res["recommendations"]


def test_repeat_submit_returns_identical_result_and_locks_answers(participant):
    a = start(participant, "manual_qa")
    answer_all(participant, a, set(range(1, 21, 2)))
    first = participant.post(f"/api/v1/attempts/{a['id']}/submit")
    second = participant.post(f"/api/v1/attempts/{a['id']}/submit")
    assert first.status_code == second.status_code == 200
    assert first.json() == second.json()
    assert participant.get(f"/api/v1/attempts/{a['id']}/results").json() == first.json()
    r = participant.put(
        f"/api/v1/attempts/{a['id']}/answers/{a['questions'][0]['question_id']}",
        json={"selected_option_id": "A"},
    )
    assert r.status_code == 409 and r.json()["code"] == "ATTEMPT_CLOSED"


def test_retake_creates_new_attempt_and_history(participant):
    a = start(participant, "qa_lead")
    answer_all(participant, a)
    participant.post(f"/api/v1/attempts/{a['id']}/submit")
    b = start(participant, "qa_lead")
    assert b["id"] != a["id"] and b["status"] == "in_progress"

    hist = participant.get("/api/v1/attempts").json()
    ids = [i["id"] for i in hist["items"]]
    assert a["id"] in ids and b["id"] in ids
    submitted = participant.get("/api/v1/attempts", params={"status": "submitted"}).json()
    item = next(i for i in submitted["items"] if i["id"] == a["id"])
    assert item["overall_score"] == 100 and item["readiness_band"] == "advanced"
    in_prog = next(i for i in hist["items"] if i["id"] == b["id"])
    assert in_prog["first_unanswered_position"] == 1 and in_prog["overall_score"] is None


def test_history_pagination(participant):
    for t in ["manual_qa", "automation_qa", "sdet"]:
        start(participant, t)
    page = participant.get("/api/v1/attempts", params={"limit": 2, "offset": 0}).json()
    assert page["total"] >= 3 and len(page["items"]) == 2 and page["limit"] == 2
    assert participant.get("/api/v1/attempts", params={"limit": 51}).status_code == 422
