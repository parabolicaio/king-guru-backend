"""Endpoint tests for Daily Essay — GET /today, PUT /draft, POST /submit,
GET /history, GET /{submission_id}.
"""

from datetime import date, datetime, timezone
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from tests.conftest import make_token

# ── Shared constants ─────────────────────────────────────────────────────────

_USER_ID   = "11111111-1111-1111-1111-111111111111"
_LEVEL_ID  = "22222222-2222-2222-2222-222222222222"
_PROMPT_ID = "33333333-3333-3333-3333-333333333333"
_SUB_ID    = "44444444-4444-4444-4444-444444444444"


def _auth_header(level_id: str | None = None) -> dict:
    return {"Authorization": f"Bearer {make_token()}"}


# ── Row factories ────────────────────────────────────────────────────────────

def _user_row(*, with_level: bool = False) -> dict:
    now = datetime.now(timezone.utc)
    return {
        "id": _USER_ID,
        "supabase_uid": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
        "email": "test@example.com",
        "phone": None,
        "full_name": "Test User",
        "display_name": None,
        "avatar_url": None,
        "age_group": "adult",
        "role_tag": "student",
        "auth_provider": "email",
        "language_preference": "en",
        "is_guest": False,
        "guest_token": None,
        "admin_role": None,
        "xp_total": 0,
        "streak_current": 0,
        "streak_longest": 0,
        "onboarding_completed_at": now,
        "placement_completed_at": None,
        "current_level_id": _LEVEL_ID if with_level else None,
        "subscription_tier": "free",
        "deleted_at": None,
        "created_at": now,
        "updated_at": now,
    }


def _level_row(*, essay_enabled: bool) -> dict:
    return {
        "id": _LEVEL_ID,
        "code": "elementary" if essay_enabled else "beginner_a",
        "name": "Elementary" if essay_enabled else "Beginner A",
        "daily_essay_enabled": essay_enabled,
        "display_order": 3 if essay_enabled else 1,
        "is_active": True,
        "description": None,
        "translations": None,
        "icon_url": None,
        "topics": None,
    }


def _prompt_row() -> dict:
    now = datetime.now(timezone.utc)
    return {
        "id": _PROMPT_ID,
        "prompt_text": "Describe your favourite place.",
        "level_id": None,
        "date_assigned": None,
        "is_active": True,
        "translations": {},
        "created_at": now,
        "updated_at": now,
    }


def _submission_row(*, is_draft: bool, grade: str | None = None) -> dict:
    now = datetime.now(timezone.utc)
    return {
        "id": _SUB_ID,
        "user_id": _USER_ID,
        "essay_prompt_id": _PROMPT_ID,
        "prompt_text": "Describe your favourite place.",
        "essay_text": "My favourite place is my home.",
        "submitted_at": None if is_draft else now,
        "submission_date": date.today(),
        "is_draft": is_draft,
        "grade": grade,
        "score_grammar": None,
        "score_vocabulary": None,
        "score_content": None,
        "score_suggestions": None,
        "ai_feedback": None,
        "ai_model": None,
        "xp_awarded": 0,
        "feedback_language": "en",
        "created_at": now,
        "updated_at": now,
    }


# ── GET /today ───────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_today_no_submission(async_client: AsyncClient, mock_conn: AsyncMock):
    """Returns prompt + submission=null when user has no submission today."""
    mock_conn.fetchrow.side_effect = [
        _user_row(),     # get_current_user
        _prompt_row(),   # get_today_prompt (level_id=None → level-null query)
        None,            # get_submission_for_today
    ]
    resp = await async_client.get("/api/v1/daily-essay/today", headers=_auth_header())
    assert resp.status_code == 200
    data = resp.json()
    assert data["prompt"]["prompt_text"] == "Describe your favourite place."
    assert data["submission"] is None


@pytest.mark.asyncio
async def test_get_today_with_draft(async_client: AsyncClient, mock_conn: AsyncMock):
    """Returns existing draft in submission field."""
    mock_conn.fetchrow.side_effect = [
        _user_row(),
        _prompt_row(),
        _submission_row(is_draft=True),
    ]
    resp = await async_client.get("/api/v1/daily-essay/today", headers=_auth_header())
    assert resp.status_code == 200
    sub = resp.json()["submission"]
    assert sub is not None
    assert sub["is_draft"] is True


@pytest.mark.asyncio
async def test_get_today_unauthenticated(async_client: AsyncClient):
    resp = await async_client.get("/api/v1/daily-essay/today")
    assert resp.status_code == 401


# ── PUT /draft ───────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_save_draft_creates_row(async_client: AsyncClient, mock_conn: AsyncMock):
    """Creating a new draft returns is_draft=True."""
    mock_conn.fetchrow.side_effect = [
        _user_row(with_level=True),      # get_current_user
        _level_row(essay_enabled=True),  # _check_level_eligibility
        None,                            # get_submission_for_today → no existing
        _prompt_row(),                   # fetch prompt by id
        _submission_row(is_draft=True),  # create_draft RETURNING *
    ]
    resp = await async_client.put(
        "/api/v1/daily-essay/draft",
        json={
            "essay_prompt_id": _PROMPT_ID,
            "draft_text": "My draft essay text here.",
            "feedback_language": "en",
        },
        headers=_auth_header(),
    )
    assert resp.status_code == 200
    assert resp.json()["is_draft"] is True


@pytest.mark.asyncio
async def test_save_draft_idempotent(async_client: AsyncClient, mock_conn: AsyncMock):
    """Saving draft when one already exists updates and returns same ID."""
    draft = _submission_row(is_draft=True)
    updated = {**draft, "essay_text": "Updated draft text."}
    mock_conn.fetchrow.side_effect = [
        _user_row(with_level=True),
        _level_row(essay_enabled=True),
        draft,           # get_submission_for_today → existing draft
        _prompt_row(),   # SELECT * FROM essay_prompt (prompt snapshot)
        updated,         # update_draft_text RETURNING *
    ]
    resp = await async_client.put(
        "/api/v1/daily-essay/draft",
        json={
            "essay_prompt_id": _PROMPT_ID,
            "draft_text": "Updated draft text.",
            "feedback_language": "en",
        },
        headers=_auth_header(),
    )
    assert resp.status_code == 200
    assert resp.json()["id"] == _SUB_ID


@pytest.mark.asyncio
async def test_save_draft_blocked_after_submit(async_client: AsyncClient, mock_conn: AsyncMock):
    """Returns 409 if today's essay has already been submitted."""
    mock_conn.fetchrow.side_effect = [
        _user_row(with_level=True),
        _level_row(essay_enabled=True),
        _submission_row(is_draft=False),  # already submitted
    ]
    resp = await async_client.put(
        "/api/v1/daily-essay/draft",
        json={
            "essay_prompt_id": _PROMPT_ID,
            "draft_text": "Another draft.",
            "feedback_language": "en",
        },
        headers=_auth_header(),
    )
    assert resp.status_code == 409
    assert resp.json()["error"]["code"] == "ESSAY_ALREADY_SUBMITTED"


# ── POST /submit ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_submit_essay_happy_path(async_client: AsyncClient, mock_conn: AsyncMock):
    """Successful submission returns is_draft=False and grade=null (grading is async)."""
    with (
        patch("app.api.v1.daily_essay._grade_in_background", new=AsyncMock()),
        patch("app.services.streak.record_qualifying_activity", new=AsyncMock()),
        patch("app.services.daily_goal_service.record_activity", new=AsyncMock()),
    ):
        mock_conn.fetchrow.side_effect = [
            _user_row(with_level=True),
            _level_row(essay_enabled=True),
            None,                                  # no existing submission
            _prompt_row(),                         # fetch prompt by id
            _submission_row(is_draft=False),       # create_submission RETURNING *
        ]
        resp = await async_client.post(
            "/api/v1/daily-essay/submit",
            json={
                "essay_prompt_id": _PROMPT_ID,
                "essay_text": "A" * 150,
                "feedback_language": "en",
            },
            headers=_auth_header(),
        )
    assert resp.status_code == 201
    data = resp.json()
    assert data["is_draft"] is False
    assert data["grade"] is None   # async grading not yet complete


@pytest.mark.asyncio
async def test_submit_twice_returns_409(async_client: AsyncClient, mock_conn: AsyncMock):
    """Submitting again when already submitted → 409 ESSAY_ALREADY_SUBMITTED."""
    with (
        patch("app.api.v1.daily_essay._grade_in_background", new=AsyncMock()),
        patch("app.services.streak.record_qualifying_activity", new=AsyncMock()),
        patch("app.services.daily_goal_service.record_activity", new=AsyncMock()),
    ):
        mock_conn.fetchrow.side_effect = [
            _user_row(with_level=True),
            _level_row(essay_enabled=True),
            _submission_row(is_draft=False),   # already submitted
        ]
        resp = await async_client.post(
            "/api/v1/daily-essay/submit",
            json={
                "essay_prompt_id": _PROMPT_ID,
                "essay_text": "B" * 150,
                "feedback_language": "en",
            },
            headers=_auth_header(),
        )
    assert resp.status_code == 409
    assert resp.json()["error"]["code"] == "ESSAY_ALREADY_SUBMITTED"


@pytest.mark.asyncio
async def test_beginner_a_level_blocked(async_client: AsyncClient, mock_conn: AsyncMock):
    """User at Beginner A (daily_essay_enabled=False) gets 403."""
    mock_conn.fetchrow.side_effect = [
        _user_row(with_level=True),
        _level_row(essay_enabled=False),  # Beginner A
    ]
    resp = await async_client.post(
        "/api/v1/daily-essay/submit",
        json={
            "essay_prompt_id": _PROMPT_ID,
            "essay_text": "C" * 150,
            "feedback_language": "en",
        },
        headers=_auth_header(),
    )
    assert resp.status_code == 403
    assert resp.json()["error"]["code"] == "ESSAY_NOT_AVAILABLE"


# ── GET /history ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_history_excludes_drafts(async_client: AsyncClient, mock_conn: AsyncMock):
    """GET /history returns submitted essays only (drafts excluded at DB level)."""
    submitted = {**_submission_row(is_draft=False), "word_count": 6}
    mock_conn.fetchrow.return_value = _user_row()
    mock_conn.fetch.return_value = [submitted]
    resp = await async_client.get("/api/v1/daily-essay/history", headers=_auth_header())
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["data"]) == 1
    assert data["data"][0]["id"] == _SUB_ID


@pytest.mark.asyncio
async def test_history_empty(async_client: AsyncClient, mock_conn: AsyncMock):
    """GET /history with no essays returns empty list and has_more=False."""
    mock_conn.fetchrow.return_value = _user_row()
    mock_conn.fetch.return_value = []
    resp = await async_client.get("/api/v1/daily-essay/history", headers=_auth_header())
    assert resp.status_code == 200
    data = resp.json()
    assert data["data"] == []
    assert data["has_more"] is False
    assert data["cursor"] is None


# ── GET /{submission_id} ─────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_submission_by_id(async_client: AsyncClient, mock_conn: AsyncMock):
    """GET /{id} returns the full submission response for an existing essay."""
    mock_conn.fetchrow.side_effect = [
        _user_row(),
        _submission_row(is_draft=False, grade="B+"),
    ]
    resp = await async_client.get(
        f"/api/v1/daily-essay/{_SUB_ID}", headers=_auth_header()
    )
    assert resp.status_code == 200
    assert resp.json()["id"] == _SUB_ID
    assert resp.json()["grade"] == "B+"


@pytest.mark.asyncio
async def test_get_submission_not_found(async_client: AsyncClient, mock_conn: AsyncMock):
    """GET /{id} for a non-existent or other user's essay returns 404."""
    mock_conn.fetchrow.side_effect = [_user_row(), None]
    resp = await async_client.get(
        f"/api/v1/daily-essay/{_SUB_ID}", headers=_auth_header()
    )
    assert resp.status_code == 404
    assert resp.json()["error"]["code"] == "ESSAY_NOT_FOUND"
