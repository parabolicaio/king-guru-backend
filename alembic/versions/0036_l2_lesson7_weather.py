"""Beginner B — Lesson 7: Weather & Seasons (Level 2 seed).

Seeds beginner_b Lesson 7 from LEVEL 2 Lesson 7.docx (7 sections). Opens with a
Review Corner (leading purpose='practice' questions in grammar — see 0034).
Text-only scope; audio activities deferred. Sinhala from the .docx source.

Revision ID: 3a7b8c9d0e1f
Revises:     2f6a7b8c9d0e
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

revision: str = "3a7b8c9d0e1f"
down_revision: Union[str, None] = "2f6a7b8c9d0e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _j(obj: object) -> str:
    return "'" + json.dumps(obj, ensure_ascii=False).replace("'", "''") + "'"


OBJECTIVES = [
    "Describe weather conditions using common weather vocabulary",
    "Talk about seasons and climate",
    "Ask and answer questions about weather",
    "Compare weather in different places using comparatives",
    "Understand weather forecasts and weather conversations",
    "Speak and write simple descriptions about weather and seasons",
]
OBJECTIVES_SI = [
    "සුලභ කාලගුණ වචන භාවිතයෙන් කාලගුණය විස්තර කිරීම",
    "ඍතු හා දේශගුණය ගැන කතා කිරීම",
    "කාලගුණය ගැන ප්‍රශ්න අසා පිළිතුරු දීම",
    "comparatives භාවිතයෙන් ස්ථාන දෙකක කාලගුණය සැසඳීම",
    "කාලගුණ අනාවැකි හා සංවාද තේරුම් ගැනීම",
    "කාලගුණය හා ඍතු ගැන සරල විස්තර කතා කර ලිවීම",
]


def upgrade() -> None:
    from uuid6 import uuid7  # noqa: PLC0415

    bind = op.get_bind()
    level_id = str(bind.execute(text("SELECT id::text FROM level WHERE code='beginner_b'")).fetchone()[0])

    l_id = ensure_lesson(bind, level_id, 7, "Weather & Seasons",
                         "Describe weather and seasons and compare places with comparatives.", str(uuid7()))
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
    insert_content_block(vocab, "text", 0, {"type": "plain", "text": "Learn weather words and the seasons."}, str(uuid7()))
    insert_content_block(vocab, "text", 1, {"type": "heading", "text": "Weather"}, str(uuid7()))
    weather = [
        (2, "Sunny",  "අව්ව සහිත",     "The sun is shining.",         "It is sunny today."),
        (3, "Rainy",  "වැසි සහිත",     "It is raining.",              "It is rainy outside."),
        (4, "Windy",  "සුළං සහිත",     "Strong winds are blowing.",   "It is windy today."),
        (5, "Cloudy", "වළාකුළු සහිත",   "The sky is full of clouds.",  "The sky is cloudy."),
        (6, "Hot",    "උණුසුම්",       "The weather is very warm.",   "It is very hot today."),
        (7, "Cold",   "සීතල",          "The weather is very cool.",   "It is cold in winter."),
        (8, "Foggy",  "මීදුම් සහිත",    "It is hard to see because of mist.", "It is foggy in Nuwara Eliya."),
    ]
    for (d, w, si, defn, ex) in weather:
        insert_word_card_tr(bind, vocab, d, w, defn, ex, str(uuid7()), str(uuid7()), si)
    insert_content_block(vocab, "text", 9, {"type": "heading", "text": "Seasons"}, str(uuid7()))
    seasons = [
        (10, "Summer", "ග්‍රීෂ්ම කාලය",  "The hot season.",       "It is hot in summer."),
        (11, "Winter", "ශීත කාලය",       "The cold season.",      "It is cold in winter."),
        (12, "Spring", "වසන්ත කාලය",     "Flowers bloom.",        "Flowers bloom in spring."),
        (13, "Autumn", "සරත් කාලය",      "Leaves fall.",          "Leaves fall in autumn."),
    ]
    for (d, w, si, defn, ex) in seasons:
        insert_word_card_tr(bind, vocab, d, w, defn, ex, str(uuid7()), str(uuid7()), si)
    insert_question(vocab, "match_pairs", "assessment", 14, "Match the season to what happens", {
        "pairs": [
            {"id": "p1", "left": "Summer", "right": "Hot weather"},
            {"id": "p2", "left": "Winter", "right": "Cold weather"},
            {"id": "p3", "left": "Spring", "right": "Flowers bloom"},
            {"id": "p4", "left": "Autumn", "right": "Leaves fall"},
        ],
        "display_shuffle": True,
        "feedback": {"correct": "Well done!", "incorrect": "Match each season to what happens."},
    }, 10, str(uuid7()))

    # GRAMMAR — Review Corner + weather grammar + comparatives
    insert_content_block(gram, "text", 0, {"type": "heading", "text": "Review Corner"}, str(uuid7()))
    review = [
        (1, "Yesterday, we ______ at home because it was rainy.",
         [{"id": "a", "text": "stayed"}, {"id": "b", "text": "stay"}], "a", "Correct! stay → stayed.", "Past of stay is 'stayed'."),
        (2, "Last weekend, we ______ to the beach.",
         [{"id": "a", "text": "went"}, {"id": "b", "text": "go"}], "a", "Correct! go → went.", "Past of go is 'went'."),
        (3, "When I have a fever, I ______ rest.",
         [{"id": "a", "text": "should"}, {"id": "b", "text": "shouldn't"}], "a", "Correct!", "You should rest."),
    ]
    for (d, s, o, c, fc, fi) in review:
        insert_question(gram, "fill_blank_options", "practice", d, s,
                        {"sentence_with_blank": s, "options": o, "correct_option_id": c,
                         "feedback": {"correct": fc, "incorrect": fi}}, 0, str(uuid7()))

    insert_content_block(gram, "text", 4, {"type": "heading", "text": "Weather & Comparatives"}, str(uuid7()))
    insert_content_block(gram, "text", 5, {"type": "plain",
        "text": ("Describe weather with 'It is + adjective' (It is sunny). Ask 'What's the weather like?' "
                 "To compare two places use a comparative + than: 'Colombo is hotter than Nuwara Eliya.' "
                 "Short adjectives add -er (hot → hotter, cold → colder); adjectives ending in -y change "
                 "to -ier (sunny → sunnier).")}, str(uuid7()))
    insert_content_block(gram, "text", 6, {"type": "example_cards", "label": "Comparatives",
        "sentences": ["Colombo is hotter than Nuwara Eliya.", "Nuwara Eliya is colder than Colombo.",
                      "Today is sunnier than yesterday."]}, str(uuid7()))
    g = [
        (7, "It is ______ today. (sun shining)",
         [{"id": "a", "text": "sunny"}, {"id": "b", "text": "receipt"}], "a", "Correct!", "It is sunny."),
        (8, "It is very ______ today. Wear a jacket.",
         [{"id": "a", "text": "cold"}, {"id": "b", "text": "hot"}], "a", "Correct!", "Wear a jacket when it is cold."),
        (9, "Colombo is ______ than Nuwara Eliya.",
         [{"id": "a", "text": "hotter"}, {"id": "b", "text": "hot"}, {"id": "c", "text": "hottest"}], "a",
         "Correct! Comparative: hotter than.", "Use 'hotter than'."),
        (10, "Nuwara Eliya is ______ than Colombo.",
         [{"id": "a", "text": "colder"}, {"id": "b", "text": "cold"}, {"id": "c", "text": "coldest"}], "a",
         "Correct! colder than.", "Use 'colder than'."),
        (11, "Today is ______ than yesterday.",
         [{"id": "a", "text": "sunnier"}, {"id": "b", "text": "sunny"}, {"id": "c", "text": "sunniest"}], "a",
         "Correct! sunny → sunnier.", "Adjectives ending in -y become -ier: 'sunnier'."),
    ]
    for (d, s, o, c, fc, fi) in g:
        insert_question(gram, "fill_blank_options", "assessment", d, s,
                        {"sentence_with_blank": s, "options": o, "correct_option_id": c,
                         "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    insert_question(gram, "match_pairs", "assessment", 12, "Match the weather to an activity", {
        "pairs": [
            {"id": "p1", "left": "Sunny", "right": "Go to the beach"},
            {"id": "p2", "left": "Rainy", "right": "Stay at home"},
            {"id": "p3", "left": "Cold", "right": "Drink hot tea"},
            {"id": "p4", "left": "Windy", "right": "Fly a kite"},
        ],
        "display_shuffle": True,
        "feedback": {"correct": "Well matched!", "incorrect": "Match the weather to a sensible activity."},
    }, 10, str(uuid7()))

    # PRONUNCIATION
    insert_content_block(pron, "text", 0, {"type": "heading", "text": "Listen & Repeat"}, str(uuid7()))
    for (d, w, nt) in [(1, "Weather", "වෙදර්"), (2, "Temperature", "ටෙම්පරචර්"), (3, "Cloudy", "ක්ලවුඩී")]:
        insert_content_block(pron, "text", d, {"type": "phrase_card", "text": w, "note": nt}, str(uuid7()))
    pq = [
        (4, "Say the sentence. Stress 'sunny'.", "It is sunny today."),
        (5, "Say the comparison clearly.", "Nuwara Eliya is colder than Colombo."),
        (6, "Say the sentence — 'weather', not 'wether'.", "The weather is hot."),
    ]
    for (d, pr, tg) in pq:
        insert_question(pron, "pronunciation_practice", "assessment", d, pr,
                        {"target_text": tg, "show_text_before_record": True, "max_duration_seconds": 10,
                         "feedback": {"correct": "Great!", "incorrect": "Try again, slowly."}}, 15, str(uuid7()))

    # LISTENING
    insert_content_block(listn, "text", 0, {"type": "heading", "text": "Weather Forecast"}, str(uuid7()))
    insert_content_block(listn, "text", 1, {"type": "plain",
        "text": ("Good evening. Here is tomorrow's weather forecast. Colombo will be sunny and hot with a "
                 "temperature of 32 degrees. Kandy will be cloudy with light rain in the afternoon. Nuwara "
                 "Eliya will be cold and foggy with a temperature of 18 degrees. Jaffna will be hot and dry. "
                 "People should carry umbrellas in Kandy and warm clothes in Nuwara Eliya.")}, str(uuid7()))
    l_mcq = [
        (2, "What will the weather be like in Colombo?", [{"id": "a", "text": "Sunny and hot"}, {"id": "b", "text": "Foggy"}], "a",
         "Correct!", "Colombo will be sunny and hot."),
        (3, "Which place will be cold and foggy?", [{"id": "a", "text": "Nuwara Eliya"}, {"id": "b", "text": "Jaffna"}], "a",
         "Correct!", "Nuwara Eliya will be cold and foggy."),
        (4, "What should people carry in Kandy?", [{"id": "a", "text": "Umbrellas"}, {"id": "b", "text": "Jackets"}], "a",
         "Correct!", "People should carry umbrellas in Kandy."),
    ]
    for (d, p, o, c, fc, fi) in l_mcq:
        insert_question(listn, "mcq_single", "assessment", d, p,
                        {"options": o, "correct_option_id": c, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    for (d, p, a, fc, fi) in [
        (5, "Kandy will have light rain. True or False?", True, "Correct!", "Kandy will be cloudy with light rain."),
        (6, "Nuwara Eliya will be hot. True or False?", False, "Correct! It will be cold.", "Nuwara Eliya will be cold and foggy."),
        (7, "Jaffna will be dry. True or False?", True, "Correct!", "Jaffna will be hot and dry."),
    ]:
        insert_question(listn, "true_false", "assessment", d, p,
                        {"correct_answer": a, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))

    # READING
    insert_content_block(read, "text", 0, {"type": "plain", "text": "Read about the weather in Sri Lanka and answer."}, str(uuid7()))
    insert_content_block(read, "text", 1, {"type": "plain",
        "text": ("Sri Lanka has different weather in different areas. Colombo is usually warm and humid. "
                 "Nuwara Eliya is cooler and often foggy. Jaffna is usually hotter and drier than many "
                 "other places. During the rainy season, many parts of the country receive heavy rain. "
                 "People often check the weather forecast before travelling.")}, str(uuid7()))
    r = [
        (2, "Which place is cooler?", [{"id": "a", "text": "Nuwara Eliya"}, {"id": "b", "text": "Colombo"}], "a", "Correct!", "Nuwara Eliya is cooler."),
        (3, "Which place is usually hotter?", [{"id": "a", "text": "Jaffna"}, {"id": "b", "text": "Nuwara Eliya"}], "a", "Correct!", "Jaffna is usually hotter."),
        (4, "What do people check before travelling?", [{"id": "a", "text": "Weather forecast"}, {"id": "b", "text": "TV schedule"}], "a",
         "Correct!", "People check the weather forecast."),
    ]
    for (d, p, o, c, fc, fi) in r:
        insert_question(read, "mcq_single", "assessment", d, p,
                        {"options": o, "correct_option_id": c, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    insert_question(read, "fill_blank_typed", "assessment", 5, "Jaffna is ______ than Nuwara Eliya. (hot, comparative)",
                    {"accepted_answers": ["hotter"], "feedback": {"correct": "Correct! hotter.", "incorrect": "Use the comparative 'hotter'."}},
                    5, str(uuid7()))

    # SPEAKING
    insert_content_block(speak, "text", 0, {"type": "heading", "text": "Repeat After Me"}, str(uuid7()))
    for (d, ph) in [(1, "It is sunny today."), (2, "The weather is very hot."),
                    (3, "Colombo is hotter than Nuwara Eliya."), (4, "I check the weather forecast.")]:
        insert_content_block(speak, "text", d, {"type": "phrase_card", "text": ph, "note": None}, str(uuid7()))
    insert_content_block(speak, "text", 5, {"type": "qa_pair", "question": "What's the weather like today?",
                                            "answer": "It's sunny and warm."}, str(uuid7()))
    insert_content_block(speak, "text", 6, {"type": "plain",
        "text": ("Speak for 60 seconds about your favourite weather. Include the weather type, activities, "
                 "your feelings, a past experience and one comparison.")}, str(uuid7()))

    # WRITING
    insert_content_block(write, "text", 0, {"type": "plain", "text": "Complete the sentences."}, str(uuid7()))
    fills = [
        (1, "Today, the weather is ______. (a weather word)", ["sunny", "rainy", "cloudy", "hot", "cold", "windy", "foggy"],
         "Good — that's a weather word!", "Write a weather word like 'sunny'."),
        (2, "Colombo is ______ than Nuwara Eliya. (hot, comparative)", ["hotter"], "Correct! hotter.", "Use 'hotter'."),
        (3, "Winter is ______ than summer. (cold, comparative)", ["colder"], "Correct! colder.", "Use 'colder'."),
    ]
    for (d, s, acc, fc, fi) in fills:
        insert_question(write, "fill_blank_typed", "assessment", d, s,
                        {"accepted_answers": acc, "feedback": {"correct": fc, "incorrect": fi}}, 5, str(uuid7()))
    insert_question(write, "fill_blank_typed", "assessment", 4, "Fix and type: 'The weather are hot.'",
                    {"accepted_answers": ["The weather is hot", "The weather is hot."],
                     "feedback": {"correct": "Correct! 'The weather is hot.'", "incorrect": "Weather is singular: 'The weather is hot.'"}},
                    8, str(uuid7()))
    insert_content_block(write, "self_check", 5, {"prompt": "Can you write this on your own?",
        "text": ("Write 8–12 sentences about a rainy day: the weather, what you planned to do, what "
                 "happened, what you did instead and how you felt.")}, str(uuid7()))
    insert_content_block(write, "text", 6, {"type": "summary",
        "items": ["Describe weather with 'It is + adjective'",
                  "Ask 'What's the weather like?'",
                  "Compare places with 'hotter/colder/sunnier than'",
                  "Talk about the four seasons"]}, str(uuid7()))


def downgrade() -> None:
    bind = op.get_bind()
    row = bind.execute(text("""
        SELECT l.id::text FROM lesson l JOIN level lv ON lv.id=l.level_id
        WHERE lv.code='beginner_b' AND l.lesson_order=7
    """)).fetchone()
    if not row:
        return
    lid = row[0]
    for tbl in ("question", "vocabulary_word", "content_block"):
        op.execute(f"DELETE FROM {tbl} WHERE lesson_section_id IN "
                   f"(SELECT id FROM lesson_section WHERE lesson_id='{lid}')")
    op.execute(f"DELETE FROM lesson_section WHERE lesson_id='{lid}'")
    op.execute(f"DELETE FROM lesson WHERE id='{lid}'")
