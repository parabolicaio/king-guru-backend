"""D-89: leaderboard privacy.

Other learners see only a first name and last initial; hidden, staff, guest
and 0-XP accounts are left out; PATCH /users/me changes only the fields sent.
"""
from unittest.mock import AsyncMock, patch

import pytest

from app.api.v1 import users as users_api
from app.db.queries.achievements import LEADERBOARD_WHERE, leaderboard_name
from app.schemas.users import UpdateProfileRequest


@pytest.mark.parametrize(
    "display_name, full_name, expected",
    [
        (None, "Sehara Fernando", "Sehara F."),
        ("  ", "nimal perera silva", "nimal S."),
        ("Kasun", "Kasun Perera", "Kasun"),
        (None, "Madonna", "Madonna"),
        (None, "", "Learner"),
        (None, None, "Learner"),
    ],
)
def test_leaderboard_name(display_name, full_name, expected):
    assert leaderboard_name(display_name, full_name) == expected


def test_leaderboard_filter_leaves_out_hidden_staff_guests_and_zero_xp():
    for clause in (
        "u.xp_total > 0",
        "u.leaderboard_hidden = FALSE",
        "u.admin_role IS NULL",
        "u.is_guest = FALSE",
        "u.deleted_at IS NULL",
    ):
        assert clause in LEADERBOARD_WHERE


@pytest.mark.asyncio
async def test_patch_me_updates_only_the_fields_sent():
    row = {"id": "11111111-1111-1111-1111-111111111111"}
    fake_update = AsyncMock(return_value=row)
    with patch.object(users_api, "update_user_profile", fake_update), \
         patch.object(users_api, "_row_to_profile", lambda r: r):
        await users_api.update_me(
            UpdateProfileRequest(leaderboard_hidden=True), row=row, conn=AsyncMock()
        )
    kwargs = fake_update.call_args.kwargs
    assert kwargs == {"leaderboard_hidden": True}


@pytest.mark.asyncio
async def test_patch_me_language_does_not_clear_other_fields():
    row = {"id": "11111111-1111-1111-1111-111111111111"}
    fake_update = AsyncMock(return_value=row)
    with patch.object(users_api, "update_user_profile", fake_update), \
         patch.object(users_api, "_row_to_profile", lambda r: r):
        await users_api.update_me(
            UpdateProfileRequest(language_preference="si"), row=row, conn=AsyncMock()
        )
    assert fake_update.call_args.kwargs == {"language_preference": "si"}
