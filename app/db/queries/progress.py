import asyncpg

SKILL_CATEGORIES = [
    "vocabulary",
    "grammar",
    "pronunciation",
    "reading",
    "listening",
    "writing",
    "speaking",
]


async def get_skill_progress(
    db: asyncpg.Connection,
    user_id: str,
    level_id: str,
) -> list[asyncpg.Record]:
    """Return per-category skill progress for a user within their current level.

    Uses latest attempt per question (not best) for accuracy calculation.
    All 7 categories are always returned; is_available=false when the level
    has no sections of that type.
    """
    return await db.fetch(
        """
        WITH
        level_sections AS (
            SELECT ls.category,
                   COUNT(DISTINCT q.id) AS total_questions
            FROM   lesson_section ls
            JOIN   lesson l  ON l.id  = ls.lesson_id
            JOIN   question q ON q.lesson_section_id = ls.id
                             AND q.purpose = 'assessment'
            WHERE  l.level_id   = $2
              AND  l.status     = 'approved'
              AND  l.deleted_at IS NULL
              AND  l.archived_at IS NULL
            GROUP  BY ls.category
        ),
        latest_attempts AS (
            SELECT DISTINCT ON (a.question_id)
                   ls.category,
                   a.score_fraction
            FROM   attempt a
            JOIN   question q  ON q.id  = a.question_id
                              AND q.purpose = 'assessment'
            JOIN   lesson_section ls ON ls.id = q.lesson_section_id
            JOIN   lesson l           ON l.id  = ls.lesson_id
            WHERE  a.user_id    = $1
              AND  l.level_id   = $2
              AND  l.status     = 'approved'
              AND  l.deleted_at IS NULL
              AND  l.archived_at IS NULL
            ORDER  BY a.question_id, a.created_at DESC
        ),
        user_stats AS (
            SELECT category,
                   COUNT(*)           AS questions_answered,
                   AVG(score_fraction) AS accuracy
            FROM   latest_attempts
            GROUP  BY category
        )
        SELECT cat.category,
               COALESCE(ls.total_questions, 0)                       AS total_questions,
               (ls.total_questions IS NOT NULL
                AND ls.total_questions > 0)                          AS is_available,
               COALESCE(us.questions_answered, 0)::int               AS questions_answered,
               us.accuracy
        FROM   (VALUES
            (1,'vocabulary'),(2,'grammar'),(3,'pronunciation'),
            (4,'reading'),(5,'listening'),(6,'writing'),(7,'speaking')
        ) AS cat(sort_order, category)
        LEFT JOIN level_sections ls ON ls.category = cat.category
        LEFT JOIN user_stats     us ON us.category = cat.category
        ORDER  BY cat.sort_order
        """,
        user_id,
        level_id,
    )


async def get_user_progress_summary(
    db: asyncpg.Connection,
    user_id: str,
) -> asyncpg.Record | None:
    return await db.fetchrow(
        """
        SELECT u.xp_total,
               u.streak_current,
               u.streak_longest,
               u.streak_last_activity_date,
               u.current_level_id,
               COUNT(lp.id) FILTER (WHERE lp.status = 'completed') AS completed_lesson_count
        FROM "user" u
        LEFT JOIN lesson_progress lp ON lp.user_id = u.id
        WHERE u.id = $1
        GROUP BY u.id
        """,
        user_id,
    )
