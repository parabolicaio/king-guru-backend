from pydantic import BaseModel
from uuid import UUID


class AttemptRequest(BaseModel):
    question_id: UUID
    response: dict


class StreakResult(BaseModel):
    status: str | None    # started | extended | maintained | null (practice)
    current: int
    longest: int
    milestone_bonus: int


class LessonResult(BaseModel):
    lesson_complete: bool
    next_lesson_id: UUID | None
    xp_from_lesson: int


class AttemptFeedback(BaseModel):
    correct: str | None = None
    incorrect: str | None = None


class PronunciationDetail(BaseModel):
    accuracy: float
    clarity: float
    fluency: float
    grade: str
    feedback: dict


class UnlockedAchievement(BaseModel):
    """Achievement unlocked BY this attempt — shown on the lesson summary
    (Task #24 Phase D). Exposes what check_and_unlock already computed."""

    id: UUID
    name: str
    xp_reward: int
    condition_type: str


class AttemptResponse(BaseModel):
    attempt_id: UUID
    score_fraction: float
    is_correct: bool
    score_numerator: int | None
    score_denominator: int | None
    xp_awarded: int
    feedback: AttemptFeedback
    lesson_result: LessonResult | None
    streak: StreakResult
    pronunciation_detail: PronunciationDetail | None = None
    # Default keeps the contract additive for old clients (sideloaded APKs).
    newly_unlocked_achievements: list[UnlockedAchievement] = []


class XPLedgerEntry(BaseModel):
    action_type: str
    xp_delta: int
    reference_type: str | None
    reference_id: UUID | None
    awarded_at: str


class XPSummaryResponse(BaseModel):
    xp_total: int
    data: list[XPLedgerEntry]
    cursor: str | None
    has_more: bool


class StreakResponse(BaseModel):
    streak_current: int
    streak_longest: int
    streak_last_activity_date: str | None
    next_milestone_days: int | None
    next_milestone_bonus_xp: int | None
