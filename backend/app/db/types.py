"""Shared column helpers."""

import uuid
from datetime import datetime
from typing import Annotated

from sqlalchemy import DateTime, Uuid, func
from sqlalchemy.orm import mapped_column

UuidPk = Annotated[uuid.UUID, mapped_column(Uuid, primary_key=True, default=uuid.uuid4)]
CreatedAt = Annotated[
    datetime, mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
]
