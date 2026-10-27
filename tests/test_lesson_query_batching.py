"""D-19: the lesson endpoint loads blocks, questions and vocabulary for the
whole lesson in three queries, not three per section."""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch
from uuid import uuid4

LESSON = str(uuid4())
SECTIONS = [str(uuid4()) for _ in range(7)]


def _lesson():
    return {
        "id": LESSON, "title": "Lesson 1", "description": None, "lesson_order": 1,
        "status": "approved", "thumbnail_url": None, "is_guest_accessible": True,
        "translations": {}, "objectives": [], "objectives_translations": {},
    }


def _section(i, sid):
    return {"id": sid, "category": "reading", "display_order": i, "title": f"S{i}", "translations": {}}


def _block(sid):
    return {"lesson_section_id": sid, "id": uuid4(), "block_type": "passage",
            "display_order": 1, "payload": {"text": "Hi"}, "translations": {}}


def _question(sid):
    return {"lesson_section_id": sid, "id": uuid4(), "type": "true_false", "purpose": "assessment",
            "display_order": 1, "prompt_text": "Q", "prompt_audio_url": None,
            "prompt_image_url": None, "payload": {"correct_answer": True}, "xp_value": 5,
            "hint_text": None, "vocabulary_word_id": None, "translations": {}}


def test_lesson_detail_uses_three_queries_for_seven_sections(test_client, mock_conn):
    mock_conn.fetch.side_effect = [
        [_block(SECTIONS[0])],                      # blocks for the whole lesson
        [_question(SECTIONS[0]), _question(SECTIONS[3])],  # questions
        [],                                         # vocabulary
    ]
    with patch("app.api.v1.lessons.get_lesson_for_learner", AsyncMock(return_value=_lesson())), \
            patch("app.api.v1.lessons.get_sections_for_lesson",
                  AsyncMock(return_value=[_section(i, s) for i, s in enumerate(SECTIONS)])), \
            patch("app.api.v1.lessons.get_section_category_image_map", AsyncMock(return_value={})), \
            patch("app.api.v1.lessons.get_guest_user_by_token", AsyncMock(return_value=None)), \
            patch("app.api.v1.lessons.get_latest_attempts_for_lesson", AsyncMock(return_value=[])), \
            patch("app.api.v1.lessons.get_section_progress_for_lesson", AsyncMock(return_value=[])):
        r = test_client.get(f"/api/v1/lessons/{LESSON}", headers={"X-Guest-Token": "tok"})

    assert r.status_code == 200, r.text
    assert mock_conn.fetch.await_count == 3
    sections = r.json()["lesson"]["sections"]
    assert len(sections) == 7
    assert len(sections[0]["content_blocks"]) == 1
    assert len(sections[0]["questions"]) == 1
    assert len(sections[3]["questions"]) == 1
    assert sections[1]["questions"] == [] and sections[1]["content_blocks"] == []
