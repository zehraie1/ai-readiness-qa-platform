from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.errors import ErrorEnvelope
from app.db.session import get_db
from app.modules.auth.dependencies import require_admin, require_participant
from app.modules.auth.models import User
from app.modules.dashboard import service
from app.modules.dashboard.schemas import AdminSummaryOut, ParticipantSummaryOut

router = APIRouter(tags=["dashboard"])
E = {"model": ErrorEnvelope}


@router.get("/dashboard/summary", response_model=ParticipantSummaryOut, responses={401: E, 403: E})
def participant_summary(
    user: User = Depends(require_participant), db: Session = Depends(get_db)
) -> ParticipantSummaryOut:
    return service.participant_summary(db, user)


@router.get(
    "/admin/dashboard/summary",
    response_model=AdminSummaryOut,
    dependencies=[Depends(require_admin)],
    responses={401: E, 403: E},
)
def admin_summary(db: Session = Depends(get_db)) -> AdminSummaryOut:
    return service.admin_summary(db)
