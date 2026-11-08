"""Administrator endpoints (Slice 1: read-only competencies; governance comes later)."""

import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import ErrorEnvelope
from app.db.session import get_db
from app.modules.auth.dependencies import require_admin
from app.modules.content.models import Competency

router = APIRouter(prefix="/admin", tags=["admin"])


class CompetencyOut(BaseModel):
    id: uuid.UUID
    code: str
    label: str
    description: str


@router.get(
    "/competencies",
    response_model=list[CompetencyOut],
    dependencies=[Depends(require_admin)],
    responses={401: {"model": ErrorEnvelope}, 403: {"model": ErrorEnvelope}},
)
def list_competencies(db: Session = Depends(get_db)) -> list[CompetencyOut]:
    rows = db.scalars(select(Competency).order_by(Competency.code))
    return [CompetencyOut(id=c.id, code=c.code, label=c.label, description=c.description) for c in rows]
