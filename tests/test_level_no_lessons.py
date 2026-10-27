"""D-16: levels with no lessons can't be bought."""

from unittest.mock import AsyncMock, patch

import pytest

from app.core.errors import AppError
from app.services import card_service, payment_service


def _level(lessons: int) -> dict:
    return {"id": "lvl", "payment_required": True, "price_amount": 1000,
            "price_currency": "LKR", "lesson_count": lessons}


@pytest.mark.asyncio
async def test_checkout_refuses_level_without_lessons():
    with patch.object(payment_service, "get_level_by_id", AsyncMock(return_value=_level(0))):
        with pytest.raises(AppError) as e:
            await payment_service.start_checkout(AsyncMock(), {"id": "u"}, "lvl")
    assert e.value.detail["code"] == "LEVEL_NO_LESSONS"
    assert e.value.status_code == 409


@pytest.mark.asyncio
async def test_saved_card_refuses_level_without_lessons():
    card = {"user_id": "u", "onepay_customer_id": "c"}
    with patch.object(card_service, "get_saved_card_by_token", AsyncMock(return_value=card)), \
            patch.object(card_service, "get_level_by_id", AsyncMock(return_value=_level(0))), \
            patch.object(card_service.onepay_customer_client, "charge_card", AsyncMock()) as charge:
        with pytest.raises(AppError) as e:
            await card_service.charge_with_saved_card(AsyncMock(), {"id": "u"}, "tok", "lvl")
    assert e.value.detail["code"] == "LEVEL_NO_LESSONS"
    charge.assert_not_awaited()


def test_level_response_reports_lesson_count():
    from app.schemas.levels import LevelResponse

    assert LevelResponse.model_fields["lesson_count"].default == 0


@pytest.mark.asyncio
async def test_level_queries_count_approved_lessons():
    from app.db.queries import levels

    db = AsyncMock()
    await levels.get_all_active_levels(db)
    await levels.get_level_by_id(db, "x")
    for call in (db.fetch.call_args, db.fetchrow.call_args):
        sql = call.args[0]
        assert "AS lesson_count" in sql and "l.status = 'approved'" in sql
