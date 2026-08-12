import asyncpg


async def insert_notification(
    db: asyncpg.Connection,
    notif_id: str,
    user_id: str,
    notif_type: str,
    title: str,
    body: str,
    reference_id: str | None,
    reference_type: str | None,
) -> asyncpg.Record:
    return await db.fetchrow(
        """
        INSERT INTO notification (id, user_id, type, title, body, reference_id, reference_type)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING id, user_id, type, title, body, read_at, reference_id, reference_type, created_at
        """,
        notif_id,
        user_id,
        notif_type,
        title,
        body,
        reference_id,
        reference_type,
    )


async def mark_notification_read(
    db: asyncpg.Connection,
    user_id: str,
    notification_id: str,
) -> asyncpg.Record | None:
    return await db.fetchrow(
        """
        UPDATE notification
        SET read_at = COALESCE(read_at, now())
        WHERE id = $2 AND user_id = $1
        RETURNING id, read_at
        """,
        user_id,
        notification_id,
    )


async def mark_all_notifications_read(
    db: asyncpg.Connection,
    user_id: str,
) -> int:
    result = await db.execute(
        """
        UPDATE notification
        SET read_at = now()
        WHERE user_id = $1 AND read_at IS NULL
        """,
        user_id,
    )
    # asyncpg returns "UPDATE N"
    return int(result.split()[-1])


async def get_notifications_for_user(
    db: asyncpg.Connection,
    user_id: str,
    limit: int = 20,
    cursor: str | None = None,
    unread_only: bool = False,
) -> list[asyncpg.Record]:
    base = """
        SELECT id, type, title, body, read_at, reference_id, reference_type, created_at,
               translations
        FROM notification
        WHERE user_id = $1
    """
    if unread_only:
        base += " AND read_at IS NULL"
    if cursor:
        base += " AND id < $3"
        base += " ORDER BY created_at DESC, id DESC LIMIT $2"
        return await db.fetch(base, user_id, limit, cursor)
    base += " ORDER BY created_at DESC, id DESC LIMIT $2"
    return await db.fetch(base, user_id, limit)


async def count_unread_notifications(
    db: asyncpg.Connection,
    user_id: str,
) -> int:
    row = await db.fetchrow(
        "SELECT COUNT(*) AS cnt FROM notification WHERE user_id = $1 AND read_at IS NULL",
        user_id,
    )
    return int(row["cnt"]) if row else 0
