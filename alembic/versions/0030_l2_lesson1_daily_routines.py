"""Beginner B — Lesson 1: Daily Routines & Frequency (Level 2 seed).

Seeds beginner_b Lesson 1 with all 7 sections from LEVEL 2 Lesson 1.docx:
  Vocabulary   — routine verbs, adverbs of frequency, time expressions
  Grammar      — present simple for routines + adverb position + Do you...?
  Pronunciation— listen & repeat phrase cards + 3 pronunciation questions
  Listening    — Nimal's routine dialogue + MCQ / TF / order questions
  Reading      — Nimal vs Saman comparison passage + comprehension
  Speaking     — guided speaking prompts, content only
  Writing      — controlled writing (sentence_builder) + typed + self_check

Text-only scope: picture/audio-select activities are deferred; audio lines are
embedded in question prompts (0020 convention). Sinhala from the .docx source.

Revision ID: 2a1b2c3d4e5f
Revises:     c6d7e8f9a0b1
Create Date: 2026-07-04
"""
import json
from typing import Sequence, Union

from alembic import op
from seed_helpers import (
    ensure_lesson,
    ensure_section,
    insert_content_block,
    insert_question,
    insert_word_card_tr,
)
from sqlalchemy import text

revision: str = "2a1b2c3d4e5f"
down_revision: Union[str, None] = "c6d7e8f9a0b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _j(obj: object) -> str:
    return "'" + json.dumps(obj, ensure_ascii=False).replace("'", "''") + "'"


OBJECTIVES = [
    "Use daily routine verbs correctly in sentences",
    "Use adverbs of frequency (always, usually, sometimes, never)",
    "Talk about your daily habits clearly",
    "Ask and answer questions about routines",
    "Understand simple spoken descriptions about daily life",
    "Speak and write about your daily routine with confidence",
]
OBJECTIVES_SI = [
    "දිනචරියා ක්‍රියාපද වාක්‍ය තුළ නිවැරදිව භාවිතා කිරීම",
    "පුරුදු පෙන්වන වචන (always, usually, sometimes, never) භාවිතා කිරීම",
    "ඔබේ දිනපතා පුරුදු පැහැදිලිව කතා කිරීම",
    "දිනචරියාව ගැන ප්‍රශ්න අසා පිළිතුරු දීම",
    "දිනචරියාව ගැන සරල කතා තේරුම් ගැනීම",
    "ඔබේ දිනචරියාව විශ්වාසයෙන් කතා කර ලිවීම",
]


def upgrade() -> None:
    from uuid6 import uuid7  # noqa: PLC0415

    bind = op.get_bind()

    row = bind.execute(text("SELECT id::text FROM level WHERE code = 'beginner_b'")).fetchone()
    assert row, "beginner_b level not found — run 0002 first"
    level_id = str(row[0])

    l_id = ensure_lesson(
        bind, level_id, 1,
        "Daily Routines & Frequency",
        "Talk about your daily habits using the present simple and adverbs of frequency.",
        str(uuid7()),
    )
    op.execute(
        f"UPDATE lesson SET objectives = {_j(OBJECTIVES)}, "
        f"objectives_translations = {_j({'si': OBJECTIVES_SI})} WHERE id = '{l_id}'"
    )

    vocab = ensure_section(bind, l_id, "vocabulary",    1, "Vocabulary",    str(uuid7()))
    gram  = ensure_section(bind, l_id, "grammar",       2, "Grammar",       str(uuid7()))
    pron  = ensure_section(bind, l_id, "pronunciation", 3, "Pronunciation", str(uuid7()))
    listn = ensure_section(bind, l_id, "listening",     4, "Listening",     str(uuid7()))
    read  = ensure_section(bind, l_id, "reading",       5, "Reading",       str(uuid7()))
    speak = ensure_section(bind, l_id, "speaking",      6, "Speaking",      str(uuid7()))
    write = ensure_section(bind, l_id, "writing",       7, "Writing",       str(uuid7()))

    # ── VOCABULARY ────────────────────────────────────────────────────────────
    insert_content_block(vocab, "text", 0, {
        "type": "plain",
        "text": ("By the end of this lesson you will be able to talk about your "
                 "daily routine using verbs, adverbs of frequency and time words."),
    }, str(uuid7()))

    insert_content_block(vocab, "text", 1, {"type": "heading", "text": "Daily Routine Verbs"}, str(uuid7()))
    verbs = [
        (2, "Wake up",         "නින්දෙන් අවදි වීම",  "Stop sleeping in the morning.", "I wake up at 6 a.m."),
        (3, "Brush teeth",     "දත් මැදීම",          "Clean your teeth.",             "I brush my teeth every morning."),
        (4, "Eat",             "ආහාර ගැනීම",         "Have food.",                    "I eat breakfast with my family."),
        (5, "Go to school",    "පාසලට යාම",          "Travel to school.",             "I go to school at 8 a.m."),
        (6, "Study",           "ඉගෙනීම",             "Learn something.",              "I study English at school."),
        (7, "Sleep",           "නිදා ගැනීම",         "Rest at night.",                "I go to sleep at 10 p.m."),
    ]
    for (d, w, si, defn, ex) in verbs:
        insert_word_card_tr(bind, vocab, d, w, defn, ex, str(uuid7()), str(uuid7()), si)

    insert_content_block(vocab, "text", 8, {"type": "heading", "text": "Adverbs of Frequency"}, str(uuid7()))
    advs = [
        (9,  "Always",    "සැමවිටම",           "Every time, 100%.",       "I always eat breakfast."),
        (10, "Usually",   "සාමාන්‍යයෙන්",      "Most of the time.",       "I usually go to school by bus."),
        (11, "Sometimes", "සමහරවිට",           "Now and then.",           "I sometimes watch TV."),
        (12, "Never",     "කිසිදා නැත",         "Not at any time, 0%.",    "I never drink coffee."),
    ]
    for (d, w, si, defn, ex) in advs:
        insert_word_card_tr(bind, vocab, d, w, defn, ex, str(uuid7()), str(uuid7()), si)

    insert_content_block(vocab, "text", 13, {"type": "heading", "text": "Time Expressions"}, str(uuid7()))
    times = [
        (14, "In the morning",   "උදේ",   "The early part of the day.", "I study in the morning."),
        (15, "In the afternoon", "දවල්",  "The middle of the day.",     "I play in the afternoon."),
        (16, "At night",         "රෑ",    "The dark part of the day.",  "I sleep at night."),
    ]
    for (d, w, si, defn, ex) in times:
        insert_word_card_tr(bind, vocab, d, w, defn, ex, str(uuid7()), str(uuid7()), si)

    insert_question(vocab, "match_pairs", "assessment", 17, "Match the word to its meaning", {
        "pairs": [
            {"id": "p1", "left": "Always",    "right": "Every time"},
            {"id": "p2", "left": "Never",     "right": "Not at any time"},
            {"id": "p3", "left": "Wake up",   "right": "Stop sleeping"},
            {"id": "p4", "left": "At night",  "right": "The dark part of the day"},
        ],
        "display_shuffle": True,
        "feedback": {"correct": "Well done!", "incorrect": "Match each word to its meaning."},
    }, 10, str(uuid7()))

    # ── GRAMMAR ───────────────────────────────────────────────────────────────
    insert_content_block(gram, "text", 0, {
        "type": "plain",
        "text": ("We use the present simple to talk about habits — things we do "
                 "every day. The adverb of frequency usually comes before the verb: "
                 "'I always wake up early.'"),
    }, str(uuid7()))
    insert_content_block(gram, "text", 1, {
        "type": "example_cards", "label": "Present Simple for Routines",
        "sentences": ["I wake up at 6 a.m.", "I go to school.", "I always wake up early."],
    }, str(uuid7()))
    insert_content_block(gram, "text", 2, {
        "type": "qa_pair", "question": "Do you exercise every day?", "answer": "Yes, I do. / No, I don't.",
    }, str(uuid7()))

    g = [
        (3, "I ______ wake up early. (100%)",
         [{"id": "a", "text": "always"}, {"id": "b", "text": "never"}], "a",
         "Correct! 'Always' means every time.",
         "100% of the time is 'always'."),
        (4, "I ______ drink coffee. (0%)",
         [{"id": "a", "text": "usually"}, {"id": "b", "text": "never"}], "b",
         "Correct! 'Never' means 0%.",
         "0% of the time is 'never'."),
        (5, "I ______ go to school by bus. (most days)",
         [{"id": "a", "text": "usually"}, {"id": "b", "text": "never"}], "a",
         "Correct! 'Usually' means most of the time.",
         "Most of the time is 'usually'."),
        (6, "Choose the correct order:",
         [{"id": "a", "text": "I always eat breakfast."}, {"id": "b", "text": "I eat always breakfast."}], "a",
         "Correct! The adverb comes before the verb.",
         "The adverb of frequency comes before the verb."),
        (7, "What ______ you usually do in the morning?",
         [{"id": "a", "text": "do"}, {"id": "b", "text": "does"}], "a",
         "Correct! With 'you' we use 'do'.",
         "With 'you' we ask with 'do'."),
        (8, "Do you exercise every day? — Yes, I ______.",
         [{"id": "a", "text": "do"}, {"id": "b", "text": "am"}], "a",
         "Correct! The short answer is 'Yes, I do.'",
         "'Do you...?' is answered with 'Yes, I do.'"),
    ]
    for (d, s, o, c, fc, fi) in g:
        insert_question(gram, "fill_blank_options", "assessment", d, s,
                        {"sentence_with_blank": s, "options": o, "correct_option_id": c,
                         "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))

    # ── PRONUNCIATION ─────────────────────────────────────────────────────────
    insert_content_block(pron, "text", 0, {"type": "heading", "text": "Listen & Repeat"}, str(uuid7()))
    for (d, ph) in [(1, "I wake up early."), (2, "I always eat breakfast."), (3, "I go to school.")]:
        insert_content_block(pron, "text", d, {"type": "phrase_card", "text": ph, "note": None}, str(uuid7()))
    insert_content_block(pron, "text", 4, {"type": "phrase_card", "text": "I ALWAYS wake up early.",
                                           "note": "Stress 'always'"}, str(uuid7()))
    pq = [
        (5, "Say the sentence. Stress 'always'.", "I always wake up early."),
        (6, "Say the two-beat words: Wake-up, Stu-dy.", "I wake up and study."),
        (7, "Say the sentence clearly.", "I always eat breakfast."),
    ]
    for (d, pr, tg) in pq:
        insert_question(pron, "pronunciation_practice", "assessment", d, pr,
                        {"target_text": tg, "show_text_before_record": True, "max_duration_seconds": 10,
                         "feedback": {"correct": "Great, that was clear!", "incorrect": "Try again, slowly."}},
                        15, str(uuid7()))

    # ── LISTENING ─────────────────────────────────────────────────────────────
    insert_content_block(listn, "text", 0, {"type": "heading", "text": "Dialogue — Nimal's Routine"}, str(uuid7()))
    insert_content_block(listn, "dialogue", 1, {
        "turns": [
            {"speaker": "Nimal", "text": "Hello! My name is Nimal."},
            {"speaker": "Nimal", "text": "I wake up at 6 a.m. every day."},
            {"speaker": "Nimal", "text": "First, I brush my teeth and take a shower."},
            {"speaker": "Nimal", "text": "Then I eat breakfast with my family."},
            {"speaker": "Nimal", "text": "I usually go to school at 8 a.m. by bus."},
            {"speaker": "Nimal", "text": "In the evening, I do my homework and sometimes watch TV."},
            {"speaker": "Nimal", "text": "At night, I go to bed at 10 p.m."},
        ],
    }, str(uuid7()))
    insert_question(listn, "mcq_single", "assessment", 2, "What time does he wake up?", {
        "options": [{"id": "a", "text": "6 a.m."}, {"id": "b", "text": "7 a.m."}],
        "correct_option_id": "a",
        "feedback": {"correct": "Correct! He wakes up at 6 a.m.", "incorrect": "He says 'I wake up at 6 a.m.'"},
    }, 5, str(uuid7()))
    insert_question(listn, "mcq_single", "assessment", 3, "How does he go to school?", {
        "options": [{"id": "a", "text": "By bus"}, {"id": "b", "text": "By car"}],
        "correct_option_id": "a",
        "feedback": {"correct": "Correct! He goes by bus.", "incorrect": "He says he goes to school by bus."},
    }, 5, str(uuid7()))
    insert_question(listn, "mcq_single", "assessment", 4, "Who does he eat breakfast with?", {
        "options": [{"id": "a", "text": "His family"}, {"id": "b", "text": "His friends"}],
        "correct_option_id": "a",
        "feedback": {"correct": "Correct! He eats with his family.", "incorrect": "He eats breakfast with his family."},
    }, 5, str(uuid7()))
    for (d, prompt, ans, fc, fi) in [
        (5, "He wakes up at 6 a.m. True or False?", True, "Correct!", "He wakes up at 6 a.m."),
        (6, "He goes to school at 9 a.m. True or False?", False, "Correct! He goes at 8 a.m.", "He goes at 8 a.m."),
        (7, "He always watches TV in the evening. True or False?", False, "Correct! Only sometimes.", "He sometimes watches TV."),
        (8, "He goes to bed at 10 p.m. True or False?", True, "Correct!", "He goes to bed at 10 p.m."),
    ]:
        insert_question(listn, "true_false", "assessment", d, prompt,
                        {"correct_answer": ans, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    insert_question(listn, "sentence_builder", "assessment", 9,
                    "Put the morning routine in order.",
                    {"items": [{"id": "c1", "text": "Wake up"}, {"id": "c2", "text": "Brush teeth"},
                               {"id": "c3", "text": "Eat breakfast"}, {"id": "c4", "text": "Go to school"}],
                     "distractors": [], "correct_order": ["c1", "c2", "c3", "c4"],
                     "feedback": {"correct": "Correct order!", "incorrect": "Wake up → Brush teeth → Eat breakfast → Go to school."}},
                    8, str(uuid7()))

    # ── READING ───────────────────────────────────────────────────────────────
    insert_content_block(read, "text", 0, {"type": "plain", "text": "Read about Nimal and Saman, then answer."}, str(uuid7()))
    insert_content_block(read, "text", 1, {
        "type": "plain",
        "text": ("Nimal: I wake up at 6 a.m. every day. First, I brush my teeth and take a shower. "
                 "Then I eat breakfast with my family. I usually go to school at 8 a.m. by bus. In the "
                 "evening, I do my homework. I sometimes watch TV or read a book. At night, I go to bed "
                 "at 10 p.m.\n\nSaman: My routine is a little different. I usually wake up at 7 a.m. I "
                 "don't always eat breakfast. I go to school by bike. After school, I play football. In "
                 "the evening, I sometimes study, but I usually watch TV. I go to bed at 11 p.m."),
    }, str(uuid7()))
    r_mcq = [
        (2, "What time does Nimal wake up?", [{"id": "a", "text": "6 a.m."}, {"id": "b", "text": "7 a.m."}], "a",
         "Correct!", "Nimal wakes up at 6 a.m."),
        (3, "How does Saman go to school?", [{"id": "a", "text": "By bike"}, {"id": "b", "text": "By bus"}], "a",
         "Correct! Saman goes by bike.", "Saman goes to school by bike."),
        (4, "Who wakes up earlier?", [{"id": "a", "text": "Nimal"}, {"id": "b", "text": "Saman"}], "a",
         "Correct! Nimal wakes up at 6 a.m.", "Nimal (6 a.m.) wakes up earlier than Saman (7 a.m.)."),
        (5, "Who goes to bed later?", [{"id": "a", "text": "Saman"}, {"id": "b", "text": "Nimal"}], "a",
         "Correct! Saman goes to bed at 11 p.m.", "Saman goes to bed at 11 p.m."),
    ]
    for (d, p, o, c, fc, fi) in r_mcq:
        insert_question(read, "mcq_single", "assessment", d, p,
                        {"options": o, "correct_option_id": c, "feedback": {"correct": fc, "incorrect": fi}},
                        5, str(uuid7()))
    for (d, p, a, fc, fi) in [
        (6, "Nimal wakes up at 6 a.m. True or False?", True, "Correct!", "Nimal wakes up at 6 a.m."),
        (7, "Saman always eats breakfast. True or False?", False, "Correct! He doesn't always.", "Saman doesn't always eat breakfast."),
        (8, "Both go to school by bus. True or False?", False, "Correct! Saman goes by bike.", "Nimal goes by bus, Saman by bike."),
    ]:
        insert_question(read, "true_false", "assessment", d, p,
                        {"correct_answer": a, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))

    # ── SPEAKING (content only) ───────────────────────────────────────────────
    insert_content_block(speak, "text", 0, {"type": "heading", "text": "Repeat After Me"}, str(uuid7()))
    for (d, ph) in [(1, "I wake up at 6 a.m."), (2, "I always eat breakfast."),
                    (3, "I brush my teeth in the morning."), (4, "I sometimes watch TV at night.")]:
        insert_content_block(speak, "text", d, {"type": "phrase_card", "text": ph, "note": None}, str(uuid7()))
    insert_content_block(speak, "text", 5, {
        "type": "plain",
        "text": ("Talk for 2 minutes about your daily routine. Include the time you wake up, your "
                 "morning activities, and your evening and night activities. Use always, usually and "
                 "sometimes."),
    }, str(uuid7()))

    # ── WRITING ───────────────────────────────────────────────────────────────
    insert_content_block(write, "text", 0, {"type": "plain",
                                            "text": "Put the words in order, then complete the sentences."}, str(uuid7()))
    builders = [
        (1, "Put in order: always / I / breakfast / eat",
         [{"id": "c1", "text": "I"}, {"id": "c2", "text": "always"}, {"id": "c3", "text": "eat"}, {"id": "c4", "text": "breakfast"}],
         ["c1", "c2", "c3", "c4"], "Correct! 'I always eat breakfast.'", "I always eat breakfast."),
        (2, "Put in order: go / I / to school / usually",
         [{"id": "c1", "text": "I"}, {"id": "c2", "text": "usually"}, {"id": "c3", "text": "go"}, {"id": "c4", "text": "to school"}],
         ["c1", "c2", "c3", "c4"], "Correct! 'I usually go to school.'", "I usually go to school."),
        (3, "Put in order: sometimes / TV / I / watch",
         [{"id": "c1", "text": "I"}, {"id": "c2", "text": "sometimes"}, {"id": "c3", "text": "watch"}, {"id": "c4", "text": "TV"}],
         ["c1", "c2", "c3", "c4"], "Correct! 'I sometimes watch TV.'", "I sometimes watch TV."),
        (4, "Put in order: never / I / late / wake up",
         [{"id": "c1", "text": "I"}, {"id": "c2", "text": "never"}, {"id": "c3", "text": "wake up"}, {"id": "c4", "text": "late"}],
         ["c1", "c2", "c3", "c4"], "Correct! 'I never wake up late.'", "I never wake up late."),
    ]
    for (d, p, items, order, fc, fi) in builders:
        insert_question(write, "sentence_builder", "assessment", d, p,
                        {"items": items, "distractors": [], "correct_order": order,
                         "feedback": {"correct": fc, "incorrect": fi}}, 8, str(uuid7()))
    insert_question(write, "fill_blank_typed", "assessment", 5,
                    "Complete about yourself: 'I wake up at ______.' (write a time, e.g. 6 a.m.)",
                    {"accepted_answers": ["6 a.m.", "6am", "6 am", "7 a.m.", "7am", "7 am", "6", "7"],
                     "feedback": {"correct": "Great — that's a complete answer!",
                                  "incorrect": "Write a time, for example '6 a.m.'"}}, 5, str(uuid7()))

    insert_content_block(write, "self_check", 6, {
        "prompt": "Can you write this on your own?",
        "text": ("Write 10 sentences about your daily routine. Use times (6 a.m., 8 a.m.), frequency "
                 "words (always, usually, sometimes) and sequence words (first, then, after that)."),
    }, str(uuid7()))
    insert_content_block(write, "text", 7, {
        "type": "summary",
        "items": ["Use present simple for daily habits",
                  "Put always/usually/sometimes/never before the verb",
                  "Ask and answer 'Do you...?' questions",
                  "Use first, then and after that to sequence your day"],
    }, str(uuid7()))


def downgrade() -> None:
    bind = op.get_bind()
    row = bind.execute(text("""
        SELECT l.id::text FROM lesson l JOIN level lv ON lv.id = l.level_id
        WHERE lv.code = 'beginner_b' AND l.lesson_order = 1
    """)).fetchone()
    if not row:
        return
    lid = row[0]
    for tbl in ("question", "vocabulary_word", "content_block"):
        op.execute(f"DELETE FROM {tbl} WHERE lesson_section_id IN "
                   f"(SELECT id FROM lesson_section WHERE lesson_id = '{lid}')")
    op.execute(f"DELETE FROM lesson_section WHERE lesson_id = '{lid}'")
    op.execute(f"DELETE FROM lesson WHERE id = '{lid}'")
