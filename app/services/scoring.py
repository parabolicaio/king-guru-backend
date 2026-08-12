"""Scoring service — pure functions, no DB access.

Called by both the attempt engine and the placement scoring path. Covers the
Phase 1 question types plus the Task #25 Phase 3a additions `categorization`
(partial credit, match_pairs-style) and `guided_writing` (completion-scored).

Note: `categorization`/`guided_writing` are not yet in the `question.type` DB
CHECK constraint — that widening ships with the first Level 3 lesson seed that
uses them (Task #25 Phase 4), not here. These scoring cases are inert until
then, so shipping them now is safe.
"""

import re
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal


@dataclass
class ScoringResult:
    score_fraction: Decimal   # NUMERIC(3,2) — display/storage only
    score_numerator: int       # correct items
    score_denominator: int     # total items
    is_correct: bool           # score_numerator == score_denominator


def _fraction(numerator: int, denominator: int) -> Decimal:
    if denominator == 0:
        return Decimal("0.00")
    raw = Decimal(numerator) / Decimal(denominator)
    return raw.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _normalise_text(s: str) -> str:
    """OQ-1.11 normalisation for fill_blank_typed and correct_mistake."""
    s = s.strip()
    s = re.sub(r"\s+", " ", s)
    s = s.lower()
    s = re.sub(r"[^\w\s']", "", s)
    return s


def score(question_type: str, payload: dict, response: dict) -> ScoringResult:
    """Score a single attempt.

    Returns ScoringResult with score_fraction, score_numerator, score_denominator,
    and is_correct (integer comparison, not float).
    """
    match question_type:
        case "mcq_single" | "mcq_long_short_form":
            correct = (
                response.get("selected_option_id")
                == payload.get("correct_option_id")
            )
            n, d = (1, 1) if correct else (0, 1)

        case "fill_blank_options":
            correct = (
                response.get("selected_option_id")
                == payload.get("correct_option_id")
            )
            n, d = (1, 1) if correct else (0, 1)

        case "true_false":
            correct = response.get("answer") == payload.get("correct_answer")
            n, d = (1, 1) if correct else (0, 1)

        case "fill_blank_typed":
            # Lesson attempts send {"answer": ...}; placement submissions send
            # {"typed_answer": ...} (both clients, both surfaces) — accept either
            # so a client-side key choice can never silently zero a question out.
            raw_answer = response.get("answer")
            if raw_answer is None:
                raw_answer = response.get("typed_answer", "")
            user_norm = _normalise_text(str(raw_answer))
            accepted = [
                _normalise_text(a) for a in payload.get("accepted_answers", [])
            ]
            n, d = (1, 1) if user_norm in accepted else (0, 1)

        case "correct_mistake":
            raw_answer = response.get("answer")
            if raw_answer is None:
                raw_answer = response.get("typed_answer", "")
            user_norm = _normalise_text(str(raw_answer))
            accepted = [
                _normalise_text(a)
                for a in payload.get("accepted_corrections", [])
            ]
            n, d = (1, 1) if user_norm in accepted else (0, 1)

        case "match_pairs":
            pairs = payload.get("pairs", [])
            d = len(pairs)
            if d == 0:
                n = 0
            else:
                pair_map = {p["id"]: p["right"] for p in pairs}
                matches = response.get("matches", [])
                n = sum(
                    1
                    for m in matches
                    if pair_map.get(m.get("left_pair_id")) == m.get("right_pair_id")
                )

        case "order_events":
            correct_order = payload.get("correct_order", [])
            user_order = response.get("order", [])
            d = len(correct_order)
            n = sum(
                1
                for i, item in enumerate(correct_order)
                if i < len(user_order) and user_order[i] == item
            )

        case "sentence_builder":
            correct_order = payload.get("correct_order", [])
            user_order = response.get("order", [])
            d = len(correct_order)
            # Distractors are excluded from denominator; only compare correct-length prefix
            n = sum(
                1
                for i, item in enumerate(correct_order)
                if i < len(user_order) and user_order[i] == item
            )

        case "categorization":
            # Sort items into buckets. Partial credit, exactly like match_pairs:
            # each item scores iff the learner filed it under its authored
            # category. d = number of items; n = correctly-filed items.
            items = payload.get("items", [])
            d = len(items)
            if d == 0:
                n = 0
            else:
                authored = {it["id"]: it.get("category_id") for it in items}
                assignments = response.get("assignments", [])
                # Last assignment for a given item wins (defensive against a
                # client that emits an item twice); missing items score 0.
                filed: dict[str, str] = {}
                for a in assignments:
                    item_id = a.get("item_id")
                    if item_id in authored:
                        filed[item_id] = a.get("category_id")
                n = sum(
                    1
                    for item_id, cat in authored.items()
                    if filed.get(item_id) == cat
                )

        case "guided_writing":
            # Productive practice, scored on COMPLETION not correctness so it
            # rewards effort and never incurs a Gemini cost. Each prompt whose
            # response meets the min word count counts; is_correct iff all do.
            prompts = payload.get("prompts", [])
            d = len(prompts)
            if d == 0:
                n = 0
            else:
                min_words = payload.get("min_words", 1)
                prompt_ids = {p["id"] for p in prompts}
                # First non-empty response per prompt is the one scored.
                answered: dict[str, str] = {}
                for r in response.get("responses", []):
                    pid = r.get("prompt_id")
                    if pid in prompt_ids and pid not in answered:
                        answered[pid] = str(r.get("text") or "")
                n = sum(
                    1
                    for pid in prompt_ids
                    if len(answered.get(pid, "").split()) >= min_words
                )

        case _:
            # Unknown type — treat as incorrect, denominator 1
            n, d = 0, 1

    return ScoringResult(
        score_fraction=_fraction(n, d),
        score_numerator=n,
        score_denominator=d,
        is_correct=(n == d),
    )
