import asyncpg


async def get_all_active_levels(db: asyncpg.Connection) -> list[asyncpg.Record]:
    return await db.fetch(
        """
        SELECT id, code, name, description, display_order,
               daily_essay_enabled, translations, icon_url, topics,
               guest_enabled, payment_required, price_amount, price_currency
        FROM level
        WHERE is_active = TRUE
        ORDER BY display_order ASC
        """
    )


async def get_level_by_id(db: asyncpg.Connection, level_id: str) -> asyncpg.Record | None:
    return await db.fetchrow(
        """
        SELECT id, code, name, description, display_order,
               daily_essay_enabled, is_active, translations, icon_url, topics,
               guest_enabled, payment_required, price_amount, price_currency
        FROM level
        WHERE id = $1
        """,
        level_id,
    )
