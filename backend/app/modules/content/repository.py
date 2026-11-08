"""Read access to published content."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.content.models import AssessmentTemplate, QuestionBankVersion


def published_bank(db: Session) -> QuestionBankVersion | None:
    return db.scalar(select(QuestionBankVersion).where(QuestionBankVersion.status == "published"))


def published_template(db: Session, track_id: str) -> AssessmentTemplate | None:
    bank = published_bank(db)
    if bank is None:
        return None
    return db.scalar(
        select(AssessmentTemplate).where(
            AssessmentTemplate.bank_version_id == bank.id,
            AssessmentTemplate.track_id == track_id,
        )
    )
