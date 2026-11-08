"""TC-008: concurrent submission creates exactly one result; concurrent start creates one attempt.
Uses real, separately committed connections (not the SAVEPOINT fixture)."""

import threading

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete, func, select

from app.core.config import get_settings
from app.db.session import SessionLocal, get_engine
from app.modules.attempts.models import AssessmentAttempt
from app.modules.auth.models import User
from app.modules.scoring.models import ScoreResult
from tests.conftest import ORIGIN
from tests.helpers import answer_all

EMAIL = "e2e-participant-07@example.com"
pytestmark = pytest.mark.concurrency


@pytest.fixture
def real_client(app):
    client = TestClient(app, headers={"Origin": ORIGIN})
    r = client.post(
        "/api/v1/auth/login", json={"email": EMAIL, "password": get_settings().seed_participant_password}
    )
    assert r.status_code == 200
    yield client
    with SessionLocal(bind=get_engine()) as db, db.begin():
        uid = db.scalar(select(User.id).where(User.email == EMAIL))
        ids = list(db.scalars(select(AssessmentAttempt.id).where(AssessmentAttempt.participant_id == uid)))
        if ids:
            db.execute(delete(ScoreResult).where(ScoreResult.attempt_id.in_(ids)))
            db.execute(delete(AssessmentAttempt).where(AssessmentAttempt.id.in_(ids)))


def _parallel(fn, n=4):
    barrier = threading.Barrier(n)
    out = [None] * n

    def run(i):
        barrier.wait()
        out[i] = fn()

    threads = [threading.Thread(target=run, args=(i,)) for i in range(n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return out


def test_concurrent_submit_creates_one_result(real_client):
    a = real_client.post("/api/v1/attempts", json={"track_id": "sdet"}).json()
    answer_all(real_client, a)
    responses = _parallel(lambda: real_client.post(f"/api/v1/attempts/{a['id']}/submit"))
    assert all(r.status_code == 200 for r in responses), [r.text for r in responses]
    assert len({r.text for r in responses}) == 1
    with SessionLocal(bind=get_engine()) as db:
        assert db.scalar(select(func.count()).where(ScoreResult.attempt_id == a["id"])) == 1


def test_concurrent_start_creates_one_attempt(real_client):
    responses = _parallel(lambda: real_client.post("/api/v1/attempts", json={"track_id": "qa_lead"}))
    assert all(r.status_code in (200, 201) for r in responses), [r.text for r in responses]
    assert len({r.json()["id"] for r in responses}) == 1
