"""D-78: Lessons 2-5 get Pronunciation, Listening, Reading, Speaking, Writing."""

import importlib.util
import sys
from pathlib import Path

import pytest

from app.services.scoring import correct_answer_for, score

_VERSIONS = Path(__file__).parent.parent / "alembic" / "versions"
sys.path.insert(0, str(_VERSIONS.parent.parent))  # seed_helpers
_s = importlib.util.spec_from_file_location("m0063", _VERSIONS / "0063_lessons_2_to_5_skill_sections.py")
m = importlib.util.module_from_spec(_s)
_s.loader.exec_module(m)


@pytest.fixture
def captured(monkeypatch):
    rows = {"blocks": [], "questions": []}
    monkeypatch.setattr(m, "insert_content_block",
                        lambda sec, bt, d, payload, _id: rows["blocks"].append((sec, bt, d, payload)))
    monkeypatch.setattr(m, "insert_question",
                        lambda sec, qt, purpose, d, prompt, payload, xp, _id:
                        rows["questions"].append((sec, qt, d, prompt, payload)))
    return rows


def _seed_all(rows):
    for order, spec in m.LESSONS.items():
        for category, _, _ in m._SECTIONS:
            key, seeder = m._SEEDERS[category]
            seeder(f"{order}-{category}", spec[key])
    return rows


def test_four_lessons_five_sections_each():
    assert sorted(m.LESSONS) == [2, 3, 4, 5]
    assert [c for c, _, _ in m._SECTIONS] == ["pronunciation", "listening", "reading", "speaking", "writing"]
    for spec in m.LESSONS.values():
        assert set(spec) == {"pron", "listen", "read", "speak", "write"}


def test_every_section_gets_content(captured):
    rows = _seed_all(captured)
    used = {sec for sec, *_ in rows["blocks"]} | {sec for sec, *_ in rows["questions"]}
    expected = {f"{o}-{c}" for o in m.LESSONS for c, _, _ in m._SECTIONS}
    assert used == expected


def test_display_orders_are_unique_per_section(captured):
    rows = _seed_all(captured)
    seen = {}
    for sec, _, d, *_ in rows["blocks"]:
        seen.setdefault(sec, []).append(d)
    for sec, _, d, *_ in rows["questions"]:
        seen.setdefault(sec, []).append(d)
    for sec, orders in seen.items():
        assert len(orders) == len(set(orders)), sec


def _right_response(qtype, payload):
    if qtype in ("mcq_single", "fill_blank_options"):
        return {"selected_option_id": payload["correct_option_id"]}
    if qtype == "true_false":
        return {"answer": payload["correct_answer"]}
    if qtype == "fill_blank_typed":
        return {"answer": payload["accepted_answers"][0]}
    if qtype == "sentence_builder":
        return {"order": payload["correct_order"]}
    return None


def test_every_question_has_a_scorable_right_answer(captured):
    rows = _seed_all(captured)
    checked = 0
    for _, qtype, _, prompt, payload in rows["questions"]:
        if qtype == "pronunciation_practice":
            assert payload["target_text"].strip()
            continue
        if qtype != "sentence_builder":
            assert correct_answer_for(qtype, payload) is not None, prompt
        assert score(qtype, payload, _right_response(qtype, payload)).is_correct, prompt
        checked += 1
    assert checked > 60


def test_option_ids_are_valid_and_answer_not_always_first(captured):
    rows = _seed_all(captured)
    firsts = 0
    total = 0
    for _, qtype, _, prompt, payload in rows["questions"]:
        if qtype in ("mcq_single", "fill_blank_options"):
            ids = [o["id"] for o in payload["options"]]
            assert payload["correct_option_id"] in ids, prompt
            total += 1
            firsts += payload["correct_option_id"] == ids[0]
    assert 0 < firsts < total


def test_place_options_keeps_the_answer():
    opts, correct = m.place_options("Who is twelve?", ["Kasun", "Ajith"], 0)
    assert {o["text"] for o in opts} == {"Kasun", "Ajith"}
    assert next(o["text"] for o in opts if o["id"] == correct) == "Kasun"
