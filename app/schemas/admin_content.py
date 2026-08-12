"""Pydantic schemas for admin content authoring endpoints (B7)."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


# ── Lesson ──────────────────────────────────────────────────────────────────

class CreateLessonRequest(BaseModel):
    level_id: UUID
    title: str
    description: str | None = None
    is_guest_accessible: bool = False
    thumbnail_url: str | None = None
    translations: dict = {}
    objectives: list[str] = []
    objectives_translations: dict = {}


class UpdateLessonRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    is_guest_accessible: bool | None = None
    thumbnail_url: str | None = None
    translations: dict | None = None
    objectives: list[str] | None = None
    objectives_translations: dict | None = None
    is_minor_edit: bool = False  # True = audit-only, status unchanged; False (default) = major edit → pending_review


class AdminLessonItem(BaseModel):
    id: UUID
    level_id: UUID
    title: str
    description: str | None
    lesson_order: int
    status: str
    is_guest_accessible: bool
    thumbnail_url: str | None
    translations: dict
    objectives: list[str]
    objectives_translations: dict
    archived_at: datetime | None
    created_at: datetime
    updated_at: datetime


class AdminLessonListResponse(BaseModel):
    data: list[AdminLessonItem]
    total: int
    page: int
    page_size: int


# ── Section ──────────────────────────────────────────────────────────────────

class CreateSectionRequest(BaseModel):
    category: str  # vocabulary | grammar | pronunciation | reading | listening | writing | speaking
    display_order: int
    title: str | None = None
    translations: dict = {}


class UpdateSectionRequest(BaseModel):
    category: str | None = None
    display_order: int | None = None
    title: str | None = None
    translations: dict | None = None


class AdminSectionItem(BaseModel):
    id: UUID
    lesson_id: UUID
    category: str
    display_order: int
    title: str | None
    translations: dict
    created_at: datetime
    updated_at: datetime


# ── Content Block ────────────────────────────────────────────────────────────

class CreateBlockRequest(BaseModel):
    block_type: str  # text | image | audio | dialogue | word_card | rich_html | self_check
    display_order: int
    payload: dict = {}
    translations: dict = {}


class UpdateBlockRequest(BaseModel):
    block_type: str | None = None
    display_order: int | None = None
    payload: dict | None = None
    translations: dict | None = None


class AdminBlockItem(BaseModel):
    id: UUID
    lesson_section_id: UUID
    block_type: str
    display_order: int
    payload: dict
    translations: dict
    created_at: datetime
    updated_at: datetime


# ── Question ─────────────────────────────────────────────────────────────────

class CreateQuestionRequest(BaseModel):
    type: str
    purpose: str  # practice | assessment
    display_order: int
    prompt_text: str | None = None
    prompt_audio_url: str | None = None
    prompt_image_url: str | None = None
    payload: dict = {}
    xp_value: int = 0
    hint_text: str | None = None
    vocabulary_word_id: UUID | None = None
    translations: dict = {}


class UpdateQuestionRequest(BaseModel):
    type: str | None = None
    purpose: str | None = None
    display_order: int | None = None
    prompt_text: str | None = None
    prompt_audio_url: str | None = None
    prompt_image_url: str | None = None
    payload: dict | None = None
    xp_value: int | None = None
    hint_text: str | None = None
    vocabulary_word_id: UUID | None = None
    translations: dict | None = None


class AdminQuestionItem(BaseModel):
    id: UUID
    lesson_section_id: UUID
    type: str
    purpose: str
    display_order: int
    prompt_text: str | None
    prompt_audio_url: str | None
    prompt_image_url: str | None
    payload: dict
    xp_value: int
    hint_text: str | None
    vocabulary_word_id: UUID | None
    translations: dict
    created_at: datetime
    updated_at: datetime


# ── Vocabulary Word ──────────────────────────────────────────────────────────

class CreateVocabularyWordRequest(BaseModel):
    word: str
    definition: str
    example_sentence: str | None = None
    pronunciation_guide_si: str | None = None
    difficulty: str  # easy | medium | hard
    image_url: str | None = None
    translations: dict = {}


class UpdateVocabularyWordRequest(BaseModel):
    word: str | None = None
    definition: str | None = None
    example_sentence: str | None = None
    pronunciation_guide_si: str | None = None
    difficulty: str | None = None
    image_url: str | None = None
    translations: dict | None = None


class AdminVocabularyWordItem(BaseModel):
    id: UUID
    lesson_section_id: UUID
    word: str
    definition: str
    example_sentence: str | None
    pronunciation_guide_si: str | None
    difficulty: str
    image_url: str | None
    audio_url: str | None
    translations: dict
    created_at: datetime
    updated_at: datetime
