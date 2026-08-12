from uuid import UUID

from pydantic import BaseModel


class PlacementQuestion(BaseModel):
    id: UUID
    type: str
    prompt_text: str | None
    payload: dict
    difficulty: str
    skill_category: str | None
    xp_value: int
    display_order: int
    translations: dict = {}


class PlacementQuestionsResponse(BaseModel):
    questions: list[PlacementQuestion]


class PlacementAnswer(BaseModel):
    question_id: UUID
    response: dict


class PlacementSubmitRequest(BaseModel):
    answers: list[PlacementAnswer]
    confirm_level_id: str | None = None  # if set, persists chosen level atomically with scoring


class PlacementAnswerDetail(BaseModel):
    """Per-question result shown on the assessment results screen."""
    question_id: UUID
    prompt_text: str | None
    skill_category: str | None
    difficulty: str
    user_response: dict
    correct_answer: dict  # extracted from payload for display; shape varies by type
    is_correct: bool
    xp_awarded: int


class PlacementSkillBreakdown(BaseModel):
    """Correct-answer breakdown by skill category."""
    skill_category: str
    correct: int
    total: int
    accuracy: float  # 0.0–100.0


class PlacementSubmitResponse(BaseModel):
    score_percent: float           # overall percentage correct
    accuracy: float                # same value; explicit field for frontend clarity
    recommended_level_id: UUID | None
    recommended_level: str
    correct_count: int
    total_count: int
    xp_awarded: int
    answers: list[PlacementAnswerDetail]
    skill_breakdown: list[PlacementSkillBreakdown]


class PlacementChooseLevelRequest(BaseModel):
    level_id: UUID


class PlacementChooseLevelResponse(BaseModel):
    current_level_id: UUID
    placement_completed_at: str
