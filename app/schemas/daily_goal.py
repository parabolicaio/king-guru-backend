"""Pydantic schemas for Daily Goal feature."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class GoalDetail(BaseModel):
    id: UUID
    title: str
    goal_type: str
    target_value: int
    xp_reward: int
    translations: dict


class GoalProgress(BaseModel):
    current_value: int
    is_completed: bool
    xp_awarded: int
    completed_at: datetime | None


class DailyGoalResponse(BaseModel):
    goal: GoalDetail | None
    progress: GoalProgress | None
