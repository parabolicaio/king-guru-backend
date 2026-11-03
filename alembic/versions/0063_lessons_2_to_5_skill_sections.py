"""Pronunciation, Listening, Reading, Speaking and Writing for Lessons 2-5 (D-78).

Level 1 Lessons 2-5 were seeded with Vocabulary and Grammar only (0002,
0015-0018 say the other sections were "deferred"), so their overview
shows 2 sections while Lessons 1 and 6-10 have 7. This adds the five
missing sections, built like Lesson 6 (0025): pronunciation cards and
recorded practice, a dialogue with questions, a short story with
questions, guided speaking phrases, and word-order / fix-the-mistake
writing with a self check and a summary.

The content follows each lesson's own vocabulary and grammar. A section
that already has content is left alone, so this is safe to re-run.

Revision ID: 9b0c1d2e3f4a
Revises:     8a9b0c1d2e3f
Create Date: 2026-11-04
"""
from typing import Sequence, Union

from alembic import op
from seed_helpers import ensure_section, insert_content_block, insert_question
from sqlalchemy import text
from uuid6 import uuid7

revision: str = "9b0c1d2e3f4a"
down_revision: Union[str, None] = "8a9b0c1d2e3f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _opts(*texts: str) -> list[dict]:
    return [{"id": chr(ord("a") + i), "text": t} for i, t in enumerate(texts)]


def place_options(prompt: str, options: list[str], correct_index: int) -> tuple[list[dict], str]:
    """Options in a stable order where the answer isn't always first.

    The shift comes from the prompt, so a re-run gives the same order.
    Returns (options with ids a, b, ...; the correct option's id).
    """
    shift = sum(map(ord, prompt)) % len(options)
    order = options[shift:] + options[:shift]
    opts = _opts(*order)
    return opts, opts[order.index(options[correct_index])]["id"]


def _chips(*words: str) -> list[dict]:
    return [{"id": f"c{i + 1}", "text": w} for i, w in enumerate(words)]


# Each lesson: the five sections' content.
#   pron:   heading, [(word, note)], [practice phrases], [(prompt, target)]
#   listen: heading, [(speaker, line)], [question]
#   read:   story, [question]
#   speak:  [phrases], challenge
#   write:  [(prompt, [words in order])], [(wrong, [accepted])], self_check, summary
# Questions: ("mcq", prompt, [options], correct_index, fb_correct, fb_wrong)
#            ("tf", prompt, answer, fb_correct, fb_wrong)
#            ("fbo", sentence, [options], correct_index, fb_correct, fb_wrong)
#            ("typed", prompt, [accepted], fb_correct, fb_wrong)
LESSONS: dict[int, dict] = {
    2: {
        "pron": (
            "His, Her and Family Words",
            [("his", "/hɪz/ — හිස්"), ("her", "/hɜːr/ — හර්"),
             ("mother", "/ˈmʌðər/ — මදර්"), ("brother", "/ˈbrʌðər/ — බ්‍රදර්")],
            ["This is my mother.", "His name is Nimal.", "Her name is Kumari.", "She is my grandmother."],
            [("Say the sentence clearly.", "This is my mother."),
             ("Say the sentence. Make the 'h' in \"his\" clear.", "His name is Nimal."),
             ("Say the sentence slowly and clearly.", "She is my grandmother.")],
        ),
        "listen": (
            "Dialogue — My Family Photo",
            [("Sara", "Ravi, who is this?"),
             ("Ravi", "This is my father. His name is Sunil."),
             ("Sara", "He is tall!"),
             ("Ravi", "Yes, he is. And this is my mother. Her name is Kamala."),
             ("Sara", "Who is the boy?"),
             ("Ravi", "He is my brother, Dinesh. He is ten."),
             ("Sara", "And the old man?"),
             ("Ravi", "He is my grandfather. He is very kind.")],
            [("mcq", "What is Ravi's father's name?", ["Sunil", "Dinesh"], 0,
              "Correct! Ravi says 'His name is Sunil.'", "Ravi says 'This is my father. His name is Sunil.'"),
             ("mcq", "Who is Kamala?", ["Ravi's mother", "Ravi's sister"], 0,
              "Correct! Kamala is Ravi's mother.", "Ravi says 'this is my mother. Her name is Kamala.'"),
             ("mcq", "How old is Dinesh?", ["Ten", "Twelve"], 0,
              "Correct! Dinesh is ten.", "Ravi says 'He is my brother, Dinesh. He is ten.'"),
             ("tf", "Ravi's grandfather is very kind. True or False?", True,
              "Correct! Ravi says 'He is very kind.'", "Ravi says his grandfather is very kind — it is true.")],
        ),
        "read": (
            "My name is Nadeesha. I have a small family. My father is a teacher. "
            "His name is Ajith. He is tall and kind. My mother is a doctor. Her name "
            "is Shanika. She is friendly.\n\nI have one brother. His name is Kasun. "
            "He is twelve. My grandmother lives with us. She is old, but she is very "
            "funny. I love my family.",
            [("tf", "Nadeesha's father is a teacher. True or False?", True,
              "Correct! Her father is a teacher.", "The story says 'My father is a teacher.'"),
             ("tf", "Nadeesha's mother is a teacher. True or False?", False,
              "Correct! Her mother is a doctor.", "The story says 'My mother is a doctor.'"),
             ("tf", "Kasun is Nadeesha's brother. True or False?", True,
              "Correct! Kasun is her brother.", "The story says 'I have one brother. His name is Kasun.'"),
             ("mcq", "What is Nadeesha's mother's name?", ["Shanika", "Kasun"], 0,
              "Correct! Her mother's name is Shanika.", "The story says 'Her name is Shanika.'"),
             ("mcq", "Who is twelve?", ["Kasun", "Ajith"], 0,
              "Correct! Kasun is twelve.", "The story says Kasun 'is twelve.'"),
             ("fbo", "Nadeesha's father: '___ name is Ajith.'", ["His", "Her"], 0,
              "Correct! We use 'his' for a man.", "Her father is a man, so we say 'His name is Ajith.'"),
             ("fbo", "Nadeesha's mother: '___ name is Shanika.'", ["Her", "His"], 0,
              "Correct! We use 'her' for a woman.", "Her mother is a woman, so we say 'Her name is Shanika.'"),
             ("typed", "Who lives with Nadeesha's family? (one word)", ["grandmother", "her grandmother", "the grandmother"],
              "Correct! Her grandmother lives with them.", "Read again — 'My grandmother lives with us.'")],
        ),
        "speak": (
            ["This is my father.", "His name is Sunil.", "This is my sister.",
             "Her name is Malmi.", "My mother is kind and my brother is tall."],
            "Mini Speaking Challenge: show a family photo (or imagine one) and say 5 sentences about your family.",
        ),
        "write": (
            [("Put the words in order: is / my / This / father", ["This", "is", "my", "father."]),
             ("Put the words in order: name / Her / Kumari / is", ["Her", "name", "is", "Kumari."]),
             ("Put the words in order: brother / is / He / my", ["He", "is", "my", "brother."])],
            [("He are my uncle.", ["He is my uncle."]),
             ("This is me mother.", ["This is my mother."]),
             ("Her name are Mala.", ["Her name is Mala."])],
            "Write 5 sentences about your family. Use 'This is my...', 'His name is...' and 'Her name is...'.\n"
            "Word bank: father, mother, brother, sister, grandfather, grandmother, uncle, aunt, cousin.",
            ["Name the people in your family", "Use my, your, his and her",
             "Describe people with 'He is' and 'She is'", "Ask 'Who is...?' about a person"],
        ),
    },
    3: {
        "pron": (
            "Numbers and Time",
            [("thirteen", "/θɜːrˈtiːn/ — තර්ටීන්"), ("thirty", "/ˈθɜːrti/ — තර්ටි"),
             ("o'clock", "/əˈklɒk/ — අක්ලොක්"), ("half past", "/hɑːf pɑːst/ — හාෆ් පාස්ට්")],
            ["It's seven o'clock.", "It's half past six.", "I get up at six o'clock.", "I am thirteen years old."],
            [("Say the time clearly.", "It's seven o'clock."),
             ("Say the time. Make \"half past\" clear.", "It's half past six."),
             ("Say the sentence. Stress the end of \"thirteen\".", "I am thirteen years old.")],
        ),
        "listen": (
            "Dialogue — What Time Do You Get Up?",
            [("Amaya", "Leo, what time do you get up?"),
             ("Leo", "I get up at six o'clock."),
             ("Amaya", "What do you do then?"),
             ("Leo", "I have breakfast at half past six."),
             ("Amaya", "What time do you go to school?"),
             ("Leo", "I go to school at seven o'clock. And you?"),
             ("Amaya", "I get up at seven o'clock. I go to school at eight o'clock.")],
            [("mcq", "What time does Leo get up?", ["Six o'clock", "Seven o'clock"], 0,
              "Correct! Leo gets up at six o'clock.", "Leo says 'I get up at six o'clock.'"),
             ("mcq", "When does Leo have breakfast?", ["Half past six", "Eight o'clock"], 0,
              "Correct! He has breakfast at half past six.", "Leo says 'I have breakfast at half past six.'"),
             ("tf", "Amaya gets up at six o'clock. True or False?", False,
              "Correct! Amaya gets up at seven o'clock.", "Amaya says 'I get up at seven o'clock.'"),
             ("tf", "Amaya goes to school at eight o'clock. True or False?", True,
              "Correct! She goes to school at eight.", "Amaya says 'I go to school at eight o'clock.'")],
        ),
        "read": (
            "Hi, I am Tharindu. I am fourteen years old. Every day, I get up at six "
            "o'clock. I brush my teeth and have a shower. I have breakfast at half past "
            "six. I go to school at seven o'clock. School finishes at two o'clock.\n\n"
            "In the evening, I do my homework and play cricket. I have dinner at eight "
            "o'clock and I go to bed at ten o'clock.",
            [("tf", "Tharindu is fourteen years old. True or False?", True,
              "Correct! He is fourteen.", "The story says 'I am fourteen years old.'"),
             ("tf", "He has breakfast at seven o'clock. True or False?", False,
              "Correct! He has breakfast at half past six.", "The story says 'I have breakfast at half past six.'"),
             ("tf", "School finishes at two o'clock. True or False?", True,
              "Correct! School finishes at two.", "The story says 'School finishes at two o'clock.'"),
             ("mcq", "What time does Tharindu go to bed?", ["Ten o'clock", "Eight o'clock"], 0,
              "Correct! He goes to bed at ten.", "The story says 'I go to bed at ten o'clock.'"),
             ("mcq", "What does he do in the evening?", ["Homework and cricket", "A shower and breakfast"], 0,
              "Correct! He does his homework and plays cricket.", "The story says 'In the evening, I do my homework and play cricket.'"),
             ("fbo", "He gets up at ___ o'clock.", ["six", "eight"], 0,
              "Correct! He gets up at six o'clock.", "The story says 'I get up at six o'clock.'"),
             ("fbo", "He has dinner at ___ o'clock.", ["eight", "ten"], 0,
              "Correct! He has dinner at eight o'clock.", "The story says 'I have dinner at eight o'clock.'"),
             ("typed", "How old is Tharindu? Type the number.", ["fourteen", "14", "fourteen years old", "14 years old"],
              "Correct! He is fourteen.", "Read again — 'I am fourteen years old.'")],
        ),
        "speak": (
            ["I get up at six o'clock.", "I have breakfast at half past six.",
             "I go to school at seven o'clock.", "I go to bed at ten o'clock.", "What time do you get up?"],
            "Mini Speaking Challenge: tell someone your day, from morning to night, in 6 sentences with times.",
        ),
        "write": (
            [("Put the words in order: up / get / I / at / six", ["I", "get", "up", "at", "six."]),
             ("Put the words in order: o'clock / It's / seven", ["It's", "seven", "o'clock."]),
             ("Put the words in order: school / I / to / go", ["I", "go", "to", "school."])],
            [("I gets up at six.", ["I get up at six."]),
             ("I has breakfast at seven.", ["I have breakfast at seven."]),
             ("You goes to bed at ten.", ["You go to bed at ten."])],
            "Write 6 sentences about your day. Say what you do and what time you do it.\n"
            "Word bank: get up, have breakfast, go to school, do homework, have dinner, go to bed.",
            ["Use numbers for time and age", "Tell the time with o'clock and half past",
             "Talk about your daily routine with I and you", "Ask 'What time do you...?'"],
        ),
    },
    4: {
        "pron": (
            "This, That, These, Those",
            [("this", "/ðɪs/ — දිස්"), ("these", "/ðiːz/ — දීස්"),
             ("that", "/ðæt/ — දැට්"), ("those", "/ðoʊz/ — දෝස්")],
            ["This is a pen.", "That is a door.", "These are books.", "Those are chairs."],
            [("Say the sentence. Make the 'th' in \"this\" clear.", "This is a pen."),
             ("Say the sentence. \"These\" has a long 'ee' sound.", "These are books."),
             ("Say the sentence slowly and clearly.", "Those are chairs.")],
        ),
        "listen": (
            "Dialogue — In the Classroom",
            [("Teacher", "Good morning, class. Nimal, what is this?"),
             ("Nimal", "It is a pencil."),
             ("Teacher", "Good. And what are these?"),
             ("Nimal", "They are books."),
             ("Teacher", "Is that a window?"),
             ("Nimal", "No, it isn't. It is a door."),
             ("Teacher", "What are those?"),
             ("Nimal", "Those are chairs.")],
            [("mcq", "The teacher shows one thing. What is it?", ["A pencil", "A pen"], 0,
              "Correct! Nimal says 'It is a pencil.'", "Nimal says 'It is a pencil.'"),
             ("mcq", "What are 'these'?", ["Books", "Bags"], 0,
              "Correct! They are books.", "Nimal says 'They are books.'"),
             ("tf", "'That' is a window. True or False?", False,
              "Correct! It is a door.", "Nimal says 'No, it isn't. It is a door.'"),
             ("mcq", "What are 'those'?", ["Chairs", "Desks"], 0,
              "Correct! Those are chairs.", "Nimal says 'Those are chairs.'")],
        ),
        "read": (
            "This is my classroom. It is big. This is my desk. On my desk, I have a book, "
            "a pencil and an eraser. That is my teacher's desk. It is near the door.\n\n"
            "These are my friends' bags. They are blue and red. Those are the windows. "
            "They are open. I like my classroom.",
            [("tf", "The classroom is big. True or False?", True,
              "Correct! The classroom is big.", "The story says 'It is big.'"),
             ("tf", "The teacher's desk is near the window. True or False?", False,
              "Correct! It is near the door.", "The story says 'It is near the door.'"),
             ("tf", "The windows are open. True or False?", True,
              "Correct! The windows are open.", "The story says 'They are open.'"),
             ("mcq", "What is on the writer's desk?", ["A book, a pencil and an eraser", "A bag and a ruler"], 0,
              "Correct!", "The story says 'I have a book, a pencil and an eraser.'"),
             ("mcq", "What color are the bags?", ["Blue and red", "Green and yellow"], 0,
              "Correct! They are blue and red.", "The story says 'They are blue and red.'"),
             ("fbo", "I have ___ eraser.", ["an", "a"], 0,
              "Correct! 'Eraser' starts with a vowel sound, so we use 'an'.", "'Eraser' starts with a vowel sound: 'an eraser'."),
             ("fbo", "___ are my friends' bags.", ["These", "This"], 0,
              "Correct! We use 'these' for more than one thing near us.", "'Bags' is more than one, so we use 'These'."),
             ("typed", "What is near the door?", ["the teacher's desk", "teacher's desk", "my teacher's desk", "the teacher desk", "teacher desk"],
              "Correct! The teacher's desk is near the door.", "Read again — 'That is my teacher's desk. It is near the door.'")],
        ),
        "speak": (
            ["This is my pen.", "That is the door.", "These are my books.", "Those are windows.", "Is this your bag?"],
            "Mini Speaking Challenge: look around you and name 5 things with this, that, these or those.",
        ),
        "write": (
            [("Put the words in order: is / This / book / a", ["This", "is", "a", "book."]),
             ("Put the words in order: are / These / pens", ["These", "are", "pens."]),
             ("Put the words in order: eraser / It / an / is", ["It", "is", "an", "eraser."])],
            [("This are my books.", ["These are my books."]),
             ("It is a eraser.", ["It is an eraser."]),
             ("Those is chairs.", ["Those are chairs."])],
            "Write 6 sentences about things in your classroom or home. Use this, that, these and those, and a or an.\n"
            "Word bank: pen, pencil, book, bag, desk, chair, door, window, eraser, ruler.",
            ["Name classroom and everyday objects", "Use this, that, these and those",
             "Ask and answer 'What is this?' and 'What are these?'", "Use a, an and the"],
        ),
    },
    5: {
        "pron": (
            "Colors and Clothes",
            [("shirt", "/ʃɜːrt/ — ෂර්ට්"), ("shoes", "/ʃuːz/ — ෂූස්"),
             ("yellow", "/ˈjeloʊ/ — යෙලෝ"), ("purple", "/ˈpɜːrpl/ — පර්පල්")],
            ["I am wearing a blue shirt.", "She is wearing a red dress.",
             "These shoes are black.", "He has a big yellow hat."],
            [("Say the sentence clearly.", "I am wearing a blue shirt."),
             ("Say the sentence. Make the 'sh' in \"shoes\" clear.", "These shoes are black."),
             ("Say the sentence slowly and clearly.", "He has a big yellow hat.")],
        ),
        "listen": (
            "Dialogue — At the Party",
            [("Kevin", "Mala, who is that girl?"),
             ("Mala", "That is Nisha. She is wearing a pink dress."),
             ("Kevin", "And the boy?"),
             ("Mala", "That is Ruwan. He is wearing a white shirt and black trousers."),
             ("Kevin", "Is he wearing a hat?"),
             ("Mala", "Yes, he is. It is a small green hat.")],
            [("mcq", "What color is Nisha's dress?", ["Pink", "Purple"], 0,
              "Correct! Nisha is wearing a pink dress.", "Mala says 'She is wearing a pink dress.'"),
             ("mcq", "What is Ruwan wearing?", ["A white shirt and black trousers", "A black shirt and white trousers"], 0,
              "Correct!", "Mala says 'He is wearing a white shirt and black trousers.'"),
             ("tf", "Ruwan's hat is big. True or False?", False,
              "Correct! It is a small hat.", "Mala says 'It is a small green hat.'"),
             ("mcq", "What color is Ruwan's hat?", ["Green", "Red"], 0,
              "Correct! It is green.", "Mala says 'It is a small green hat.'")],
        ),
        "read": (
            "Today is a school trip. Dilini is wearing a long blue skirt and a white "
            "T-shirt. Her shoes are new. They are black.\n\nHer brother Asela is wearing "
            "short brown trousers and a green shirt. He has a big red cap. Their mother "
            "is wearing a beautiful yellow saree. Everyone is happy.",
            [("tf", "Dilini's skirt is long. True or False?", True,
              "Correct! She is wearing a long blue skirt.", "The story says 'a long blue skirt'."),
             ("tf", "Dilini's shoes are old. True or False?", False,
              "Correct! Her shoes are new.", "The story says 'Her shoes are new.'"),
             ("tf", "Asela's cap is small. True or False?", False,
              "Correct! He has a big red cap.", "The story says 'He has a big red cap.'"),
             ("tf", "Their mother is wearing a yellow saree. True or False?", True,
              "Correct!", "The story says 'Their mother is wearing a beautiful yellow saree.'"),
             ("mcq", "What color is Asela's shirt?", ["Green", "Brown"], 0,
              "Correct! His shirt is green.", "The story says 'a green shirt'. His trousers are brown."),
             ("fbo", "Dilini is wearing a ___ skirt.", ["blue", "red"], 0,
              "Correct! Her skirt is blue.", "The story says 'a long blue skirt'."),
             ("fbo", "Asela has a big red ___.", ["cap", "skirt"], 0,
              "Correct! He has a big red cap.", "The story says 'He has a big red cap.'"),
             ("typed", "What color are Dilini's shoes?", ["black", "they are black"],
              "Correct! They are black.", "Read again — 'Her shoes are new. They are black.'")],
        ),
        "speak": (
            ["I am wearing a white shirt.", "My shoes are black.", "She is wearing a red dress.",
             "These trousers are long.", "My favourite color is blue."],
            "Mini Speaking Challenge: describe what you are wearing today in 5 sentences. Say the colors.",
        ),
        "write": (
            [("Put the words in order: wearing / I / am / a / hat", ["I", "am", "wearing", "a", "hat."]),
             ("Put the words in order: shoes / are / My / black", ["My", "shoes", "are", "black."]),
             ("Put the words in order: dress / She / a / red / is / wearing", ["She", "is", "wearing", "a", "red", "dress."])],
            [("She is wearing a dress red.", ["She is wearing a red dress."]),
             ("I have two shoe.", ["I have two shoes."]),
             ("My shirt are blue.", ["My shirt is blue."])],
            "Write 5 sentences about what you and your family are wearing. Use colors and adjectives.\n"
            "Word bank: shirt, T-shirt, dress, skirt, trousers, shoes, hat, cap, red, blue, black, white, big, small, long, short.",
            ["Name colors and clothes", "Use singular and plural nouns",
             "Put the adjective before the noun: a red dress", "Say what people are wearing"],
        ),
    },
}

_SECTIONS = [
    ("pronunciation", 3, "Pronunciation"),
    ("listening", 4, "Listening"),
    ("reading", 5, "Reading"),
    ("speaking", 6, "Speaking"),
    ("writing", 7, "Writing"),
]


def _insert_q(section_id: str, disp: int, q: tuple) -> None:
    kind = q[0]
    if kind == "mcq":
        _, prompt, options, idx, fb_c, fb_i = q
        opts, correct_id = place_options(prompt, options, idx)
        insert_question(section_id, "mcq_single", "assessment", disp, prompt,
                        {"options": opts, "correct_option_id": correct_id,
                         "feedback": {"correct": fb_c, "incorrect": fb_i}}, 5, str(uuid7()))
    elif kind == "tf":
        _, prompt, answer, fb_c, fb_i = q
        insert_question(section_id, "true_false", "assessment", disp, prompt,
                        {"correct_answer": answer, "feedback": {"correct": fb_c, "incorrect": fb_i}},
                        5, str(uuid7()))
    elif kind == "fbo":
        _, sentence, options, idx, fb_c, fb_i = q
        opts, correct_id = place_options(sentence, options, idx)
        insert_question(section_id, "fill_blank_options", "assessment", disp, sentence,
                        {"sentence_with_blank": sentence, "options": opts,
                         "correct_option_id": correct_id,
                         "feedback": {"correct": fb_c, "incorrect": fb_i}}, 5, str(uuid7()))
    elif kind == "typed":
        _, prompt, accepted, fb_c, fb_i = q
        insert_question(section_id, "fill_blank_typed", "assessment", disp, prompt,
                        {"accepted_answers": accepted, "feedback": {"correct": fb_c, "incorrect": fb_i}},
                        5, str(uuid7()))
    else:  # pragma: no cover - guarded by tests
        raise ValueError(kind)


def _seed_pronunciation(sec: str, spec: tuple) -> None:
    heading, words, phrases, practice = spec
    d = 0
    insert_content_block(sec, "text", d, {"type": "heading", "text": heading}, str(uuid7()))
    for word, note in words:
        d += 1
        insert_content_block(sec, "text", d, {"type": "phrase_card", "text": word, "note": note}, str(uuid7()))
    d += 1
    insert_content_block(sec, "text", d, {"type": "heading", "text": "Practice"}, str(uuid7()))
    for phrase in phrases:
        d += 1
        insert_content_block(sec, "text", d, {"type": "phrase_card", "text": phrase, "note": None}, str(uuid7()))
    for prompt, target in practice:
        d += 1
        insert_question(sec, "pronunciation_practice", "assessment", d, prompt, {
            "target_text": target,
            "show_text_before_record": True,
            "max_duration_seconds": 10,
            "feedback": {"correct": "Great! That was clear.",
                         "incorrect": "Try again — say each word slowly and clearly."},
        }, 15, str(uuid7()))


def _seed_listening(sec: str, spec: tuple) -> None:
    heading, turns, questions = spec
    insert_content_block(sec, "text", 0, {"type": "heading", "text": heading}, str(uuid7()))
    insert_content_block(sec, "dialogue", 1, {
        "turns": [{"speaker": s, "text": t} for s, t in turns],
    }, str(uuid7()))
    for i, q in enumerate(questions):
        _insert_q(sec, 2 + i, q)


def _seed_reading(sec: str, spec: tuple) -> None:
    story, questions = spec
    insert_content_block(sec, "text", 0, {"type": "plain", "text": "Read the story and answer the questions."},
                         str(uuid7()))
    insert_content_block(sec, "text", 1, {"type": "plain", "text": story}, str(uuid7()))
    for i, q in enumerate(questions):
        _insert_q(sec, 2 + i, q)


def _seed_speaking(sec: str, spec: tuple) -> None:
    phrases, challenge = spec
    insert_content_block(sec, "text", 0, {"type": "heading", "text": "Guided Speaking"}, str(uuid7()))
    for i, phrase in enumerate(phrases):
        insert_content_block(sec, "text", 1 + i, {"type": "phrase_card", "text": phrase, "note": None},
                             str(uuid7()))
    insert_content_block(sec, "text", 1 + len(phrases), {"type": "plain", "text": challenge}, str(uuid7()))


def _seed_writing(sec: str, spec: tuple) -> None:
    builders, corrections, self_check, summary = spec
    insert_content_block(sec, "text", 0, {
        "type": "plain",
        "text": "Put the words in the correct order, then fix the broken sentences.",
    }, str(uuid7()))
    d = 0
    for prompt, words in builders:
        d += 1
        items = _chips(*words)
        sentence = " ".join(words)
        insert_question(sec, "sentence_builder", "assessment", d, prompt, {
            "items": items,
            "distractors": [],
            "correct_order": [c["id"] for c in items],
            "feedback": {"correct": f"Correct! '{sentence}'", "incorrect": f"The correct order is: {sentence}"},
        }, 8, str(uuid7()))
    for wrong, accepted in corrections:
        d += 1
        insert_question(sec, "fill_blank_typed", "assessment", d,
                        f"Fix the mistake and type the correct sentence: '{wrong}'", {
                            "accepted_answers": accepted,
                            "feedback": {"correct": "Correct!",
                                         "incorrect": f"The correct sentence is: {accepted[0]}"},
                        }, 8, str(uuid7()))
    d += 1
    insert_content_block(sec, "self_check", d, {"prompt": "Can you write this on your own?", "text": self_check},
                         str(uuid7()))
    d += 1
    insert_content_block(sec, "text", d, {"type": "summary", "items": summary}, str(uuid7()))


_SEEDERS = {
    "pronunciation": ("pron", _seed_pronunciation),
    "listening": ("listen", _seed_listening),
    "reading": ("read", _seed_reading),
    "speaking": ("speak", _seed_speaking),
    "writing": ("write", _seed_writing),
}


def _has_content(bind, section_id: str) -> bool:
    row = bind.execute(text(
        "SELECT EXISTS (SELECT 1 FROM content_block WHERE lesson_section_id = :s) "
        "OR EXISTS (SELECT 1 FROM question WHERE lesson_section_id = :s)"
    ), {"s": section_id}).scalar()
    return bool(row)


def upgrade() -> None:
    bind = op.get_bind()
    for order, spec in LESSONS.items():
        row = bind.execute(text(
            "SELECT l.id::text FROM lesson l JOIN level lv ON lv.id = l.level_id "
            # 0045 renamed beginner_a to beginner; accept both (see 0066).
            "WHERE lv.code IN ('beginner', 'beginner_a') AND l.lesson_order = :o AND l.deleted_at IS NULL"
        ), {"o": order}).fetchone()
        if not row:
            continue
        lesson_id = row[0]
        for category, display_order, title in _SECTIONS:
            sec = ensure_section(bind, lesson_id, category, display_order, title, str(uuid7()))
            if _has_content(bind, sec):
                continue
            key, seeder = _SEEDERS[category]
            seeder(sec, spec[key])


def downgrade() -> None:
    # Learners may have progress in these sections by now; leave them.
    pass
