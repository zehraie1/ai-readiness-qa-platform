"""TC-001 tracks; TC-006 role enforcement."""


def test_four_tracks_for_authenticated_user(participant):
    tracks = participant.get("/api/v1/assessment-tracks").json()
    assert [t["id"] for t in tracks] == ["manual_qa", "automation_qa", "sdet", "qa_lead"]
    assert all(t["question_count"] == 20 and t["available"] for t in tracks)
    assert {t["content_provenance"] for t in tracks} == {"placeholder_unverified"}


def test_tracks_require_auth(anon):
    assert anon.get("/api/v1/assessment-tracks").status_code == 401


def test_participant_cannot_use_admin_endpoints(participant):
    r = participant.get("/api/v1/admin/competencies")
    assert r.status_code == 403 and r.json()["code"] == "FORBIDDEN"


def test_admin_can_list_competencies(admin):
    r = admin.get("/api/v1/admin/competencies")
    assert r.status_code == 200 and len(r.json()) == 6


def test_admin_cannot_take_assessments(admin):
    # P6
    r = admin.post("/api/v1/attempts", json={"track_id": "sdet"})
    assert r.status_code == 403
    assert admin.get("/api/v1/attempts").status_code == 403
