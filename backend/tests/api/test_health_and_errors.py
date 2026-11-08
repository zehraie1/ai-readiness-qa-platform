"""Operational endpoints and TC-015 error-envelope consistency."""

import pytest
from fastapi.testclient import TestClient

ENVELOPE_KEYS = {"code", "message", "details", "request_id"}


def assert_envelope(resp, status, code):
    assert resp.status_code == status, resp.text
    body = resp.json()
    assert set(body) == ENVELOPE_KEYS
    assert body["code"] == code
    assert body["request_id"] == resp.headers["x-request-id"]


def test_health_and_ready(anon):
    assert anon.get("/health").json() == {"status": "ok"}
    assert anon.get("/ready").json() == {"status": "ready"}


def test_request_id_is_echoed_when_safe(anon):
    r = anon.get("/health", headers={"X-Request-ID": "abc-123"})
    assert r.headers["x-request-id"] == "abc-123"
    r = anon.get("/health", headers={"X-Request-ID": "bad id with spaces"})
    assert r.headers["x-request-id"] != "bad id with spaces"


@pytest.mark.parametrize(
    ("method", "path", "status", "code"),
    [
        ("get", "/api/v1/me", 401, "UNAUTHENTICATED"),
        ("get", "/api/v1/nope", 404, "NOT_FOUND"),
        ("delete", "/api/v1/me", 405, "METHOD_NOT_ALLOWED"),
    ],
)
def test_envelope_for_framework_errors(anon, method, path, status, code):
    assert_envelope(getattr(anon, method)(path), status, code)


def test_validation_error_envelope_does_not_echo_input(anon):
    r = anon.post("/api/v1/auth/login", json={"email": "x", "password": ""})
    assert_envelope(r, 422, "VALIDATION_ERROR")
    assert all("input" not in d for d in r.json()["details"])


def test_participant_errors_use_envelope(participant):
    assert_envelope(participant.get("/api/v1/admin/competencies"), 403, "FORBIDDEN")
    assert_envelope(
        participant.get("/api/v1/attempts/00000000-0000-0000-0000-000000000000"), 404, "ATTEMPT_NOT_FOUND"
    )


def test_unhandled_error_is_sanitised(app, db):
    from app.modules.tracks import router as tracks_router

    def boom(*a, **k):
        raise RuntimeError("secret internals")

    client = TestClient(app, raise_server_exceptions=False, headers={"Origin": "http://localhost:5173"})
    original = tracks_router.published_bank
    tracks_router.published_bank = boom
    try:
        from app.core.config import get_settings

        client.post(
            "/api/v1/auth/login",
            json={
                "email": "e2e-participant-00@example.com",
                "password": get_settings().seed_participant_password,
            },
        )
        r = client.get("/api/v1/assessment-tracks")
    finally:
        tracks_router.published_bank = original
    assert r.status_code == 500
    assert r.json()["code"] == "INTERNAL_ERROR"
    assert "secret" not in r.text
    assert r.json()["request_id"] == r.headers["x-request-id"]
