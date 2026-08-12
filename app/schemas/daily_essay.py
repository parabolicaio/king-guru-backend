"""Pydantic schemas for Daily Essay feature."""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel


class EssayPromptResponse(BaseModel):
    id: UUID
    prompt_text: str
    level_id: UUID | None
    date_assigned: date | None
    translations: dict


class SaveDraftRequest(BaseModel):
    essay_prompt_id: UUID
    draft_text: str
    feedback_language: str = "en"


class SubmitEssayRequest(BaseModel):
    essay_text: str
    essay_prompt_id: UUID
    feedback_language: str = "en"


class EssayGradeDetail(BaseModel):
    score_grammar: float | None
    score_vocabulary: float | None
    score_content: float | None
    score_suggestions: float | None
    overall_summary: str | None
    ai_feedback: dict | None


class EssaySubmissionResponse(BaseModel):
    id: UUID
    essay_prompt_id: UUID
    prompt_text: str
    essay_text: str
    submitted_at: datetime | None      # NULL while is_draft=True
    submission_date: date
    is_draft: bool
    grade: str | None                  # NULL until Gemini grades
    xp_awarded: int
    feedback_language: str
    grading: EssayGradeDetail | None   # populated once grade is available


class TodayEssayResponse(BaseModel):
    prompt: EssayPromptResponse
    submission: EssaySubmissionResponse | None  # None = not started


class EssayHistoryItem(BaseModel):
    id: UUID
    essay_prompt_id: UUID
    prompt_text: str
    submission_date: date
    grade: str | None
    xp_awarded: int
    submitted_at: datetime
    word_count: int


class EssayHistoryResponse(BaseModel):
    data: list[EssayHistoryItem]
    cursor: str | None
    has_more: bool
