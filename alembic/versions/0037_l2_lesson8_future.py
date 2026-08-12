"""Beginner B — Lesson 8: Future Plans (Going To) (Level 2 seed).

Seeds beginner_b Lesson 8 from LEVEL 2 Lesson 8.docx (7 sections). Opens with a
Review Corner (leading purpose='practice' questions in grammar — see 0034).
Text-only scope; audio activities deferred. Sinhala from the .docx source.

Revision ID: 3b8c9d0e1f2a
Revises:     3a7b8c9d0e1f
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

revision: str = "3b8c9d0e1f2a"
down_revision: Union[str, None] = "3a7b8c9d0e1f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _j(obj: object) -> str:
    return "'" + json.dumps(obj, ensure_ascii=False).replace("'", "''") + "'"


OBJECTIVES = [
    "Use 'going to' for future intentions and plans",
    "Talk about holidays and future activities",
    "Ask and answer questions about future plans",
    "Understand spoken plans and intentions",
    "Speak about weekend and holiday plans",
    "Write about future intentions and activities",
]
OBJECTIVES_SI = [
    "අනාගත සැලසුම් සඳහා 'going to' භාවිතා කිරීම",
    "නිවාඩු හා අනාගත ක්‍රියාකාරකම් ගැන කතා කිරීම",
    "අනාගත සැලසුම් ගැන ප්‍රශ්න අසා පිළිතුරු දීම",
    "කතා කරන සැලසුම් තේරුම් ගැනීම",
    "සති අන්ත හා නිවාඩු සැලසුම් ගැන කතා කිරීම",
    "අනාගත චේතනා හා ක්‍රියාකාරකම් ගැන ලිවීම",
]


def upgrade() -> None:
    from uuid6 import uuid7  # noqa: PLC0415

    bind = op.get_bind()
    level_id = str(bind.execute(text("SELECT id::text FROM level WHERE code='beginner_b'")).fetchone()[0])

    l_id = ensure_lesson(bind, level_id, 8, "Future Plans (Going To)",
                         "Talk about future plans and holidays with 'going to'.", str(uuid7()))
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
    insert_content_block(vocab, "text", 0, {"type": "plain", "text": "Learn words for future plans and holidays."}, str(uuid7()))
    insert_content_block(vocab, "text", 1, {"type": "heading", "text": "Future Plans"}, str(uuid7()))
    words = [
        (2, "Holiday",    "නිවාඩුව",         "Time away from work or school.", "We are going to have a holiday."),
        (3, "Travel",     "සංචාරය කිරීම",    "Go from one place to another.",  "I am going to travel by train."),
        (4, "Trip",       "චාරිකාව",         "A short journey.",               "We are planning a trip to Kandy."),
        (5, "Book",       "වෙන්කරගැනීම",     "Reserve something.",             "My father is going to book tickets."),
        (6, "Visit",      "බලන්න යාම",       "Go and see a place or person.",  "We are going to visit grandparents."),
        (7, "Weekend",    "සති අන්තය",       "Saturday and Sunday.",           "This weekend I am going to relax."),
        (8, "Tomorrow",   "හෙට",             "The day after today.",           "Tomorrow I am going to study."),
        (9, "Next month", "ලබන මාසයේ",       "The month after this one.",      "Next month we are going to Kandy."),
    ]
    for (d, w, si, defn, ex) in words:
        insert_word_card_tr(bind, vocab, d, w, defn, ex, str(uuid7()), str(uuid7()), si)
    insert_question(vocab, "match_pairs", "assessment", 10, "Match the word to its meaning", {
        "pairs": [
            {"id": "p1", "left": "Holiday", "right": "Time away from work or school"},
            {"id": "p2", "left": "Book", "right": "Reserve something"},
            {"id": "p3", "left": "Visit", "right": "Go and see a place"},
            {"id": "p4", "left": "Weekend", "right": "Saturday and Sunday"},
        ],
        "display_shuffle": True,
        "feedback": {"correct": "Well done!", "incorrect": "Match each word to its meaning."},
    }, 10, str(uuid7()))

    # GRAMMAR — Review Corner + going to
    insert_content_block(gram, "text", 0, {"type": "heading", "text": "Review Corner"}, str(uuid7()))
    review = [
        (1, "Last year, I ______ to Galle.",
         [{"id": "a", "text": "went"}, {"id": "b", "text": "go"}], "a", "Correct! go → went.", "Past of go is 'went'."),
        (2, "We ______ many photographs.",
         [{"id": "a", "text": "took"}, {"id": "b", "text": "take"}], "a", "Correct! take → took.", "Past of take is 'took'."),
        (3, "The weather was ______.",
         [{"id": "a", "text": "sunny"}, {"id": "b", "text": "holiday"}], "a", "Correct!", "Use a weather word: 'sunny'."),
    ]
    for (d, s, o, c, fc, fi) in review:
        insert_question(gram, "fill_blank_options", "practice", d, s,
                        {"sentence_with_blank": s, "options": o, "correct_option_id": c,
                         "feedback": {"correct": fc, "incorrect": fi}}, 0, str(uuid7()))

    insert_content_block(gram, "text", 4, {"type": "heading", "text": "Future with Going To"}, str(uuid7()))
    insert_content_block(gram, "text", 5, {"type": "plain",
        "text": ("We use 'am/is/are + going to + verb' for future plans. I am going to visit Kandy. She "
                 "is going to travel. They are going to stay in a hotel. Questions: 'What are you going "
                 "to do?' 'Where are you going to go?'")}, str(uuid7()))
    insert_content_block(gram, "text", 6, {"type": "example_cards", "label": "Going To",
        "sentences": ["I am going to visit Kandy.", "She is going to travel next month.",
                      "They are going to stay in a hotel."]}, str(uuid7()))
    g = [
        (7, "I ______ visit Kandy next month.",
         [{"id": "a", "text": "am going to"}, {"id": "b", "text": "went"}], "a", "Correct!", "Use 'am going to' for a future plan."),
        (8, "She ______ travel by train.",
         [{"id": "a", "text": "is going to"}, {"id": "b", "text": "was"}], "a", "Correct!", "With 'she' use 'is going to'."),
        (9, "We ______ stay in a hotel.",
         [{"id": "a", "text": "are going to"}, {"id": "b", "text": "stayed"}], "a", "Correct!", "With 'we' use 'are going to'."),
        (10, "______ are you going to do tomorrow?",
         [{"id": "a", "text": "What"}, {"id": "b", "text": "Who"}], "a", "Correct!", "'What are you going to do?'"),
        (11, "______ are you going to stay?",
         [{"id": "a", "text": "Where"}, {"id": "b", "text": "When"}], "a", "Correct!", "'Where are you going to stay?'"),
    ]
    for (d, s, o, c, fc, fi) in g:
        insert_question(gram, "fill_blank_options", "assessment", d, s,
                        {"sentence_with_blank": s, "options": o, "correct_option_id": c,
                         "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    insert_question(gram, "sentence_builder", "assessment", 12, "Put in order: going / I / visit / am / to / Kandy",
                    {"items": [{"id": "c1", "text": "I"}, {"id": "c2", "text": "am"}, {"id": "c3", "text": "going"},
                               {"id": "c4", "text": "to"}, {"id": "c5", "text": "visit"}, {"id": "c6", "text": "Kandy"}],
                     "distractors": [], "correct_order": ["c1", "c2", "c3", "c4", "c5", "c6"],
                     "feedback": {"correct": "Correct! 'I am going to visit Kandy.'", "incorrect": "I am going to visit Kandy."}},
                    8, str(uuid7()))
    insert_question(gram, "match_pairs", "assessment", 13, "Match the question to the answer", {
        "pairs": [
            {"id": "p1", "left": "Where are you going to go?", "right": "I am going to go to Kandy."},
            {"id": "p2", "left": "Who are you going to visit?", "right": "I am going to visit my grandparents."},
            {"id": "p3", "left": "How are you going to travel?", "right": "I am going to travel by train."},
        ],
        "display_shuffle": True,
        "feedback": {"correct": "Well matched!", "incorrect": "Match each question to its answer."},
    }, 10, str(uuid7()))

    # PRONUNCIATION
    insert_content_block(pron, "text", 0, {"type": "heading", "text": "Listen & Repeat"}, str(uuid7()))
    for (d, w, nt) in [(1, "Holiday", "හොලිඩේ"), (2, "Vacation", "වෙකේෂන්"), (3, "Photograph", "ෆෝටෝග්‍රාෆ්")]:
        insert_content_block(pron, "text", d, {"type": "phrase_card", "text": w, "note": nt}, str(uuid7()))
    pq = [
        (4, "Say the sentence. Stress 'going'.", "I am going to travel."),
        (5, "Say the sentence clearly.", "We are going to visit Kandy."),
        (6, "Say the question — raise your voice at the end.", "What are you going to do?"),
    ]
    for (d, pr, tg) in pq:
        insert_question(pron, "pronunciation_practice", "assessment", d, pr,
                        {"target_text": tg, "show_text_before_record": True, "max_duration_seconds": 10,
                         "feedback": {"correct": "Great!", "incorrect": "Try again, slowly."}}, 15, str(uuid7()))

    # LISTENING
    insert_content_block(listn, "text", 0, {"type": "heading", "text": "Our Holiday Plans"}, str(uuid7()))
    insert_content_block(listn, "text", 1, {"type": "plain",
        "text": ("Next month, my family is going to visit Kandy. We are going to travel by train. First, "
                 "we are going to visit the Temple of the Tooth. Then, we are going to walk around the "
                 "city. After that, we are going to go shopping. My brother is going to take many "
                 "photographs. We are going to stay in a hotel for two nights. Finally, we are going to "
                 "return home.")}, str(uuid7()))
    l_mcq = [
        (2, "Where is the family going?", [{"id": "a", "text": "Kandy"}, {"id": "b", "text": "Galle"}], "a", "Correct!", "They are going to Kandy."),
        (3, "How are they going to travel?", [{"id": "a", "text": "Train"}, {"id": "b", "text": "Bus"}], "a", "Correct!", "They are going by train."),
        (4, "How many nights are they staying?", [{"id": "a", "text": "Two"}, {"id": "b", "text": "Three"}], "a", "Correct!", "They are staying two nights."),
    ]
    for (d, p, o, c, fc, fi) in l_mcq:
        insert_question(listn, "mcq_single", "assessment", d, p,
                        {"options": o, "correct_option_id": c, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    for (d, p, a, fc, fi) in [
        (5, "They are going to travel by plane. True or False?", False, "Correct! By train.", "They are going by train."),
        (6, "The brother is going to take photographs. True or False?", True, "Correct!", "The brother is going to take photographs."),
        (7, "They are going to stay in a hotel. True or False?", True, "Correct!", "They are going to stay in a hotel."),
    ]:
        insert_question(listn, "true_false", "assessment", d, p,
                        {"correct_answer": a, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    insert_question(listn, "sentence_builder", "assessment", 8, "Order the plan.",
                    {"items": [{"id": "c1", "text": "Visit the Temple of the Tooth"}, {"id": "c2", "text": "Walk around the city"},
                               {"id": "c3", "text": "Go shopping"}, {"id": "c4", "text": "Return home"}],
                     "distractors": [], "correct_order": ["c1", "c2", "c3", "c4"],
                     "feedback": {"correct": "Correct order!", "incorrect": "Temple → walk → shopping → home."}}, 8, str(uuid7()))

    # READING
    insert_content_block(read, "text", 0, {"type": "plain", "text": "Read about the weekend plans and answer."}, str(uuid7()))
    insert_content_block(read, "text", 1, {"type": "plain",
        "text": ("Next weekend, I am going to spend time with my friends. On Saturday morning, we are "
                 "going to play cricket at the park. Then, we are going to have lunch together. In the "
                 "afternoon, we are going to watch a movie. After that, we are going to visit a shopping "
                 "mall. On Sunday, I am going to stay at home and complete my homework.")}, str(uuid7()))
    r = [
        (2, "Who is the writer going to spend time with?", [{"id": "a", "text": "Friends"}, {"id": "b", "text": "Family"}], "a",
         "Correct!", "The writer is going to spend time with friends."),
        (3, "What are they going to play?", [{"id": "a", "text": "Cricket"}, {"id": "b", "text": "Football"}], "a", "Correct!", "They are going to play cricket."),
        (4, "What is the writer going to do on Sunday?", [{"id": "a", "text": "Homework"}, {"id": "b", "text": "Travel"}], "a",
         "Correct!", "The writer is going to complete homework."),
    ]
    for (d, p, o, c, fc, fi) in r:
        insert_question(read, "mcq_single", "assessment", d, p,
                        {"options": o, "correct_option_id": c, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    insert_question(read, "true_false", "assessment", 5, "They are going to watch a movie in the afternoon. True or False?",
                    {"correct_answer": True, "feedback": {"correct": "Correct!", "incorrect": "They are going to watch a movie in the afternoon."}},
                    5, str(uuid7()))

    # SPEAKING
    insert_content_block(speak, "text", 0, {"type": "heading", "text": "Repeat After Me"}, str(uuid7()))
    for (d, ph) in [(1, "I am going to visit Kandy next month."), (2, "We are going to travel by train."),
                    (3, "I am going to buy some souvenirs."), (4, "Next weekend, I am going to meet my friends.")]:
        insert_content_block(speak, "text", d, {"type": "phrase_card", "text": ph, "note": None}, str(uuid7()))
    insert_content_block(speak, "text", 5, {"type": "qa_pair", "question": "What are you going to do during the holidays?",
                                            "answer": "I am going to visit Kandy with my family."}, str(uuid7()))
    insert_content_block(speak, "text", 6, {"type": "plain",
        "text": ("Speak for 60–90 seconds about your plans for next month: where you are going, who with, "
                 "what you are going to do, where you are going to stay and why you are excited.")}, str(uuid7()))

    # WRITING
    insert_content_block(write, "text", 0, {"type": "plain", "text": "Complete the sentences."}, str(uuid7()))
    fills = [
        (1, "Tomorrow, I am going to ______. (an activity)",
         ["study", "rest", "play", "travel", "visit my friends", "read", "go shopping"],
         "Good — that's a plan!", "Write an activity, e.g. 'study'."),
        (2, "She ______ going to travel by train. (am/is/are)", ["is"], "Correct! With 'she' use 'is'.", "With 'she' use 'is going to'."),
        (3, "We ______ going to stay in a hotel. (am/is/are)", ["are"], "Correct! With 'we' use 'are'.", "With 'we' use 'are going to'."),
    ]
    for (d, s, acc, fc, fi) in fills:
        insert_question(write, "fill_blank_typed", "assessment", d, s,
                        {"accepted_answers": acc, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    insert_question(write, "sentence_builder", "assessment", 4, "Put in order: stay / are / hotel / in / going / We / a / to",
                    {"items": [{"id": "c1", "text": "We"}, {"id": "c2", "text": "are"}, {"id": "c3", "text": "going"},
                               {"id": "c4", "text": "to"}, {"id": "c5", "text": "stay"}, {"id": "c6", "text": "in"},
                               {"id": "c7", "text": "a"}, {"id": "c8", "text": "hotel"}],
                     "distractors": [], "correct_order": ["c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8"],
                     "feedback": {"correct": "Correct! 'We are going to stay in a hotel.'", "incorrect": "We are going to stay in a hotel."}},
                    8, str(uuid7()))
    insert_content_block(write, "self_check", 5, {"prompt": "Can you write this on your own?",
        "text": ("Write 8–15 sentences about your dream holiday. Include the destination, transport, "
                 "accommodation, activities and at least 5 'going to' sentences, plus one comparison with "
                 "a past holiday.")}, str(uuid7()))
    insert_content_block(write, "text", 6, {"type": "summary",
        "items": ["Use 'am/is/are + going to + verb' for future plans",
                  "Match the be-verb to the subject (I am, she is, we are)",
                  "Ask 'What/Where/Who are you going to...?'",
                  "Connect past holidays with future plans"]}, str(uuid7()))


def downgrade() -> None:
    bind = op.get_bind()
    row = bind.execute(text("""
        SELECT l.id::text FROM lesson l JOIN level lv ON lv.id=l.level_id
        WHERE lv.code='beginner_b' AND l.lesson_order=8
    """)).fetchone()
    if not row:
        return
    lid = row[0]
    for tbl in ("question", "vocabulary_word", "content_block"):
        op.execute(f"DELETE FROM {tbl} WHERE lesson_section_id IN "
                   f"(SELECT id FROM lesson_section WHERE lesson_id='{lid}')")
    op.execute(f"DELETE FROM lesson_section WHERE lesson_id='{lid}'")
    op.execute(f"DELETE FROM lesson WHERE id='{lid}'")
