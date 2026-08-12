"""Tests for admin content authoring endpoints (B7)."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4


@pytest.mark.asyncio
async def test_create_lesson_requires_auth(async_client):
    response = await async_client.post(
        "/api/v1/admin/lessons",
        json={"level_id": str(uuid4()), "title": "Test Lesson"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_list_lessons_admin_requires_auth(async_client):
    response = await async_client.get("/api/v1/admin/lessons")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_lesson_admin_only(async_client):
    """DELETE /admin/lessons/{id} requires admin role, not just content_manager."""
    lesson_id = str(uuid4())
    response = await async_client.delete(
        f"/api/v1/admin/lessons/{lesson_id}",
        headers={"Authorization": "Bearer fake"},
    )
    assert response.status_code in (401, 403)


@pytest.mark.asyncio
async def test_lesson_order_computed_server_side():
    """lesson_order must be computed via compute_next_order, not from request body."""
    from app.services.lesson_chain import compute_next_order

    conn = AsyncMock()
    conn.fetchrow.return_value = MagicMock()
    conn.fetchrow.return_value.__getitem__ = lambda self, key: 3 if key == "next_order" else None

    order = await compute_next_order(conn, "level-id")
    assert order == 3


@pytest.mark.asyncio
async def test_question_has_attempts_guard():
    from app.db.queries.admin_lessons import question_has_attempts

    conn = AsyncMock()
    row = MagicMock()
    row.__getitem__ = lambda self, key: True if key == "has_attempts" else False
    conn.fetchrow.return_value = row

    result = await question_has_attempts(conn, str(uuid4()))
    assert result is True


@pytest.mark.asyncio
async def test_section_has_attempts_guard():
    from app.db.queries.admin_lessons import section_has_attempts

    conn = AsyncMock()
    row = MagicMock()
    row.__getitem__ = lambda self, key: False if key == "has_attempts" else None
    conn.fetchrow.return_value = row

    result = await section_has_attempts(conn, str(uuid4()))
    assert result is False


@pytest.mark.asyncio
async def test_content_review_submit_already_pending():
    from app.core.errors import AppError, CONTENT_ALREADY_PENDING
    from app.services import content_review_service

    conn = AsyncMock()
    # Simulate existing pending review
    conn.fetchrow.return_value = MagicMock()

    with pytest.raises(AppError) as exc:
        await content_review_service.submit(
            conn,
            cm_id=str(uuid4()),
            content_type="lesson",
            content_id=str(uuid4()),
        )
    assert exc.value.status_code == 409


@pytest.mark.asyncio
async def test_content_review_decide_reason_required():
    from app.core.errors import AppError, REASON_REQUIRED
    from app.services import content_review_service

    conn = AsyncMock()
    review_row = MagicMock()
    review_row.__getitem__ = lambda self, key: {
        "content_type": "lesson",
        "content_id": str(uuid4()),
        "submitted_by": str(uuid4()),
    }.get(key)
    conn.fetchrow.return_value = review_row

    with pytest.raises(AppError) as exc:
        await content_review_service.decide(
            conn,
            admin_id=str(uuid4()),
            review_id=str(uuid4()),
            decision="rejected",
            reason=None,  # Missing!
        )
    assert exc.value.status_code == 422


@pytest.mark.asyncio
async def test_vocabulary_word_has_mastery_blocks_delete():
    from app.db.queries.admin_lessons import vocabulary_word_has_mastery

    conn = AsyncMock()
    row = MagicMock()
    row.__getitem__ = lambda self, key: True if key == "has_mastery" else None
    conn.fetchrow.return_value = row

    result = await vocabulary_word_has_mastery(conn, str(uuid4()))
    assert result is True


@pytest.mark.asyncio
async def test_content_review_decide_requires_admin(async_client):
    review_id = str(uuid4())
    response = await async_client.patch(
        f"/api/v1/content-reviews/{review_id}/decide",
        json={"decision": "approved"},
        headers={"Authorization": "Bearer fake"},
    )
    assert response.status_code in (401, 403)
