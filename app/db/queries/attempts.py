import asyncpg


async def get_question_with_lesson(
    db: asyncpg.Connection,
    question_id: str,
) -> asyncpg.Record | None:
    """Return question + section + lesson context for access checks."""
    return await db.fetchrow(
        """
        SELECT q.id, q.type, q.purpose, q.xp_value,
               q.payload, q.vocabulary_word_id,
               q.lesson_section_id,
               ls.lesson_id,
               l.status      AS lesson_status,
               l.is_guest_accessible,
               l.lesson_order
        FROM question q
        JOIN lesson_section ls ON ls.id = q.lesson_section_id
        JOIN lesson          l  ON l.id  = ls.lesson_id
        WHERE q.id = $1
        """,
        question_id,
    )


async def insert_attempt(
    db: asyncpg.Connection,
    attempt_id: str,
    user_id: str | None,
    guest_token: str | None,
    question_id: str,
    lesson_section_id: str,
    lesson_id: str,
    response: dict,
    score_fraction: str,
    score_numerator: int,
    score_denominator: int,
    xp_awarded: int,
    ai_feedback: dict | None = None,
) -> asyncpg.Record:
    return await db.fetchrow(
        """
        INSERT INTO attempt (
            id, user_id, guest_token, question_id, lesson_section_id, lesson_id,
            response, score_fraction, score_numerator, score_denominator, xp_awarded,
            ai_feedback
        )
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
        RETURNING id, score_fraction, score_numerator, score_denominator, xp_awarded, created_at
        """,
        attempt_id,
        user_id,
        guest_token,
        question_id,
        lesson_section_id,
        lesson_id,
        response,
        score_fraction,
        score_numerator,
        score_denominator,
        xp_awarded,
        ai_feedback,
    )


async def get_assessment_question_ids_for_lesson(
    db: asyncpg.Connection,
    lesson_id: str,
) -> list[str]:
    rows = await db.fetch(
        """
        SELECT q.id
        FROM question q
        JOIN lesson_section ls ON ls.id = q.lesson_section_id
        WHERE ls.lesson_id = $1 AND q.purpose = 'assessment'
        """,
        lesson_id,
    )
    return [str(r["id"]) for r in rows]


async def get_answered_assessment_question_ids(
    db: asyncpg.Connection,
    user_id: str,
    lesson_id: str,
) -> list[str]:
    rows = await db.fetch(
        """
        SELECT DISTINCT a.question_id
        FROM attempt a
        JOIN question q      ON q.id  = a.question_id
        JOIN lesson_section ls ON ls.id = q.lesson_section_id
        WHERE ls.lesson_id = $1
          AND a.user_id    = $2::uuid
          AND q.purpose    = 'assessment'
        """,
        lesson_id,
        user_id,
    )
    return [str(r["question_id"]) for r in rows]
