"""D-77: Lesson 2's chips/correct_sequence sentence builder is converted."""

import importlib.util
from pathlib import Path

from app.services.scoring import score

_p = Path(__file__).parent.parent / "alembic" / "versions" / "0062_sentence_builder_chips_payload.py"
_s = importlib.util.spec_from_file_location("m0062", _p)
m = importlib.util.module_from_spec(_s)
_s.loader.exec_module(m)

LESSON2 = {
    "chips": [{"id": "c1", "text": "She"}, {"id": "c2", "text": "is"},
              {"id": "c3", "text": "my"}, {"id": "c4", "text": "sister."},
              {"id": "c5", "text": "He"}, {"id": "c6", "text": "your"}],
    "correct_sequence": ["c1", "c2", "c3", "c4"],
    "feedback": {"correct": "Well done!", "incorrect": "She is my sister."},
}


def test_lesson2_payload():
    out = m.convert(LESSON2)
    assert out["items"] == [{"id": "c1", "text": "She"}, {"id": "c2", "text": "is"},
                            {"id": "c3", "text": "my"}, {"id": "c4", "text": "sister."}]
    assert out["distractors"] == [{"id": "c5", "text": "He"}, {"id": "c6", "text": "your"}]
    assert out["correct_order"] == ["c1", "c2", "c3", "c4"]
    assert out["feedback"] == LESSON2["feedback"]


def test_unknown_ids_in_sequence_are_dropped():
    out = m.convert({"chips": [{"id": "a", "text": "Hi"}], "correct_sequence": ["a", "zz"]})
    assert out["correct_order"] == ["a"]


def test_converted_payload_scores():
    out = m.convert(LESSON2)
    assert score("sentence_builder", out, {"order": ["c1", "c2", "c3", "c4"]}).is_correct
    assert not score("sentence_builder", out, {"order": ["c5", "c2", "c3", "c4"]}).is_correct
