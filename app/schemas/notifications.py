from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class NotificationItem(BaseModel):
    id: UUID
    type: str
    title: str
    body: str
    is_read: bool
    read_at: datetime | None
    reference_id: UUID | None
    reference_type: str | None
    created_at: datetime
    translations: dict = {}


class NotificationsListResponse(BaseModel):
    unread_count: int
    data: list[NotificationItem]
    cursor: str | None
    has_more: bool


class MarkReadResponse(BaseModel):
    id: UUID
    is_read: bool
    read_at: datetime


class MarkAllReadResponse(BaseModel):
    updated_count: int
