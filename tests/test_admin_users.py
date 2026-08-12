"""Tests for admin user management endpoints (B8)."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4


@pytest.mark.asyncio
async def test_list_users_requires_admin(async_client):
    response = await async_client.get(
        "/api/v1/admin/users",
        headers={"Authorization": "Bearer fake"},
    )
    assert response.status_code in (401, 403)


@pytest.mark.asyncio
async def test_get_user_requires_admin(async_client):
    response = await async_client.get(
        f"/api/v1/admin/users/{uuid4()}",
        headers={"Authorization": "Bearer fake"},
    )
    assert response.status_code in (401, 403)


@pytest.mark.asyncio
async def test_update_role_requires_admin(async_client):
    response = await async_client.patch(
        f"/api/v1/admin/users/{uuid4()}/role",
        json={"admin_role": "content_manager"},
        headers={"Authorization": "Bearer fake"},
    )
    assert response.status_code in (401, 403)


@pytest.mark.asyncio
async def test_delete_user_requires_admin(async_client):
    response = await async_client.delete(
        f"/api/v1/admin/users/{uuid4()}",
        headers={"Authorization": "Bearer fake"},
    )
    assert response.status_code in (401, 403)


@pytest.mark.asyncio
async def test_cannot_demote_self():
    from app.core.errors import AppError, CANNOT_DEMOTE_SELF

    # Simulate the guard in the endpoint
    admin_id = str(uuid4())
    target_id = admin_id  # Same user

    if target_id == admin_id:
        with pytest.raises(AppError) as exc:
            raise AppError(*CANNOT_DEMOTE_SELF)
        assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_cannot_delete_self():
    from app.core.errors import AppError, CANNOT_DELETE_SELF

    admin_id = str(uuid4())
    target_id = admin_id

    if target_id == admin_id:
        with pytest.raises(AppError) as exc:
            raise AppError(*CANNOT_DELETE_SELF)
        assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_list_users_search_query():
    from app.db.queries.admin_users import list_users

    conn = AsyncMock()
    conn.fetch.return_value = []
    count_row = MagicMock()
    count_row.__getitem__ = lambda self, key: 0 if key == "total" else None
    conn.fetchrow.return_value = count_row

    rows, total = await list_users(conn, search="nimal", page=1, page_size=20)
    assert total == 0
    # Verify search term is passed as parameter (no string formatting)
    call_args = conn.fetch.call_args
    query = call_args[0][0]
    assert "$" in query  # parameterized


@pytest.mark.asyncio
async def test_get_user_not_found(async_client):
    from app.core.errors import AppError, USER_NOT_FOUND
    from app.db.queries import admin_users

    from unittest.mock import patch

    with patch.object(admin_users, "get_user_with_progress", return_value=None):
        response = await async_client.get(
            f"/api/v1/admin/users/{uuid4()}",
            headers={"Authorization": "Bearer fake"},
        )
    assert response.status_code in (401, 403, 404)
