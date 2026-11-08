"""TC-014 and bank invariants."""

import copy

import pytest
from alembic import command
from sqlalchemy import func, select, text
from sqlalchemy.exc import IntegrityError

from app.core.config import get_settings
from app.db.session import SessionLocal, get_engine
from app.modules.auth.models import User
from app.modules.content.models import Question, QuestionRevision, TemplateQuestion
from app.seed.bank_schema import BankInvariantError, load_bank, validate_invariants
from app.seed.seeder import SeedRefused, seed_content
from app.seed.users import seed_users
from tests.conftest import alembic_config


def _counts(db):
    return tuple(
        db.scalar(select(func.count()).select_from(m))
        for m in (Question, QuestionRevision, TemplateQuestion, User)
    )


def test_seed_is_idempotent():
    with SessionLocal(bind=get_engine()) as db:
        before = _counts(db)
    with SessionLocal(bind=get_engine()) as db, db.begin():
        seed_content(db, load_bank(), "test")
        seed_users(db, "test", get_settings())
    with SessionLocal(bind=get_engine()) as db:
        assert _counts(db) == before == (50, 50, 80, 9)


def test_bank_invariants_hold():
    bank = load_bank()
    validate_invariants(bank)
    for track in bank.role_files:
        order = bank.template_order(track)
        assert [p for p, _, _ in order] == list(range(1, 21))
        assert [c for _, _, c in order] == ["common"] * 10 + ["role_specific"] * 10


def test_invariants_reject_overlap_and_wrong_counts():
    bank = load_bank()
    broken = copy.deepcopy(bank)
    broken.role_files["sdet"].questions[0] = broken.role_files["qa_lead"].questions[0]
    with pytest.raises(BankInvariantError, match="duplicate"):
        validate_invariants(broken)
    broken = copy.deepcopy(bank)
    broken.common.questions.pop()
    with pytest.raises(BankInvariantError, match="10 common"):
        validate_invariants(broken)


def test_seed_refuses_placeholder_in_production():
    with SessionLocal(bind=get_engine()) as db, pytest.raises(SeedRefused):
        seed_content(db, load_bank(), "production")


def test_db_rejects_common_question_with_track(db):
    with pytest.raises(IntegrityError):
        db.execute(
            text(
                "INSERT INTO questions (id, code, scope, track_id) VALUES (gen_random_uuid(), 'X1', 'common', 'sdet')"
            )
        )
        db.flush()


def test_db_rejects_five_options(db):
    rev = db.scalar(select(QuestionRevision).limit(1))
    with pytest.raises(IntegrityError):
        db.execute(
            text(
                'UPDATE question_revisions SET options_json = options_json || \'[{"id":"E","text":"x"}]\'::jsonb WHERE id = :id'
            ),
            {"id": rev.id},
        )
        db.flush()


def test_migrations_downgrade_and_upgrade_cleanly():
    """Runs last-ish: re-creates schema and re-seeds so later tests still have data."""
    cfg = alembic_config()
    get_engine().dispose()
    command.downgrade(cfg, "base")
    command.upgrade(cfg, "head")
    with SessionLocal(bind=get_engine()) as db, db.begin():
        seed_content(db, load_bank(), "test")
        seed_users(db, "test", get_settings())
    with SessionLocal(bind=get_engine()) as db:
        assert _counts(db) == (50, 50, 80, 9)
