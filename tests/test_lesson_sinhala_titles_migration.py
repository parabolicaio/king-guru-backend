"""D-38: Sinhala lesson titles and Level 1 objectives (migration 0061)."""

import ast
import importlib.util
import re
from pathlib import Path

import pytest

_VERSIONS = Path(__file__).parent.parent / "alembic" / "versions"


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, _VERSIONS / filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


m = _load("m0061", "0061_lesson_sinhala_titles_objectives.py")
m60 = _load("m0060", "0060_lesson_objectives_from_intro.py")


def _seed_file(prefix: str) -> str:
    (path,) = _VERSIONS.glob(f"{prefix}_*.py")
    return path.read_text(encoding="utf-8")


def _constant(prefix: str, name: str):
    tree = ast.parse(_seed_file(prefix))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise AssertionError(f"{name} not found in {prefix}")


def _intro_card(prefix: str, needle: str) -> str:
    """The 'By the end of this lesson' string literal from a seed file."""
    tree = ast.parse(_seed_file(prefix))
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and needle in node.value:
            # Drop a markdown heading such as "## Lesson Objectives".
            return node.value[node.value.index(needle):]
    raise AssertionError(f"intro card not found in {prefix}")


# Every seeded Level 1 and Level 2 lesson title has a Sinhala title.
SEEDED_TITLES = {
    "0020": "Greetings & Introductions",
    "0016": "Numbers, Time & Daily Routines",
    "0017": "Classroom & Everyday Objects",
    "0018": "Colors, Clothing & Adjectives",
    "0025": "Food, Drinks & Preferences",
    "0026": "My Home & Prepositions of Place",
    "0027": "Health, Body & Feelings",
    "0028": "Animals, Pets & Abilities",
    "0029": "My Town & Community",
    "0030": "Daily Routines & Frequency",
    "0031": "My Neighborhood & Directions",
    "0032": "Past Simple (Regular Verbs)",
    "0033": "Past Simple (Irregular Verbs & Memories)",
    "0034": "Food, Shopping & Quantifiers",
    "0035": "Health, Body & Feelings",
    "0036": "Weather & Seasons",
    "0037": "Future Plans (Going To)",
    "0038": "Travel, Transport & Experiences",
    "0039": "Work, Technology & Communication",
}


@pytest.mark.parametrize("prefix,title", SEEDED_TITLES.items())
def test_seeded_title_has_sinhala(prefix, title):
    assert f'"{title}"' in _seed_file(prefix)
    assert m.TITLES_SI[title].strip()


def test_lesson2_title_has_sinhala():
    assert "'Family and Describing People'" in _seed_file("0002_seed")
    assert m.TITLES_SI["Family and Describing People"].strip()


def test_all_twenty_lessons_covered():
    # 19 distinct titles: "Health, Body & Feelings" is used in both levels.
    assert len(m.TITLES_SI) == 19
    assert len(m.LEVEL1_OBJECTIVES) == 10


@pytest.mark.parametrize("prefix,title", [
    ("0025", "Food, Drinks & Preferences"),
    ("0026", "My Home & Prepositions of Place"),
    ("0027", "Health, Body & Feelings"),
    ("0028", "Animals, Pets & Abilities"),
    ("0029", "My Town & Community"),
])
def test_level1_objectives_match_seed_lists(prefix, title):
    assert [e for e, _ in m.LEVEL1_OBJECTIVES[title]] == _constant(prefix, "OBJECTIVES")


def test_lesson1_objectives_match_what_0060_parsed():
    card = _intro_card("0020", "By the end of this lesson")
    assert [e for e, _ in m.LEVEL1_OBJECTIVES["Greetings & Introductions"]] == m60.parse_objectives(card)


@pytest.mark.parametrize("prefix,title", [
    ("0016", "Numbers, Time & Daily Routines"),
    ("0017", "Classroom & Everyday Objects"),
    ("0018", "Colors, Clothing & Adjectives"),
])
def test_markdown_card_objectives_match(prefix, title):
    card = _intro_card(prefix, "By the end of this lesson")
    assert [e for e, _ in m.LEVEL1_OBJECTIVES[title]] == m60.parse_objectives(card)


def test_lesson2_markdown_card_objectives_match():
    src = _seed_file("0002_seed")
    match = re.search(r'_l2_obj_md = \((.*?)\n    \)', src, re.S)
    card = ast.literal_eval("(" + match.group(1) + ")")
    card = card.split("\n\n", 1)[1] if card.startswith("##") else card
    assert [e for e, _ in m.LEVEL1_OBJECTIVES["Family and Describing People"]] == m60.parse_objectives(card)


def test_every_objective_has_sinhala():
    for pairs in m.LEVEL1_OBJECTIVES.values():
        for en, si in pairs:
            assert en.strip() and si.strip()
            assert re.search(r"[඀-෿]", si), si


# ── plan_update ──────────────────────────────────────────────────────────────

def test_fills_title_and_empty_objectives():
    title = "Classroom & Everyday Objects"
    changes = m.plan_update(title, {}, [], {})
    en = [e for e, _ in m.LEVEL1_OBJECTIVES[title]]
    assert changes["translations"] == {"si": {"title": m.TITLES_SI[title]}}
    assert changes["objectives"] == en
    assert changes["objectives_translations"]["si"] == [s for _, s in m.LEVEL1_OBJECTIVES[title]]


def test_keeps_other_translation_fields():
    changes = m.plan_update("Weather & Seasons", {"si": {"description": "x"}, "ta": {"title": "y"}}, [], {})
    assert changes["translations"] == {
        "si": {"description": "x", "title": m.TITLES_SI["Weather & Seasons"]},
        "ta": {"title": "y"},
    }
    assert "objectives" not in changes  # Level 2 objectives are not touched


def test_does_not_overwrite_existing_sinhala():
    title = "My Town & Community"
    en = [e for e, _ in m.LEVEL1_OBJECTIVES[title]]
    changes = m.plan_update(title, {"si": {"title": "edited"}}, en, {"si": ["edited"]})
    assert changes == {}


def test_edited_english_objectives_get_no_sinhala():
    changes = m.plan_update("My Town & Community", {"si": {"title": "t"}}, ["Something new"], {})
    assert changes == {}


def test_accepts_json_strings():
    changes = m.plan_update("Weather & Seasons", '{"si": {}}', "[]", "{}")
    assert changes["translations"]["si"]["title"] == m.TITLES_SI["Weather & Seasons"]


def test_unknown_title_untouched():
    assert m.plan_update("Some Other Lesson", {}, [], {}) == {}
