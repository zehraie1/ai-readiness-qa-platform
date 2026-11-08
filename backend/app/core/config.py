"""Application settings loaded from environment variables / the repo-root .env file."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=REPO_ROOT / ".env", extra="ignore")

    # "demo" = production-grade security, but the DRAFT placeholder bank is allowed (ADR-011).
    app_env: Literal["development", "test", "demo", "production"] = "development"
    database_url: str = "postgresql+psycopg://airqa:airqa_dev_only@localhost:5433/airqa"
    test_database_url: str | None = None
    allowed_origins: str = "http://localhost:5173"
    # Set automatically by Render (e.g. https://ai-readiness-qa.onrender.com); added to allowed origins.
    render_external_url: str | None = None
    session_cookie_name: str = "airqa_session"
    session_ttl_hours: int = 12
    cookie_secure: bool = False
    log_level: str = "INFO"
    seed_admin_password: str | None = None
    seed_participant_password: str | None = None

    # Login throttling (failed attempts within the window).
    login_window_minutes: int = 15
    login_max_failures_per_email: int = 5
    login_max_failures_per_ip: int = 20

    # Serve the built SPA (frontend/dist) from FastAPI: single-origin deployment.
    serve_frontend: bool = False
    frontend_dist: Path = REPO_ROOT / "frontend" / "dist"

    @field_validator("database_url", "test_database_url")
    @classmethod
    def _psycopg_driver(cls, v: str | None) -> str | None:
        """Hosting providers (e.g. Render) hand out postgres:// or postgresql:// URLs."""
        if v is None:
            return v
        for prefix in ("postgres://", "postgresql://"):
            if v.startswith(prefix):
                return "postgresql+psycopg://" + v[len(prefix) :]
        return v

    @property
    def is_production_like(self) -> bool:
        return self.app_env in ("demo", "production")

    @property
    def allowed_origin_list(self) -> list[str]:
        origins = [o.strip().rstrip("/") for o in self.allowed_origins.split(",") if o.strip()]
        if self.render_external_url:
            origins.append(self.render_external_url.rstrip("/"))
        return origins


@lru_cache
def get_settings() -> Settings:
    return Settings()
