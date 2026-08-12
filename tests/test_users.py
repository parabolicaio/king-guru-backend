"""Endpoint tests — GET/PATCH/DELETE /api/v1/users/me, POST /me/onboarding."""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from tests.conftest import make_token


def _user_row(
    user_id: str = "11111111-1111-1111-1111-111111111111",
    onboarding_completed_at=None,
    deleted_at=None,
) -> dict:
    now = datetime.now(timezone.utc)
    return {
        "id": user_id,
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
        "onboarding_completed_at": onboarding_completed_at,
        "placement_completed_at": None,
        "current_level_id": None,
        "subscription_tier": "free",
        "deleted_at": deleted_at,
        "created_at": now,
        "updated_at": now,
    }


def _auth_header() -> dict:
    return {"Authorization": f"Bearer {make_token()}"}


# ── GET /users/me ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_me(async_client: AsyncClient, mock_conn: AsyncMock):
    mock_conn.fetchrow.return_value = _user_row()
    resp = await async_client.get("/api/v1/users/me", headers=_auth_header())
    assert resp.status_code == 200
    assert resp.json()["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_get_me_unauthenticated(async_client: AsyncClient):
    resp = await async_client.get("/api/v1/users/me")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_get_me_deleted_user(async_client: AsyncClient, mock_conn: AsyncMock):
    mock_conn.fetchrow.return_value = _user_row(deleted_at=datetime.now(timezone.utc))
    resp = await async_client.get("/api/v1/users/me", headers=_auth_header())
    assert resp.status_code == 401
    assert resp.json()["error"]["code"] == "USER_DELETED"


# ── PATCH /users/me ──────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_patch_me(async_client: AsyncClient, mock_conn: AsyncMock):
    updated = _user_row()
    updated["display_name"] = "Nimal"
    mock_conn.fetchrow.side_effect = [_user_row(), updated]
    resp = await async_client.patch(
        "/api/v1/users/me",
        json={"display_name": "Nimal"},
        headers=_auth_header(),
    )
    assert resp.status_code == 200


# ── DELETE /users/me ─────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_delete_me(async_client: AsyncClient, mock_conn: AsyncMock):
    mock_conn.fetchrow.return_value = _user_row()
    with (
        patch("app.core.supabase_admin.sign_out_user", new_callable=AsyncMock),
        patch("app.core.supabase_admin.delete_user_recordings", new_callable=AsyncMock) as purge,
        patch("app.services.audit_service.log", new_callable=AsyncMock),
    ):
        resp = await async_client.delete("/api/v1/users/me", headers=_auth_header())
    assert resp.status_code == 204
    assert mock_conn.execute.called
    # Account deletion must purge the user's uploaded recordings from Storage.
    purge.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_me_pii_anonymised(async_client: AsyncClient, mock_conn: AsyncMock):
    """Verify the UPDATE statement includes anonymised PII placeholders."""
    row = _user_row(user_id="22222222-2222-2222-2222-222222222222")
    mock_conn.fetchrow.return_value = row
    with (
        patch("app.core.supabase_admin.sign_out_user", new_callable=AsyncMock),
        patch("app.core.supabase_admin.delete_user_recordings", new_callable=AsyncMock),
        patch("app.services.audit_service.log", new_callable=AsyncMock),
    ):
        resp = await async_client.delete("/api/v1/users/me", headers=_auth_header())
    assert resp.status_code == 204
    sql_call = mock_conn.execute.call_args_list[0]
    assert "[deleted-" in str(sql_call)


# ── POST /users/me/onboarding ────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_complete_onboarding(async_client: AsyncClient, mock_conn: AsyncMock):
    now = datetime.now(timezone.utc)
    completed_row = _user_row(onboarding_completed_at=now)
    mock_conn.fetchrow.side_effect = [_user_row(), completed_row]
    resp = await async_client.post(
        "/api/v1/users/me/onboarding",
        json={
            "full_name": "Nimal Perera",
            "age_group": "adult",
            "role_tag": "student",
            "language_preference": "en",
        },
        headers=_auth_header(),
    )
    assert resp.status_code == 200
    assert "onboarding_completed_at" in resp.json()


@pytest.mark.asyncio
async def test_complete_onboarding_missing_field(async_client: AsyncClient, mock_conn: AsyncMock):
    mock_conn.fetchrow.return_value = _user_row()
    resp = await async_client.post(
        "/api/v1/users/me/onboarding",
        json={"full_name": "Nimal"},  # missing required fields
        headers=_auth_header(),
    )
    assert resp.status_code == 422
