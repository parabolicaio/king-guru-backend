"""D-72: open fill-in questions accept any real answer."""

import importlib.util
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from app.services.scoring import score

OPEN = {"accepted_answers": ["Sri Lanka"], "accept_any": True}
CLOSED = {"accepted_answers": ["Sri Lanka"]}


@pytest.mark.parametrize("answer", ["Kandy", "sri lanka", "Galle", "India", "  Colombo "])
def test_open_question_accepts_any_place(answer):
    assert score("fill_blank_typed", OPEN, {"answer": answer}).is_correct


@pytest.mark.parametrize("answer", ["", "   ", ".", "1", "a"])
def test_open_question_still_needs_a_real_answer(answer):
    assert not score("fill_blank_typed", OPEN, {"answer": answer}).is_correct


def test_closed_question_unchanged():
    assert score("fill_blank_typed", CLOSED, {"answer": "Sri Lanka"}).is_correct
    assert not score("fill_blank_typed", CLOSED, {"answer": "Kandy"}).is_correct


def _migration():
    path = Path(__file__).parent.parent / "alembic" / "versions" / "0059_open_answer_questions.py"
    spec = importlib.util.spec_from_file_location("m0059", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_migration_marks_question_open_and_keeps_old_feedback():
    m = _migration()
    bind = MagicMock()
    bind.execute.return_value.mappings.return_value.all.return_value = [
        {"id": "q3", "payload": {"accepted_answers": ["Sri Lanka"], "feedback": {"correct": "old"}}}
    ]
    with patch.object(m.op, "get_bind", return_value=bind):
        m.upgrade()
    payload = json.loads(bind.execute.call_args_list[1].args[1]["p"])
    assert payload["accept_any"] is True
    assert payload["original_feedback"] == {"correct": "old"}
    assert "Kandy" in payload["feedback"]["incorrect"]
