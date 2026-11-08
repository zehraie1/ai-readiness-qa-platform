"""Authentication and server-side session management."""

from datetime import UTC, datetime, timedelta

from sqlalchemy import delete, func, select, update
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.core.errors import AppError, ErrorCode
from app.core.security import dummy_verify, hash_token, new_session_token, verify_password
from app.modules.auth.models import ROLE_ADMINISTRATOR, LoginAttempt, User, UserSession
from app.modules.auth.schemas import MeOut

PERMISSIONS = {
    "participant": ["assessment:take", "results:read_own"],
    ROLE_ADMINISTRATOR: ["admin:read"],
}


def authenticate(db: Session, email: str, password: str) -> User | None:
    user = db.scalar(select(User).where(User.email == email))
    if user is None:
        dummy_verify()
        return None
    if not verify_password(password, user.password_hash) or not user.is_active:
        return None
    return user


def check_login_throttle(db: Session, email: str, ip: str, settings: Settings) -> None:
    """Reject sign-in when too many recent failures exist for this email or source IP."""
    since = datetime.now(UTC) - timedelta(minutes=settings.login_window_minutes)
    recent = select(func.count()).select_from(LoginAttempt).where(LoginAttempt.created_at > since)
    by_email = db.scalar(recent.where(LoginAttempt.email == email)) or 0
    by_ip = db.scalar(recent.where(LoginAttempt.ip_address == ip)) or 0
    if by_email >= settings.login_max_failures_per_email or by_ip >= settings.login_max_failures_per_ip:
        retry = settings.login_window_minutes * 60
        raise AppError(
            429,
            ErrorCode.TOO_MANY_ATTEMPTS,
            "Too many sign-in attempts. Please wait and try again later.",
            headers={"Retry-After": str(retry)},
        )


def record_login_failure(db: Session, email: str, ip: str) -> None:
    db.add(LoginAttempt(email=email, ip_address=ip))


def clear_login_failures(db: Session, email: str) -> None:
    db.execute(delete(LoginAttempt).where(LoginAttempt.email == email))


def create_session(db: Session, user: User, settings: Settings) -> str:
    token = new_session_token()
    db.add(
        UserSession(
            user_id=user.id,
            token_hash=hash_token(token),
            expires_at=datetime.now(UTC) + timedelta(hours=settings.session_ttl_hours),
        )
    )
    return token


def resolve_session(db: Session, token: str) -> User | None:
    return db.scalar(
        select(User)
        .join(UserSession, UserSession.user_id == User.id)
        .where(
            UserSession.token_hash == hash_token(token),
            UserSession.revoked_at.is_(None),
            UserSession.expires_at > datetime.now(UTC),
            User.is_active.is_(True),
        )
    )


def revoke_session(db: Session, token: str) -> None:
    db.execute(
        update(UserSession)
        .where(UserSession.token_hash == hash_token(token), UserSession.revoked_at.is_(None))
        .values(revoked_at=datetime.now(UTC))
    )


def to_me(user: User) -> MeOut:
    return MeOut(
        id=user.id,
        email=user.email,
        display_name=user.display_name,
        role=user.system_role,
        permissions=PERMISSIONS.get(user.system_role, []),
    )
