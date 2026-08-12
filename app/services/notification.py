"""Notification service."""

import asyncpg

from app.db.queries.notifications import (
    count_unread_notifications,
    insert_notification,
    mark_all_notifications_read,
    mark_notification_read,
)
from app.db.utils import new_uuid
from app.core.errors import AppError, NOTIFICATION_NOT_FOUND, NOTIFICATION_NOT_OWNED


async def create(
    db: asyncpg.Connection,
    user_id: str,
    notif_type: str,
    title: str,
    body: str,
    reference_id: str | None = None,
    reference_type: str | None = None,
) -> asyncpg.Record:
    return await insert_notification(
        db,
        notif_id=str(new_uuid()),
        user_id=user_id,
        notif_type=notif_type,
        title=title,
        body=body,
        reference_id=reference_id,
        reference_type=reference_type,
    )


async def mark_read(
    db: asyncpg.Connection,
    user_id: str,
    notification_id: str,
) -> asyncpg.Record:
    row = await mark_notification_read(db, user_id, notification_id)
    if row is None:
        raise AppError(*NOTIFICATION_NOT_OWNED)
    return row


async def mark_all_read(
    db: asyncpg.Connection,
    user_id: str,
) -> int:
    return await mark_all_notifications_read(db, user_id)
