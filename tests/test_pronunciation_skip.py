"""D-17: learners without a microphone can skip a pronunciation question."""

from unittest.mock import patch

import pytest

from app.api.v1 import attempts


@pytest.mark.asyncio
async def test_skip_records_zero_without_grading_or_upload():
    q_row = {"type": "pronunciation_practice", "payload": {"target_text": "Hello"}}
    with patch("httpx.AsyncClient") as http, \
            patch("app.services.pronunciation_service.grade") as grade:
        result, feedback = await attempts._score_pronunciation(
            None, q_row, {"skipped": True, "reason": "no_mic"}, "att-1"
        )
    http.assert_not_called()
    grade.assert_not_called()
    assert result.score_numerator == 0 and result.score_denominator == 20
    assert result.is_correct is False
    assert feedback["skipped"] is True
    assert feedback["grade"] == "Skipped"
    assert "no microphone" in feedback["summary"]


@pytest.mark.asyncio
async def test_skip_summary_in_sinhala():
    q_row = {"type": "pronunciation_practice", "payload": {}}
    _, feedback = await attempts._score_pronunciation(
        None, q_row, {"skipped": True, "feedback_language": "si"}, "att-2"
    )
    assert feedback["summary"] == attempts._SKIPPED_SUMMARY["si"]


@pytest.mark.asyncio
async def test_without_skip_audio_is_still_required():
    from fastapi import HTTPException

    q_row = {"type": "pronunciation_practice", "payload": {}}
    with pytest.raises(HTTPException) as e:
        await attempts._score_pronunciation(None, q_row, {"skipped": "yes"}, "att-3")
    assert e.value.status_code == 422
