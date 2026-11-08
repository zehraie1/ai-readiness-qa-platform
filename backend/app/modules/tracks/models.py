from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AssessmentTrack(Base):
    __tablename__ = "assessment_tracks"

    id: Mapped[str] = mapped_column(Text, primary_key=True)  # e.g. "sdet"
    name: Mapped[str] = mapped_column(Text, unique=True)
    description: Mapped[str] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer)
