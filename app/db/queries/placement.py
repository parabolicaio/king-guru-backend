import asyncpg


async def get_placement_questions(db: asyncpg.Connection) -> list[asyncpg.Record]:
    return await db.fetch(
        """
        SELECT id, type, prompt_text, payload, difficulty,
               skill_category, xp_value, display_order, translations
        FROM placement_question
        ORDER BY display_order ASC
        """
    )


async def get_placement_scoring_rules(db: asyncpg.Connection) -> list[asyncpg.Record]:
    return await db.fetch(
        """
        SELECT min_percent, max_percent, recommended_level_id
        FROM placement_scoring_rule
        ORDER BY min_percent ASC
        """
    )


async def get_populated_level_ids(db: asyncpg.Connection) -> set[str]:
    """Level ids that have at least one non-deleted lesson.

    Used to cap placement recommendations at content that actually exists —
    recommending a level with zero lessons dead-ends the user (Task #17).
    Data-driven so the cap self-removes as content is added; no hardcoded
    level list to maintain.
    """
    rows = await db.fetch(
        """
        SELECT DISTINCT level_id
        FROM lesson
        WHERE deleted_at IS NULL
        """
    )
    return {str(r["level_id"]) for r in rows}


async def get_lesson_1_for_level(
    db: asyncpg.Connection, level_id: str
) -> asyncpg.Record | None:
    return await db.fetchrow(
        """
        SELECT id, lesson_order, status
        FROM lesson
        WHERE level_id = $1
          AND deleted_at IS NULL
        ORDER BY lesson_order ASC
        LIMIT 1
        """,
        level_id,
    )


async def get_lesson_progress(
    db: asyncpg.Connection, user_id: str, lesson_id: str
) -> asyncpg.Record | None:
    return await db.fetchrow(
        """
        SELECT id, status, completion_pct, completed_at
        FROM lesson_progress
        WHERE user_id = $1 AND lesson_id = $2
        """,
        user_id,
        lesson_id,
    )


async def create_lesson_progress(
    db: asyncpg.Connection,
    progress_id: str,
    user_id: str,
    lesson_id: str,
    status: str = "not_started",
) -> asyncpg.Record:
    return await db.fetchrow(
        """
        INSERT INTO lesson_progress (id, user_id, lesson_id, status, completion_pct)
        VALUES ($1, $2, $3, $4, 0)
        ON CONFLICT (user_id, lesson_id) DO UPDATE
            SET status = EXCLUDED.status,
                updated_at = now()
        RETURNING id, user_id, lesson_id, status, completion_pct, completed_at
        """,
        progress_id,
        user_id,
        lesson_id,
        status,
    )


async def set_user_level_and_placement(
    db: asyncpg.Connection,
    user_id: str,
    level_id: str,
) -> asyncpg.Record:
    return await db.fetchrow(
        """
        UPDATE "user"
        SET current_level_id = $2,
            placement_completed_at = now(),
            updated_at = now()
        WHERE id = $1
        RETURNING id, current_level_id, placement_completed_at
        """,
        user_id,
        level_id,
    )
