"""Participant summary (own data only) and admin aggregates (no individual data)."""

from tests.helpers import answer_all, start


def test_summary_requires_participant(anon, admin):
    assert anon.get("/api/v1/dashboard/summary").status_code == 401
    assert admin.get("/api/v1/dashboard/summary").status_code == 403


def test_participant_summary_reflects_own_attempts(participant, participant2):
    empty = participant.get("/api/v1/dashboard/summary").json()
    assert [t["status"] for t in empty["tracks"]] == ["not_started"] * 4
    assert empty["latest_result"] is None and empty["score_history"] == []
    assert empty["content_provenance"] == "placeholder_unverified"

    a = start(participant, "sdet")
    answer_all(participant, a)  # 100
    participant.post(f"/api/v1/attempts/{a['id']}/submit")
    b = start(participant, "sdet")
    answer_all(participant, b, set(range(1, 11)))  # 50
    participant.post(f"/api/v1/attempts/{b['id']}/submit")
    c = start(participant, "qa_lead")
    answer_all(participant, {**c, "questions": c["questions"][:3]})

    s = participant.get("/api/v1/dashboard/summary").json()
    by_track = {t["track_id"]: t for t in s["tracks"]}
    sdet = by_track["sdet"]
    assert sdet["status"] == "completed" and sdet["attempts_completed"] == 2
    assert (sdet["latest_score"], sdet["best_score"], sdet["latest_band"]) == (50, 100, "developing")
    lead = by_track["qa_lead"]
    assert lead["status"] == "in_progress" and lead["answered_count"] == 3 and lead["resume_position"] == 4
    assert [p["overall_score"] for p in s["score_history"]] == [100, 50]
    assert s["latest_result"]["attempt_id"] == b["id"] and s["latest_result"]["overall_score"] == 50
    assert {c["code"] for c in s["latest_result"]["competencies"]} >= {"PH_AI_FUNDAMENTALS"}

    other = participant2.get("/api/v1/dashboard/summary").json()
    assert other["score_history"] == [] and other["latest_result"] is None


def test_admin_summary_aggregates(admin, participant, participant2):
    for client, track, correct in [(participant, "sdet", None), (participant2, "sdet", set(range(1, 9)))]:
        a = start(client, track)
        answer_all(client, a, correct)
        client.post(f"/api/v1/attempts/{a['id']}/submit")
    start(participant, "manual_qa")

    s = admin.get("/api/v1/admin/dashboard/summary").json()
    assert s["published_bank"]["version_label"] == "placeholder-v0"
    sdet = next(t for t in s["tracks"] if t["track_id"] == "sdet")
    assert sdet["attempts_submitted"] == 2 and sdet["average_score"] == 70.0  # (100 + 40) / 2
    manual = next(t for t in s["tracks"] if t["track_id"] == "manual_qa")
    assert manual["attempts_started"] == 1 and manual["attempts_submitted"] == 0
    assert manual["average_score"] is None
    bands = {b["key"]: b["count"] for b in s["band_distribution"]}
    assert bands["advanced"] == 1 and bands["developing"] == 1
    assert [q["count"] for q in s["questions_by_scope"]] == [10, 10, 10, 10, 10]
    assert sum(q["count"] for q in s["questions_by_competency"]) == 50
    assert s["participants_with_results"] == 2
    assert any("DRAFT" in w for w in s["warnings"])
    # Aggregates only: no emails or participant identifiers.
    assert "@" not in str(s)


def test_participant_cannot_read_admin_summary(participant):
    assert participant.get("/api/v1/admin/dashboard/summary").status_code == 403
