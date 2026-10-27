"""D-32: achievements must unlock as soon as they are earned, and drafts are not essays."""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from httpx import AsyncClient

from app.services import achievement_service as svc
from tests.conftest import make_token
from tests.test_daily_essay import _user_row

UID = "11111111-2222-3333-4444-555555555555"


def _ach(name, ctype, cval, xp=0, unlocked=None):
    return {
        "id": uuid4(), "name": name, "description": name, "icon_url": None,
        "condition_type": ctype, "condition_value": cval, "xp_reward": xp,
        "is_active": True, "translations": {}, "unlocked_at": unlocked,
    }


def _db(achievements_per_pass, users=()):
    db = AsyncMock()
    db.fetchval.return_value = 0
    db.fetchrow.side_effect = list(users)
    return db, patch.object(
        svc, "get_all_achievements_with_user_state", AsyncMock(side_effect=achievements_per_pass)
    )


@pytest.mark.asyncio
async def test_century_unlocks_at_154_xp():
    century = _ach("Century", "xp_total", 100)
    db, p = _db([[century]])
    with p, patch.object(svc, "unlock_achievement", AsyncMock()) as unlock, \
            patch("app.services.notification.create", AsyncMock()):
        got = await svc.check_and_unlock(db, {"id": UID, "xp_total": 154, "streak_current": 0})
    assert [a["name"] for a in got] == ["Century"]
    unlock.assert_awaited_once()


@pytest.mark.asyncio
async def test_xp_from_one_achievement_can_unlock_century():
    first = _ach("First Essay", "essay_count", 1, xp=50)
    century = _ach("Century", "xp_total", 100)
    db, p = _db(
        [[first, century], [dict(first, unlocked_at="now"), century]],
        users=[{"id": UID, "xp_total": 110, "streak_current": 0}],
    )
    db.fetchval.side_effect = [0, 0, 1, 0, 0, 1]  # lessons, words, essays per pass
    with p, patch.object(svc, "unlock_achievement", AsyncMock()), \
            patch("app.services.xp.award", AsyncMock()), \
            patch("app.services.notification.create", AsyncMock()):
        got = await svc.check_and_unlock(db, {"id": UID, "xp_total": 60, "streak_current": 0})
    assert [a["name"] for a in got] == ["First Essay", "Century"]


@pytest.mark.asyncio
async def test_essay_count_ignores_drafts():
    db = AsyncMock()
    db.fetchval.return_value = 0
    await svc._compute_stats(db, {"id": UID, "xp_total": 0, "streak_current": 0})
    essay_sql = [c.args[0] for c in db.fetchval.call_args_list if "daily_essay_submission" in c.args[0]]
    assert essay_sql and "is_draft = FALSE" in essay_sql[0]


@pytest.mark.asyncio
async def test_list_achievements_rechecks_first(async_client: AsyncClient, mock_conn: AsyncMock):
    mock_conn.fetchrow.side_effect = [_user_row()]
    with patch("app.api.v1.achievements.achievement_service.check_and_unlock", AsyncMock()) as chk, \
            patch("app.api.v1.achievements.get_all_achievements_with_user_state",
                  AsyncMock(return_value=[])):
        r = await async_client.get(
            "/api/v1/achievements", headers={"Authorization": f"Bearer {make_token()}"}
        )
    assert r.status_code == 200, r.text
    chk.assert_awaited_once()


@pytest.mark.asyncio
async def test_list_achievements_survives_recheck_failure(async_client: AsyncClient, mock_conn: AsyncMock):
    mock_conn.fetchrow.side_effect = [_user_row()]
    with patch("app.api.v1.achievements.achievement_service.check_and_unlock",
               AsyncMock(side_effect=RuntimeError("boom"))), \
            patch("app.api.v1.achievements.get_all_achievements_with_user_state",
                  AsyncMock(return_value=[])):
        r = await async_client.get(
            "/api/v1/achievements", headers={"Authorization": f"Bearer {make_token()}"}
        )
    assert r.status_code == 200
