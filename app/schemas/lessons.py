from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class LatestAttempt(BaseModel):
    id: UUID
    score_fraction: float
    is_correct: bool
    response: dict
    xp_awarded: int
    created_at: datetime


class VocabularyMastery(BaseModel):
    attempt_count: int
    correct_attempt_count: int
    is_mastered: bool


class VocabularyWordInLesson(BaseModel):
    id: UUID
    word: str
    definition: str
    example_sentence: str | None
    pronunciation_guide_si: str | None
    difficulty: str
    image_url: str | None
    audio_url: str | None
    translations: dict = {}
    mastery: VocabularyMastery | None = None


class ContentBlock(BaseModel):
    id: UUID
    block_type: str
    display_order: int
    payload: dict
    translations: dict = {}


class QuestionInLesson(BaseModel):
    id: UUID
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
    translations: dict = {}
    latest_attempt: LatestAttempt | None = None


class LessonSection(BaseModel):
    id: UUID
    category: str
    display_order: int
    title: str | None
    image_url: str | None = None
    translations: dict = {}
    content_blocks: list[ContentBlock] = []
    questions: list[QuestionInLesson] = []
    vocabulary_words: list[VocabularyWordInLesson] = []


class LessonDetail(BaseModel):
    id: UUID
    title: str
    description: str | None
    lesson_order: int
    status: str
    thumbnail_url: str | None
    is_guest_accessible: bool
    translations: dict = {}
    objectives: list[str] = []
    objectives_translations: dict = {}
    sections: list[LessonSection] = []


class LessonDetailResponse(BaseModel):
    lesson: LessonDetail


class LessonProgress(BaseModel):
    status: str
    completion_pct: float
    completed_at: datetime | None


class LessonSummary(BaseModel):
    id: UUID
    title: str
    description: str | None
    lesson_order: int
    thumbnail_url: str | None
    is_guest_accessible: bool
    translations: dict = {}
    progress: LessonProgress


class LevelInfo(BaseModel):
    id: UUID
    name: str
    code: str


class LessonsListResponse(BaseModel):
    level: LevelInfo
    lessons: list[LessonSummary]


class UserProgressSummary(BaseModel):
    xp_total: int
    streak_current: int
    streak_longest: int
    streak_last_activity_date: str | None
    current_level_id: UUID | None
    completed_lesson_count: int


class UserProgressResponse(BaseModel):
    user: UserProgressSummary
    current_level: LevelInfo | None
    lessons: list[LessonSummary]
