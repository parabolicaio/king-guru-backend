"""D-82: the second valid answer is replaced by a clearly wrong one."""

import importlib.util
from pathlib import Path

_p = Path(__file__).parent.parent / "alembic" / "versions" / "0064_single_right_option.py"
_s = importlib.util.spec_from_file_location("m0064", _p)
m = importlib.util.module_from_spec(_s)
_s.loader.exec_module(m)


def _payload(correct="b"):
    return {"options": [{"id": "a", "text": "in"}, {"id": "b", "text": "from"}, {"id": "c", "text": "to"}],
            "correct_option_id": correct}


def test_in_becomes_at_and_answer_kept():
    out = m.swap_option(_payload(), "in", "at")
    assert [o["text"] for o in out["options"]] == ["at", "from", "to"]
    assert out["correct_option_id"] == "b"


def test_already_changed_is_none():
    assert m.swap_option({"options": [{"id": "a", "text": "at"}], "correct_option_id": "b"}, "in", "at") is None


def test_never_renames_the_right_answer():
    assert m.swap_option(_payload(correct="a"), "in", "at") is None
