"""Raw SQL query functions for Daily Essay."""

from datetime import date

import asyncpg

from app.db.utils import new_uuid


async def get_today_prompt(
    db: asyncpg.Connection,
    level_id: str | None,
    today: date,
) -> asyncpg.Record | None:
    """Level-scoped prompt first, then level-null, then any active prompt."""
    if level_id:
        row = await db.fetchrow(
            """
            SELECT * FROM essay_prompt
            WHERE is_active = TRUE
              AND (date_assigned = $2 OR date_assigned IS NULL)
              AND level_id = $1::uuid
            ORDER BY date_assigned DESC NULLS LAST
            LIMIT 1
            """,
            level_id, today,
        )
        if row:
            return row

    row = await db.fetchrow(
        """
        SELECT * FROM essay_prompt
        WHERE is_active = TRUE
          AND (date_assigned = $1 OR date_assigned IS NULL)
          AND level_id IS NULL
        ORDER BY date_assigned DESC NULLS LAST
        LIMIT 1
        """,
        today,
    )
    if row:
        return row

    # Fallback: any active prompt
    return await db.fetchrow(
        "SELECT * FROM essay_prompt WHERE is_active = TRUE ORDER BY created_at ASC LIMIT 1"
    )


async def get_submission_for_today(
    db: asyncpg.Connection,
    user_id: str,
    today: date,
) -> asyncpg.Record | None:
    """Returns the draft or submitted row for today, or None."""
    return await db.fetchrow(
        "SELECT * FROM daily_essay_submission WHERE user_id = $1::uuid AND submission_date = $2",
        user_id, today,
    )


async def get_submission_by_id(
    db: asyncpg.Connection,
    user_id: str,
    submission_id: str,
) -> asyncpg.Record | None:
    """Return a specific submitted (non-draft) essay by ID, scoped to the user."""
    return await db.fetchrow(
        "SELECT * FROM daily_essay_submission "
        "WHERE id = $1::uuid AND user_id = $2::uuid AND is_draft = FALSE",
        submission_id, user_id,
    )


async def create_draft(
    db: asyncpg.Connection,
    *,
    user_id: str,
    essay_prompt_id: str,
    prompt_text: str,
    draft_text: str,
    submission_date: date,
    feedback_language: str = "en",
) -> asyncpg.Record:
    """Insert a new draft row (is_draft=TRUE, submitted_at=NULL)."""
    sub_id = new_uuid()
    return await db.fetchrow(
        """
        INSERT INTO daily_essay_submission (
            id, user_id, essay_prompt_id, prompt_text, essay_text,
            submission_date, is_draft, feedback_language, created_at, updated_at
        )
        VALUES ($1, $2::uuid, $3::uuid, $4, $5, $6, TRUE, $7, now(), now())
        RETURNING *
        """,
        sub_id, user_id, essay_prompt_id, prompt_text, draft_text,
        submission_date, feedback_language,
    )


async def update_draft_text(
    db: asyncpg.Connection,
    submission_id: str,
    draft_text: str,
    feedback_language: str = "en",
) -> asyncpg.Record:
    """Overwrite essay_text and feedback_language on an existing draft row."""
    return await db.fetchrow(
        """
        UPDATE daily_essay_submission
        SET essay_text        = $2,
            feedback_language = $3,
            updated_at        = now()
        WHERE id = $1 AND is_draft = TRUE
        RETURNING *
        """,
        submission_id, draft_text, feedback_language,
    )


async def promote_draft_to_submission(
    db: asyncpg.Connection,
    submission_id: str,
    final_text: str,
    feedback_language: str = "en",
) -> asyncpg.Record:
    """Flip is_draft → FALSE and stamp submitted_at on an existing draft."""
    return await db.fetchrow(
        """
        UPDATE daily_essay_submission
        SET essay_text        = $2,
            feedback_language = $3,
            is_draft          = FALSE,
            submitted_at      = now(),
            updated_at        = now()
        WHERE id = $1 AND is_draft = TRUE
        RETURNING *
        """,
        submission_id, final_text, feedback_language,
    )


async def create_submission(
    db: asyncpg.Connection,
    *,
    user_id: str,
    essay_prompt_id: str,
    prompt_text: str,
    essay_text: str,
    submission_date: date,
    feedback_language: str = "en",
) -> asyncpg.Record:
    """Insert a directly-submitted row (no prior draft)."""
    sub_id = new_uuid()
    return await db.fetchrow(
        """
        INSERT INTO daily_essay_submission (
            id, user_id, essay_prompt_id, prompt_text, essay_text,
            submission_date, is_draft, submitted_at, feedback_language,
            created_at, updated_at
        )
        VALUES ($1, $2::uuid, $3::uuid, $4, $5, $6, FALSE, now(), $7, now(), now())
        RETURNING *
        """,
        sub_id, user_id, essay_prompt_id, prompt_text, essay_text,
        submission_date, feedback_language,
    )


async def update_submission_grade(
    db: asyncpg.Connection,
    submission_id: str,
    *,
    grade: str,
    score_grammar: float,
    score_vocabulary: float,
    score_content: float,
    score_suggestions: float,
    ai_feedback: dict,
    ai_model: str,
    xp_awarded: int,
) -> asyncpg.Record:
    return await db.fetchrow(
        """
        UPDATE daily_essay_submission
        SET grade            = $2,
            score_grammar    = $3,
            score_vocabulary = $4,
            score_content    = $5,
            score_suggestions = $6,
            ai_feedback      = $7,
            ai_model         = $8,
            xp_awarded       = $9,
            updated_at       = now()
        WHERE id = $1
        RETURNING *
        """,
        submission_id, grade, score_grammar, score_vocabulary,
        score_content, score_suggestions, ai_feedback, ai_model, xp_awarded,
    )


async def get_essay_history(
    db: asyncpg.Connection,
    user_id: str,
    *,
    limit: int = 10,
    cursor: str | None = None,
) -> list[asyncpg.Record]:
    """Cursor-paginated submitted essays (drafts excluded), with word_count computed."""
    word_count_expr = (
        "array_length(regexp_split_to_array(trim(s.essay_text), '\\s+'), 1)"
    )
    if cursor:
        return await db.fetch(
            f"""
            SELECT s.*,
                   ep.prompt_text AS prompt_text_display,
                   COALESCE({word_count_expr}, 0) AS word_count
            FROM daily_essay_submission s
            JOIN essay_prompt ep ON ep.id = s.essay_prompt_id
            WHERE s.user_id = $1::uuid
              AND s.is_draft = FALSE
              AND s.id < $2::uuid
            ORDER BY s.submission_date DESC
            LIMIT $3
            """,
            user_id, cursor, limit,
        )
    return await db.fetch(
        f"""
        SELECT s.*,
               ep.prompt_text AS prompt_text_display,
               COALESCE({word_count_expr}, 0) AS word_count
        FROM daily_essay_submission s
        JOIN essay_prompt ep ON ep.id = s.essay_prompt_id
        WHERE s.user_id = $1::uuid
          AND s.is_draft = FALSE
        ORDER BY s.submission_date DESC
        LIMIT $2
        """,
        user_id, limit,
    )
