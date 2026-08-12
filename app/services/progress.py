"""Lesson progress service."""

from dataclasses import dataclass

import asyncpg

from app.db.queries.attempts import (
    get_answered_assessment_question_ids,
    get_assessment_question_ids_for_lesson,
)
from app.db.utils import new_uuid
from app.services import notification as notification_service
from app.services.lesson_chain import unlock_next_lesson


@dataclass
class ProgressResult:
    lesson_complete: bool
    next_lesson_id: str | None
    xp_from_lesson: int


async def record_attempt(
    db: asyncpg.Connection,
    user_id: str,
    lesson_id: str,
    purpose: str,
) -> ProgressResult:
    """Update lesson progress after an attempt.

    Checks if all assessment questions now have at least one attempt.
    On completion: unlocks next lesson + creates notifications.

    Returns ProgressResult with completion state and any lesson-complete XP.
    Must be called within the attempt transaction.
    """
    from app.services import xp as xp_service

    if purpose != "assessment":
        return ProgressResult(lesson_complete=False, next_lesson_id=None, xp_from_lesson=0)

    # Upsert lesson_progress — creates the row on first attempt (e.g. Lesson 1
    # which has no row yet) and advances not_started → in_progress on conflict.
    await db.execute(
        """
        INSERT INTO lesson_progress (id, user_id, lesson_id, status, completion_pct, started_at)
        VALUES ($1, $2, $3, 'in_progress', 0, now())
        ON CONFLICT (user_id, lesson_id) DO UPDATE
        SET status      = CASE
                WHEN lesson_progress.status = 'completed'   THEN 'completed'
                WHEN lesson_progress.status = 'not_started' THEN 'in_progress'
                ELSE lesson_progress.status
            END,
            started_at  = COALESCE(lesson_progress.started_at, now()),
            updated_at  = now()
        """,
        str(new_uuid()),
        user_id,
        lesson_id,
    )

    all_ids = set(await get_assessment_question_ids_for_lesson(db, lesson_id))
    answered_ids = set(await get_answered_assessment_question_ids(db, user_id, lesson_id))

    if not all_ids or not all_ids.issubset(answered_ids):
        total = len(all_ids)
        done = len(answered_ids & all_ids)
        pct = (done / total * 100) if total > 0 else 0
        await db.execute(
            """
            UPDATE lesson_progress
            SET completion_pct = $3, updated_at = now()
            WHERE user_id = $1 AND lesson_id = $2
            """,
            user_id,
            lesson_id,
            pct,
        )
        return ProgressResult(lesson_complete=False, next_lesson_id=None, xp_from_lesson=0)

    # All assessment questions answered — mark complete (no-op if already completed)
    update_result = await db.execute(
        """
        UPDATE lesson_progress
        SET status = 'completed',
            completion_pct = 100,
            completed_at = COALESCE(completed_at, now()),
            updated_at = now()
        WHERE user_id = $1 AND lesson_id = $2 AND status != 'completed'
        """,
        user_id,
        lesson_id,
    )

    # UPDATE 0 rows → lesson was already completed on a prior run; skip all side-effects
    if update_result == "UPDATE 0":
        return ProgressResult(lesson_complete=False, next_lesson_id=None, xp_from_lesson=0)

    # First completion — award XP, notify, unlock
    lesson_xp = await xp_service.lookup(db, "lesson_complete")
    xp_from_lesson = 0
    if lesson_xp > 0:
        await xp_service.award(
            db,
            user_id=user_id,
            action_type="lesson_complete",
            xp_delta=lesson_xp,
            reference_id=lesson_id,
            reference_type="lesson",
        )
        xp_from_lesson = lesson_xp

    await notification_service.create(
        db,
        user_id=user_id,
        notif_type="lesson_complete",
        title="Lesson completed!",
        body="You have finished a lesson.",
        reference_id=lesson_id,
        reference_type="lesson",
    )

    next_lesson_id = await unlock_next_lesson(db, user_id, lesson_id)

    if next_lesson_id:
        await notification_service.create(
            db,
            user_id=user_id,
            notif_type="lesson_unlocked",
            title="New lesson unlocked!",
            body="Your next lesson is ready.",
            reference_id=next_lesson_id,
            reference_type="lesson",
        )

    return ProgressResult(
        lesson_complete=True,
        next_lesson_id=next_lesson_id,
        xp_from_lesson=xp_from_lesson,
    )
