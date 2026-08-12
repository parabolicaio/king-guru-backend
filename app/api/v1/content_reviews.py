"""Content review endpoints (B7)."""

from uuid import UUID

import asyncpg
from fastapi import APIRouter, Depends

from app.core.errors import AppError, CONTENT_REVIEW_NOT_FOUND, FORBIDDEN
from app.core.security import get_admin_user, get_content_manager_user
from app.db.pool import get_db
from app.db.queries.content_review import get_review_by_id, list_content_reviews
from app.schemas.content_review import (
    ContentReviewItem,
    ContentReviewListResponse,
    DecideReviewRequest,
    SubmitReviewRequest,
)
from app.services import content_review_service

router = APIRouter(prefix="/api/v1/content-reviews", tags=["content-reviews"])


def _row_to_item(row: asyncpg.Record) -> ContentReviewItem:
    return ContentReviewItem(
        id=row["id"],
        content_type=row["content_type"],
        content_id=row["content_id"],
        submitted_by=row["submitted_by"],
        submitted_at=row["submitted_at"],
        reviewer_id=row["reviewer_id"],
        decision=row["decision"],
        reason=row["reason"],
        reviewed_at=row["reviewed_at"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


@router.post("", response_model=ContentReviewItem, status_code=201)
async def submit_for_review(
    body: SubmitReviewRequest,
    user: asyncpg.Record = Depends(get_content_manager_user),
    db: asyncpg.Connection = Depends(get_db),
) -> ContentReviewItem:
    row = await content_review_service.submit(
        db,
        cm_id=str(user["id"]),
        content_type=body.content_type,
        content_id=str(body.content_id),
    )
    return _row_to_item(row)


@router.get("", response_model=ContentReviewListResponse)
async def list_reviews(
    content_type: str | None = None,
    decision: str | None = None,
    page: int = 1,
    page_size: int = 20,
    user: asyncpg.Record = Depends(get_content_manager_user),
    db: asyncpg.Connection = Depends(get_db),
) -> ContentReviewListResponse:
    is_admin = user["admin_role"] == "admin"
    submitted_by = None if is_admin else str(user["id"])

    rows, total = await list_content_reviews(
        db,
        content_type=content_type,
        decision=decision,
        submitted_by=submitted_by,
        page=page,
        page_size=page_size,
    )
    return ContentReviewListResponse(
        data=[_row_to_item(r) for r in rows],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{review_id}", response_model=ContentReviewItem)
async def get_review(
    review_id: UUID,
    user: asyncpg.Record = Depends(get_content_manager_user),
    db: asyncpg.Connection = Depends(get_db),
) -> ContentReviewItem:
    row = await get_review_by_id(db, str(review_id))
    if row is None:
        raise AppError(*CONTENT_REVIEW_NOT_FOUND)
    # CM can only see their own reviews; Admin sees all
    if user["admin_role"] != "admin" and str(row["submitted_by"]) != str(user["id"]):
        raise AppError(*FORBIDDEN)
    return _row_to_item(row)


@router.patch("/{review_id}/decide", response_model=ContentReviewItem)
async def decide_review(
    review_id: UUID,
    body: DecideReviewRequest,
    user: asyncpg.Record = Depends(get_admin_user),
    db: asyncpg.Connection = Depends(get_db),
) -> ContentReviewItem:
    row = await content_review_service.decide(
        db,
        admin_id=str(user["id"]),
        review_id=str(review_id),
        decision=body.decision,
        reason=body.reason,
    )
    return _row_to_item(row)
