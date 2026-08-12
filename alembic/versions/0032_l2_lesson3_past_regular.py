"""Beginner B — Lesson 3: Past Simple (Regular Verbs) (Level 2 seed).

Seeds beginner_b Lesson 3 from LEVEL 2 Lesson 3.docx (7 sections). Text-only
scope; audio activities deferred. Sinhala from the .docx source.

Revision ID: 2c3d4e5f6a7b
Revises:     2b2c3d4e5f6a
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

revision: str = "2c3d4e5f6a7b"
down_revision: Union[str, None] = "2b2c3d4e5f6a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _j(obj: object) -> str:
    return "'" + json.dumps(obj, ensure_ascii=False).replace("'", "''") + "'"


OBJECTIVES = [
    "Use past simple tense with regular verbs correctly",
    "Talk about actions that happened in the past",
    "Use common past time expressions such as yesterday and last night",
    "Ask and answer questions using Did you...?",
    "Understand short stories about past events",
    "Speak and write about what you did yesterday",
]
OBJECTIVES_SI = [
    "Regular verbs සමඟ past simple නිවැරදිව භාවිතා කිරීම",
    "අතීතයේ සිදු වූ ක්‍රියා ගැන කතා කිරීම",
    "yesterday, last night වැනි කාල ප්‍රකාශන භාවිතා කිරීම",
    "Did you...? භාවිතයෙන් ප්‍රශ්න අසා පිළිතුරු දීම",
    "අතීත සිදුවීම් ගැන කෙටි කතා තේරුම් ගැනීම",
    "ඊයේ ඔබ කළ දේ ගැන කතා කර ලිවීම",
]


def upgrade() -> None:
    from uuid6 import uuid7  # noqa: PLC0415

    bind = op.get_bind()
    level_id = str(bind.execute(text("SELECT id::text FROM level WHERE code='beginner_b'")).fetchone()[0])

    l_id = ensure_lesson(bind, level_id, 3, "Past Simple (Regular Verbs)",
                         "Talk about the past with regular -ed verbs and time words like yesterday.", str(uuid7()))
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
        "text": "Learn regular past tense verbs (verb + -ed) and past time expressions."}, str(uuid7()))
    insert_content_block(vocab, "text", 1, {"type": "heading", "text": "Regular Past Tense Verbs"}, str(uuid7()))
    verbs = [
        (2,  "Walked",  "ඇවිද්දා",       "Past of walk.",   "I walked to school yesterday."),
        (3,  "Played",  "ක්‍රීඩා කළා",   "Past of play.",   "I played football yesterday."),
        (4,  "Watched", "බැලුවා",        "Past of watch.",  "We watched TV last night."),
        (5,  "Visited", "බලන්න ගියා",    "Past of visit.",  "She visited her grandmother."),
        (6,  "Studied", "ඉගෙන ගත්තා",    "Past of study.",  "I studied English yesterday."),
        (7,  "Cooked",  "උයලා",          "Past of cook.",   "My mother cooked dinner."),
        (8,  "Cleaned", "පිරිසිදු කළා",  "Past of clean.",  "They cleaned the classroom."),
        (9,  "Helped",  "උදව් කළා",      "Past of help.",   "I helped my mother."),
    ]
    for (d, w, si, defn, ex) in verbs:
        insert_word_card_tr(bind, vocab, d, w, defn, ex, str(uuid7()), str(uuid7()), si)

    insert_content_block(vocab, "text", 10, {"type": "heading", "text": "Past Time Expressions"}, str(uuid7()))
    times = [
        (11, "Yesterday",   "ඊයේ",             "The day before today.",  "I played football yesterday."),
        (12, "Last night",  "ඊයේ රාත්‍රියේ",   "The night before today.", "We watched TV last night."),
        (13, "Last weekend","පසුගිය සති අන්තයේ","The weekend before this one.", "I visited my uncle last weekend."),
    ]
    for (d, w, si, defn, ex) in times:
        insert_word_card_tr(bind, vocab, d, w, defn, ex, str(uuid7()), str(uuid7()), si)

    insert_question(vocab, "match_pairs", "assessment", 14, "Match present to past", {
        "pairs": [
            {"id": "p1", "left": "play", "right": "played"},
            {"id": "p2", "left": "watch", "right": "watched"},
            {"id": "p3", "left": "study", "right": "studied"},
            {"id": "p4", "left": "clean", "right": "cleaned"},
        ],
        "display_shuffle": True,
        "feedback": {"correct": "Well done!", "incorrect": "Add -ed to make the past form."},
    }, 10, str(uuid7()))

    # GRAMMAR
    insert_content_block(gram, "text", 0, {"type": "plain",
        "text": ("We use the past simple for finished actions. For regular verbs we add -ed: "
                 "play → played. In questions we use 'Did + subject + base verb': 'Did you play?' — "
                 "the verb goes back to its base form after 'did'.")}, str(uuid7()))
    insert_content_block(gram, "text", 1, {"type": "example_cards", "label": "Past Simple",
        "sentences": ["I played football yesterday.", "She visited her grandmother.",
                      "We watched TV last night."]}, str(uuid7()))
    insert_content_block(gram, "text", 2, {"type": "qa_pair", "question": "Did you play football?",
                                           "answer": "Yes, I did. / No, I didn't."}, str(uuid7()))
    g = [
        (3, "Yesterday I ______ football.",
         [{"id": "a", "text": "played"}, {"id": "b", "text": "play"}, {"id": "c", "text": "playing"}], "a",
         "Correct! Past of play is 'played'.", "Add -ed: 'played'."),
        (4, "We ______ TV last night.",
         [{"id": "a", "text": "watched"}, {"id": "b", "text": "watch"}, {"id": "c", "text": "watches"}], "a",
         "Correct!", "Past of watch is 'watched'."),
        (5, "I ______ English yesterday.",
         [{"id": "a", "text": "studied"}, {"id": "b", "text": "study"}, {"id": "c", "text": "studies"}], "a",
         "Correct! study → studied.", "study becomes 'studied' (y → ied)."),
        (6, "Did you ______ TV?",
         [{"id": "a", "text": "watch"}, {"id": "b", "text": "watched"}], "a",
         "Correct! After 'did' use the base verb.", "After 'did' use the base verb: 'watch'."),
        (7, "Did he ______ yesterday?",
         [{"id": "a", "text": "work"}, {"id": "b", "text": "worked"}], "a",
         "Correct! Base verb after 'did'.", "After 'did' use 'work', not 'worked'."),
    ]
    for (d, s, o, c, fc, fi) in g:
        insert_question(gram, "fill_blank_options", "assessment", d, s,
                        {"sentence_with_blank": s, "options": o, "correct_option_id": c,
                         "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    builders = [
        (8, "Put in order: yesterday / walked / to school / I",
         [{"id": "c1", "text": "I"}, {"id": "c2", "text": "walked"}, {"id": "c3", "text": "to school"}, {"id": "c4", "text": "yesterday"}],
         ["c1", "c2", "c3", "c4"], "Correct! 'I walked to school yesterday.'", "I walked to school yesterday."),
        (9, "Put in order: her grandmother / visited / last weekend / She",
         [{"id": "c1", "text": "She"}, {"id": "c2", "text": "visited"}, {"id": "c3", "text": "her grandmother"}, {"id": "c4", "text": "last weekend"}],
         ["c1", "c2", "c3", "c4"], "Correct! 'She visited her grandmother last weekend.'",
         "She visited her grandmother last weekend."),
    ]
    for (d, p, items, order, fc, fi) in builders:
        insert_question(gram, "sentence_builder", "assessment", d, p,
                        {"items": items, "distractors": [], "correct_order": order,
                         "feedback": {"correct": fc, "incorrect": fi}}, 8, str(uuid7()))
    insert_question(gram, "match_pairs", "assessment", 10, "Match the question to the answer", {
        "pairs": [
            {"id": "p1", "left": "Did you play football?", "right": "Yes, I did."},
            {"id": "p2", "left": "Did they watch TV?", "right": "No, they didn't."},
            {"id": "p3", "left": "Did he work yesterday?", "right": "No, he didn't."},
        ],
        "display_shuffle": True,
        "feedback": {"correct": "Well matched!", "incorrect": "Match each question to a short answer."},
    }, 10, str(uuid7()))

    # PRONUNCIATION — three -ed sounds
    insert_content_block(pron, "text", 0, {"type": "heading", "text": "The Three -ed Sounds"}, str(uuid7()))
    insert_content_block(pron, "text", 1, {"type": "phrase_card", "text": "Walked, Watched, Worked", "note": "/t/ sound"}, str(uuid7()))
    insert_content_block(pron, "text", 2, {"type": "phrase_card", "text": "Played, Cleaned, Called", "note": "/d/ sound"}, str(uuid7()))
    insert_content_block(pron, "text", 3, {"type": "phrase_card", "text": "Visited, Wanted, Needed", "note": "/ɪd/ — extra beat"}, str(uuid7()))
    pq = [
        (4, "Say the /t/ ending clearly.", "I walked to school."),
        (5, "Say the /d/ ending clearly.", "I played football yesterday."),
        (6, "Say the extra beat: Vis-it-ed.", "She visited her grandmother."),
    ]
    for (d, pr, tg) in pq:
        insert_question(pron, "pronunciation_practice", "assessment", d, pr,
                        {"target_text": tg, "show_text_before_record": True, "max_duration_seconds": 10,
                         "feedback": {"correct": "Great -ed sound!", "incorrect": "Listen for the -ed sound and try again."}},
                        15, str(uuid7()))

    # LISTENING
    insert_content_block(listn, "text", 0, {"type": "heading", "text": "Saturday"}, str(uuid7()))
    insert_content_block(listn, "text", 1, {"type": "plain",
        "text": ("Yesterday was Saturday. I walked to the park in the morning. I played football with my "
                 "friends. In the afternoon, I visited my grandmother. At night, I watched TV and studied "
                 "English.")}, str(uuid7()))
    l_mcq = [
        (2, "Where did he walk?", [{"id": "a", "text": "Park"}, {"id": "b", "text": "School"}], "a", "Correct!", "He walked to the park."),
        (3, "What did he play?", [{"id": "a", "text": "Football"}, {"id": "b", "text": "Cricket"}], "a", "Correct!", "He played football."),
        (4, "Who did he visit?", [{"id": "a", "text": "Grandmother"}, {"id": "b", "text": "Teacher"}], "a", "Correct!", "He visited his grandmother."),
    ]
    for (d, p, o, c, fc, fi) in l_mcq:
        insert_question(listn, "mcq_single", "assessment", d, p,
                        {"options": o, "correct_option_id": c, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    for (d, p, a, fc, fi) in [
        (5, "He walked to the park. True or False?", True, "Correct!", "He walked to the park."),
        (6, "He played cricket. True or False?", False, "Correct! He played football.", "He played football."),
        (7, "He studied English. True or False?", True, "Correct!", "He studied English at night."),
    ]:
        insert_question(listn, "true_false", "assessment", d, p,
                        {"correct_answer": a, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    insert_question(listn, "sentence_builder", "assessment", 8, "Order the events.",
                    {"items": [{"id": "c1", "text": "Walked to the park"}, {"id": "c2", "text": "Played football"},
                               {"id": "c3", "text": "Visited grandmother"}, {"id": "c4", "text": "Watched TV"}],
                     "distractors": [], "correct_order": ["c1", "c2", "c3", "c4"],
                     "feedback": {"correct": "Correct order!", "incorrect": "Walk → play → visit → watch."}}, 8, str(uuid7()))

    # READING
    insert_content_block(read, "text", 0, {"type": "plain", "text": "Read about Nimal's beach trip and answer."}, str(uuid7()))
    insert_content_block(read, "text", 1, {"type": "plain",
        "text": ("Last Sunday, Nimal and his family visited a beautiful beach near their town. They "
                 "arrived at the beach at 8:00 a.m. The weather was sunny and pleasant. Nimal and his "
                 "sister built a large sandcastle. At noon, the family had lunch together and drank fresh "
                 "juice. After lunch, Nimal went swimming with his father. In the evening, they watched "
                 "the sunset before returning home. Everyone felt happy.")}, str(uuid7()))
    r = [
        (2, "Where did Nimal and his family go?", [{"id": "a", "text": "A beach"}, {"id": "b", "text": "A zoo"}], "a", "Correct!", "They visited a beach."),
        (3, "What time did they arrive?", [{"id": "a", "text": "8:00 a.m."}, {"id": "b", "text": "10:00 a.m."}], "a", "Correct!", "They arrived at 8:00 a.m."),
        (4, "What did the family drink at lunch?", [{"id": "a", "text": "Fresh juice"}, {"id": "b", "text": "Tea"}], "a", "Correct!", "They drank fresh juice."),
        (5, "Who went swimming with Nimal?", [{"id": "a", "text": "His father"}, {"id": "b", "text": "His sister"}], "a", "Correct!", "Nimal went swimming with his father."),
    ]
    for (d, p, o, c, fc, fi) in r:
        insert_question(read, "mcq_single", "assessment", d, p,
                        {"options": o, "correct_option_id": c, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    insert_question(read, "fill_blank_typed", "assessment", 6,
                    "Nimal and his sister built a large ______.",
                    {"accepted_answers": ["sandcastle", "sand castle"],
                     "feedback": {"correct": "Correct! A sandcastle.", "incorrect": "Read again — they built a sandcastle."}},
                    5, str(uuid7()))
    insert_question(read, "true_false", "assessment", 7,
                    "Everyone felt happy at the end of the day. True or False?",
                    {"correct_answer": True, "feedback": {"correct": "Correct!", "incorrect": "Everyone felt happy."}},
                    5, str(uuid7()))

    # SPEAKING
    insert_content_block(speak, "text", 0, {"type": "heading", "text": "Repeat After Me"}, str(uuid7()))
    for (d, ph) in [(1, "I played football yesterday."), (2, "I visited my grandmother."),
                    (3, "I watched TV last night."), (4, "I studied English yesterday.")]:
        insert_content_block(speak, "text", d, {"type": "phrase_card", "text": ph, "note": None}, str(uuid7()))
    insert_content_block(speak, "text", 5, {"type": "qa_pair", "question": "What did you do yesterday?",
                                            "answer": "I played football and watched TV."}, str(uuid7()))
    insert_content_block(speak, "text", 6, {"type": "plain",
        "text": ("Speak for 30–45 seconds about yesterday. Use at least 4 past tense verbs, plus "
                 "'yesterday' and 'last night'.")}, str(uuid7()))

    # WRITING
    insert_content_block(write, "text", 0, {"type": "plain", "text": "Reorder the words, then correct the mistakes."}, str(uuid7()))
    builders = [
        (1, "Put in order: Yesterday / rice / cooked / I",
         [{"id": "c1", "text": "Yesterday"}, {"id": "c2", "text": "I"}, {"id": "c3", "text": "cooked"}, {"id": "c4", "text": "rice"}],
         ["c1", "c2", "c3", "c4"], "Correct! 'Yesterday I cooked rice.'", "Yesterday I cooked rice."),
        (2, "Put in order: visited / uncle / my / I",
         [{"id": "c1", "text": "I"}, {"id": "c2", "text": "visited"}, {"id": "c3", "text": "my"}, {"id": "c4", "text": "uncle"}],
         ["c1", "c2", "c3", "c4"], "Correct! 'I visited my uncle.'", "I visited my uncle."),
    ]
    for (d, p, items, order, fc, fi) in builders:
        insert_question(write, "sentence_builder", "assessment", d, p,
                        {"items": items, "distractors": [], "correct_order": order,
                         "feedback": {"correct": fc, "incorrect": fi}}, 8, str(uuid7()))
    corrections = [
        (3, "Fix and type: 'I play football yesterday.'", ["I played football yesterday", "I played football yesterday."],
         "Correct! Past of play is 'played'.", "Use the past form: 'I played football yesterday.'"),
        (4, "Fix and type: 'We watch TV last night.'", ["We watched TV last night", "We watched TV last night."],
         "Correct! Past of watch is 'watched'.", "Use the past form: 'We watched TV last night.'"),
    ]
    for (d, p, acc, fc, fi) in corrections:
        insert_question(write, "fill_blank_typed", "assessment", d, p,
                        {"accepted_answers": acc, "feedback": {"correct": fc, "incorrect": fi}}, 8, str(uuid7()))
    insert_content_block(write, "self_check", 5, {"prompt": "Can you write this on your own?",
        "text": ("Write 5–6 sentences about yesterday. Use 4 regular past tense verbs, plus 'yesterday' "
                 "and 'last night'. Include a morning and an evening activity.")}, str(uuid7()))
    insert_content_block(write, "text", 6, {"type": "summary",
        "items": ["Add -ed to make regular past verbs",
                  "Use time words: yesterday, last night, last weekend",
                  "Ask questions with 'Did you...?' and a base verb",
                  "Answer with 'Yes, I did.' / 'No, I didn't.'"]}, str(uuid7()))


def downgrade() -> None:
    bind = op.get_bind()
    row = bind.execute(text("""
        SELECT l.id::text FROM lesson l JOIN level lv ON lv.id=l.level_id
        WHERE lv.code='beginner_b' AND l.lesson_order=3
    """)).fetchone()
    if not row:
        return
    lid = row[0]
    for tbl in ("question", "vocabulary_word", "content_block"):
        op.execute(f"DELETE FROM {tbl} WHERE lesson_section_id IN "
                   f"(SELECT id FROM lesson_section WHERE lesson_id='{lid}')")
    op.execute(f"DELETE FROM lesson_section WHERE lesson_id='{lid}'")
    op.execute(f"DELETE FROM lesson WHERE id='{lid}'")
