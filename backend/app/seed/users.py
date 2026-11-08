"""Seed-only account provisioning (no self-registration, ADR-008). Passwords come from env."""

from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.core.config import Settings
from app.core.security import hash_password, verify_password
from app.modules.auth.models import ROLE_ADMINISTRATOR, ROLE_PARTICIPANT, User
from app.seed.seeder import SeedRefused, sid

E2E_WORKERS = 8
WEAK_PASSWORDS = {"change-me-locally", "password", "changeme"}
MIN_DEMO_PASSWORD_LENGTH = 12


@dataclass(frozen=True)
class SeedUser:
    email: str
    display_name: str
    role: str


def users_for_profile(profile: str) -> list[SeedUser]:
    if profile == "dev":
        return [
            SeedUser("admin@example.com", "Demo Administrator", ROLE_ADMINISTRATOR),
            SeedUser("participant1@example.com", "Demo Participant One", ROLE_PARTICIPANT),
            SeedUser("participant2@example.com", "Demo Participant Two", ROLE_PARTICIPANT),
        ]
    if profile == "demo":
        return [
            SeedUser("demo-admin@example.com", "Demo Administrator", ROLE_ADMINISTRATOR),
            SeedUser("demo-participant-1@example.com", "Demo Participant One", ROLE_PARTICIPANT),
            SeedUser("demo-participant-2@example.com", "Demo Participant Two", ROLE_PARTICIPANT),
            SeedUser("demo-participant-3@example.com", "Demo Participant Three", ROLE_PARTICIPANT),
        ]
    if profile == "test":
        return [SeedUser("e2e-admin@example.com", "E2E Administrator", ROLE_ADMINISTRATOR)] + [
            SeedUser(f"e2e-participant-{i:02d}@example.com", f"E2E Participant {i:02d}", ROLE_PARTICIPANT)
            for i in range(E2E_WORKERS)
        ]
    raise ValueError(f"Unknown seed profile: {profile}")


def seed_users(db: Session, profile: str, settings: Settings) -> list[User]:
    if settings.app_env == "production":
        raise SeedRefused("Refusing to create demo accounts in production.")
    if not settings.seed_admin_password or not settings.seed_participant_password:
        raise SeedRefused("SEED_ADMIN_PASSWORD and SEED_PARTICIPANT_PASSWORD must be set.")
    if settings.app_env == "demo":
        if profile != "demo":
            raise SeedRefused("Only the 'demo' profile may be seeded when APP_ENV=demo.")
        for pw in (settings.seed_admin_password, settings.seed_participant_password):
            if len(pw) < MIN_DEMO_PASSWORD_LENGTH or pw.lower() in WEAK_PASSWORDS:
                raise SeedRefused(f"Demo passwords must be at least {MIN_DEMO_PASSWORD_LENGTH} characters.")
    created: list[User] = []
    for su in users_for_profile(profile):
        password = (
            settings.seed_admin_password
            if su.role == ROLE_ADMINISTRATOR
            else settings.seed_participant_password
        )
        uid = sid("user", su.email)
        user = db.get(User, uid)
        if user is None:
            user = User(
                id=uid,
                email=su.email,
                password_hash=hash_password(password),
                display_name=su.display_name,
                system_role=su.role,
                is_active=True,
            )
            db.add(user)
        else:
            user.display_name, user.system_role, user.is_active = su.display_name, su.role, True
            if not verify_password(password, user.password_hash):
                user.password_hash = hash_password(password)
        created.append(user)
    db.flush()
    return created
