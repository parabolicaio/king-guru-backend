from uuid import UUID

from pydantic import BaseModel


class LevelResponse(BaseModel):
    id: UUID
    code: str
    name: str
    description: str | None
    display_order: int
    daily_essay_enabled: bool
    translations: dict = {}
    icon_url: str | None = None
    topics: list = []
    guest_enabled: bool = False
    payment_required: bool = False


class LevelsListResponse(BaseModel):
    levels: list[LevelResponse]
