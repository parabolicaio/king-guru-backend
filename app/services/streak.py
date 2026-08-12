"""Streak service — daily streak tracking with SLST day-boundary logic."""

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import asyncpg

from app.db.queries.streak import (
    get_streak_milestones,
    get_streak_state,
    update_streak,
)
from app.services import notification as notification_service
from app.services import xp as xp_service


def today_slst() -> date:
    """Return today's date in SLST (Asia/Colombo).

    Never hardcode UTC+5:30 — always use ZoneInfo.
    """
    return datetime.now(tz=ZoneInfo("Asia/Colombo")).date()


@dataclass
class StreakResult:
    status: str         # started | extended | maintained | unchanged
    streak_current: int
    streak_longest: int
    milestone_bonus: int


async def record_qualifying_activity(
    db: asyncpg.Connection,
    user_id: str,
) -> StreakResult:
    """Record a qualifying streak activity for today.

    Qualifying: assessment question attempt OR daily essay submission.
    Practice question attempts do NOT qualify.

    Returns the new streak state. Idempotent for the same SLST day.
    """
    state = await get_streak_state(db, user_id)
    if state is None:
        return StreakResult(status="unchanged", streak_current=0, streak_longest=0, milestone_bonus=0)

    today = today_slst()
    last = state["streak_last_activity_date"]

    current = state["streak_current"]
    longest = state["streak_longest"]

    if last is not None and last == today:
        # Already qualified today — idempotent
        return StreakResult(
            status="maintained",
            streak_current=current,
            streak_longest=longest,
            milestone_bonus=0,
        )

    if last is not None and last == today - timedelta(days=1):
        new_current = current + 1
        status = "extended"
    elif last is None or last < today - timedelta(days=1):
        new_current = 1
        status = "started"
    else:
        new_current = current
        status = "maintained"

    new_longest = max(longest, new_current)

    await update_streak(db, user_id, new_current, new_longest, today)

    # Award daily streak base XP
    streak_day_xp = await xp_service.lookup(db, "streak_day")
    if streak_day_xp > 0:
        await xp_service.award(db, user_id, "streak_day", streak_day_xp)

    # Check milestones
    milestone_bonus = 0
    milestones = await get_streak_milestones(db)
    for m in milestones:
        if m["days"] == new_current:
            bonus = m["bonus_xp"]
            await xp_service.award(db, user_id, "streak_milestone", bonus)
            milestone_bonus = bonus
            await notification_service.create(
                db,
                user_id=user_id,
                notif_type="streak_milestone",
                title=f"{new_current}-day streak!",
                body=f"You earned {bonus} bonus XP for keeping your streak alive.",
            )
            break

    return StreakResult(
        status=status,
        streak_current=new_current,
        streak_longest=new_longest,
        milestone_bonus=milestone_bonus,
    )
