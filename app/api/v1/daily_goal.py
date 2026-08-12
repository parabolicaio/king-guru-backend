"""Daily Goal endpoint."""

import asyncpg
from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.db.pool import get_db
from app.schemas.daily_goal import DailyGoalResponse
from app.services import daily_goal_service

router = APIRouter(prefix="/api/v1/daily-goal", tags=["daily-goal"])


@router.get("/today", response_model=DailyGoalResponse)
async def get_today(
    user: asyncpg.Record = Depends(get_current_user),
    db: asyncpg.Connection = Depends(get_db),
) -> DailyGoalResponse:
    """Return today's goal and the authenticated user's progress.

    Lazily generates the assignment for the user's level if none exists yet.
    Returns goal=null if the user has no level assigned yet.
    """
    result = await daily_goal_service.get_today(db, user)
    assignment = result["assignment"]
    progress = result["progress"]

    if assignment is None:
        return DailyGoalResponse(goal=None, progress=None)

    from app.schemas.daily_goal import GoalDetail, GoalProgress

    goal = GoalDetail(
        id=str(assignment["goal_id"]),
        title=assignment["title"],
        goal_type=assignment["goal_type"],
        target_value=assignment["target_value"],
        xp_reward=assignment["xp_reward"],
        translations=dict(assignment["translations"] or {}),
    )

    prog = None
    if progress is not None:
        prog = GoalProgress(
            current_value=progress["current_value"],
            is_completed=progress["is_completed"],
            xp_awarded=progress["xp_awarded"],
            completed_at=progress["completed_at"],
        )

    return DailyGoalResponse(goal=goal, progress=prog)
