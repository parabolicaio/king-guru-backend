from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class VocabMasteryDetail(BaseModel):
    attempt_count: int
    correct_attempt_count: int
    is_mastered: bool
    last_seen_at: datetime | None


class VocabularyWordItem(BaseModel):
    id: UUID
    word: str
    definition: str
    example_sentence: str | None
    pronunciation_guide_si: str | None
    difficulty: str
    image_url: str | None
    audio_url: str | None
    level_code: str
    translations: dict = {}
    mastery: VocabMasteryDetail


class VocabularyListResponse(BaseModel):
    data: list[VocabularyWordItem]
    cursor: str | None
    has_more: bool
