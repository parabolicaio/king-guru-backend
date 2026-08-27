"""Endpoint tests — POST /api/v1/auth/signup, POST /api/v1/auth/session,
POST /api/v1/users/guest.

JWT secret and other settings are injected via os.environ in conftest.py
before any app module is imported, so no patching is required here.
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from tests.conftest import make_token


def _fake_user_row(
    user_id: str = "11111111-1111-1111-1111-111111111111",
    supabase_uid: str = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
    admin_role: str | None = None,
    deleted_at=None,
    onboarding_completed_at=None,
) -> dict:
    now = datetime.now(timezone.utc)
    return {
        "id": user_id,
        "supabase_uid": supabase_uid,
        "email": "test@example.com",
        "phone": None,
        "full_name": "",
        "display_name": None,
        "avatar_url": None,
        "age_group": None,
        "role_tag": "",
        "english_level": None,
        "auth_provider": "email",
        "language_preference": "en",
        "is_guest": False,
        "guest_token": None,
        "admin_role": admin_role,
        "xp_total": 0,
        "streak_current": 0,
        "streak_longest": 0,
        "onboarding_completed_at": onboarding_completed_at,
        "placement_completed_at": None,
        "current_level_id": None,
        "subscription_tier": "free",
        "deleted_at": deleted_at,
        "created_at": now,
        "updated_at": now,
    }


# ── Shared helpers ───────────────────────────────────────────────────────────

_SIGNUP_BODY = {
    "full_name": "Nimal Perera",
    "age_group": "19_25",
    "role_tag": "working_adult",
    "english_level": "little",
    "language_preference": "en",
}

_LEVEL_ID = "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"


def _fake_level_row(is_active: bool = True) -> dict:
    return {
        "id": _LEVEL_ID,
        "code": "beginner_a",
        "name": "Beginner A",
        "is_active": is_active,
        "display_order": 1,
        "daily_essay_enabled": False,
        "description": None,
        "translations": None,
        "icon_url": None,
        "topics": None,
    }


def _fake_placement_row() -> dict:
    return {
        "id": "11111111-1111-1111-1111-111111111111",
        "current_level_id": _LEVEL_ID,
        "placement_completed_at": datetime.now(timezone.utc),
    }


# ── POST /auth/signup ─────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_signup_no_token_returns_401(async_client: AsyncClient):
    resp = await async_client.post("/api/v1/auth/signup", json=_SIGNUP_BODY)
    assert resp.status_code == 401
    assert resp.json()["error"]["code"] == "UNAUTHORIZED"


@pytest.mark.asyncio
async def test_signup_missing_fields_returns_422(async_client: AsyncClient):
    token = make_token(email=None, phone="+94771234567")
    resp = await async_client.post(
        "/api/v1/auth/signup",
        json={"full_name": "Nimal"},       # missing age_group, role_tag, etc.
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_signup_invalid_age_group_returns_422(async_client: AsyncClient):
    token = make_token(email=None, phone="+94771234567")
    resp = await async_client.post(
        "/api/v1/auth/signup",
        json={**_SIGNUP_BODY, "age_group": "not_a_real_group"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_signup_new_user_happy_path(async_client: AsyncClient, mock_conn: AsyncMock):
    """New phone-only user — no placement, no guest token."""
    token = make_token(email=None, phone="+94771234567")
    now = datetime.now(timezone.utc)
    created_row = _fake_user_row(onboarding_completed_at=None)
    onboarded_row = _fake_user_row(onboarding_completed_at=now)
    final_row = _fake_user_row(onboarding_completed_at=now)

    # fetchrow call order:
    # 1. get_user_by_supabase_uid → None (new user)
    # 2. create_user → get_user_by_id → created_row
    # 3. complete_onboarding → get_user_by_id → onboarded_row
    # 4. final get_user_by_supabase_uid → final_row
    mock_conn.fetchrow.side_effect = [None, created_row, onboarded_row, final_row]

    with patch("app.services.audit_service.log", new_callable=AsyncMock):
        resp = await async_client.post(
            "/api/v1/auth/signup",
            json=_SIGNUP_BODY,
            headers={"Authorization": f"Bearer {token}"},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["onboarding_completed"] is True
    assert data["placement_completed"] is False


@pytest.mark.asyncio
async def test_signup_idempotent_already_onboarded(
    async_client: AsyncClient, mock_conn: AsyncMock
):
    """If onboarding is already complete, return existing profile unchanged."""
    token = make_token(email=None, phone="+94771234567")
    now = datetime.now(timezone.utc)
    existing_row = _fake_user_row(onboarding_completed_at=now)

    mock_conn.fetchrow.return_value = existing_row

    resp = await async_client.post(
        "/api/v1/auth/signup",
        json=_SIGNUP_BODY,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resp.status_code == 200
    assert resp.json()["onboarding_completed"] is True
    # Only one fetchrow call made — returned immediately
    assert mock_conn.fetchrow.call_count == 1


@pytest.mark.asyncio
async def test_signup_deleted_user_returns_401(
    async_client: AsyncClient, mock_conn: AsyncMock
):
    token = make_token(email=None, phone="+94771234567")
    mock_conn.fetchrow.return_value = _fake_user_row(
        deleted_at=datetime.now(timezone.utc)
    )
    resp = await async_client.post(
        "/api/v1/auth/signup",
        json=_SIGNUP_BODY,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 401
    assert resp.json()["error"]["code"] == "USER_DELETED"


@pytest.mark.asyncio
async def test_signup_with_valid_placement_level(
    async_client: AsyncClient, mock_conn: AsyncMock
):
    """Explicit placement_level_id is validated then applied."""
    token = make_token(email=None, phone="+94771234567")
    now = datetime.now(timezone.utc)
    created_row = _fake_user_row()
    onboarded_row = _fake_user_row(onboarding_completed_at=now)
    final_row = _fake_user_row(onboarding_completed_at=now)

    # fetchrow call order:
    # 1. get_user_by_supabase_uid → None
    # 2. get_level_by_id → level_row
    # 3. create_user → get_user_by_id → created_row
    # 4. complete_onboarding → get_user_by_id → onboarded_row
    # 5. set_user_level_and_placement (RETURNING) → placement_row
    # 6. final get_user_by_supabase_uid → final_row
    mock_conn.fetchrow.side_effect = [
        None,
        _fake_level_row(),
        created_row,
        onboarded_row,
        _fake_placement_row(),
        final_row,
    ]

    with patch("app.services.audit_service.log", new_callable=AsyncMock):
        resp = await async_client.post(
            "/api/v1/auth/signup",
            json={**_SIGNUP_BODY, "placement_level_id": _LEVEL_ID},
            headers={"Authorization": f"Bearer {token}"},
        )

    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_signup_invalid_placement_level_returns_404(
    async_client: AsyncClient, mock_conn: AsyncMock
):
    """placement_level_id that doesn't exist → 404 before any writes."""
    token = make_token(email=None, phone="+94771234567")

    # fetchrow call order:
    # 1. get_user_by_supabase_uid → None
    # 2. get_level_by_id → None (not found)
    mock_conn.fetchrow.side_effect = [None, None]

    resp = await async_client.post(
        "/api/v1/auth/signup",
        json={**_SIGNUP_BODY, "placement_level_id": _LEVEL_ID},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resp.status_code == 404
    assert resp.json()["error"]["code"] == "LEVEL_NOT_FOUND"
    # No writes should have been made
    mock_conn.execute.assert_not_called()


@pytest.mark.asyncio
async def test_signup_inactive_placement_level_returns_400(
    async_client: AsyncClient, mock_conn: AsyncMock
):
    token = make_token(email=None, phone="+94771234567")

    mock_conn.fetchrow.side_effect = [None, _fake_level_row(is_active=False)]

    resp = await async_client.post(
        "/api/v1/auth/signup",
        json={**_SIGNUP_BODY, "placement_level_id": _LEVEL_ID},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resp.status_code == 400
    assert resp.json()["error"]["code"] == "LEVEL_NOT_ACTIVE"
    mock_conn.execute.assert_not_called()


@pytest.mark.asyncio
async def test_signup_with_guest_token_reattributes(
    async_client: AsyncClient, mock_conn: AsyncMock
):
    """guest_token triggers reattribute; patched to isolate from guest DB logic."""
    token = make_token(email=None, phone="+94771234567")
    now = datetime.now(timezone.utc)
    created_row = _fake_user_row()
    onboarded_row = _fake_user_row(onboarding_completed_at=now)
    final_row = _fake_user_row(onboarding_completed_at=now)

    mock_conn.fetchrow.side_effect = [None, created_row, onboarded_row, final_row]

    with (
        patch("app.services.audit_service.log", new_callable=AsyncMock),
        patch("app.services.guest_service.reattribute", new_callable=AsyncMock) as mock_reattribute,
    ):
        resp = await async_client.post(
            "/api/v1/auth/signup",
            json={**_SIGNUP_BODY, "guest_token": "12345678-1234-1234-1234-123456789abc"},
            headers={"Authorization": f"Bearer {token}"},
        )

    assert resp.status_code == 200
    mock_reattribute.assert_called_once()


# ── POST /auth/session ───────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_session_existing_user(async_client: AsyncClient, mock_conn: AsyncMock):
    token = make_token()
    mock_conn.fetchrow.return_value = _fake_user_row()
    resp = await async_client.post(
        "/api/v1/auth/session",
        json={},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == "test@example.com"
    assert data["onboarding_completed"] is False
    assert data["admin_role"] is None


@pytest.mark.asyncio
async def test_create_session_new_user(async_client: AsyncClient, mock_conn: AsyncMock):
    token = make_token()
    created_row = _fake_user_row()
    mock_conn.fetchrow.side_effect = [None, created_row]
    with patch("app.services.audit_service.log", new_callable=AsyncMock):
        resp = await async_client.post(
            "/api/v1/auth/session",
            json={},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    assert mock_conn.execute.called


@pytest.mark.asyncio
async def test_create_session_no_token_returns_401(async_client: AsyncClient):
    resp = await async_client.post("/api/v1/auth/session", json={})
    assert resp.status_code == 401
    assert resp.json()["error"]["code"] == "UNAUTHORIZED"


@pytest.mark.asyncio
async def test_create_session_expired_token(async_client: AsyncClient):
    token = make_token(expired=True)
    resp = await async_client.post(
        "/api/v1/auth/session",
        json={},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 401
    assert resp.json()["error"]["code"] == "JWT_EXPIRED"


@pytest.mark.asyncio
async def test_create_session_invalid_token(async_client: AsyncClient):
    resp = await async_client.post(
        "/api/v1/auth/session",
        json={},
        headers={"Authorization": "Bearer not.a.real.token"},
    )
    assert resp.status_code == 401
    assert resp.json()["error"]["code"] == "JWT_INVALID"


@pytest.mark.asyncio
async def test_create_session_deleted_user(async_client: AsyncClient, mock_conn: AsyncMock):
    token = make_token()
    mock_conn.fetchrow.return_value = _fake_user_row(deleted_at=datetime.now(timezone.utc))
    resp = await async_client.post(
        "/api/v1/auth/session",
        json={},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 401
    assert resp.json()["error"]["code"] == "USER_DELETED"


# ── POST /users/guest ─────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_guest_new(async_client: AsyncClient, mock_conn: AsyncMock):
    guest_token = "12345678-1234-1234-1234-123456789abc"
    now = datetime.now(timezone.utc)
    guest_row = {
        "id": "99999999-9999-9999-9999-999999999999",
        "guest_token": guest_token,
        "created_at": now,
        "is_guest": True,
        "deleted_at": None,
        "supabase_uid": None,
        "email": None, "phone": None, "full_name": "",
        "display_name": None, "avatar_url": None, "age_group": None,
        "role_tag": "", "auth_provider": None, "language_preference": "en",
        "admin_role": None, "xp_total": 0, "streak_current": 0,
        "streak_longest": 0, "onboarding_completed_at": None,
        "placement_completed_at": None, "current_level_id": None,
        "subscription_tier": "free", "updated_at": now,
    }
    mock_conn.fetchrow.side_effect = [None, guest_row]
    resp = await async_client.post("/api/v1/users/guest", json={"guest_token": guest_token})
    assert resp.status_code == 200
    assert resp.json()["guest_token"] == guest_token


@pytest.mark.asyncio
async def test_create_guest_invalid_uuid(async_client: AsyncClient):
    resp = await async_client.post("/api/v1/users/guest", json={"guest_token": "not-a-uuid"})
    assert resp.status_code == 422
