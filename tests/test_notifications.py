"""Tests for notifications endpoints."""

import pytest
from unittest.mock import AsyncMock
from uuid import uuid4


@pytest.mark.asyncio
async def test_list_notifications_requires_auth(async_client):
    response = await async_client.get("/api/v1/notifications")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_mark_all_read_requires_auth(async_client):
    response = await async_client.post("/api/v1/notifications/read-all")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_mark_notification_read_not_owned(async_client, mock_conn):
    from app.core.errors import AppError, NOTIFICATION_NOT_OWNED

    notif_id = str(uuid4())
    # mark_notification_read returns None = not owned
    mock_conn.fetchrow.return_value = None

    from app.services import notification as ns
    from unittest.mock import patch

    with patch.object(ns, "mark_read", side_effect=AppError(*NOTIFICATION_NOT_OWNED)):
        response = await async_client.patch(
            f"/api/v1/notifications/{notif_id}/read",
            headers={"Authorization": "Bearer fake"},
        )
    assert response.status_code in (401, 403)
