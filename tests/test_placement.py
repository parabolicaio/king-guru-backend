"""Tests for placement scoring and level selection — 100% coverage required."""

import pytest
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from app.services import placement_service
from app.services.scoring import score, ScoringResult


# ---------------------------------------------------------------------------
# scoring_service unit tests (pure functions — no DB)
# ---------------------------------------------------------------------------

class TestScoring:
    def test_mcq_single_correct(self):
        r = score("mcq_single", {"correct_option_id": "a"}, {"selected_option_id": "a"})
        assert r.is_correct is True
        assert r.score_numerator == 1
        assert r.score_denominator == 1

    def test_mcq_single_incorrect(self):
        r = score("mcq_single", {"correct_option_id": "a"}, {"selected_option_id": "b"})
        assert r.is_correct is False
        assert r.score_numerator == 0

    def test_true_false_correct(self):
        r = score("true_false", {"correct_answer": True}, {"answer": True})
        assert r.is_correct is True

    def test_true_false_incorrect(self):
        r = score("true_false", {"correct_answer": True}, {"answer": False})
        assert r.is_correct is False

    def test_fill_blank_typed_exact(self):
        r = score(
            "fill_blank_typed",
            {"accepted_answers": ["hello world"]},
            {"answer": "hello world"},
        )
        assert r.is_correct is True

    def test_fill_blank_typed_case_insensitive(self):
        r = score(
            "fill_blank_typed",
            {"accepted_answers": ["Hello World"]},
            {"answer": "hello world"},
        )
        assert r.is_correct is True

    def test_fill_blank_typed_whitespace(self):
        r = score(
            "fill_blank_typed",
            {"accepted_answers": ["hello world"]},
            {"answer": "  hello   world  "},
        )
        assert r.is_correct is True

    def test_fill_blank_typed_punctuation_stripped(self):
        r = score(
            "fill_blank_typed",
            {"accepted_answers": ["hello world"]},
            {"answer": "hello, world!"},
        )
        assert r.is_correct is True

    def test_fill_blank_typed_apostrophe_kept(self):
        r = score(
            "fill_blank_typed",
            {"accepted_answers": ["it's fine"]},
            {"answer": "it's fine"},
        )
        assert r.is_correct is True

    def test_fill_blank_typed_wrong(self):
        r = score(
            "fill_blank_typed",
            {"accepted_answers": ["cat"]},
            {"answer": "dog"},
        )
        assert r.is_correct is False

    def test_fill_blank_typed_accepts_typed_answer_key(self):
        # Regression test for the P0 bug (2026-07-20): both clients' placement
        # submission sends {"typed_answer": ...}, not {"answer": ...} — the
        # scorer must accept either key or every fill_blank_typed placement
        # question silently scores wrong for every user.
        r = score(
            "fill_blank_typed",
            {"accepted_answers": ["hello world"]},
            {"typed_answer": "hello world"},
        )
        assert r.is_correct is True

    def test_fill_blank_typed_answer_key_takes_precedence(self):
        # If a caller somehow sends both keys, "answer" (the lesson-attempt
        # contract) wins — typed_answer is the placement-only fallback.
        r = score(
            "fill_blank_typed",
            {"accepted_answers": ["cat"]},
            {"answer": "cat", "typed_answer": "dog"},
        )
        assert r.is_correct is True

    def test_correct_mistake_accepts_typed_answer_key(self):
        r = score(
            "correct_mistake",
            {"accepted_corrections": ["I am happy"]},
            {"typed_answer": "i am happy"},
        )
        assert r.is_correct is True

    def test_fill_blank_options_correct(self):
        r = score("fill_blank_options", {"correct_option_id": "x"}, {"selected_option_id": "x"})
        assert r.is_correct is True

    def test_skipped_response_is_incorrect_mcq(self):
        # Task #24 B3: the "I don't know" button submits {"skipped": true}.
        # Scoring must treat this unknown shape as incorrect, never crash.
        r = score("mcq_single", {"correct_option_id": "a"}, {"skipped": True})
        assert r.is_correct is False

    def test_skipped_response_is_incorrect_fill_blank(self):
        r = score("fill_blank_typed", {"accepted_answers": ["cat"]}, {"skipped": True})
        assert r.is_correct is False

    def test_timed_out_response_is_incorrect(self):
        # Task #24 B4: timer expiry submits {"skipped": true, "timed_out": true}.
        r = score(
            "true_false",
            {"correct_answer": True},
            {"skipped": True, "timed_out": True},
        )
        assert r.is_correct is False

    def test_correct_mistake_normalised(self):
        r = score(
            "correct_mistake",
            {"accepted_corrections": ["I am happy"]},
            {"answer": "i am happy"},
        )
        assert r.is_correct is True

    def test_match_pairs_all_correct(self):
        payload = {"pairs": [{"id": "1", "left": "a", "right": "A"}, {"id": "2", "left": "b", "right": "B"}]}
        response = {"matches": [{"left_pair_id": "1", "right_pair_id": "A"}, {"left_pair_id": "2", "right_pair_id": "B"}]}
        r = score("match_pairs", payload, response)
        assert r.is_correct is True
        assert r.score_numerator == 2
        assert r.score_denominator == 2

    def test_match_pairs_partial(self):
        payload = {"pairs": [{"id": "1", "left": "a", "right": "A"}, {"id": "2", "left": "b", "right": "B"}]}
        response = {"matches": [{"left_pair_id": "1", "right_pair_id": "A"}, {"left_pair_id": "2", "right_pair_id": "X"}]}
        r = score("match_pairs", payload, response)
        assert r.score_numerator == 1
        assert r.score_denominator == 2
        assert r.is_correct is False

    def test_match_pairs_empty(self):
        r = score("match_pairs", {"pairs": []}, {"matches": []})
        assert r.score_denominator == 0
        assert r.is_correct is True  # 0 == 0

    def test_order_events_all_correct(self):
        r = score(
            "order_events",
            {"correct_order": ["a", "b", "c"]},
            {"order": ["a", "b", "c"]},
        )
        assert r.is_correct is True
        assert r.score_numerator == 3

    def test_order_events_partial(self):
        r = score(
            "order_events",
            {"correct_order": ["a", "b", "c"]},
            {"order": ["a", "c", "b"]},
        )
        assert r.score_numerator == 1
        assert r.score_denominator == 3

    def test_sentence_builder_distractors_excluded(self):
        # correct_order has 3 items; distractors not in denominator
        r = score(
            "sentence_builder",
            {"correct_order": ["I", "am", "happy"]},
            {"order": ["I", "am", "happy"]},
        )
        assert r.is_correct is True
        assert r.score_denominator == 3

    def test_sentence_builder_partial(self):
        r = score(
            "sentence_builder",
            {"correct_order": ["I", "am", "happy"]},
            {"order": ["I", "happy", "am"]},
        )
        assert r.score_numerator == 1
        assert r.score_denominator == 3

    def test_unknown_type_is_incorrect(self):
        r = score("unknown_future_type", {}, {})
        assert r.is_correct is False
        assert r.score_denominator == 1


# ---------------------------------------------------------------------------
# placement_service.score_answers — 100% coverage
# ---------------------------------------------------------------------------

def _make_mcq_question(qid: str, correct_id: str) -> dict:
    return {
        "id": qid,
        "type": "mcq_single",
        "payload": {"correct_option_id": correct_id},
        "display_order": 1,
        "prompt_text": "Q?",
        "translations": {},
        "xp_value": 0,
        "skill_category": None,
        "difficulty": "beginner_a",
    }


def _make_tf_question(qid: str, correct: bool) -> dict:
    return {
        "id": qid,
        "type": "true_false",
        "payload": {"correct_answer": correct},
        "display_order": 1,
        "prompt_text": "Q?",
        "translations": {},
    }


@pytest.mark.asyncio
async def test_score_answers_all_correct():
    q1 = str(uuid4())
    q2 = str(uuid4())
    level_id = str(uuid4())
    mock_db = AsyncMock()
    mock_db.fetch.side_effect = [
        # get_placement_questions
        [_make_mcq_question(q1, "a"), _make_mcq_question(q2, "b")],
        # get_placement_scoring_rules
        [{"min_percent": 0, "max_percent": 100, "recommended_level_id": level_id}],
        # get_populated_level_ids — recommended level has content
        [{"level_id": level_id}],
    ]
    mock_db.fetchrow.return_value = {"code": "advanced", "is_active": True, "id": level_id}

    answers = [
        {"question_id": q1, "response": {"selected_option_id": "a"}},
        {"question_id": q2, "response": {"selected_option_id": "b"}},
    ]
    result = await placement_service.score_answers(mock_db, answers)
    assert result.correct_count == 2
    assert result.score_percent == 100.0


@pytest.mark.asyncio
async def test_score_answers_all_wrong():
    q1 = str(uuid4())
    mock_db = AsyncMock()
    level_id = str(uuid4())
    mock_db.fetch.side_effect = [
        [_make_mcq_question(q1, "a")],
        [{"min_percent": 0, "max_percent": 30, "recommended_level_id": level_id}],
        [{"level_id": level_id}],
    ]
    mock_db.fetchrow.return_value = {"code": "beginner_a", "is_active": True, "id": level_id}

    answers = [{"question_id": q1, "response": {"selected_option_id": "wrong"}}]
    result = await placement_service.score_answers(mock_db, answers)
    assert result.correct_count == 0
    assert result.score_percent == 0.0
    assert result.recommended_level_code == "beginner_a"


@pytest.mark.asyncio
async def test_score_answers_unknown_question_ignored():
    q1 = str(uuid4())
    unknown_id = str(uuid4())
    mock_db = AsyncMock()
    level_id = str(uuid4())
    mock_db.fetch.side_effect = [
        [_make_mcq_question(q1, "a")],
        [{"min_percent": 0, "max_percent": 100, "recommended_level_id": level_id}],
        [{"level_id": level_id}],
    ]
    mock_db.fetchrow.return_value = {"code": "beginner_a", "is_active": True, "id": level_id}

    answers = [
        {"question_id": q1, "response": {"selected_option_id": "a"}},
        {"question_id": unknown_id, "response": {"selected_option_id": "x"}},
    ]
    result = await placement_service.score_answers(mock_db, answers)
    # Unknown question ID must not crash; only scored question counts
    assert result.correct_count == 1


@pytest.mark.asyncio
async def test_score_answers_awards_placement_xp():
    q1 = str(uuid4())
    user_id = str(uuid4())
    level_id = str(uuid4())
    mock_db = AsyncMock()
    mock_db.fetch.side_effect = [
        [
            {
                **_make_mcq_question(q1, "a"),
                "xp_value": 10,
                "skill_category": "grammar",
                "difficulty": "easy",
            }
        ],
        [{"min_percent": 0, "max_percent": 100, "recommended_level_id": level_id}],
        [{"level_id": level_id}],
    ]
    mock_db.fetchrow.return_value = {"code": "beginner_a", "is_active": True, "id": level_id}

    with patch("app.services.xp.award", new_callable=AsyncMock) as mock_award:
        result = await placement_service.score_answers(
            mock_db,
            [{"question_id": q1, "response": {"selected_option_id": "a"}}],
            tracking_user_id=user_id,
        )
        mock_award.assert_awaited_once_with(
            mock_db,
            user_id=user_id,
            action_type="placement_question",
            xp_delta=10,
            reference_id=None,
            reference_type="placement",
        )

    assert result.xp_awarded == 10


@pytest.mark.asyncio
async def test_score_answers_boundary_30_percent():
    """Score at boundary — 30% should recommend beginner_b (min=31) or beginner_a (max=30)."""
    qs = [str(uuid4()) for _ in range(10)]
    level_a = str(uuid4())
    level_b = str(uuid4())
    mock_db = AsyncMock()
    mock_db.fetch.side_effect = [
        [_make_mcq_question(q, "a") for q in qs],
        [
            {"min_percent": 0,  "max_percent": 30,  "recommended_level_id": level_a},
            {"min_percent": 31, "max_percent": 65,  "recommended_level_id": level_b},
        ],
        [{"level_id": level_a}, {"level_id": level_b}],
    ]
    mock_db.fetchrow.return_value = {"code": "beginner_a", "is_active": True, "id": level_a}

    # 3 correct out of 10 = 30%
    answers = [
        {"question_id": qs[i], "response": {"selected_option_id": "a" if i < 3 else "wrong"}}
        for i in range(10)
    ]
    result = await placement_service.score_answers(mock_db, answers)
    assert result.score_percent == 30.0
    assert result.recommended_level_id == level_a


# ---------------------------------------------------------------------------
# Recommended-level cap — never recommend a level with zero lessons
# (Task #24 P0 ride-along: a strong scorer must not dead-end in an empty
# level, capped at the highest-scoring rule whose level actually has content)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_score_answers_caps_to_highest_populated_level():
    q1 = str(uuid4())
    level_beginner_b = str(uuid4())
    level_advanced = str(uuid4())
    mock_db = AsyncMock()
    mock_db.fetch.side_effect = [
        [_make_mcq_question(q1, "a")],
        [
            {"min_percent": 0,  "max_percent": 50,  "recommended_level_id": level_beginner_b},
            {"min_percent": 51, "max_percent": 100, "recommended_level_id": level_advanced},
        ],
        # Only beginner_b has lessons — advanced is empty content
        [{"level_id": level_beginner_b}],
    ]
    mock_db.fetchrow.return_value = {"code": "beginner_b", "is_active": True, "id": level_beginner_b}

    # 100% score naturally matches the "advanced" rule, but it must be
    # capped down to beginner_b since that's the highest populated level.
    answers = [{"question_id": q1, "response": {"selected_option_id": "a"}}]
    result = await placement_service.score_answers(mock_db, answers)
    assert result.score_percent == 100.0
    assert result.recommended_level_id == level_beginner_b


@pytest.mark.asyncio
async def test_score_answers_no_cap_when_level_populated():
    q1 = str(uuid4())
    level_advanced = str(uuid4())
    mock_db = AsyncMock()
    mock_db.fetch.side_effect = [
        [_make_mcq_question(q1, "a")],
        [{"min_percent": 0, "max_percent": 100, "recommended_level_id": level_advanced}],
        [{"level_id": level_advanced}],
    ]
    mock_db.fetchrow.return_value = {"code": "advanced", "is_active": True, "id": level_advanced}

    answers = [{"question_id": q1, "response": {"selected_option_id": "a"}}]
    result = await placement_service.score_answers(mock_db, answers)
    assert result.recommended_level_id == level_advanced


# ---------------------------------------------------------------------------
# placement_service.choose_level
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_choose_level_happy_path():
    level_id = str(uuid4())
    user_id = str(uuid4())
    lesson_id = str(uuid4())

    mock_db = AsyncMock()
    mock_db.fetchrow.side_effect = [
        # get_level_by_id
        {"id": level_id, "code": "beginner_a", "is_active": True},
        # set_user_level_and_placement
        {
            "id": user_id,
            "current_level_id": level_id,
            "placement_completed_at": __import__("datetime").datetime.utcnow(),
        },
        # get_lesson_1_for_level
        {"id": lesson_id, "lesson_order": 1, "status": "approved"},
        # get_lesson_progress — None means no existing row
        None,
    ]
    mock_db.execute = AsyncMock()

    row = await placement_service.choose_level(mock_db, user_id, level_id)
    assert str(row["current_level_id"]) == level_id


@pytest.mark.asyncio
async def test_choose_level_not_found():
    from app.core.errors import AppError
    mock_db = AsyncMock()
    mock_db.fetchrow.return_value = None  # level not found

    with pytest.raises(AppError) as exc_info:
        await placement_service.choose_level(mock_db, str(uuid4()), str(uuid4()))
    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_choose_level_not_active():
    from app.core.errors import AppError
    level_id = str(uuid4())
    mock_db = AsyncMock()
    mock_db.fetchrow.return_value = {"id": level_id, "code": "beginner_a", "is_active": False}

    with pytest.raises(AppError) as exc_info:
        await placement_service.choose_level(mock_db, str(uuid4()), level_id)
    assert exc_info.value.status_code == 400


# ---------------------------------------------------------------------------
# Endpoint integration tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_levels_public(async_client, mock_conn):
    level_id = str(uuid4())
    mock_conn.fetch.return_value = [
        {
            "id": level_id,
            "code": "beginner_a",
            "name": "Beginner A",
            "description": None,
            "display_order": 1,
            "daily_essay_enabled": False,
            "translations": {},
        }
    ]
    response = await async_client.get("/api/v1/levels")
    assert response.status_code == 200
    data = response.json()
    assert len(data["levels"]) == 1
    assert data["levels"][0]["code"] == "beginner_a"


@pytest.mark.asyncio
async def test_get_placement_questions_requires_auth(async_client):
    response = await async_client.get("/api/v1/placement/questions")
    assert response.status_code == 401
