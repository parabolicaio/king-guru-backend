from datetime import date

import asyncpg


async def get_streak_state(
    db: asyncpg.Connection,
    user_id: str,
) -> asyncpg.Record | None:
    return await db.fetchrow(
        """
        SELECT streak_current, streak_longest, streak_last_activity_date
        FROM "user"
        WHERE id = $1
        """,
        user_id,
    )


async def update_streak(
    db: asyncpg.Connection,
    user_id: str,
    new_current: int,
    new_longest: int,
    last_activity_date: date,
) -> None:
    await db.execute(
        """
        UPDATE "user"
        SET streak_current = $2,
            streak_longest = $3,
            streak_last_activity_date = $4,
            updated_at = now()
        WHERE id = $1
        """,
        user_id,
        new_current,
        new_longest,
        last_activity_date,
    )


async def get_streak_milestones(db: asyncpg.Connection) -> list[asyncpg.Record]:
    return await db.fetch(
        "SELECT days, bonus_xp FROM streak_milestone ORDER BY days ASC"
    )
