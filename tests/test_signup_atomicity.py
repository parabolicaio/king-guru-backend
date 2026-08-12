"""Regression guard: the signup / session write paths run inside a DB transaction.

The production review found create_account / get_or_create_session_user doing
multiple writes (incl. guest reattribute) on an autocommit pooled connection, so
a mid-sequence failure left a half-migrated guest and a retry double-applied the
non-idempotent xp_ledger INSERT / xp_total bump. These tests assert the write
paths open `conn.transaction()`, so the wrapper can't be silently removed.
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from tests.conftest import make_token
from tests.test_auth import _LEVEL_ID, _SIGNUP_BODY, _fake_user_row


@pytest.mark.asyncio
async def test_signup_with_guest_runs_in_transaction(
    async_client: AsyncClient, mock_conn: AsyncMock
):
    token = make_token(email=None, phone="+94771234567")
    now = datetime.now(timezone.utc)
    mock_conn.fetchrow.side_effect = [
        None,                              # get_user_by_supabase_uid → new user
        {"current_level_id": _LEVEL_ID},   # guest-level lookup
        _fake_user_row(),                  # create_user → get_user_by_id
        _fake_user_row(onboarding_completed_at=now),  # complete_onboarding
        _fake_user_row(onboarding_completed_at=now),  # final reload
    ]
    with (
        patch("app.services.audit_service.log", new_callable=AsyncMock),
        patch("app.services.guest_service.reattribute", new_callable=AsyncMock),
    ):
        resp = await async_client.post(
            "/api/v1/auth/signup",
            json={**_SIGNUP_BODY, "guest_token": "12345678-1234-1234-1234-123456789abc"},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    mock_conn.transaction.assert_called()  # writes are wrapped


@pytest.mark.asyncio
async def test_session_new_user_runs_in_transaction(
    async_client: AsyncClient, mock_conn: AsyncMock
):
    token = make_token()
    mock_conn.fetchrow.side_effect = [None, _fake_user_row()]
    with patch("app.services.audit_service.log", new_callable=AsyncMock):
        resp = await async_client.post(
            "/api/v1/auth/session",
            json={},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    mock_conn.transaction.assert_called()


@pytest.mark.asyncio
async def test_signup_validation_failure_opens_no_transaction(
    async_client: AsyncClient, mock_conn: AsyncMock
):
    """Read-only validation stays OUTSIDE the transaction (fail fast, no writes)."""
    token = make_token(email=None, phone="+94771234567")
    mock_conn.fetchrow.side_effect = [None, None]  # user None, level not found
    resp = await async_client.post(
        "/api/v1/auth/signup",
        json={**_SIGNUP_BODY, "placement_level_id": _LEVEL_ID},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 404
    mock_conn.transaction.assert_not_called()
    mock_conn.execute.assert_not_called()
