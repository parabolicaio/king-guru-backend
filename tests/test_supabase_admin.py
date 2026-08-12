"""Unit tests for app.core.supabase_admin.delete_user_recordings.

Verifies the account-deletion Storage purge: lists recordings/{user_id}/ in the
``audio`` bucket (paginated) and bulk-deletes every object by full path.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.core import supabase_admin

USER_ID = "11111111-1111-1111-1111-111111111111"


def _resp(status_code: int = 200, json_body=None):
    r = MagicMock()
    r.status_code = status_code
    r.text = ""
    r.json.return_value = json_body if json_body is not None else []
    r.raise_for_status.return_value = None
    return r


def _obj(name: str) -> dict:
    # A real Storage file entry has a non-null id; folder pseudo-entries have id=None.
    return {"name": name, "id": f"id-{name}"}


def _patched_client(post_side_effect, request_return):
    """Build a MagicMock standing in for httpx.AsyncClient (async context mgr)."""
    client = MagicMock()
    client.post = AsyncMock(side_effect=post_side_effect)
    client.request = AsyncMock(return_value=request_return)
    ctx = MagicMock()
    ctx.__aenter__ = AsyncMock(return_value=client)
    ctx.__aexit__ = AsyncMock(return_value=False)
    factory = MagicMock(return_value=ctx)
    return factory, client


@pytest.mark.asyncio
async def test_delete_user_recordings_deletes_all_objects():
    list_resp = _resp(json_body=[_obj("a1.ogg"), _obj("a2.webm")])
    del_resp = _resp(status_code=200)
    factory, client = _patched_client([list_resp], del_resp)

    with patch.object(supabase_admin.httpx, "AsyncClient", factory):
        await supabase_admin.delete_user_recordings(USER_ID)

    client.request.assert_awaited_once()
    _, kwargs = client.request.call_args
    assert kwargs["json"]["prefixes"] == [
        f"recordings/{USER_ID}/a1.ogg",
        f"recordings/{USER_ID}/a2.webm",
    ]


@pytest.mark.asyncio
async def test_delete_user_recordings_paginates():
    """A full page (100) triggers a second list call; a short page ends it."""
    page1 = _resp(json_body=[_obj(f"f{i}.ogg") for i in range(supabase_admin._LIST_PAGE_SIZE)])
    page2 = _resp(json_body=[_obj("last.ogg")])
    del_resp = _resp(status_code=200)
    factory, client = _patched_client([page1, page2], del_resp)

    with patch.object(supabase_admin.httpx, "AsyncClient", factory):
        await supabase_admin.delete_user_recordings(USER_ID)

    assert client.post.await_count == 2
    _, kwargs = client.request.call_args
    assert len(kwargs["json"]["prefixes"]) == supabase_admin._LIST_PAGE_SIZE + 1
    assert f"recordings/{USER_ID}/last.ogg" in kwargs["json"]["prefixes"]


@pytest.mark.asyncio
async def test_delete_user_recordings_noop_when_empty():
    factory, client = _patched_client([_resp(json_body=[])], _resp())

    with patch.object(supabase_admin.httpx, "AsyncClient", factory):
        await supabase_admin.delete_user_recordings(USER_ID)

    client.request.assert_not_awaited()


@pytest.mark.asyncio
async def test_delete_user_recordings_skips_folder_pseudo_entries():
    objs = [_obj("real.ogg"), {"name": "subfolder", "id": None}]
    factory, client = _patched_client([_resp(json_body=objs)], _resp())

    with patch.object(supabase_admin.httpx, "AsyncClient", factory):
        await supabase_admin.delete_user_recordings(USER_ID)

    _, kwargs = client.request.call_args
    assert kwargs["json"]["prefixes"] == [f"recordings/{USER_ID}/real.ogg"]


@pytest.mark.asyncio
async def test_delete_user_recordings_swallows_errors():
    """A Storage failure must never propagate — DB soft-delete already happened."""
    factory, _ = _patched_client([RuntimeError("storage down")], _resp())

    with patch.object(supabase_admin.httpx, "AsyncClient", factory):
        # Must not raise.
        await supabase_admin.delete_user_recordings(USER_ID)
