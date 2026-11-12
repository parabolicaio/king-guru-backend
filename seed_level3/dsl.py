"""Small helpers for writing Level 3 lesson content as data.

Each helper returns a plain dict ("item"). A lesson is a dict of section
category -> list of items, in the order the learner meets them. build.py
turns items into content_block / vocabulary_word / question rows.

Kinds:
  heading, plain, passage, phrases, examples, qa, summary, self_check,
  words                      -> content (shown, not graded)
  mcq, tf, fbo, typed, open, match, cat, order, write, speak
                             -> questions (graded)

`review=True` on any question marks an answer key or model answer written
by the King Guru team, not the lesson authors, for the experts to check.
"""
from __future__ import annotations


# ── content ──────────────────────────────────────────────────────────────────

def heading(text: str) -> dict:
    return {"kind": "heading", "text": text}


def plain(text: str) -> dict:
    return {"kind": "plain", "text": text}


def passage(title: str, text: str, summary_si: str | None = None) -> dict:
    """A reading passage. The app shows it above each question after it."""
    return {"kind": "passage", "title": title, "text": text, "summary_si": summary_si}


def words(title: str, pairs: list[tuple[str, str]], meanings: dict[str, str] | None = None) -> dict:
    """Vocabulary words with Sinhala, shown as word cards. `meanings` gives an
    English definition where the lesson has one (from its matching task)."""
    return {"kind": "words", "title": title, "pairs": pairs, "meanings": meanings or {}}


def phrases(title: str | None, items: list, ) -> dict:
    """Phrase cards with a play button. Items are 'text' or ('text', 'note')."""
    return {"kind": "phrases", "title": title,
            "items": [i if isinstance(i, tuple) else (i, None) for i in items]}


def examples(label: str, sentences: list[str]) -> dict:
    return {"kind": "examples", "label": label, "sentences": sentences}


def qa(question: str, answer: str) -> dict:
    return {"kind": "qa", "question": question, "answer": answer}


def summary(items: list[str]) -> dict:
    return {"kind": "summary", "items": items}


def self_check(text: str, prompt: str = "Can you do this?") -> dict:
    return {"kind": "self_check", "prompt": prompt, "text": text}


# ── questions ────────────────────────────────────────────────────────────────

def mcq(prompt: str, options: list[str], answer: str, *, listen: str | None = None,
        review: bool = False, fb: tuple[str, str] | None = None) -> dict:
    """Multiple choice. `answer` is the text of the right option."""
    return {"kind": "mcq", "prompt": prompt, "options": options, "answer": answer,
            "listen": listen, "review": review, "fb": fb}


def tf(prompt: str, answer: bool, *, listen: str | None = None, review: bool = False) -> dict:
    return {"kind": "tf", "prompt": prompt, "answer": answer, "listen": listen, "review": review}


def fbo(sentence: str, options: list[str], answer: str, *, listen: str | None = None,
        review: bool = False) -> dict:
    """Fill the blank by choosing an option. `sentence` contains ______."""
    return {"kind": "fbo", "prompt": sentence, "options": options, "answer": answer,
            "listen": listen, "review": review}


def typed(prompt: str, accepted: list[str], *, listen: str | None = None, review: bool = False) -> dict:
    """Type the answer; any of `accepted` is right (case and punctuation ignored)."""
    return {"kind": "typed", "prompt": prompt, "accepted": accepted, "listen": listen, "review": review}


def open_answer(prompt: str, example: str | None = None, *, listen: str | None = None) -> dict:
    """Type your own answer; any real answer is right (accept_any, D-72)."""
    return {"kind": "open", "prompt": prompt, "example": example, "listen": listen}


def match(prompt: str, pairs: list[tuple[str, str]], *, review: bool = False) -> dict:
    return {"kind": "match", "prompt": prompt, "pairs": pairs, "review": review}


def cat(prompt: str, groups: dict[str, list[str]], *, review: bool = False) -> dict:
    """Sort items into groups. `groups` maps group label -> its items."""
    return {"kind": "cat", "prompt": prompt, "groups": groups, "review": review}


def order(prompt: str, items_in_order: list[str], *, review: bool = False) -> dict:
    """Put items in order. Give them in the right order; they are shuffled."""
    return {"kind": "order", "prompt": prompt, "items": items_in_order, "review": review}


def write(prompt: str, starters: list[str], *, min_words: int = 3,
          models: list[str] | None = None, review: bool = False, listen: str | None = None) -> dict:
    """Guided writing, scored on completion. One box per starter (a sentence
    to complete or a task). `models` are model answers shown afterwards."""
    return {"kind": "write", "prompt": prompt, "starters": starters, "min_words": min_words,
            "models": models, "review": review, "listen": listen}


def speak(prompt: str, target: str, *, seconds: int = 30, review: bool = False) -> dict:
    """Recorded speaking, graded on saying `target` (a phrase, or a model
    answer for an open question)."""
    return {"kind": "speak", "prompt": prompt, "target": target, "seconds": seconds, "review": review}


def interview(intro: str, questions_and_models: list[tuple[str, str]], *,
              expressions: list[str] | None = None, vocabulary: list[str] | None = None,
              review: bool = True) -> list[dict]:
    """App-as-interviewer: the intro, useful expressions / key words, then one
    recorded question per (question, model answer). Model answers were
    written by the King Guru team, so review defaults to True."""
    out: list[dict] = [plain(intro)]
    if expressions:
        out.append(examples("Useful expressions", expressions))
    if vocabulary:
        out.append(examples("Key vocabulary", [" • ".join(vocabulary)]))
    for q, model in questions_and_models:
        out.append(speak(f"Answer out loud: {q}", model, seconds=45, review=review))
    return out


QUESTION_KINDS = {"mcq", "tf", "fbo", "typed", "open", "match", "cat", "order", "write", "speak"}


# Follow-up Part D: how the app shows a "Discuss ..." instruction (no partner).
DISCUSS = "Think about these questions, then record your answer or write it in full sentences."
