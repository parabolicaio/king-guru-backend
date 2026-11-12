"""Leaderboard endpoint."""

import asyncpg
from fastapi import APIRouter, Depends

from app.core.config import settings
from app.core.security import get_current_user
from app.db.pool import get_db
from app.db.queries.achievements import get_leaderboard, get_user_rank, leaderboard_name
from app.schemas.achievements import LeaderboardEntry, LeaderboardResponse

router = APIRouter(prefix="/api/v1/leaderboard", tags=["leaderboard"])


@router.get("", response_model=LeaderboardResponse)
async def get_leaderboard_endpoint(
    limit: int = 50,
    user: asyncpg.Record = Depends(get_current_user),
    db: asyncpg.Connection = Depends(get_db),
) -> LeaderboardResponse:
    limit = min(limit, 100)
    rows = await get_leaderboard(db, limit=limit)

    current_user_id = str(user["id"])
    current_user_rank: int | None = None
    entries = []

    for r in rows:
        is_current = str(r["id"]) == current_user_id
        if is_current:
            current_user_rank = int(r["rank"])

        entries.append(
            LeaderboardEntry(
                rank=int(r["rank"]),
                user_id=r["id"],
                display_name=leaderboard_name(r["display_name"], r["full_name"]),
                avatar_url=settings.build_cdn_url(r["avatar_url"]),
                xp_total=r["xp_total"],
                level_code=r["level_code"],
                is_current_user=is_current,
            )
        )

    # Not in the top N: their rank among the people shown. None when they
    # are not shown at all (hidden, or no XP yet).
    if current_user_rank is None:
        current_user_rank = await get_user_rank(db, current_user_id)

    return LeaderboardResponse(
        data=entries,
        current_user_rank=current_user_rank,
        period="all_time",
    )
