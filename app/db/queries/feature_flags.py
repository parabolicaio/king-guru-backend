import asyncpg


async def get_all_feature_flags(db: asyncpg.Connection) -> list[asyncpg.Record]:
    return await db.fetch(
        "SELECT flag_key, default_value FROM feature_flag ORDER BY flag_key"
    )
