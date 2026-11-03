"""D-84: Speaking sections get recorded tasks from their cards."""

import importlib.util
from pathlib import Path

_p = Path(__file__).parent.parent / "alembic" / "versions" / "0065_speaking_recorded_tasks.py"
_s = importlib.util.spec_from_file_location("m0065", _p)
m = importlib.util.module_from_spec(_s)
_s.loader.exec_module(m)


def test_phrase_cards_and_qa_pairs_become_tasks():
    blocks = [
        {"type": "heading", "text": "Repeat After Me"},
        {"type": "phrase_card", "text": "I feel sick.", "note": None},
        {"type": "phrase_card", "text": "I have a headache."},
        {"type": "qa_pair", "question": "How do you feel today?", "answer": "I feel tired."},
        {"type": "plain", "text": "Speak for 60 seconds about..."},
    ]
    assert m.plan_tasks(blocks) == [
        ("Say it out loud.", "I feel sick."),
        ("Say it out loud.", "I have a headache."),
        ("Answer out loud: 'How do you feel today?'", "I feel tired."),
    ]


def test_duplicates_and_blanks_dropped_and_capped():
    blocks = [{"type": "phrase_card", "text": t} for t in
              ["Hello.", "hello.", "", "A.", "B.", "C.", "D.", "E.", "F."]]
    tasks = m.plan_tasks(blocks)
    assert [t for _, t in tasks] == ["Hello.", "A.", "B.", "C.", "D.", "E."]
    assert len(tasks) == m.MAX_TASKS


def test_no_cards_no_tasks():
    assert m.plan_tasks([{"type": "heading", "text": "x"}]) == []
