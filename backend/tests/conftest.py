"""Test harness: dedicated test DB (TEST_DATABASE_URL), fresh migrations + seed per session,
and per-test transactional isolation via SAVEPOINT."""

import os

from app.core.config import Settings, get_settings

_base = Settings()
assert _base.test_database_url, "TEST_DATABASE_URL must be set (see .env.example)"
os.environ["APP_ENV"] = "test"
os.environ["DATABASE_URL"] = _base.test_database_url
get_settings.cache_clear()

from collections.abc import Callable, Iterator  # noqa: E402

import pytest  # noqa: E402
from alembic import command  # noqa: E402
from alembic.config import Config  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402

from app.core.config import REPO_ROOT  # noqa: E402
from app.db.session import SessionLocal, get_db, get_engine  # noqa: E402
from app.main import create_app  # noqa: E402
from app.seed.bank_schema import load_bank  # noqa: E402
from app.seed.seeder import seed_content  # noqa: E402
from app.seed.users import seed_users  # noqa: E402

ORIGIN = "http://localhost:5173"
PARTICIPANT = "e2e-participant-00@example.com"
PARTICIPANT_2 = "e2e-participant-01@example.com"
ADMIN = "e2e-admin@example.com"


def alembic_config() -> Config:
    cfg = Config(str(REPO_ROOT / "backend" / "alembic.ini"))
    cfg.set_main_option("script_location", str(REPO_ROOT / "database" / "migrations"))
    cfg.set_main_option("sqlalchemy.url", get_settings().database_url)
    return cfg


@pytest.fixture(scope="session", autouse=True)
def database() -> None:
    cfg = alembic_config()
    command.downgrade(cfg, "base")
    command.upgrade(cfg, "head")
    with SessionLocal(bind=get_engine()) as db, db.begin():
        seed_content(db, load_bank(), "test")
        seed_users(db, "test", get_settings())


@pytest.fixture(scope="session")
def app():
    return create_app()


@pytest.fixture
def db(app) -> Iterator[Session]:
    connection = get_engine().connect()
    outer = connection.begin()
    session = Session(bind=connection, join_transaction_mode="create_savepoint", expire_on_commit=False)
    app.dependency_overrides[get_db] = lambda: session
    try:
        yield session
    finally:
        app.dependency_overrides.pop(get_db, None)
        session.close()
        outer.rollback()
        connection.close()


def _login(client: TestClient, email: str, password: str | None = None) -> TestClient:
    s = get_settings()
    if password is None:
        password = s.seed_admin_password if "admin" in email else s.seed_participant_password
    resp = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200, resp.text
    return client


@pytest.fixture
def client_factory(app, db) -> Callable[..., TestClient]:
    def make(email: str | None = None) -> TestClient:
        client = TestClient(app, headers={"Origin": ORIGIN})
        return _login(client, email) if email else client

    return make


@pytest.fixture
def anon(client_factory) -> TestClient:
    return client_factory()


@pytest.fixture
def participant(client_factory) -> TestClient:
    return client_factory(PARTICIPANT)


@pytest.fixture
def participant2(client_factory) -> TestClient:
    return client_factory(PARTICIPANT_2)


@pytest.fixture
def admin(client_factory) -> TestClient:
    return client_factory(ADMIN)
