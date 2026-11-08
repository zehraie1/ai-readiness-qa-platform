"""Server-side authorization dependencies. Frontend guards are convenience only."""

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.errors import AppError, ErrorCode
from app.db.session import get_db
from app.modules.auth.models import ROLE_ADMINISTRATOR, ROLE_PARTICIPANT, User
from app.modules.auth.service import resolve_session


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> User:
    token = request.cookies.get(settings.session_cookie_name)
    user = resolve_session(db, token) if token else None
    if user is None:
        raise AppError(401, ErrorCode.UNAUTHENTICATED, "Authentication required.")
    return user


def require_participant(user: User = Depends(get_current_user)) -> User:
    if user.system_role != ROLE_PARTICIPANT:
        raise AppError(403, ErrorCode.FORBIDDEN, "Only participants can take assessments.")
    return user


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.system_role != ROLE_ADMINISTRATOR:
        raise AppError(403, ErrorCode.FORBIDDEN, "Administrator access required.")
    return user
