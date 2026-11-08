from pydantic import BaseModel


class TrackOut(BaseModel):
    id: str
    name: str
    description: str
    question_count: int
    available: bool
    content_provenance: str | None
