"""Pydantic schemas for content review workflow (B7)."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SubmitReviewRequest(BaseModel):
    content_type: str  # lesson | question_group | question
    content_id: UUID


class DecideReviewRequest(BaseModel):
    decision: str  # approved | rejected | needs_revision
    reason: str | None = None


class ContentReviewItem(BaseModel):
    id: UUID
    content_type: str
    content_id: UUID
    submitted_by: UUID
    submitted_at: datetime
    reviewer_id: UUID | None
    decision: str
    reason: str | None
    reviewed_at: datetime | None
    created_at: datetime
    updated_at: datetime


class ContentReviewListResponse(BaseModel):
    data: list[ContentReviewItem]
    total: int
    page: int
    page_size: int
