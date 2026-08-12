"""Beginner B — Lesson 6: Health, Body & Feelings (Level 2 seed).

Seeds beginner_b Lesson 6 from LEVEL 2 Lesson 6.docx (7 sections). Opens with a
Review Corner (seeded as leading purpose='practice' questions in the grammar
section — see 0034 for the rationale). Text-only scope; audio activities
deferred. Sinhala from the .docx source.

Revision ID: 2f6a7b8c9d0e
Revises:     2e5f6a7b8c9d
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

revision: str = "2f6a7b8c9d0e"
down_revision: Union[str, None] = "2e5f6a7b8c9d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _j(obj: object) -> str:
    return "'" + json.dumps(obj, ensure_ascii=False).replace("'", "''") + "'"


OBJECTIVES = [
    "Identify internal body parts and common health problems",
    "Use expressions such as I feel sick, I feel tired, I feel better",
    "Give basic health advice using should and shouldn't",
    "Understand conversations about health and symptoms",
    "Speak about how you feel and describe simple health problems",
    "Write about health conditions and experiences",
]
OBJECTIVES_SI = [
    "අභ්‍යන්තර ශරීර අවයව හා සුලභ සෞඛ්‍ය ගැටලු හඳුනා ගැනීම",
    "I feel sick, I feel tired, I feel better වැනි ප්‍රකාශන භාවිතා කිරීම",
    "should හා shouldn't භාවිතයෙන් සෞඛ්‍ය උපදෙස් දීම",
    "සෞඛ්‍යය හා රෝග ලක්ෂණ ගැන සංවාද තේරුම් ගැනීම",
    "ඔබට දැනෙන ආකාරය හා සෞඛ්‍ය ගැටලු කතා කිරීම",
    "සෞඛ්‍ය තත්ත්ව හා අත්දැකීම් ගැන ලිවීම",
]


def upgrade() -> None:
    from uuid6 import uuid7  # noqa: PLC0415

    bind = op.get_bind()
    level_id = str(bind.execute(text("SELECT id::text FROM level WHERE code='beginner_b'")).fetchone()[0])

    l_id = ensure_lesson(bind, level_id, 6, "Health, Body & Feelings",
                         "Talk about health and feelings and give advice with should and shouldn't.", str(uuid7()))
    op.execute(f"UPDATE lesson SET objectives={_j(OBJECTIVES)}, "
               f"objectives_translations={_j({'si': OBJECTIVES_SI})} WHERE id='{l_id}'")

    vocab = ensure_section(bind, l_id, "vocabulary",    1, "Vocabulary",    str(uuid7()))
    gram  = ensure_section(bind, l_id, "grammar",       2, "Grammar",       str(uuid7()))
    pron  = ensure_section(bind, l_id, "pronunciation", 3, "Pronunciation", str(uuid7()))
    listn = ensure_section(bind, l_id, "listening",     4, "Listening",     str(uuid7()))
    read  = ensure_section(bind, l_id, "reading",       5, "Reading",       str(uuid7()))
    speak = ensure_section(bind, l_id, "speaking",      6, "Speaking",      str(uuid7()))
    write = ensure_section(bind, l_id, "writing",       7, "Writing",       str(uuid7()))

    # VOCABULARY
    insert_content_block(vocab, "text", 0, {"type": "plain",
        "text": "Learn body parts, common health problems and feelings words."}, str(uuid7()))
    insert_content_block(vocab, "text", 1, {"type": "heading", "text": "Body Parts"}, str(uuid7()))
    body = [
        (2, "Head",    "හිස",     "The top of your body.",      "My head hurts."),
        (3, "Heart",   "හදවත",    "It pumps blood.",            "The heart is an organ."),
        (4, "Stomach", "බඩ",      "Where food goes.",           "I have a stomachache."),
        (5, "Throat",  "උගුර",    "Inside your neck.",          "I have a sore throat."),
        (6, "Back",    "පිට",     "The rear of your body.",     "My back hurts."),
        (7, "Teeth",   "දත්",     "You bite with them.",        "I have a toothache."),
    ]
    for (d, w, si, defn, ex) in body:
        insert_word_card_tr(bind, vocab, d, w, defn, ex, str(uuid7()), str(uuid7()), si)
    insert_content_block(vocab, "text", 8, {"type": "heading", "text": "Health Problems"}, str(uuid7()))
    prob = [
        (9,  "Headache",     "හිසරදය",         "Pain in the head.",     "I have a headache."),
        (10, "Stomachache",  "බඩේ අමාරුව",     "Pain in the stomach.",  "She has a stomachache."),
        (11, "Sore throat",  "උගුරේ අමාරුව",   "Pain in the throat.",   "I have a sore throat."),
        (12, "Fever",        "උණ",             "A high temperature.",   "He has a fever."),
        (13, "Cold",         "සෙම්ප්‍රතිශ්‍යාව", "A blocked or runny nose.", "I have a cold."),
        (14, "Cough",        "කැස්ස",          "Noisy air from the throat.", "I have a bad cough."),
    ]
    for (d, w, si, defn, ex) in prob:
        insert_word_card_tr(bind, vocab, d, w, defn, ex, str(uuid7()), str(uuid7()), si)
    insert_content_block(vocab, "text", 15, {"type": "heading", "text": "Feelings"}, str(uuid7()))
    feel = [
        (16, "Sick",    "අසනීපයි",    "Not well.",             "I feel sick."),
        (17, "Tired",   "මහන්සියි",   "Needing rest.",         "I feel tired."),
        (18, "Better",  "හොඳ වෙලා",   "Well again.",           "I feel better now."),
        (19, "Weak",    "දුර්වලයි",   "Little strength.",      "I feel weak after being sick."),
        (20, "Dizzy",   "කරකැවිල්ලයි", "The room seems to spin.", "I feel dizzy."),
    ]
    for (d, w, si, defn, ex) in feel:
        insert_word_card_tr(bind, vocab, d, w, defn, ex, str(uuid7()), str(uuid7()), si)
    insert_question(vocab, "match_pairs", "assessment", 21, "Match the body part to its problem", {
        "pairs": [
            {"id": "p1", "left": "Head", "right": "Headache"},
            {"id": "p2", "left": "Stomach", "right": "Stomachache"},
            {"id": "p3", "left": "Throat", "right": "Sore throat"},
            {"id": "p4", "left": "Teeth", "right": "Toothache"},
        ],
        "display_shuffle": True,
        "feedback": {"correct": "Well done!", "incorrect": "Match the body part to the matching ache."},
    }, 10, str(uuid7()))

    # GRAMMAR — Review Corner (practice) + should/shouldn't (assessment)
    insert_content_block(gram, "text", 0, {"type": "heading", "text": "Review Corner"}, str(uuid7()))
    review = [
        (1, "Yesterday, I ______ to the hospital.",
         [{"id": "a", "text": "went"}, {"id": "b", "text": "go"}], "a", "Correct! go → went.", "Past of go is 'went'."),
        (2, "My mother ______ me to the doctor.",
         [{"id": "a", "text": "took"}, {"id": "b", "text": "take"}], "a", "Correct! take → took.", "Past of take is 'took'."),
        (3, "The pharmacy is ______ the hospital.",
         [{"id": "a", "text": "next to"}, {"id": "b", "text": "tired"}], "a", "Correct! A place word.", "Use 'next to'."),
    ]
    for (d, s, o, c, fc, fi) in review:
        insert_question(gram, "fill_blank_options", "practice", d, s,
                        {"sentence_with_blank": s, "options": o, "correct_option_id": c,
                         "feedback": {"correct": fc, "incorrect": fi}}, 0, str(uuid7()))

    insert_content_block(gram, "text", 4, {"type": "heading", "text": "Feelings & Advice"}, str(uuid7()))
    insert_content_block(gram, "text", 5, {"type": "plain",
        "text": ("Use 'I feel + adjective' for feelings (I feel sick / tired / better). Give advice with "
                 "'You should + base verb' (You should rest) and negative advice with 'You shouldn't + "
                 "base verb' (You shouldn't stay up late). Never use 'to' after should.")}, str(uuid7()))
    insert_content_block(gram, "text", 6, {"type": "example_cards", "label": "Advice",
        "sentences": ["You should rest.", "You should drink water.", "You shouldn't eat too much junk food."]}, str(uuid7()))
    g = [
        (7, "I have a headache. You should ______.",
         [{"id": "a", "text": "rest"}, {"id": "b", "text": "run"}], "a", "Correct!", "For a headache you should rest."),
        (8, "You ______ drink water when you have a fever.",
         [{"id": "a", "text": "should"}, {"id": "b", "text": "shouldn't"}], "a", "Correct!", "You should drink water."),
        (9, "You ______ eat too much junk food.",
         [{"id": "a", "text": "shouldn't"}, {"id": "b", "text": "should"}], "a", "Correct!", "You shouldn't eat too much junk food."),
        (10, "Choose the correct sentence:",
         [{"id": "a", "text": "You should rest."}, {"id": "b", "text": "You should to rest."}], "a",
         "Correct! No 'to' after should.", "We never use 'to' after 'should'."),
        (11, "Yesterday I ______ sick. (feel, past)",
         [{"id": "a", "text": "felt"}, {"id": "b", "text": "feel"}], "a", "Correct! feel → felt.", "Past of feel is 'felt'."),
        (12, "After resting, I feel ______.",
         [{"id": "a", "text": "better"}, {"id": "b", "text": "pharmacy"}], "a", "Correct!", "After resting you feel better."),
    ]
    for (d, s, o, c, fc, fi) in g:
        insert_question(gram, "fill_blank_options", "assessment", d, s,
                        {"sentence_with_blank": s, "options": o, "correct_option_id": c,
                         "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    insert_question(gram, "match_pairs", "assessment", 13, "Match the problem to the advice", {
        "pairs": [
            {"id": "p1", "left": "Fever", "right": "You should visit a doctor."},
            {"id": "p2", "left": "Toothache", "right": "You should see a dentist."},
            {"id": "p3", "left": "Cold", "right": "You should drink warm tea."},
            {"id": "p4", "left": "Tired", "right": "You should sleep."},
        ],
        "display_shuffle": True,
        "feedback": {"correct": "Good advice!", "incorrect": "Match each problem to sensible advice."},
    }, 10, str(uuid7()))

    # PRONUNCIATION
    insert_content_block(pron, "text", 0, {"type": "heading", "text": "Listen & Repeat"}, str(uuid7()))
    for (d, w, nt) in [(1, "Headache", "හෙඩෙක්"), (2, "Doctor", "ඩොක්ටර් — clear 'r'"), (3, "Medicine", "මෙඩිසින්")]:
        insert_content_block(pron, "text", d, {"type": "phrase_card", "text": w, "note": nt}, str(uuid7()))
    pq = [
        (4, "Say the sentence. Stress 'feel'.", "I feel sick."),
        (5, "Say the sentence. Stress 'should'.", "You should rest."),
        (6, "Say the sentence clearly.", "I have a headache."),
    ]
    for (d, pr, tg) in pq:
        insert_question(pron, "pronunciation_practice", "assessment", d, pr,
                        {"target_text": tg, "show_text_before_record": True, "max_duration_seconds": 10,
                         "feedback": {"correct": "Great!", "incorrect": "Try again, slowly."}}, 15, str(uuid7()))

    # LISTENING
    insert_content_block(listn, "text", 0, {"type": "heading", "text": "A Visit to the Doctor"}, str(uuid7()))
    insert_content_block(listn, "text", 1, {"type": "plain",
        "text": ("Yesterday, I felt very sick. First, I stayed at home because I had a fever. Then, my "
                 "mother took me to the doctor. The doctor checked me and gave me some medicine. After "
                 "that, we went to the pharmacy. Finally, I came home and rested. Today, I feel much "
                 "better.")}, str(uuid7()))
    l_mcq = [
        (2, "How did the speaker feel?", [{"id": "a", "text": "Sick"}, {"id": "b", "text": "Happy"}], "a", "Correct!", "The speaker felt sick."),
        (3, "Who took the speaker to the doctor?", [{"id": "a", "text": "Mother"}, {"id": "b", "text": "Father"}], "a", "Correct!", "The mother took the speaker."),
        (4, "What did the doctor give?", [{"id": "a", "text": "Medicine"}, {"id": "b", "text": "Water"}], "a", "Correct!", "The doctor gave medicine."),
    ]
    for (d, p, o, c, fc, fi) in l_mcq:
        insert_question(listn, "mcq_single", "assessment", d, p,
                        {"options": o, "correct_option_id": c, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    for (d, p, a, fc, fi) in [
        (5, "The speaker had a fever. True or False?", True, "Correct!", "The speaker had a fever."),
        (6, "The father took the speaker to the doctor. True or False?", False, "Correct! The mother.", "The mother took the speaker."),
        (7, "The speaker feels better today. True or False?", True, "Correct!", "Today the speaker feels much better."),
    ]:
        insert_question(listn, "true_false", "assessment", d, p,
                        {"correct_answer": a, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    insert_question(listn, "sentence_builder", "assessment", 8, "Order the events.",
                    {"items": [{"id": "c1", "text": "Stayed at home"}, {"id": "c2", "text": "Visited the doctor"},
                               {"id": "c3", "text": "Went to the pharmacy"}, {"id": "c4", "text": "Felt better"}],
                     "distractors": [], "correct_order": ["c1", "c2", "c3", "c4"],
                     "feedback": {"correct": "Correct order!", "incorrect": "Home → doctor → pharmacy → better."}}, 8, str(uuid7()))

    # READING
    insert_content_block(read, "text", 0, {"type": "plain", "text": "Read about healthy habits and answer."}, str(uuid7()))
    insert_content_block(read, "text", 1, {"type": "plain",
        "text": ("Saman wants to stay healthy. Every day, he drinks a lot of water. He eats fruits and "
                 "vegetables. He sleeps for eight hours every night. He exercises three times a week. "
                 "When he feels tired, he rests. When he feels sick, he visits a doctor. Because of these "
                 "habits, he is usually healthy.")}, str(uuid7()))
    r = [
        (2, "What does Saman drink?", [{"id": "a", "text": "Water"}, {"id": "b", "text": "Cola"}], "a", "Correct!", "He drinks a lot of water."),
        (3, "How many hours does he sleep?", [{"id": "a", "text": "Eight"}, {"id": "b", "text": "Four"}], "a", "Correct!", "He sleeps eight hours."),
        (4, "What does he do when he feels sick?", [{"id": "a", "text": "Visits a doctor"}, {"id": "b", "text": "Plays football"}], "a",
         "Correct!", "He visits a doctor."),
    ]
    for (d, p, o, c, fc, fi) in r:
        insert_question(read, "mcq_single", "assessment", d, p,
                        {"options": o, "correct_option_id": c, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    insert_question(read, "true_false", "assessment", 5, "Saman exercises three times a week. True or False?",
                    {"correct_answer": True, "feedback": {"correct": "Correct!", "incorrect": "He exercises three times a week."}},
                    5, str(uuid7()))

    # SPEAKING
    insert_content_block(speak, "text", 0, {"type": "heading", "text": "Repeat After Me"}, str(uuid7()))
    for (d, ph) in [(1, "I feel sick."), (2, "I have a headache."), (3, "You should rest."),
                    (4, "You should drink water.")]:
        insert_content_block(speak, "text", d, {"type": "phrase_card", "text": ph, "note": None}, str(uuid7()))
    insert_content_block(speak, "text", 5, {"type": "qa_pair", "question": "How do you feel today?",
                                            "answer": "I feel tired and I have a sore throat."}, str(uuid7()))
    insert_content_block(speak, "text", 6, {"type": "plain",
        "text": ("Speak for 60 seconds about a time you were sick: a health problem, how you felt, who "
                 "helped you, the advice you received and how you felt afterwards.")}, str(uuid7()))

    # WRITING
    insert_content_block(write, "text", 0, {"type": "plain", "text": "Complete the sentences, then write advice."}, str(uuid7()))
    fills = [
        (1, "I feel ______ today. (a feeling, e.g. sick)", ["sick", "tired", "better", "weak", "dizzy", "healthy"],
         "Good — that's a feeling!", "Write a feeling like 'sick' or 'tired'."),
        (2, "You ______ visit a doctor. (should/shouldn't)", ["should"], "Correct! You should visit a doctor.", "Use 'should' for good advice."),
        (3, "I have a headache. You should ______. (advice verb)", ["rest", "sleep"], "Good advice!", "For a headache you should rest."),
    ]
    for (d, s, acc, fc, fi) in fills:
        insert_question(write, "fill_blank_typed", "assessment", d, s,
                        {"accepted_answers": acc, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    insert_question(write, "fill_blank_typed", "assessment", 4,
                    "Fix and type: 'You should to rest.'",
                    {"accepted_answers": ["You should rest", "You should rest."],
                     "feedback": {"correct": "Correct! No 'to' after should.", "incorrect": "Remove 'to': 'You should rest.'"}},
                    8, str(uuid7()))
    insert_content_block(write, "self_check", 5, {"prompt": "Can you write this on your own?",
        "text": ("Write 8–10 sentences about a day you felt sick. Include how you felt, what happened "
                 "first, who helped you, the advice you received and how you felt afterwards.")}, str(uuid7()))
    insert_content_block(write, "text", 6, {"type": "summary",
        "items": ["Name body parts, health problems and feelings",
                  "Say 'I feel + adjective' for feelings",
                  "Give advice with 'You should' and 'You shouldn't' + base verb",
                  "Never use 'to' after should"]}, str(uuid7()))


def downgrade() -> None:
    bind = op.get_bind()
    row = bind.execute(text("""
        SELECT l.id::text FROM lesson l JOIN level lv ON lv.id=l.level_id
        WHERE lv.code='beginner_b' AND l.lesson_order=6
    """)).fetchone()
    if not row:
        return
    lid = row[0]
    for tbl in ("question", "vocabulary_word", "content_block"):
        op.execute(f"DELETE FROM {tbl} WHERE lesson_section_id IN "
                   f"(SELECT id FROM lesson_section WHERE lesson_id='{lid}')")
    op.execute(f"DELETE FROM lesson_section WHERE lesson_id='{lid}'")
    op.execute(f"DELETE FROM lesson WHERE id='{lid}'")
