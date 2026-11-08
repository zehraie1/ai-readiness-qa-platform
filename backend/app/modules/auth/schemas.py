import uuid

from pydantic import BaseModel, Field, field_validator


class LoginIn(BaseModel):
    # Plain str (not EmailStr): avoids leaking validation differences and special-use TLD issues.
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=1, max_length=256)

    @field_validator("email")
    @classmethod
    def _normalise(cls, v: str) -> str:
        return v.strip().lower()


class MeOut(BaseModel):
    id: uuid.UUID
    email: str
    display_name: str
    role: str
    permissions: list[str]
