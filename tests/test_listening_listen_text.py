"""D-08: listening questions no longer print the heard line on screen."""

import importlib.util
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

_PATH = Path(__file__).parent.parent / "alembic" / "versions" / "0058_listening_listen_text.py"
_spec = importlib.util.spec_from_file_location("m0058", _PATH)
m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m)


@pytest.mark.parametrize(
    "prompt,expected",
    [
        ("My name is Kamal. What is his name?", ("My name is Kamal.", "What is his name?")),
        ("I am a student. What is Kamal?", ("I am a student.", "What is Kamal?")),
        ("I am from Sri Lanka. Where is Kamal from?", ("I am from Sri Lanka.", "Where is Kamal from?")),
        ("Anna says: 'I like tea.' Who likes tea?", ("Anna says: I like tea.", "Who likes tea?")),
        ("'There is medicine in the box.' Where is the medicine?",
         ("There is medicine in the box.", "Where is the medicine?")),
        ("'Where are your shoes?' — choose the correct answer.",
         ("Where are your shoes?", "Choose the correct answer.")),
        # Nothing heard: leave alone
        ("Who likes juice?", None),
        ("What time does he wake up?", None),
        ("The book is ______ the cupboard.", None),
        ("Put the morning routine in order.", None),
        # A claim to judge, not audio
        ("Tom likes pizza very much. True or False?", None),
        ("", None),
    ],
)
def test_split_listening_prompt(prompt, expected):
    assert m.split_listening_prompt(prompt) == expected


def _run_upgrade(rows):
    bind = MagicMock()
    bind.execute.return_value.mappings.return_value.all.return_value = rows
    with patch.object(m.op, "get_bind", return_value=bind):
        m.upgrade()
    return [c.args[1] for c in bind.execute.call_args_list[1:]]


def test_upgrade_moves_heard_line_into_listen_text():
    updates = _run_upgrade([{
        "id": "q1", "type": "mcq_single",
        "prompt_text": "My name is Kamal. What is his name?",
        "payload": {"correct_option_id": "b"}, "translations": {},
    }])
    assert len(updates) == 1
    u = updates[0]
    assert u["ask"] == "What is his name?"
    payload = json.loads(u["payload"])
    assert payload["listen_text"] == "My name is Kamal."
    assert payload["original_prompt_text"] == "My name is Kamal. What is his name?"
    assert payload["correct_option_id"] == "b"


def test_upgrade_skips_questions_without_heard_part():
    assert _run_upgrade([{
        "id": "q2", "type": "mcq_single", "prompt_text": "Who likes juice?",
        "payload": {}, "translations": {},
    }]) == []


def test_downgrade_restores_original_text():
    bind = MagicMock()
    bind.execute.return_value.mappings.return_value.all.return_value = [{
        "id": "q1",
        "payload": {"listen_text": "My name is Kamal.",
                    "original_prompt_text": "My name is Kamal. What is his name?", "x": 1},
        "translations": {},
    }]
    with patch.object(m.op, "get_bind", return_value=bind):
        m.downgrade()
    params = bind.execute.call_args_list[1].args[1]
    assert params["p"] == "My name is Kamal. What is his name?"
    assert json.loads(params["payload"]) == {"x": 1}
