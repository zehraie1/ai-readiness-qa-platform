import uuid
from typing import Literal

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.core.errors import ErrorEnvelope
from app.db.session import get_db
from app.modules.attempts import service
from app.modules.attempts.schemas import (
    AnswerIn,
    AnswerOut,
    AttemptListOut,
    AttemptOut,
    ReviewOut,
    StartAttemptIn,
)
from app.modules.auth.dependencies import require_participant
from app.modules.auth.models import User
from app.modules.results.schemas import RecommendationOut, ResultOut

router = APIRouter(prefix="/attempts", tags=["attempts"])
E = {"model": ErrorEnvelope}
ERRORS = {401: E, 403: E, 404: E, 409: E, 422: E}


@router.post("", response_model=AttemptOut, status_code=201, responses={200: {"model": AttemptOut}, **ERRORS})
def start(
    body: StartAttemptIn,
    response: Response,
    user: User = Depends(require_participant),
    db: Session = Depends(get_db),
) -> AttemptOut:
    attempt, created = service.start_attempt(db, user, body.track_id)
    if not created:
        response.status_code = 200
    return service.attempt_detail(db, attempt)


@router.get("", response_model=AttemptListOut, responses=ERRORS)
def list_mine(
    status: Literal["in_progress", "submitted"] | None = None,
    limit: int = Query(20, ge=1, le=50),
    offset: int = Query(0, ge=0),
    user: User = Depends(require_participant),
    db: Session = Depends(get_db),
) -> AttemptListOut:
    return service.list_attempts(db, user, status, limit, offset)


@router.get("/{attempt_id}", response_model=AttemptOut, responses=ERRORS)
def get_one(
    attempt_id: uuid.UUID, user: User = Depends(require_participant), db: Session = Depends(get_db)
) -> AttemptOut:
    return service.attempt_detail(db, service.load_owned(db, user, attempt_id))


@router.put("/{attempt_id}/answers/{question_id}", response_model=AnswerOut, responses=ERRORS)
def answer(
    attempt_id: uuid.UUID,
    question_id: uuid.UUID,
    body: AnswerIn,
    user: User = Depends(require_participant),
    db: Session = Depends(get_db),
) -> AnswerOut:
    return service.save_answer(db, user, attempt_id, question_id, body.selected_option_id)


@router.get("/{attempt_id}/review", response_model=ReviewOut, responses=ERRORS)
def review(
    attempt_id: uuid.UUID, user: User = Depends(require_participant), db: Session = Depends(get_db)
) -> ReviewOut:
    return service.review(db, user, attempt_id)


@router.post("/{attempt_id}/submit", response_model=ResultOut, responses=ERRORS)
def submit(
    attempt_id: uuid.UUID, user: User = Depends(require_participant), db: Session = Depends(get_db)
) -> ResultOut:
    return service.submit(db, user, attempt_id)


@router.get("/{attempt_id}/results", response_model=ResultOut, responses=ERRORS)
def results(
    attempt_id: uuid.UUID, user: User = Depends(require_participant), db: Session = Depends(get_db)
) -> ResultOut:
    return service.results_for(db, user, attempt_id)


@router.get("/{attempt_id}/recommendations", response_model=list[RecommendationOut], responses=ERRORS)
def recommendations(
    attempt_id: uuid.UUID, user: User = Depends(require_participant), db: Session = Depends(get_db)
) -> list[RecommendationOut]:
    return service.results_for(db, user, attempt_id).recommendations
