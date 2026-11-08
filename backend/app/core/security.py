"""Password hashing (pwdlib/Argon2) and session-token helpers. No hand-rolled crypto."""

import hashlib
import secrets
from functools import lru_cache

from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

_hasher = PasswordHash((Argon2Hasher(),))


def hash_password(password: str) -> str:
    return _hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return _hasher.verify(password, password_hash)


@lru_cache
def _dummy_hash() -> str:
    return _hasher.hash("timing-equaliser-not-a-real-password")


def dummy_verify() -> None:
    """Spend comparable time when the account does not exist (user-enumeration defence)."""
    _hasher.verify("not-the-password", _dummy_hash())


def new_session_token() -> str:
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> bytes:
    return hashlib.sha256(token.encode("utf-8")).digest()
