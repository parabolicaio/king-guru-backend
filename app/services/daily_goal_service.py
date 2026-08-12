"""Daily Goal service — lazy assignment generation and progress tracking."""

import logging
import random
from datetime import date
from zoneinfo import ZoneInfo

import asyncpg

from app.db.queries.daily_goal import (
    get_assignment,
    get_progress,
    get_templates_for_level,
    insert_assignment,
    mark_complete,
    upsert_progress,
)

logger = logging.getLogger(__name__)

SLST = ZoneInfo("Asia/Colombo")


def today_slst() -> date:
    from datetime import datetime
    return datetime.now(SLST).date()


async def get_today(
    db: asyncpg.Connection,
    user: asyncpg.Record,
) -> dict:
    """Return today's goal and the user's progress.

    Lazily generates the assignment for the user's level if none exists yet.
    Returns: { "assignment": Record, "progress": Record | None }
    """
    level_id = str(user["current_level_id"]) if user["current_level_id"] else None
    if level_id is None:
        return {"assignment": None, "progress": None}

    today = today_slst()
    assignment = await get_assignment(db, level_id, today)

    if assignment is None:
        assignment = await _generate_assignment(db, level_id, today)

    if assignment is None:
        return {"assignment": None, "progress": None}

    progress = await get_progress(
        db, str(user["id"]), str(assignment["goal_id"]), today
    )
    return {"assignment": assignment, "progress": progress}


async def _generate_assignment(
    db: asyncpg.Connection,
    level_id: str,
    goal_date: date,
) -> asyncpg.Record | None:
    """Pick a random template for the level and write the assignment row.

    ON CONFLICT DO NOTHING in insert_assignment handles the race condition where
    two concurrent requests both find no assignment and try to generate one.
    We re-fetch after the insert to get whichever row won.
    """
    templates = await get_templates_for_level(db, level_id)
    if not templates:
        logger.warning("No daily goal templates found for level_id=%s", level_id)
        return None

    chosen = random.choice(templates)
    await insert_assignment(db, level_id, str(chosen["id"]), goal_date)
    return await get_assignment(db, level_id, goal_date)


async def record_activity(
    db: asyncpg.Connection,
    user_id: str,
    action_type: str,
    increment: int = 1,
    level_id: str | None = None,
) -> None:
    """Increment today's goal progress if the active goal matches action_type.

    Safe to call without knowing whether a goal is active — returns quickly
    if there is no matching goal or if the goal is already complete.

    level_id is optional; if omitted it is looked up from the user row.
    """
    try:
        if increment <= 0:
            return

        if level_id is None:
            row = await db.fetchrow(
                'SELECT current_level_id FROM "user" WHERE id = $1::uuid', user_id
            )
            if row is None or row["current_level_id"] is None:
                return
            level_id = str(row["current_level_id"])

        today = today_slst()
        assignment = await get_assignment(db, level_id, today)
        if assignment is None or assignment["goal_type"] != action_type:
            return

        daily_goal_id = str(assignment["goal_id"])
        progress = await upsert_progress(db, user_id, daily_goal_id, today, increment)

        if (
            not progress["is_completed"]
            and progress["current_value"] >= assignment["target_value"]
        ):
            completed_row = await mark_complete(
                db, user_id, daily_goal_id, today, assignment["xp_reward"]
            )
            if completed_row is not None and assignment["xp_reward"] > 0:
                from app.services import xp as xp_service
                await xp_service.award(
                    db,
                    user_id=user_id,
                    action_type="daily_goal_complete",
                    xp_delta=assignment["xp_reward"],
                    reference_id=str(completed_row["id"]),
                    reference_type="daily_goal",
                )

    except Exception:
        # Never let goal tracking break the primary request
        logger.exception(
            "daily_goal record_activity failed user=%s action=%s", user_id, action_type
        )
