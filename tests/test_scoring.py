"""Unit tests for the pure scoring service (no DB).

Focus: the Task #25 Phase 3a additions `categorization` and `guided_writing`,
plus regression coverage on the ordering/matching families they sit beside.
"""

from decimal import Decimal

from app.services.scoring import score

# ── categorization ────────────────────────────────────────────────────────────

_CAT_PAYLOAD = {
    "categories": [{"id": "health", "label": "Health"}, {"id": "cities", "label": "Cities"}],
    "items": [
        {"id": "i1", "text": "Fitness", "category_id": "health"},
        {"id": "i2", "text": "Architecture", "category_id": "cities"},
        {"id": "i3", "text": "Diet", "category_id": "health"},
    ],
}


def test_categorization_all_correct():
    resp = {"assignments": [
        {"item_id": "i1", "category_id": "health"},
        {"item_id": "i2", "category_id": "cities"},
        {"item_id": "i3", "category_id": "health"},
    ]}
    r = score("categorization", _CAT_PAYLOAD, resp)
    assert (r.score_numerator, r.score_denominator) == (3, 3)
    assert r.is_correct is True
    assert r.score_fraction == Decimal("1.00")


def test_categorization_partial_credit():
    resp = {"assignments": [
        {"item_id": "i1", "category_id": "health"},   # correct
        {"item_id": "i2", "category_id": "health"},   # wrong
        {"item_id": "i3", "category_id": "health"},   # correct
    ]}
    r = score("categorization", _CAT_PAYLOAD, resp)
    assert (r.score_numerator, r.score_denominator) == (2, 3)
    assert r.is_correct is False


def test_categorization_missing_item_scores_zero_for_it():
    resp = {"assignments": [{"item_id": "i1", "category_id": "health"}]}
    r = score("categorization", _CAT_PAYLOAD, resp)
    assert (r.score_numerator, r.score_denominator) == (1, 3)
    assert r.is_correct is False


def test_categorization_unknown_item_ignored():
    resp = {"assignments": [
        {"item_id": "i1", "category_id": "health"},
        {"item_id": "i2", "category_id": "cities"},
        {"item_id": "i3", "category_id": "health"},
        {"item_id": "ghost", "category_id": "health"},  # not an authored item
    ]}
    r = score("categorization", _CAT_PAYLOAD, resp)
    assert (r.score_numerator, r.score_denominator) == (3, 3)
    assert r.is_correct is True


def test_categorization_empty_response():
    r = score("categorization", _CAT_PAYLOAD, {"assignments": []})
    assert (r.score_numerator, r.score_denominator) == (0, 3)
    assert r.is_correct is False


def test_categorization_no_items():
    r = score("categorization", {"items": []}, {"assignments": []})
    assert (r.score_numerator, r.score_denominator) == (0, 0)
    assert r.is_correct is True  # n == d == 0


# ── guided_writing ────────────────────────────────────────────────────────────

_GW_PAYLOAD = {
    "prompts": [
        {"id": "p1", "starter": "This year I learned…"},
        {"id": "p2", "starter": "Next I want to…"},
    ],
    "min_words": 3,
}


def test_guided_writing_all_complete():
    resp = {"responses": [
        {"prompt_id": "p1", "text": "I learned past tense"},
        {"prompt_id": "p2", "text": "study more english daily"},
    ]}
    r = score("guided_writing", _GW_PAYLOAD, resp)
    assert (r.score_numerator, r.score_denominator) == (2, 2)
    assert r.is_correct is True


def test_guided_writing_below_min_words_incomplete():
    resp = {"responses": [
        {"prompt_id": "p1", "text": "I learned lots"},   # 3 words → ok
        {"prompt_id": "p2", "text": "study"},            # 1 word → short
    ]}
    r = score("guided_writing", _GW_PAYLOAD, resp)
    assert (r.score_numerator, r.score_denominator) == (1, 2)
    assert r.is_correct is False


def test_guided_writing_default_min_words_is_one():
    payload = {"prompts": [{"id": "p1"}]}
    r = score("guided_writing", payload, {"responses": [{"prompt_id": "p1", "text": "ok"}]})
    assert r.is_correct is True


def test_guided_writing_whitespace_only_is_incomplete():
    resp = {"responses": [
        {"prompt_id": "p1", "text": "   "},
        {"prompt_id": "p2", "text": "one two three"},
    ]}
    r = score("guided_writing", _GW_PAYLOAD, resp)
    assert (r.score_numerator, r.score_denominator) == (1, 2)


def test_guided_writing_none_text_is_incomplete():
    resp = {"responses": [
        {"prompt_id": "p1", "text": None},
        {"prompt_id": "p2", "text": "one two three"},
    ]}
    r = score("guided_writing", _GW_PAYLOAD, resp)
    assert (r.score_numerator, r.score_denominator) == (1, 2)


def test_guided_writing_no_prompts():
    r = score("guided_writing", {"prompts": []}, {"responses": []})
    assert (r.score_numerator, r.score_denominator) == (0, 0)
    assert r.is_correct is True


# ── order_events regression (client renderer added in 3a; scoring unchanged) ──

def test_order_events_exact():
    payload = {"correct_order": ["e1", "e2", "e3"]}
    r = score("order_events", payload, {"order": ["e1", "e2", "e3"]})
    assert (r.score_numerator, r.score_denominator) == (3, 3)
    assert r.is_correct is True


def test_order_events_partial():
    payload = {"correct_order": ["e1", "e2", "e3"]}
    r = score("order_events", payload, {"order": ["e1", "e3", "e2"]})
    assert (r.score_numerator, r.score_denominator) == (1, 3)
    assert r.is_correct is False


def test_unknown_type_is_incorrect():
    r = score("nonexistent_type", {}, {})
    assert (r.score_numerator, r.score_denominator) == (0, 1)
    assert r.is_correct is False
