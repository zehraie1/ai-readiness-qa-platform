from datetime import UTC, datetime, timedelta

from sqlalchemy import update

from app.core.config import get_settings
from app.modules.auth.models import User, UserSession
from tests.conftest import ADMIN, ORIGIN, PARTICIPANT


def test_login_sets_httponly_cookie_and_me_works(anon):
    pw = get_settings().seed_participant_password
    r = anon.post("/api/v1/auth/login", json={"email": "  E2E-Participant-00@Example.com ", "password": pw})
    assert r.status_code == 200
    cookie = r.headers["set-cookie"]
    assert "airqa_session=" in cookie and "HttpOnly" in cookie and "SameSite=lax" in cookie
    me = anon.get("/api/v1/me").json()
    assert me["email"] == PARTICIPANT and me["role"] == "participant"
    assert "password_hash" not in me


def test_wrong_password_and_unknown_email_are_indistinguishable(anon):
    a = anon.post("/api/v1/auth/login", json={"email": PARTICIPANT, "password": "wrong"})
    b = anon.post("/api/v1/auth/login", json={"email": "nobody@example.com", "password": "wrong"})
    assert a.status_code == b.status_code == 401
    assert a.json()["code"] == b.json()["code"] == "INVALID_CREDENTIALS"
    assert a.json()["message"] == b.json()["message"]


def test_inactive_user_cannot_log_in(anon, db):
    db.execute(update(User).where(User.email == PARTICIPANT).values(is_active=False))
    db.flush()
    r = anon.post(
        "/api/v1/auth/login",
        json={"email": PARTICIPANT, "password": get_settings().seed_participant_password},
    )
    assert r.status_code == 401


def test_logout_revokes_session(participant):
    token = participant.cookies.get("airqa_session")
    assert participant.post("/api/v1/auth/logout").status_code == 204
    participant.cookies.set("airqa_session", token)  # replaying the old token must fail
    assert participant.get("/api/v1/me").status_code == 401


def test_expired_session_rejected(participant, db):
    db.execute(update(UserSession).values(expires_at=datetime.now(UTC) - timedelta(minutes=1)))
    db.flush()
    assert participant.get("/api/v1/me").status_code == 401


def test_foreign_origin_rejected_for_unsafe_methods(participant):
    r = participant.post(
        "/api/v1/attempts", json={"track_id": "sdet"}, headers={"Origin": "https://evil.example"}
    )
    assert r.status_code == 403 and r.json()["code"] == "CSRF_REJECTED"


def test_cookie_request_without_origin_rejected(app, db, participant):
    from fastapi.testclient import TestClient

    bare = TestClient(app)  # no Origin header
    bare.cookies.set("airqa_session", participant.cookies.get("airqa_session"))
    r = bare.post("/api/v1/attempts", json={"track_id": "sdet"})
    assert r.status_code == 403 and r.json()["code"] == "CSRF_REJECTED"
    # Safe methods are unaffected.
    assert bare.get("/api/v1/me").status_code == 200


def test_referer_fallback_accepted(app, db, participant):
    from fastapi.testclient import TestClient

    c = TestClient(app, headers={"Referer": f"{ORIGIN}/assessments/tracks"})
    c.cookies.set("airqa_session", participant.cookies.get("airqa_session"))
    assert c.post("/api/v1/attempts", json={"track_id": "sdet"}).status_code in (200, 201)


def test_admin_me_has_admin_role(admin):
    me = admin.get("/api/v1/me").json()
    assert me["email"] == ADMIN and me["role"] == "administrator"
