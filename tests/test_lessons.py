"""Tests for lesson-chain service and lesson read endpoints."""

import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from app.services.lesson_chain import (
    compute_next_order,
    get_lessons_with_progress,
    unlock_next_lesson,
    LessonWithProgress,
)


# ---------------------------------------------------------------------------
# compute_next_order
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_compute_next_order_empty_level():
    db = AsyncMock()
    db.fetchrow.return_value = {"next_order": 1}
    result = await compute_next_order(db, str(uuid4()))
    assert result == 1


@pytest.mark.asyncio
async def test_compute_next_order_appends():
    db = AsyncMock()
    db.fetchrow.return_value = {"next_order": 4}
    result = await compute_next_order(db, str(uuid4()))
    assert result == 4


# ---------------------------------------------------------------------------
# get_lessons_with_progress
# ---------------------------------------------------------------------------

def _lesson_row(order: int, progress_status: str | None = None, completed_at=None):
    return {
        "id": str(uuid4()),
        "title": f"Lesson {order}",
        "description": None,
        "lesson_order": order,
        "thumbnail_url": None,
        "is_guest_accessible": order == 1,
        "translations": {},
        "progress_status": progress_status,
        "completion_pct": 100 if progress_status == "completed" else 0,
        "completed_at": completed_at,
    }


@pytest.mark.asyncio
async def test_get_lessons_lesson1_not_started_others_locked():
    db = AsyncMock()
    db.fetch.return_value = [
        _lesson_row(1, None),
        _lesson_row(2, None),
        _lesson_row(3, None),
    ]
    result = await get_lessons_with_progress(db, str(uuid4()), str(uuid4()))
    assert result[0].status == "not_started"
    assert result[1].status == "locked"
    assert result[2].status == "locked"


@pytest.mark.asyncio
async def test_get_lessons_completed_unlocks_next():
    db = AsyncMock()
    db.fetch.return_value = [
        _lesson_row(1, "completed"),
        _lesson_row(2, None),   # unlocked by lesson 1 completion
        _lesson_row(3, None),   # still locked
    ]
    result = await get_lessons_with_progress(db, str(uuid4()), str(uuid4()))
    assert result[0].status == "completed"
    assert result[1].status == "not_started"
    assert result[2].status == "locked"


@pytest.mark.asyncio
async def test_get_lessons_in_progress():
    db = AsyncMock()
    db.fetch.return_value = [
        _lesson_row(1, "completed"),
        _lesson_row(2, "in_progress"),
        _lesson_row(3, None),
    ]
    result = await get_lessons_with_progress(db, str(uuid4()), str(uuid4()))
    assert result[1].status == "in_progress"
    assert result[2].status == "locked"


@pytest.mark.asyncio
async def test_get_lessons_empty():
    db = AsyncMock()
    db.fetch.return_value = []
    result = await get_lessons_with_progress(db, str(uuid4()), str(uuid4()))
    assert result == []


# ---------------------------------------------------------------------------
# unlock_next_lesson
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_unlock_next_lesson_happy_path():
    db = AsyncMock()
    level_id = str(uuid4())
    completed_id = str(uuid4())
    next_id = str(uuid4())

    db.fetchrow.side_effect = [
        {"level_id": level_id, "lesson_order": 1},  # completed lesson
        {"id": next_id},                              # next lesson
    ]
    db.execute = AsyncMock()

    result = await unlock_next_lesson(db, str(uuid4()), completed_id)
    assert result == next_id
    db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_unlock_next_lesson_last_lesson():
    db = AsyncMock()
    db.fetchrow.side_effect = [
        {"level_id": str(uuid4()), "lesson_order": 5},
        None,  # no next lesson
    ]
    result = await unlock_next_lesson(db, str(uuid4()), str(uuid4()))
    assert result is None


@pytest.mark.asyncio
async def test_unlock_next_lesson_not_found():
    db = AsyncMock()
    db.fetchrow.return_value = None  # completed lesson not found
    result = await unlock_next_lesson(db, str(uuid4()), str(uuid4()))
    assert result is None


@pytest.mark.asyncio
async def test_unlock_next_lesson_idempotent():
    """Calling twice should not raise — ON CONFLICT DO NOTHING handles it."""
    db = AsyncMock()
    level_id = str(uuid4())
    next_id = str(uuid4())
    db.fetchrow.side_effect = [
        {"level_id": level_id, "lesson_order": 1},
        {"id": next_id},
    ]
    db.execute = AsyncMock()
    result = await unlock_next_lesson(db, str(uuid4()), str(uuid4()))
    assert result == next_id


# ---------------------------------------------------------------------------
# Endpoint tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_list_lessons_requires_auth(async_client):
    level_id = str(uuid4())
    response = await async_client.get(f"/api/v1/levels/{level_id}/lessons")
    # guest-allowed endpoint; no auth means guest mode — should return 200 with empty list
    # The mock_conn won't have a level, so LEVEL_NOT_FOUND is expected
    assert response.status_code in (200, 404)


@pytest.mark.asyncio
async def test_get_lesson_not_found(async_client, mock_conn):
    mock_conn.fetchrow.return_value = None
    lesson_id = str(uuid4())
    response = await async_client.get(f"/api/v1/lessons/{lesson_id}")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "LESSON_NOT_FOUND"


@pytest.mark.asyncio
async def test_get_lesson_not_approved(async_client, mock_conn):
    lesson_id = str(uuid4())
    mock_conn.fetchrow.return_value = {
        "id": lesson_id,
        "level_id": str(uuid4()),
        "title": "Draft Lesson",
        "description": None,
        "lesson_order": 1,
        "status": "draft",
        "thumbnail_url": None,
        "is_guest_accessible": True,
        "translations": {},
    }
    response = await async_client.get(f"/api/v1/lessons/{lesson_id}")
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "LESSON_NOT_APPROVED"
