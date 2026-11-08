"""Login throttling, security headers, demo-mode guards, settings normalisation, SPA serving."""

import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings, get_settings
from app.main import create_app
from app.seed.seeder import SeedRefused
from app.seed.users import seed_users
from tests.conftest import ORIGIN, PARTICIPANT


def _fail(client, email=PARTICIPANT):
    return client.post("/api/v1/auth/login", json={"email": email, "password": "wrong-password"})


def test_email_is_throttled_after_five_failures(anon):
    for _ in range(5):
        assert _fail(anon).status_code == 401
    r = _fail(anon)
    assert r.status_code == 429 and r.json()["code"] == "TOO_MANY_ATTEMPTS"
    assert r.headers["retry-after"] == "900"
    # Even the correct password is refused while throttled.
    ok = anon.post(
        "/api/v1/auth/login",
        json={"email": PARTICIPANT, "password": get_settings().seed_participant_password},
    )
    assert ok.status_code == 429


def test_successful_login_clears_email_failures(anon):
    for _ in range(4):
        _fail(anon)
    pw = get_settings().seed_participant_password
    assert anon.post("/api/v1/auth/login", json={"email": PARTICIPANT, "password": pw}).status_code == 200
    for _ in range(4):
        assert _fail(anon).status_code == 401


def test_ip_is_throttled_across_emails(anon):
    for i in range(20):
        assert _fail(anon, f"nobody-{i}@example.com").status_code == 401
    assert _fail(anon, "another@example.com").status_code == 429


def test_baseline_security_headers(anon):
    r = anon.get("/health")
    assert r.headers["x-content-type-options"] == "nosniff"
    assert r.headers["x-frame-options"] == "DENY"
    assert r.headers["referrer-policy"] == "strict-origin-when-cross-origin"
    assert "content-security-policy" not in r.headers  # dev/test keeps /docs usable


@pytest.fixture
def demo_app(monkeypatch, tmp_path):
    dist = tmp_path / "dist"
    (dist / "assets").mkdir(parents=True)
    (dist / "index.html").write_text("<!doctype html><title>SPA shell</title>")
    (dist / "assets" / "app.js").write_text("console.log('ok')")
    (dist / "robots.txt").write_text("User-agent: *")
    monkeypatch.setenv("APP_ENV", "demo")
    monkeypatch.setenv("SERVE_FRONTEND", "true")
    monkeypatch.setenv("FRONTEND_DIST", str(dist))
    get_settings.cache_clear()
    try:
        yield create_app()
    finally:
        get_settings.cache_clear()


def test_demo_mode_hides_docs_and_sets_strict_headers(demo_app, db):
    c = TestClient(demo_app, headers={"Origin": ORIGIN})
    assert c.get("/openapi.json").status_code == 404
    r = c.get("/health")
    assert "default-src 'self'" in r.headers["content-security-policy"]
    assert "frame-ancestors 'none'" in r.headers["content-security-policy"]
    assert r.headers["strict-transport-security"].startswith("max-age=")


def test_spa_is_served_with_history_fallback(demo_app, db):
    c = TestClient(demo_app, headers={"Origin": ORIGIN})
    for path in ["/", "/login", "/attempts/abc/questions/3"]:
        r = c.get(path)
        assert r.status_code == 200 and "SPA shell" in r.text
        assert r.headers["cache-control"] == "no-cache"
    assert c.get("/assets/app.js").text == "console.log('ok')"
    assert c.get("/robots.txt").text == "User-agent: *"
    # API and reserved paths are never swallowed by the SPA fallback.
    r = c.get("/api/v1/nope")
    assert r.status_code == 404 and r.json()["code"] == "NOT_FOUND"
    assert c.get("/api/v1/me").status_code == 401
    assert c.get("/docs").status_code == 404
    assert c.get("/../../etc/passwd").status_code in (200, 404)
    assert "root:" not in c.get("/%2e%2e/%2e%2e/etc/passwd").text


def test_database_url_is_normalised_for_psycopg():
    for raw in ["postgres://u:p@h:5432/d", "postgresql://u:p@h:5432/d"]:
        assert Settings(database_url=raw).database_url == "postgresql+psycopg://u:p@h:5432/d"


@pytest.mark.parametrize(
    ("profile", "admin_pw", "participant_pw"),
    [
        ("demo", "change-me-locally", "a-strong-password-1"),
        ("demo", "short", "a-strong-password-1"),
        ("dev", "a-strong-password-1", "a-strong-password-2"),
    ],
)
def test_demo_seed_rejects_weak_passwords_and_other_profiles(db, profile, admin_pw, participant_pw):
    s = Settings(app_env="demo", seed_admin_password=admin_pw, seed_participant_password=participant_pw)
    with pytest.raises(SeedRefused):
        seed_users(db, profile, s)


def test_demo_seed_creates_demo_accounts(db):
    s = Settings(
        app_env="demo",
        seed_admin_password="a-strong-password-1",
        seed_participant_password="a-strong-password-2",
    )
    users = seed_users(db, "demo", s)
    assert sorted(u.email for u in users)[0] == "demo-admin@example.com"
    assert len(users) == 4
