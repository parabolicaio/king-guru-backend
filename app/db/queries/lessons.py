"""Raw SQL queries for the learner lesson-read path."""

from datetime import datetime, timezone

import asyncpg

from app.db.utils import new_uuid


async def upsert_section_progress(
    db: asyncpg.Connection,
    *,
    lesson_section_id: str,
    step_index: int,
    total_steps: int,
    user_id: str | None = None,
    guest_token: str | None = None,
) -> asyncpg.Record:
    """Record the furthest step reached in a section — never regresses even
    if a later report arrives with a smaller step_index (e.g. navigating
    back through already-seen steps shouldn't undo completed progress).
    Returns the row as actually stored (the GREATEST-clamped value), not
    necessarily what was just submitted.

    Exactly one of user_id/guest_token should be given, mirroring how
    `attempt` rows are keyed (see get_latest_attempts_for_lesson below).
    """
    now = datetime.now(timezone.utc)
    if user_id is not None:
        return await db.fetchrow(
            """
            INSERT INTO lesson_section_progress
                (id, user_id, lesson_section_id, furthest_step_index, total_steps, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5, $6, $6)
            ON CONFLICT (user_id, lesson_section_id) WHERE user_id IS NOT NULL
            DO UPDATE SET
                furthest_step_index = GREATEST(lesson_section_progress.furthest_step_index, EXCLUDED.furthest_step_index),
                total_steps = EXCLUDED.total_steps,
                updated_at = EXCLUDED.updated_at
            RETURNING furthest_step_index, total_steps
            """,
            new_uuid(), user_id, lesson_section_id, step_index, total_steps, now,
        )
    else:
        return await db.fetchrow(
            """
            INSERT INTO lesson_section_progress
                (id, guest_token, lesson_section_id, furthest_step_index, total_steps, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5, $6, $6)
            ON CONFLICT (guest_token, lesson_section_id) WHERE guest_token IS NOT NULL
            DO UPDATE SET
                furthest_step_index = GREATEST(lesson_section_progress.furthest_step_index, EXCLUDED.furthest_step_index),
                total_steps = EXCLUDED.total_steps,
                updated_at = EXCLUDED.updated_at
            RETURNING furthest_step_index, total_steps
            """,
            new_uuid(), guest_token, lesson_section_id, step_index, total_steps, now,
        )


async def get_section_progress_for_lesson(
    db: asyncpg.Connection,
    lesson_id: str,
    *,
    user_id: str | None = None,
    guest_token: str | None = None,
) -> list[asyncpg.Record]:
    """Return each section's furthest_step_index/total_steps for one identity."""
    if user_id is None and guest_token is None:
        return []
    identity_col = "user_id" if user_id is not None else "guest_token"
    return await db.fetch(
        f"""
        SELECT lesson_section_id, furthest_step_index, total_steps
        FROM lesson_section_progress
        WHERE lesson_section_id IN (
            SELECT id FROM lesson_section WHERE lesson_id = $1
        )
          AND {identity_col} = $2
        """,
        lesson_id,
        user_id if user_id is not None else guest_token,
    )


async def get_section_category_image_map(
    db: asyncpg.Connection,
) -> dict[str, str]:
    """Return a mapping of category → storage_path from section_category_image."""
    rows = await db.fetch("SELECT category, image_url FROM section_category_image")
    return {row["category"]: row["image_url"] for row in rows}


async def get_lessons_for_level(
    db: asyncpg.Connection,
    level_id: str,
    user_id: str | None,
) -> list[asyncpg.Record]:
    """Return approved, non-archived, non-deleted lessons with progress state."""
    return await db.fetch(
        """
        SELECT l.id, l.title, l.description, l.lesson_order,
               l.thumbnail_url, l.is_guest_accessible, l.translations,
               COALESCE(lp.status, 'locked') AS progress_status,
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


async def get_level_with_lessons(
    db: asyncpg.Connection,
    level_id: str,
) -> asyncpg.Record | None:
    return await db.fetchrow(
        "SELECT id, name, code FROM level WHERE id = $1",
        level_id,
    )


async def get_lesson_for_learner(
    db: asyncpg.Connection,
    lesson_id: str,
) -> asyncpg.Record | None:
    return await db.fetchrow(
        """
        SELECT id, level_id, title, description, lesson_order, status,
               thumbnail_url, is_guest_accessible, translations,
               objectives, objectives_translations
        FROM lesson
        WHERE id = $1 AND deleted_at IS NULL
        """,
        lesson_id,
    )


async def get_sections_for_lesson(
    db: asyncpg.Connection,
    lesson_id: str,
) -> list[asyncpg.Record]:
    return await db.fetch(
        """
        SELECT id, category, display_order, title, translations
        FROM lesson_section
        WHERE lesson_id = $1
        ORDER BY display_order ASC
        """,
        lesson_id,
    )


def _group_by_section(rows: list[asyncpg.Record]) -> dict[str, list[asyncpg.Record]]:
    grouped: dict[str, list[asyncpg.Record]] = {}
    for row in rows:
        grouped.setdefault(str(row["lesson_section_id"]), []).append(row)
    return grouped


async def get_content_blocks_for_lesson(
    db: asyncpg.Connection,
    lesson_id: str,
) -> dict[str, list[asyncpg.Record]]:
    """Content blocks for every section of a lesson in one query, keyed by
    section id (D-19: one query per section made lessons take ~15 s)."""
    rows = await db.fetch(
        """
        SELECT cb.lesson_section_id, cb.id, cb.block_type, cb.display_order,
               cb.payload, cb.translations
        FROM content_block cb
        JOIN lesson_section ls ON ls.id = cb.lesson_section_id
        WHERE ls.lesson_id = $1
        ORDER BY cb.lesson_section_id, cb.display_order ASC
        """,
        lesson_id,
    )
    return _group_by_section(rows)


async def get_questions_for_lesson(
    db: asyncpg.Connection,
    lesson_id: str,
) -> dict[str, list[asyncpg.Record]]:
    """Questions for every section of a lesson in one query, keyed by section id."""
    rows = await db.fetch(
        """
        SELECT q.lesson_section_id, q.id, q.type, q.purpose, q.display_order,
               q.prompt_text, q.prompt_audio_url, q.prompt_image_url,
               q.payload, q.xp_value, q.hint_text,
               q.vocabulary_word_id, q.translations
        FROM question q
        JOIN lesson_section ls ON ls.id = q.lesson_section_id
        WHERE ls.lesson_id = $1
        ORDER BY q.lesson_section_id, q.display_order ASC
        """,
        lesson_id,
    )
    return _group_by_section(rows)


async def get_vocabulary_words_for_lesson(
    db: asyncpg.Connection,
    lesson_id: str,
) -> dict[str, list[asyncpg.Record]]:
    """Vocabulary words for every section of a lesson in one query, keyed by section id."""
    rows = await db.fetch(
        """
        SELECT vw.lesson_section_id, vw.id, vw.word, vw.definition,
               vw.example_sentence, vw.pronunciation_guide_si, vw.difficulty,
               vw.image_url, vw.audio_url, vw.translations
        FROM vocabulary_word vw
        JOIN lesson_section ls ON ls.id = vw.lesson_section_id
        WHERE ls.lesson_id = $1
        ORDER BY vw.lesson_section_id, vw.id ASC
        """,
        lesson_id,
    )
    return _group_by_section(rows)





async def get_latest_attempts_for_lesson(
    db: asyncpg.Connection,
    lesson_id: str,
    *,
    user_id: str | None = None,
    guest_token: str | None = None,
) -> list[asyncpg.Record]:
    """Return the latest attempt per question for a given user + lesson.

    Exactly one of user_id/guest_token should be given — mirrors how
    submit_attempt (api/v1/attempts.py) stores a row under exactly one of
    those two columns depending on whether the attempt came from a
    registered user or a guest (a guest never holds a user_id there).
    """
    if user_id is None and guest_token is None:
        return []
    identity_col = "a.user_id" if user_id is not None else "a.guest_token"
    return await db.fetch(
        f"""
        SELECT DISTINCT ON (a.question_id)
               a.id, a.question_id, a.score_fraction,
               a.score_numerator, a.score_denominator,
               a.xp_awarded, a.response, a.created_at
        FROM attempt a
        JOIN question q ON q.id = a.question_id
        WHERE q.lesson_section_id IN (
            SELECT id FROM lesson_section WHERE lesson_id = $1
        )
          AND {identity_col} = $2
        ORDER BY a.question_id, a.created_at DESC
        """,
        lesson_id,
        user_id if user_id is not None else guest_token,
    )


async def get_vocabulary_mastery_for_lesson(
    db: asyncpg.Connection,
    lesson_id: str,
    user_id: str,
) -> list[asyncpg.Record]:
    return await db.fetch(
        """
        SELECT vm.vocabulary_word_id,
               vm.attempt_count,
               vm.correct_attempt_count,
               vm.is_mastered
        FROM vocabulary_mastery vm
        JOIN vocabulary_word vw ON vw.id = vm.vocabulary_word_id
        WHERE vw.lesson_section_id IN (
            SELECT id FROM lesson_section WHERE lesson_id = $1
        )
          AND vm.user_id = $2
        """,
        lesson_id,
        user_id,
    )


async def get_lesson_progress_for_user(
    db: asyncpg.Connection,
    user_id: str,
    lesson_id: str,
) -> asyncpg.Record | None:
    return await db.fetchrow(
        """
        SELECT status, completion_pct, completed_at
        FROM lesson_progress
        WHERE user_id = $1 AND lesson_id = $2
        """,
        user_id,
        lesson_id,
    )
