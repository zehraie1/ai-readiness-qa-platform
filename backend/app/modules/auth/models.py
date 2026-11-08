import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    LargeBinary,
    Text,
    true,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.types import CreatedAt, UuidPk

ROLE_PARTICIPANT = "participant"
ROLE_ADMINISTRATOR = "administrator"


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("system_role IN ('participant','administrator')", name="system_role"),
        CheckConstraint("email = lower(email)", name="email_lowercase"),
    )

    id: Mapped[UuidPk]
    email: Mapped[str] = mapped_column(Text, unique=True)
    password_hash: Mapped[str] = mapped_column(Text)
    display_name: Mapped[str] = mapped_column(Text)
    system_role: Mapped[str] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=true())
    created_at: Mapped[CreatedAt]


class UserSession(Base):
    __tablename__ = "user_sessions"
    __table_args__ = (Index("ix_user_sessions_user_id", "user_id"),)

    id: Mapped[UuidPk]
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    token_hash: Mapped[bytes] = mapped_column(LargeBinary, unique=True)
    created_at: Mapped[CreatedAt]
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class LoginAttempt(Base):
    """Failed sign-in records used for throttling (successful sign-in clears the email's failures)."""

    __tablename__ = "login_attempts"
    __table_args__ = (
        Index("ix_login_attempts_email_created", "email", "created_at"),
        Index("ix_login_attempts_ip_created", "ip_address", "created_at"),
    )

    id: Mapped[UuidPk]
    email: Mapped[str] = mapped_column(Text)
    ip_address: Mapped[str] = mapped_column(Text)
    created_at: Mapped[CreatedAt]
