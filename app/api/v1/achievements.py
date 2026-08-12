"""Achievements endpoints."""

import asyncpg
from fastapi import APIRouter, Depends

from app.core.config import settings
from app.core.security import get_current_user
from app.db.pool import get_db
from app.db.queries.achievements import get_all_achievements_with_user_state
from app.schemas.achievements import AchievementItem, AchievementsResponse

router = APIRouter(prefix="/api/v1/achievements", tags=["achievements"])


@router.get("", response_model=AchievementsResponse)
async def list_achievements(
    user: asyncpg.Record = Depends(get_current_user),
    db: asyncpg.Connection = Depends(get_db),
) -> AchievementsResponse:
    rows = await get_all_achievements_with_user_state(db, str(user["id"]))
    unlocked = sum(1 for r in rows if r["unlocked_at"] is not None)

    return AchievementsResponse(
        data=[
            AchievementItem(
                id=r["id"],
                name=r["name"],
                description=r["description"],
                icon_url=settings.build_cdn_url(r["icon_url"]),
                condition_type=r["condition_type"],
                condition_value=r["condition_value"],
                xp_reward=r["xp_reward"],
                is_active=r["is_active"],
                translations=dict(r["translations"] or {}),
                unlocked_at=r["unlocked_at"],
            )
            for r in rows
        ],
        unlocked_count=unlocked,
        total_count=len(rows),
    )
