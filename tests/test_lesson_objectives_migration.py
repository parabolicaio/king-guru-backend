"""D-38: lesson objectives are filled from each lesson's intro card."""

import importlib.util
from pathlib import Path

import pytest

_p = Path(__file__).parent.parent / "alembic" / "versions" / "0060_lesson_objectives_from_intro.py"
_s = importlib.util.spec_from_file_location("m0060", _p)
m = importlib.util.module_from_spec(_s)
_s.loader.exec_module(m)
parse = m.parse_objectives


def test_comma_list():
    assert parse(
        "By the end of this lesson you will be able to: greet people in English, say your "
        "name and ask for someone else's name, use am and are correctly, and introduce "
        "yourself in a few sentences."
    ) == [
        "Greet people in English",
        "Say your name and ask for someone else's name",
        "Use am and are correctly",
        "Introduce yourself in a few sentences",
    ]


def test_comma_inside_an_item_is_kept():
    assert parse(
        "By the end of this lesson you will be able to: name the rooms in a home and common "
        "furniture, and say where things are using in, on and under."
    ) == [
        "Name the rooms in a home and common furniture",
        "Say where things are using in, on and under",
    ]


def test_bullet_list_strips_markdown():
    assert parse(
        "By the end of this lesson you will be able to:\n\n- Identify common objects\n"
        "- Use **this**, **that**, **these**, and **those** correctly\n"
        "- Tell the time using *o'clock*"
    ) == [
        "Identify common objects",
        "Use this, that, these, and those correctly",
        "Tell the time using o'clock",
    ]


def test_single_sentence_without_colon():
    assert parse(
        "By the end of this lesson you will be able to talk about your daily routine using "
        "verbs, adverbs of frequency and time words."
    ) == ["Talk about your daily routine using verbs, adverbs of frequency and time words"]


@pytest.mark.parametrize("text", ["", "Greetings", "Fill in each blank with the correct word."])
def test_other_cards_are_ignored(text):
    assert parse(text) == []
