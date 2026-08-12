import asyncpg


async def get_xp_rules(db: asyncpg.Connection) -> list[asyncpg.Record]:
    return await db.fetch(
        """
        SELECT action_type, context_key, xp_value
        FROM xp_rule
        WHERE is_active = TRUE
          AND (effective_from IS NULL OR effective_from <= now())
          AND (effective_to   IS NULL OR effective_to   >= now())
        """
    )


async def insert_xp_ledger(
    db: asyncpg.Connection,
    ledger_id: str,
    user_id: str,
    action_type: str,
    xp_delta: int,
    reference_id: str | None,
    reference_type: str | None,
) -> None:
    await db.execute(
        """
        INSERT INTO xp_ledger (id, user_id, action_type, xp_delta, reference_id, reference_type, awarded_at)
        VALUES ($1, $2, $3, $4, $5, $6, now())
        """,
        ledger_id,
        user_id,
        action_type,
        xp_delta,
        reference_id,
        reference_type,
    )


async def increment_user_xp(
    db: asyncpg.Connection,
    user_id: str,
    delta: int,
) -> None:
    await db.execute(
        """
        UPDATE "user"
        SET xp_total = xp_total + $2, updated_at = now()
        WHERE id = $1
        """,
        user_id,
        delta,
    )


async def get_xp_ledger_for_user(
    db: asyncpg.Connection,
    user_id: str,
    limit: int = 20,
    cursor: str | None = None,
) -> list[asyncpg.Record]:
    if cursor:
        return await db.fetch(
            """
            SELECT id, action_type, xp_delta, reference_type, reference_id, awarded_at
            FROM xp_ledger
            WHERE user_id = $1 AND id < $3
            ORDER BY awarded_at DESC, id DESC
            LIMIT $2
            """,
            user_id,
            limit,
            cursor,
        )
    return await db.fetch(
        """
        SELECT id, action_type, xp_delta, reference_type, reference_id, awarded_at
        FROM xp_ledger
        WHERE user_id = $1
        ORDER BY awarded_at DESC, id DESC
        LIMIT $2
        """,
        user_id,
        limit,
    )
