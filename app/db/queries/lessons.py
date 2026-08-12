"""Raw SQL queries for the learner lesson-read path."""

import asyncpg


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


async def get_content_blocks_for_section(
    db: asyncpg.Connection,
    section_id: str,
) -> list[asyncpg.Record]:
    return await db.fetch(
        """
        SELECT id, block_type, display_order, payload, translations
        FROM content_block
        WHERE lesson_section_id = $1
        ORDER BY display_order ASC
        """,
        section_id,
    )


async def get_questions_for_section(
    db: asyncpg.Connection,
    section_id: str,
) -> list[asyncpg.Record]:
    return await db.fetch(
        """
        SELECT id, type, purpose, display_order,
               prompt_text, prompt_audio_url, prompt_image_url,
               payload, xp_value, hint_text,
               vocabulary_word_id, translations
        FROM question
        WHERE lesson_section_id = $1
        ORDER BY display_order ASC
        """,
        section_id,
    )


async def get_vocabulary_words_for_section(
    db: asyncpg.Connection,
    section_id: str,
) -> list[asyncpg.Record]:
    return await db.fetch(
        """
        SELECT id, word, definition, example_sentence,
               pronunciation_guide_si, difficulty,
               image_url, audio_url, translations
        FROM vocabulary_word
        WHERE lesson_section_id = $1
        ORDER BY id ASC
        """,
        section_id,
    )


async def get_latest_attempts_for_lesson(
    db: asyncpg.Connection,
    lesson_id: str,
    user_id: str,
) -> list[asyncpg.Record]:
    """Return the latest attempt per question for a given user + lesson."""
    return await db.fetch(
        """
        SELECT DISTINCT ON (a.question_id)
               a.id, a.question_id, a.score_fraction,
               a.score_numerator, a.score_denominator,
               a.xp_awarded, a.response, a.created_at
        FROM attempt a
        JOIN question q ON q.id = a.question_id
        WHERE q.lesson_section_id IN (
            SELECT id FROM lesson_section WHERE lesson_id = $1
        )
          AND a.user_id = $2
        ORDER BY a.question_id, a.created_at DESC
        """,
        lesson_id,
        user_id,
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
