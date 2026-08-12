"""Achievement unlock service.

Called after relevant events (attempt submission, essay, streak milestones).
Checks condition against user state and unlocks if met.
"""

import asyncpg

from app.db.queries.achievements import (
    get_all_achievements_with_user_state,
    get_user_achievement,
    unlock_achievement,
)


async def check_and_unlock(
    db: asyncpg.Connection,
    user: asyncpg.Record,
) -> list[asyncpg.Record]:
    """Check all active achievements for the user and unlock any newly met conditions.

    Returns list of newly unlocked achievement rows.
    """
    achievements = await get_all_achievements_with_user_state(db, str(user["id"]))
    stats = await _compute_stats(db, user)
    newly_unlocked = []

    for ach in achievements:
        if ach["unlocked_at"] is not None:
            continue  # already unlocked

        met = _condition_met(ach, stats)
        if met:
            await unlock_achievement(db, str(user["id"]), str(ach["id"]))
            # Return the ACHIEVEMENT row (name/xp_reward/etc.), not the join
            # row — Task #24 Phase D surfaces these on the lesson summary.
            newly_unlocked.append(ach)

            # Award XP
            if ach["xp_reward"] > 0:
                from app.services import xp as xp_service
                await xp_service.award(
                    db,
                    user_id=str(user["id"]),
                    action_type="achievement_unlocked",
                    xp_delta=ach["xp_reward"],
                    reference_id=str(ach["id"]),
                    reference_type="achievement",
                )

            # Notify
            from app.services import notification as notification_service
            await notification_service.create(
                db,
                user_id=str(user["id"]),
                notif_type="achievement_unlocked",
                title=f"Achievement unlocked: {ach['name']}",
                body=ach["description"],
                reference_id=str(ach["id"]),
                reference_type=None,
            )

    return newly_unlocked


async def _compute_stats(db: asyncpg.Connection, user: asyncpg.Record) -> dict[str, int]:
    """Gather the metrics every achievement condition_type is measured against.

    Keyed by condition_type so `_condition_met` is a direct lookup. Denormalised
    xp_total / streak_current come off the user row; the rest are counted live.
    """
    uid = str(user["id"])
    lesson_count = await db.fetchval(
        "SELECT count(*) FROM lesson_progress WHERE user_id = $1::uuid AND status = 'completed'",
        uid,
    )
    words_mastered = await db.fetchval(
        "SELECT count(*) FROM vocabulary_mastery WHERE user_id = $1::uuid AND is_mastered = TRUE",
        uid,
    )
    essay_count = await db.fetchval(
        "SELECT count(*) FROM daily_essay_submission WHERE user_id = $1::uuid",
        uid,
    )
    return {
        "xp_total": user["xp_total"] or 0,
        "streak_days": user["streak_current"] or 0,
        "lesson_count": lesson_count or 0,
        "words_mastered": words_mastered or 0,
        "essay_count": essay_count or 0,
    }


def _condition_met(ach: asyncpg.Record, stats: dict[str, int]) -> bool:
    ctype = ach["condition_type"]
    cval = ach["condition_value"]
    # `custom` (and any unknown type) has no automatic metric — never auto-unlocks.
    if ctype not in stats:
        return False
    return stats[ctype] >= cval
