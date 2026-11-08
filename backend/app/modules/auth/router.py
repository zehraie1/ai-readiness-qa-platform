from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.errors import AppError, ErrorCode, ErrorEnvelope
from app.db.session import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.auth.schemas import LoginIn, MeOut
from app.modules.auth.service import (
    authenticate,
    check_login_throttle,
    clear_login_failures,
    create_session,
    record_login_failure,
    revoke_session,
    to_me,
)

router = APIRouter(tags=["auth"])
ERRORS = {401: {"model": ErrorEnvelope}, 422: {"model": ErrorEnvelope}, 429: {"model": ErrorEnvelope}}


@router.post("/auth/login", response_model=MeOut, responses=ERRORS)
def login(
    body: LoginIn,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> MeOut:
    # Behind a proxy, uvicorn --proxy-headers resolves the client from X-Forwarded-For.
    ip = request.client.host if request.client else "unknown"
    check_login_throttle(db, body.email, ip, settings)
    user = authenticate(db, body.email, body.password)
    if user is None:
        record_login_failure(db, body.email, ip)
        db.commit()
        # Same response for unknown email, wrong password and inactive account.
        raise AppError(401, ErrorCode.INVALID_CREDENTIALS, "Email or password is incorrect.")
    clear_login_failures(db, body.email)
    token = create_session(db, user, settings)
    db.commit()
    response.set_cookie(
        settings.session_cookie_name,
        token,
        max_age=settings.session_ttl_hours * 3600,
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
        path="/",
    )
    return to_me(user)


@router.post("/auth/logout", status_code=204, responses=ERRORS)
def logout(
    request: Request,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> Response:
    token = request.cookies.get(settings.session_cookie_name)
    if token:
        revoke_session(db, token)
        db.commit()
    resp = Response(status_code=204)
    resp.delete_cookie(
        settings.session_cookie_name,
        path="/",
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
    )
    return resp


@router.get("/me", response_model=MeOut, responses=ERRORS)
def me(user: User = Depends(get_current_user)) -> MeOut:
    return to_me(user)
