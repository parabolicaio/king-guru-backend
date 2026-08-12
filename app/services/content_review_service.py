"""Content review workflow service."""

import asyncpg

from app.core.errors import (
    AppError,
    CONTENT_ALREADY_PENDING,
    CONTENT_REVIEW_NOT_FOUND,
    REASON_REQUIRED,
)
from app.db.queries.content_review import (
    create_content_review,
    decide_review,
    get_pending_review_for_content,
    get_review_by_id,
)


async def submit(
    db: asyncpg.Connection,
    cm_id: str,
    content_type: str,
    content_id: str,
) -> asyncpg.Record:
    """Submit content for review. Raises CONTENT_ALREADY_PENDING if a pending review exists."""
    existing = await get_pending_review_for_content(db, content_type, content_id)
    if existing is not None:
        raise AppError(*CONTENT_ALREADY_PENDING)

    review = await create_content_review(
        db,
        content_type=content_type,
        content_id=content_id,
        submitted_by=cm_id,
    )

    # Set content status to pending_review
    if content_type == "lesson":
        await db.execute(
            "UPDATE lesson SET status = 'pending_review', updated_at = now() WHERE id = $1::uuid",
            content_id,
        )

    return review


async def decide(
    db: asyncpg.Connection,
    admin_id: str,
    review_id: str,
    decision: str,
    reason: str | None = None,
) -> asyncpg.Record:
    """Approve or reject a content review. Reason required for rejected/needs_revision."""
    if decision in ("rejected", "needs_revision") and not reason:
        raise AppError(*REASON_REQUIRED)

    review = await get_review_by_id(db, review_id)
    if review is None:
        raise AppError(*CONTENT_REVIEW_NOT_FOUND)

    updated = await decide_review(
        db,
        review_id,
        reviewer_id=admin_id,
        decision=decision,
        reason=reason,
    )

    # Update content status
    content_type = review["content_type"]
    content_id = str(review["content_id"])

    if content_type == "lesson":
        new_status = "approved" if decision == "approved" else "rejected"
        await db.execute(
            "UPDATE lesson SET status = $2, updated_at = now() WHERE id = $1::uuid",
            content_id, new_status,
        )

    # Notify submitting CM
    from app.services import notification as notification_service
    cm_id = str(review["submitted_by"])
    title = "Content approved" if decision == "approved" else "Content needs revision"
    body = f"Your submitted content has been {decision}."
    if reason:
        body += f" Reason: {reason}"

    await notification_service.create(
        db,
        user_id=cm_id,
        notif_type="content_review_decision",
        title=title,
        body=body,
        reference_id=review_id,
        reference_type=None,
    )

    # Audit log
    from app.services import audit_service
    await audit_service.log(
        db,
        action=f"content_review.{decision}",
        actor_id=admin_id,
        target_type="content_review",
        target_id=review_id,
    )

    return updated
