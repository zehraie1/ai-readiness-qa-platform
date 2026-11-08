"""FastAPI application factory."""

from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.router import api_router
from app.api.spa import mount_spa
from app.core.config import get_settings
from app.core.csrf import OriginCheckMiddleware
from app.core.errors import register_exception_handlers
from app.core.logging import configure_logging
from app.core.request_id import RequestIdMiddleware
from app.core.security_headers import SecurityHeadersMiddleware


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)
    app = FastAPI(
        title="AI Readiness & QE Assessment API",
        version="0.2.0",
        docs_url=None if settings.is_production_like else "/docs",
        redoc_url=None,
        openapi_url=None if settings.is_production_like else "/openapi.json",
    )
    register_exception_handlers(app)
    # add_middleware wraps outward: RequestId (outermost) -> SecurityHeaders -> OriginCheck -> app.
    app.add_middleware(
        OriginCheckMiddleware,
        allowed_origins=settings.allowed_origin_list,
        cookie_name=settings.session_cookie_name,
    )
    app.add_middleware(SecurityHeadersMiddleware, production_like=settings.is_production_like)
    app.add_middleware(RequestIdMiddleware)
    app.include_router(health_router)
    app.include_router(api_router)
    if settings.serve_frontend:
        mount_spa(app, settings.frontend_dist)
    return app


app = create_app()
