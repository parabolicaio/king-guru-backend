"""D-58: finishing a section with nothing to answer (Speaking) must be able
to complete the lesson, and guest answers must count towards completion."""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from app.services.progress import ProgressResult

SECTION = str(uuid4())
LESSON = str(uuid4())
NEXT = str(uuid4())
URL = f"/api/v1/lessons/sections/{SECTION}/progress"


def _patch(row, completion=None):
    guest = MagicMock()
    guest.__getitem__.side_effect = lambda k: {"id": "guest-user-id"}[k]
    return (
        patch("app.api.v1.lessons.upsert_section_progress", AsyncMock(return_value=row)),
        patch(
            "app.api.v1.lessons.progress_service.check_lesson_completion",
            AsyncMock(return_value=completion
                      or ProgressResult(lesson_complete=False, next_lesson_id=None, xp_from_lesson=0)),
        ),
        patch("app.services.guest_service.ensure_guest_user", AsyncMock(return_value=guest)),
    )


def test_finishing_last_step_runs_completion_and_reports_unlock(test_client, mock_conn):
    mock_conn.fetchval.return_value = LESSON
    up, check, guest = _patch(
        {"furthest_step_index": 5, "total_steps": 5},
        ProgressResult(lesson_complete=True, next_lesson_id=NEXT, xp_from_lesson=20),
    )
    with up, check as c, guest:
        r = test_client.post(URL, json={"step_index": 5, "total_steps": 5},
                             headers={"X-Guest-Token": "tok"})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["lesson_complete"] is True
    assert body["next_lesson_id"] == NEXT
    c.assert_awaited_once_with(mock_conn, "guest-user-id", LESSON)


def test_mid_section_does_not_run_completion(test_client, mock_conn):
    mock_conn.fetchval.return_value = LESSON
    up, check, guest = _patch({"furthest_step_index": 2, "total_steps": 5})
    with up, check as c, guest:
        r = test_client.post(URL, json={"step_index": 2, "total_steps": 5},
                             headers={"X-Guest-Token": "tok"})
    assert r.status_code == 200, r.text
    assert r.json()["lesson_complete"] is False
    c.assert_not_awaited()


def test_unknown_section_is_404(test_client, mock_conn):
    mock_conn.fetchval.return_value = None
    r = test_client.post(URL, json={"step_index": 1, "total_steps": 1},
                         headers={"X-Guest-Token": "tok"})
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_answered_questions_include_guest_attempts():
    from app.db.queries.attempts import get_answered_assessment_question_ids

    db = AsyncMock()
    db.fetch.return_value = []
    await get_answered_assessment_question_ids(db, "u1", "l1")
    sql = db.fetch.call_args.args[0]
    assert "a.guest_token" in sql and "is_guest" in sql


@pytest.mark.asyncio
async def test_record_attempt_skips_non_assessment():
    from app.services import progress

    with patch.object(progress, "check_lesson_completion", AsyncMock()) as c:
        r = await progress.record_attempt(AsyncMock(), "u", "l", "practice")
    assert r.lesson_complete is False
    c.assert_not_awaited()
