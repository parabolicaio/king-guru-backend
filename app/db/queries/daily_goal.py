"""Raw SQL query functions for Daily Goal."""

from datetime import date

import asyncpg

from app.db.utils import new_uuid

# Joined SELECT reused by get_assignment and generate_assignment
_ASSIGNMENT_SELECT = """
    SELECT
        dga.id            AS assignment_id,
        dga.level_id,
        dga.goal_date,
        dg.id             AS goal_id,
        dg.goal_type,
        dg.title,
        dg.target_value,
        dg.xp_reward,
        dg.translations
    FROM daily_goal_assignment dga
    JOIN daily_goal dg ON dg.id = dga.daily_goal_id
"""


async def get_assignment(
    db: asyncpg.Connection,
    level_id: str,
    goal_date: date,
) -> asyncpg.Record | None:
    return await db.fetchrow(
        f"{_ASSIGNMENT_SELECT} WHERE dga.level_id = $1::uuid AND dga.goal_date = $2",
        level_id,
        goal_date,
    )


async def get_templates_for_level(
    db: asyncpg.Connection,
    level_id: str,
) -> list[asyncpg.Record]:
    return await db.fetch(
        "SELECT * FROM daily_goal WHERE level_id = $1::uuid AND is_active = TRUE",
        level_id,
    )


async def insert_assignment(
    db: asyncpg.Connection,
    level_id: str,
    daily_goal_id: str,
    goal_date: date,
) -> None:
    """Insert assignment row.  ON CONFLICT DO NOTHING absorbs concurrent inserts."""
    row_id = new_uuid()
    await db.execute(
        """
        INSERT INTO daily_goal_assignment (id, daily_goal_id, level_id, goal_date, created_at)
        VALUES ($1, $2::uuid, $3::uuid, $4, now())
        ON CONFLICT (level_id, goal_date) DO NOTHING
        """,
        row_id,
        daily_goal_id,
        level_id,
        goal_date,
    )


async def get_progress(
    db: asyncpg.Connection,
    user_id: str,
    daily_goal_id: str,
    goal_date: date,
) -> asyncpg.Record | None:
    return await db.fetchrow(
        """
        SELECT * FROM daily_goal_progress
        WHERE user_id = $1::uuid AND daily_goal_id = $2::uuid AND goal_date = $3
        """,
        user_id,
        daily_goal_id,
        goal_date,
    )


async def upsert_progress(
    db: asyncpg.Connection,
    user_id: str,
    daily_goal_id: str,
    goal_date: date,
    increment: int,
) -> asyncpg.Record:
    """Increment current_value.  No-op if the goal is already completed."""
    row_id = new_uuid()
    return await db.fetchrow(
        """
        INSERT INTO daily_goal_progress
            (id, user_id, daily_goal_id, goal_date, current_value, is_completed,
             created_at, updated_at)
        VALUES ($1, $2::uuid, $3::uuid, $4, $5, FALSE, now(), now())
        ON CONFLICT (user_id, daily_goal_id, goal_date) DO UPDATE
            SET current_value = CASE
                    WHEN daily_goal_progress.is_completed THEN daily_goal_progress.current_value
                    ELSE daily_goal_progress.current_value + EXCLUDED.current_value
                END,
                updated_at = now()
        RETURNING *
        """,
        row_id,
        user_id,
        daily_goal_id,
        goal_date,
        increment,
    )


async def mark_complete(
    db: asyncpg.Connection,
    user_id: str,
    daily_goal_id: str,
    goal_date: date,
    xp_awarded: int,
) -> asyncpg.Record | None:
    """Flip is_completed = TRUE only if not already complete and target is met.
    Returns the updated row if the update took effect, None if it was already done.
    """
    return await db.fetchrow(
        """
        UPDATE daily_goal_progress
        SET is_completed = TRUE,
            completed_at = now(),
            xp_awarded   = $4,
            updated_at   = now()
        WHERE user_id       = $1::uuid
          AND daily_goal_id = $2::uuid
          AND goal_date     = $3
          AND is_completed  = FALSE
        RETURNING *
        """,
        user_id,
        daily_goal_id,
        goal_date,
        xp_awarded,
    )
