"""Level 3 content: every lesson builds, and every question's right answer scores."""

import pytest

from app.services.scoring import score
from seed_level3 import load_lessons
from seed_level3.build import build_lesson

LESSONS = load_lessons()


def _right(qtype, p):
    if qtype in ("mcq_single", "fill_blank_options"):
        return {"selected_option_id": p["correct_option_id"]}
    if qtype == "true_false":
        return {"answer": p["correct_answer"]}
    if qtype == "fill_blank_typed":
        return {"answer": p["accepted_answers"][0] if p["accepted_answers"] else "My own answer"}
    if qtype == "match_pairs":
        return {"matches": [{"left_pair_id": x["id"], "right_pair_id": x["right"]} for x in p["pairs"]]}
    if qtype == "categorization":
        return {"assignments": [{"item_id": i["id"], "category_id": i["category_id"]} for i in p["items"]]}
    if qtype == "order_events":
        return {"order": p["correct_order"]}
    if qtype == "guided_writing":
        return {"responses": [{"prompt_id": w["id"], "text": " ".join(["word"] * p["min_words"])} for w in p["prompts"]]}
    return None


def test_lessons_present():
    assert LESSONS, "no Level 3 lessons"
    orders = [l["order"] for l in LESSONS]
    assert orders == sorted(set(orders))


@pytest.mark.parametrize("lesson", LESSONS, ids=lambda l: f"L{l['order']}")
def test_lesson_builds_and_scores(lesson):
    assert lesson["title"].strip() and lesson["objectives"]
    sections = build_lesson(lesson)
    cats = [s["category"] for s in sections]
    assert cats[0] == "vocabulary" and len(cats) == 7, cats
    for s in sections:
        orders = [r["order"] for r in s["rows"]]
        assert orders == list(range(len(orders))), s["category"]
        qs = [r for r in s["rows"] if r["t"] == "question"]
        assert qs, f"{s['category']} has no questions"
        for q in qs:
            p = q["payload"]
            if q["type"] == "pronunciation_practice":
                assert p["target_text"].strip(), q["prompt"]
                continue
            if q["type"] == "fill_blank_typed" and p.get("accept_any"):
                continue
            res = score(q["type"], p, _right(q["type"], p))
            assert res.is_correct, (s["category"], q["prompt"])


@pytest.mark.parametrize("lesson", LESSONS, ids=lambda l: f"L{l['order']}")
def test_listening_questions_carry_audio(lesson):
    listening = next(s for s in build_lesson(lesson) if s["category"] == "listening")
    graded = [r for r in listening["rows"] if r["t"] == "question"]
    assert all(r["payload"].get("listen_text") for r in graded), "listening question without audio"


@pytest.mark.parametrize("lesson", LESSONS, ids=lambda l: f"L{l['order']}")
def test_answers_not_always_first(lesson):
    firsts = total = 0
    for s in build_lesson(lesson):
        for r in s["rows"]:
            if r["t"] == "question" and r["type"] in ("mcq_single", "fill_blank_options"):
                total += 1
                firsts += r["payload"]["correct_option_id"] == "a"
    assert total == 0 or firsts < total
