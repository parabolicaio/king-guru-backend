"""Lesson chain service — ordering, unlock state, and chain traversal."""

from dataclasses import dataclass
from uuid import UUID

import asyncpg

from app.db.utils import new_uuid


@dataclass
class LessonWithProgress:
    id: str
    title: str
    description: str | None
    lesson_order: int
    thumbnail_url: str | None
    is_guest_accessible: bool
    translations: dict
    status: str           # locked | not_started | in_progress | completed
    completion_pct: float
    completed_at: str | None


async def compute_next_order(db: asyncpg.Connection, level_id: str) -> int:
    """Return lesson_order for a new lesson appended to a level.

    This is the ONLY source of a new lesson_order value — never accept it
    from request bodies.
    """
    row = await db.fetchrow(
        """
        SELECT COALESCE(MAX(lesson_order), 0) + 1 AS next_order
        FROM lesson
        WHERE level_id = $1 AND deleted_at IS NULL
        """,
        level_id,
    )
    return row["next_order"]


async def get_lessons_with_progress(
    db: asyncpg.Connection,
    level_id: str,
    user_id: str | None,
) -> list[LessonWithProgress]:
    """Return approved, non-archived, non-deleted lessons for a level,
    each annotated with the user's progress state.

    user_id may be None (guest / anonymous) — the progress LEFT JOIN then
    matches nothing (lp.user_id = NULL is never true), so every lesson comes
    back with no progress, which is the correct guest view."""

    lessons = await db.fetch(
        """
        SELECT l.id, l.title, l.description, l.lesson_order,
               l.thumbnail_url, l.is_guest_accessible, l.translations,
               lp.status AS progress_status,
               COALESCE(lp.completion_pct, 0) AS completion_pct,
               lp.completed_at
        FROM lesson l
        LEFT JOIN lesson_progress lp
            ON lp.lesson_id = l.id AND lp.user_id = $2
        WHERE l.level_id = $1
          AND l.status = 'approved'
          AND l.archived_at IS NULL
          AND l.deleted_at IS NULL
        ORDER BY l.lesson_order ASC
        """,
        level_id,
        user_id,
    )

    result: list[LessonWithProgress] = []
    prev_completed = True   # lesson_order=1 is always accessible

    for row in lessons:
        raw_status = row["progress_status"]

        if raw_status == "completed":
            status = "completed"
            prev_completed = True
        elif raw_status in ("in_progress", "not_started"):
            status = raw_status
            prev_completed = False
        else:
            # No lesson_progress row
            status = "not_started" if prev_completed else "locked"
            prev_completed = False

        result.append(
            LessonWithProgress(
                id=str(row["id"]),
                title=row["title"],
                description=row["description"],
                lesson_order=row["lesson_order"],
                thumbnail_url=row["thumbnail_url"],
                is_guest_accessible=row["is_guest_accessible"],
                translations=dict(row["translations"] or {}),
                status=status,
                completion_pct=float(row["completion_pct"]),
                completed_at=(
                    row["completed_at"].isoformat() if row["completed_at"] else None
                ),
            )
        )

    return result


async def unlock_next_lesson(
    db: asyncpg.Connection,
    user_id: str,
    completed_lesson_id: str,
) -> str | None:
    """Create a lesson_progress row for the next lesson in the chain.

    Returns the next lesson's ID, or None if the completed lesson was the last.
    Idempotent — safe to call even if the progress row already exists.
    """
    completed = await db.fetchrow(
        "SELECT level_id, lesson_order FROM lesson WHERE id = $1",
        completed_lesson_id,
    )
    if completed is None:
        return None

    next_lesson = await db.fetchrow(
        """
        SELECT id FROM lesson
        WHERE level_id = $1
          AND lesson_order > $2
          AND status = 'approved'
          AND archived_at IS NULL
          AND deleted_at IS NULL
        ORDER BY lesson_order ASC
        LIMIT 1
        """,
        str(completed["level_id"]),
        completed["lesson_order"],
    )
    if next_lesson is None:
        return None

    next_id = str(next_lesson["id"])

    # Upsert — idempotent
    await db.execute(
        """
        INSERT INTO lesson_progress (id, user_id, lesson_id, status, completion_pct)
        VALUES ($1, $2, $3, 'not_started', 0)
        ON CONFLICT (user_id, lesson_id) DO NOTHING
        """,
        str(new_uuid()),
        user_id,
        next_id,
    )

    return next_id
