"""Turn a Level 3 lesson spec (see dsl.py) into rows to insert.

Pure functions, no database, so tests can check every question scores.

build_lesson(spec) -> list of sections:
  {"category", "display_order", "title", "rows": [row, ...]}
Rows, in display order within their section:
  {"t": "block", "block_type", "order", "payload"}
  {"t": "word", "order", "word", "definition", "si"}   (+ a word_card block)
  {"t": "question", "order", "type", "prompt", "payload", "xp"}
"""
from __future__ import annotations

from .dsl import QUESTION_KINDS

SECTIONS = [
    ("vocabulary", "Vocabulary"),
    ("grammar", "Grammar"),
    ("pronunciation", "Pronunciation"),
    ("listening", "Listening"),
    ("reading", "Reading"),
    ("speaking", "Speaking"),
    ("writing", "Writing"),
]

XP = {"mcq": 5, "tf": 5, "fbo": 5, "typed": 5, "open": 5, "match": 8, "cat": 8,
      "order": 8, "write": 10, "speak": 15}


def _shift(key: str, n: int) -> int:
    return sum(map(ord, key)) % n if n else 0


def place(prompt: str, options: list[str], answer: str) -> tuple[list[dict], str]:
    """Options with ids a, b, c... in a stable order where the right one is
    not always first. Returns (options, correct id)."""
    if answer not in options:
        raise ValueError(f"answer {answer!r} not in options for {prompt!r}")
    s = _shift(prompt, len(options))
    ordered = options[s:] + options[:s]
    opts = [{"id": chr(ord("a") + i), "text": t} for i, t in enumerate(ordered)]
    return opts, opts[ordered.index(answer)]["id"]


def _feedback(item: dict, right_text: str | None) -> dict:
    if item.get("fb"):
        c, w = item["fb"]
        return {"correct": c, "incorrect": w}
    if right_text:
        return {"correct": "Correct!", "incorrect": f"The answer is: {right_text}"}
    return {"correct": "Well done!", "incorrect": "Have another look and try again."}


def _question(item: dict) -> tuple[str, str, dict]:
    """(question type, prompt text, payload) for a question item."""
    kind = item["kind"]
    prompt = item["prompt"]
    payload: dict
    if kind in ("mcq", "fbo"):
        opts, cid = place(prompt, item["options"], item["answer"])
        qtype = "mcq_single" if kind == "mcq" else "fill_blank_options"
        payload = {"options": opts, "correct_option_id": cid, "feedback": _feedback(item, item["answer"])}
        if kind == "fbo":
            payload["sentence_with_blank"] = prompt
    elif kind == "tf":
        qtype = "true_false"
        payload = {"correct_answer": bool(item["answer"]),
                   "feedback": _feedback(item, "True" if item["answer"] else "False")}
    elif kind == "typed":
        qtype = "fill_blank_typed"
        payload = {"accepted_answers": item["accepted"], "feedback": _feedback(item, item["accepted"][0])}
    elif kind == "open":
        qtype = "fill_blank_typed"
        payload = {"accepted_answers": [], "accept_any": True,
                   "feedback": {"correct": "Good answer!" + (f" For example: {item['example']}" if item.get("example") else ""),
                                "incorrect": "Write a real answer of your own."}}
    elif kind == "match":
        qtype = "match_pairs"
        pairs = [{"id": f"p{i + 1}", "left": l, "right": r} for i, (l, r) in enumerate(item["pairs"])]
        payload = {"pairs": pairs, "display_shuffle": True,
                   "feedback": {"correct": "Well done!", "incorrect": "Have another look at each pair."}}
    elif kind == "cat":
        qtype = "categorization"
        cats, items = [], []
        n = 0
        for ci, (label, members) in enumerate(item["groups"].items()):
            cats.append({"id": f"c{ci + 1}", "label": label})
            for m in members:
                n += 1
                items.append({"id": f"i{n}", "text": m, "category_id": f"c{ci + 1}"})
        s = _shift(prompt, len(items))
        items = items[s:] + items[:s]
        payload = {"categories": cats, "items": items,
                   "feedback": {"correct": "Well done!", "incorrect": "Have another look at each group."}}
    elif kind == "order":
        qtype = "order_events"
        ids = [{"id": f"e{i + 1}", "text": t} for i, t in enumerate(item["items"])]
        correct = [e["id"] for e in ids]
        # Shown shuffled: reversed then rotated, so never already in order.
        shown = list(reversed(ids))
        s = _shift(prompt, len(shown))
        shown = shown[s:] + shown[:s]
        if [e["id"] for e in shown] == correct and len(shown) > 1:
            shown = shown[1:] + shown[:1]
        payload = {"items": shown, "correct_order": correct,
                   "feedback": {"correct": "Well done!",
                                "incorrect": "The right order is: " + " → ".join(item["items"])}}
    elif kind == "write":
        qtype = "guided_writing"
        models = item.get("models") or []
        prompts = [{"id": f"w{i + 1}", "starter": s,
                    **({"model_answer": models[i]} if i < len(models) and models[i] else {})}
                   for i, s in enumerate(item["starters"])]
        payload = {"prompts": prompts, "min_words": item["min_words"],
                   "feedback": {"correct": "Well done! Compare yours with the model answers.",
                                "incorrect": f"Write at least {item['min_words']} words in each box."}}
    elif kind == "speak":
        qtype = "pronunciation_practice"
        payload = {"target_text": item["target"], "show_text_before_record": True,
                   "max_duration_seconds": item["seconds"],
                   "feedback": {"correct": "Great speaking!",
                                "incorrect": "Try again — speak slowly and clearly."}}
    else:  # pragma: no cover
        raise ValueError(kind)
    if item.get("listen"):
        payload["listen_text"] = item["listen"]
    if item.get("review"):
        payload["needs_expert_review"] = True
    return qtype, prompt, payload


def _rows(items: list[dict]) -> list[dict]:
    rows: list[dict] = []
    order = 0

    def nxt() -> int:
        nonlocal order
        order += 1
        return order - 1

    for item in items:
        kind = item["kind"]
        if kind in QUESTION_KINDS:
            qtype, prompt, payload = _question(item)
            rows.append({"t": "question", "order": nxt(), "type": qtype, "prompt": prompt,
                         "payload": payload, "xp": XP[kind]})
        elif kind == "heading":
            rows.append({"t": "block", "block_type": "text", "order": nxt(),
                         "payload": {"type": "heading", "text": item["text"]}})
        elif kind == "plain":
            rows.append({"t": "block", "block_type": "text", "order": nxt(),
                         "payload": {"type": "plain", "text": item["text"]}})
        elif kind == "passage":
            rows.append({"t": "block", "block_type": "text", "order": nxt(),
                         "payload": {"type": "plain", "role": "passage", "title": item["title"],
                                     "text": item["text"]}})
            if item.get("summary_si"):
                rows.append({"t": "block", "block_type": "text", "order": nxt(),
                             "payload": {"type": "plain", "role": "summary_si",
                                         "text": "Sinhala summary\n" + item["summary_si"]}})
        elif kind == "words":
            rows.append({"t": "block", "block_type": "text", "order": nxt(),
                         "payload": {"type": "heading", "text": item["title"]}})
            for w, si in item["pairs"]:
                rows.append({"t": "word", "order": nxt(), "word": w,
                             "definition": item["meanings"].get(w, ""), "si": si})
        elif kind == "phrases":
            if item.get("title"):
                rows.append({"t": "block", "block_type": "text", "order": nxt(),
                             "payload": {"type": "heading", "text": item["title"]}})
            for text, note in item["items"]:
                rows.append({"t": "block", "block_type": "text", "order": nxt(),
                             "payload": {"type": "phrase_card", "text": text, "note": note}})
        elif kind == "examples":
            rows.append({"t": "block", "block_type": "text", "order": nxt(),
                         "payload": {"type": "example_cards", "label": item["label"],
                                     "sentences": item["sentences"]}})
        elif kind == "qa":
            rows.append({"t": "block", "block_type": "text", "order": nxt(),
                         "payload": {"type": "qa_pair", "question": item["question"], "answer": item["answer"]}})
        elif kind == "summary":
            rows.append({"t": "block", "block_type": "text", "order": nxt(),
                         "payload": {"type": "summary", "items": item["items"]}})
        elif kind == "self_check":
            rows.append({"t": "block", "block_type": "self_check", "order": nxt(),
                         "payload": {"prompt": item["prompt"], "text": item["text"]}})
        else:  # pragma: no cover
            raise ValueError(kind)
    return rows


def build_lesson(spec: dict) -> list[dict]:
    out = []
    for i, (category, title) in enumerate(SECTIONS):
        items = spec["sections"].get(category) or []
        if not items:
            continue
        out.append({"category": category, "display_order": i + 1, "title": title, "rows": _rows(items)})
    return out
