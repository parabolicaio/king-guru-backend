"""Pydantic schemas for achievements and leaderboard."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AchievementItem(BaseModel):
    id: UUID
    name: str
    description: str
    icon_url: str | None
    condition_type: str
    condition_value: int
    xp_reward: int
    is_active: bool
    translations: dict
    unlocked_at: datetime | None  # null if not yet unlocked


class AchievementsResponse(BaseModel):
    data: list[AchievementItem]
    unlocked_count: int
    total_count: int


class LeaderboardEntry(BaseModel):
    rank: int
    user_id: UUID
    display_name: str
    avatar_url: str | None
    xp_total: int
    level_code: str | None
    is_current_user: bool


class LeaderboardResponse(BaseModel):
    data: list[LeaderboardEntry]
    current_user_rank: int | None
    period: str  # all_time | weekly
