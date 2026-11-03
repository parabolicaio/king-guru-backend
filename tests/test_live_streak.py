"""D-71: a streak shown after missed days is 0, not the stored value."""

from datetime import date

from app.services.streak import live_streak

TODAY = date(2026, 11, 4)


def test_active_today_or_yesterday_keeps_streak():
    assert live_streak(5, date(2026, 11, 4), TODAY) == 5
    assert live_streak(5, date(2026, 11, 3), TODAY) == 5


def test_missed_a_day_shows_zero():
    assert live_streak(2, date(2026, 11, 2), TODAY) == 0
    assert live_streak(2, date(2026, 10, 28), TODAY) == 0


def test_no_last_date_returns_stored():
    assert live_streak(3, None, TODAY) == 3
    assert live_streak(None, None, TODAY) == 0
