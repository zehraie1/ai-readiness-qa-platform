from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import ErrorEnvelope
from app.db.session import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.content.models import AssessmentTemplate
from app.modules.content.repository import published_bank
from app.modules.tracks.models import AssessmentTrack
from app.modules.tracks.schemas import TrackOut

router = APIRouter(tags=["tracks"])
QUESTIONS_PER_ATTEMPT = 20


@router.get(
    "/assessment-tracks",
    response_model=list[TrackOut],
    dependencies=[Depends(get_current_user)],
    responses={401: {"model": ErrorEnvelope}},
)
def list_tracks(db: Session = Depends(get_db)) -> list[TrackOut]:
    bank = published_bank(db)
    available: set[str] = set()
    if bank is not None:
        available = set(
            db.scalars(
                select(AssessmentTemplate.track_id).where(AssessmentTemplate.bank_version_id == bank.id)
            )
        )
    tracks = db.scalars(select(AssessmentTrack).order_by(AssessmentTrack.sort_order))
    return [
        TrackOut(
            id=t.id,
            name=t.name,
            description=t.description,
            question_count=QUESTIONS_PER_ATTEMPT,
            available=t.id in available,
            content_provenance=bank.content_provenance if bank else None,
        )
        for t in tracks
    ]
