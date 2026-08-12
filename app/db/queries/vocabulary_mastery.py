import asyncpg


async def upsert_vocabulary_mastery(
    db: asyncpg.Connection,
    mastery_id: str,
    user_id: str,
    vocabulary_word_id: str,
    is_correct: bool,
) -> asyncpg.Record:
    increment = 1 if is_correct else 0
    return await db.fetchrow(
        """
        INSERT INTO vocabulary_mastery (
            id, user_id, vocabulary_word_id,
            attempt_count, correct_attempt_count, is_mastered, last_seen_at
        )
        VALUES ($1, $2, $3, 1, $4, false, now())
        ON CONFLICT (user_id, vocabulary_word_id) DO UPDATE SET
            attempt_count = vocabulary_mastery.attempt_count + 1,
            correct_attempt_count = vocabulary_mastery.correct_attempt_count + $4,
            last_seen_at = now(),
            updated_at = now()
        RETURNING id, attempt_count, correct_attempt_count, is_mastered
        """,
        mastery_id,
        user_id,
        vocabulary_word_id,
        increment,
    )


async def set_mastered(
    db: asyncpg.Connection,
    user_id: str,
    vocabulary_word_id: str,
) -> None:
    await db.execute(
        """
        UPDATE vocabulary_mastery
        SET is_mastered = true, updated_at = now()
        WHERE user_id = $1 AND vocabulary_word_id = $2
        """,
        user_id,
        vocabulary_word_id,
    )


async def get_vocabulary_word_difficulty(
    db: asyncpg.Connection,
    vocabulary_word_id: str,
) -> str | None:
    row = await db.fetchrow(
        "SELECT difficulty FROM vocabulary_word WHERE id = $1",
        vocabulary_word_id,
    )
    return row["difficulty"] if row else None
