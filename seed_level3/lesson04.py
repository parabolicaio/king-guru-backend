"""Level 3 Lesson 4 — Health, Psychology & Well-being.

Source: LEVEL_3_L4_individual.docx. Follow-up Part B1 (app lines for the
Advice Clinic role play) and Part C1/C2 solo lines applied. review=True
marks keys/models by the King Guru team.
"""
from .dsl import (DISCUSS, cat, examples, heading, match, mcq, passage, phrases, plain, self_check,
                  speak, summary, words, write)

TEXT1 = (
    "Nuwan is a first-year university student. Recently, he has been finding it difficult to balance his "
    "studies, part-time job and personal life. \"I usually stay up late finishing assignments,\" he says. \"By "
    "the time I go to bed, I'm too tired to sleep properly because I keep thinking about everything I still "
    "have to do.\" His lecturer noticed that he looked exhausted during class and suggested visiting the "
    "university counselling centre. The counsellor listened carefully before asking about his daily routine. "
    "Nuwan explained that he rarely exercised, skipped breakfast most mornings and spent several hours "
    "scrolling through social media every night. The counsellor suggested making small changes instead of "
    "trying to change everything at once. \"You might feel less stressed if you organise your day better,\" "
    "she said. \"You may also find it helpful to take short breaks while studying. Regular exercise and "
    "enough sleep might improve both your physical and mental well-being.\" After following the advice for "
    "several weeks, Nuwan noticed that he felt calmer, more organised and more confident."
)
TEXT2 = (
    "At a job interview, communication is not only about the words people use. Body language also plays an "
    "important role. During one interview, two candidates answered the same questions equally well. "
    "However, their body language was very different. The first candidate smiled naturally, maintained eye "
    "contact and sat confidently. Although he admitted that he was nervous, his positive body language "
    "helped him appear confident and interested. The second candidate avoided eye contact, crossed his arms "
    "frequently and looked at the floor while speaking. The interviewers thought he seemed uncomfortable, "
    "even though he had excellent qualifications. A career adviser later explained that body language does "
    "not always reveal how a person truly feels. Someone may appear nervous because they are shy or anxious "
    "rather than unprepared. She advised students to practise interviews with friends before attending real "
    "interviews. She also reminded them that a confident posture, a friendly smile and active listening may "
    "create a positive first impression."
)
PASSAGE1 = (
    "Stress is a natural part of life, and everyone experiences it at different times. Students may feel "
    "stressed because of examinations, assignments or family responsibilities, while adults often worry about "
    "work, finances and personal relationships.\n\nAlthough a small amount of stress can motivate people to "
    "perform well, too much stress can affect both physical and mental health. People who experience "
    "long-term stress may have difficulty sleeping, concentrating or making decisions. They may also become "
    "impatient, anxious or easily frustrated.\n\nHealth experts recommend several ways to manage stress "
    "effectively. Regular exercise, healthy eating habits and enough sleep help both the body and the mind. "
    "Taking short breaks while studying or working can improve concentration and reduce mental fatigue. "
    "Talking to trusted friends, teachers or counsellors may also help people feel supported during "
    "difficult times.\n\nMany people believe that successful individuals never feel stressed. However, this "
    "is a common misunderstanding. Even successful people experience challenges, but they learn healthy ways "
    "to manage pressure instead of allowing it to control their lives.\n\nLearning how to manage stress is "
    "an important life skill that can improve relationships, confidence and overall well-being."
)
PASSAGE2 = (
    "People often communicate without saying a single word. The way we stand, smile, move our hands or make "
    "eye contact can influence how others understand us.\n\nResearchers believe that positive body language "
    "can improve communication in many situations, including classrooms, workplaces and interviews. For "
    "example, maintaining eye contact often shows confidence and interest, while smiling may help people "
    "appear friendly and approachable.\n\nHowever, body language is not always easy to interpret. A person "
    "who avoids eye contact may simply feel nervous rather than dishonest. Someone with crossed arms may be "
    "cold instead of angry.\n\nThis is why good communicators avoid making quick judgments. Instead, they "
    "observe the whole situation before deciding what another person's body language means.\n\n"
    "Understanding body language helps people become better listeners, more effective communicators and "
    "more empathetic friends."
)

# Follow-up Part B1: what the app says as the person with each problem.
ROLE_PLAY = [
    ("Exam stress",
     "My final exams start in two weeks, and I feel very stressed. I can't sleep properly, and I keep thinking I will fail. What should I do?",
     "If I were you, I would make a study plan for the next two weeks. You might feel calmer if you take short breaks and sleep for at least seven hours."),
    ("Homesickness",
     "I moved to Colombo for university three months ago. I miss my family and my village every day, and sometimes I want to go back home. Can you help me?",
     "Have you considered calling your family at the same time every evening? If I were you, I would also join a university club, because new friends may make Colombo feel like home."),
    ("Fear of public speaking",
     "I have to give a presentation in front of my class next week. Whenever I speak in public, my hands shake and I forget everything. What can I do?",
     "Why don't you practise your presentation in front of a friend every day? If I were you, I would write short notes, because they might help you remember your ideas."),
    ("Time management",
     "I have assignments, a part-time job and sports practice. I never have enough time, and I always finish my work late at night. How can I manage my time better?",
     "If I were you, I would write a weekly timetable. You may want to finish one assignment before practice, and you might ask your manager for fewer hours during exams."),
    ("Friendship problems",
     "My best friend and I had an argument last week, and now she doesn't talk to me. I don't know how to fix our friendship. What do you think I should do?",
     "Have you considered sending her a kind message? If I were you, I would apologise and ask to meet, because talking face to face might solve the problem."),
    ("Low confidence",
     "I always feel that other people are better than me. I don't share my ideas in class because I'm afraid they are wrong. How can I become more confident?",
     "If I were you, I would share one small idea in every class. You might also write down your successes, because they may remind you how much you can do."),
    ("Poor sleeping habits",
     "I usually go to bed after one o'clock because I use my phone late at night. In the morning I feel tired and I can't concentrate. What would you advise?",
     "Why don't you put your phone in another room at ten o'clock? If I were you, I would go to bed at the same time every night, and you may feel much better in the morning."),
    ("Work-life balance",
     "I work long hours, and I often bring work home. I don't have time for my family or my hobbies any more. How can I find a better balance?",
     "If I were you, I would stop checking work emails after seven o'clock. You might plan one evening a week for your family and your hobbies."),
]

LESSON = {
    "order": 4,
    "title": "Health, Psychology & Well-being",
    "title_si": "සෞඛ්‍යය, මනෝවිද්‍යාව සහ යහපැවැත්ම",
    "description": "Talk about emotions and body language, give advice with the Second Conditional and may/might (B1).",
    "objectives": [
        "Describe emotions, feelings, and body language in different situations",
        "Use the Second Conditional to talk about imaginary situations and give advice",
        "Use may and might to express possibility and uncertainty",
        "Discuss mental and physical well-being using appropriate vocabulary",
        "Interpret body language and emotional expressions",
        "Take part in discussions about healthy lifestyles and emotional well-being",
        "Write advice paragraphs and hypothetical essays using appropriate grammar",
    ],
    "sections": {
        "vocabulary": [
            words("A. Emotions & Feelings", [
                ("Confident", "ආත්ම විශ්වාසයෙන් යුතු"), ("Anxious", "කනස්සල්ලෙන්"), ("Overwhelmed", "අධික පීඩනයට ලක් වූ"),
                ("Motivated", "උනන්දු වූ"), ("Frustrated", "කලකිරුණු"), ("Optimistic", "සුභවාදී"),
                ("Embarrassed", "ලැජ්ජාවට පත් වූ"), ("Calm", "සන්සුන්"), ("Stressed", "ආතතියෙන්"),
                ("Determined", "අධිෂ්ඨානශීලී"), ("Empathetic", "අනුකම්පාශීලී"), ("Resilient", "නැවත නැගී සිටිය හැකි"),
            ]),
            *[mcq(f"Activity 2 – Well-being Check-In: {s}", o, a, review=True) for s, o, a in [
                ("You passed your final examination after studying for months.", ["Proud", "Disappointed", "Nervous"], "Proud"),
                ("You forgot an important presentation at university.", ["Worried", "Excited", "Grateful"], "Worried"),
                ("Your best friend surprised you on your birthday.", ["Excited", "Worried", "Disappointed"], "Excited"),
                ("You are about to speak in front of 500 people.", ["Nervous", "Relieved", "Grateful"], "Nervous"),
                ("You finally solved a difficult problem after several attempts.", ["Relieved", "Disappointed", "Nervous"], "Relieved"),
                ("You lost your mobile phone while travelling.", ["Worried", "Proud", "Excited"], "Worried"),
                ("A stranger thanked you for helping them.", ["Proud", "Worried", "Disappointed"], "Proud"),
                ("You are starting your first job next week.", ["Excited", "Disappointed", "Relieved"], "Excited"),
            ]],
            speak("Activity 2 – After selecting the emotion, record one or two sentences explaining your choice. Model:",
                  "I would feel proud if I passed my final examination, because I studied for many months.", seconds=20, review=True),
            *[mcq(f"Activity 3 – Emotion Compass: {s}", o, a, review=True) for s, o, a in [
                ("She received a scholarship after working hard for three years.", ["Optimistic", "Embarrassed", "Frustrated"], "Optimistic"),
                ("He has an important interview tomorrow morning.", ["Anxious", "Calm", "Empathetic"], "Anxious"),
                ("She forgot her speech while standing on stage.", ["Embarrassed", "Optimistic", "Calm"], "Embarrassed"),
                ("He completed his first marathon after months of training.", ["Determined", "Embarrassed", "Frustrated"], "Determined"),
                ("A doctor explained that his medical test results were normal.", ["Calm", "Frustrated", "Overwhelmed"], "Calm"),
                ("She failed her driving test for the second time.", ["Frustrated", "Optimistic", "Calm"], "Frustrated"),
                ("He successfully solved a difficult research problem.", ["Confident", "Anxious", "Embarrassed"], "Confident"),
                ("She is moving to another country for higher studies.", ["Motivated", "Embarrassed", "Frustrated"], "Motivated"),
                ("A friend apologised after a misunderstanding.", ["Calm", "Embarrassed", "Stressed"], "Calm"),
                ("He has too many assignments due this week.", ["Overwhelmed", "Calm", "Optimistic"], "Overwhelmed"),
            ]],
            write(f"Activity 3 – {DISCUSS}", [
                "Which emotions were easiest to identify?", "Which situations could produce more than one emotion?",
                "Have you experienced any similar situations?",
            ], min_words=5),
            heading("Activity 4 – Emotional Intelligence Challenge"),
            plain("Choose two situations. Record your advice for each and explain your reasons."),
            *[speak(f"Activity 4 – {s}", m, seconds=40, review=True) for s, m in [
                ("Your classmate looks worried before an examination. What would you say? What advice would you give?",
                 "I would say, don't worry, you have studied well. I would advise them to breathe slowly and read each question carefully."),
                ("Your friend is feeling lonely after moving to another city. How could you support them?",
                 "I could call them often and help them find a club, so they can meet new people."),
                ("Your younger brother feels disappointed after losing a competition. How would you encourage him?",
                 "I would tell him that losing is part of learning, and that he can practise and try again next time."),
                ("A colleague looks stressed because of work. Suggest three ways to reduce stress.",
                 "They could take short breaks, go for a walk after work and talk to the manager about their workload."),
                ("A friend feels anxious about speaking English in front of the class. What practical advice would you give?",
                 "I would advise them to practise with a friend first and to speak slowly, because nobody expects perfect English."),
            ]],
            words("B. Body Language", [
                ("Facial Expression", "මුහුණේ ඉරියව්"), ("Eye Contact", "ඇස් සම්බන්ධතාවය"), ("Posture", "ශරීර ඉරියව්"),
                ("Gesture", "අත් ඉඟිය"), ("Smile", "සිනහව"), ("Frown", "රැළි ගැසූ මුහුණ"),
                ("Crossed Arms", "අත් බැඳගෙන සිටීම"), ("Nod", "හිස සෙලවීම"), ("Handshake", "අතට අත දීම"),
                ("Personal Space", "පුද්ගලික ඉඩ"), ("Confidence", "ආත්ම විශ්වාසය"), ("Communication", "සන්නිවේදනය"),
            ]),
            *[mcq(f"Activity 5 – Body Language Detective: {s} What does it probably suggest?", o, a, review=True) for s, o, a in [
                ("A student avoids eye contact during a presentation.", ["Nervousness", "Anger", "Boredom with the topic"], "Nervousness"),
                ("A manager smiles warmly while welcoming a new employee.", ["Friendliness", "Impatience", "Worry"], "Friendliness"),
                ("A customer crosses their arms during a conversation.", ["They may disagree or feel uncomfortable", "They are very happy", "They want to leave immediately"], "They may disagree or feel uncomfortable"),
                ("Two friends maintain eye contact while talking.", ["Interest and trust", "Fear", "Dishonesty"], "Interest and trust"),
                ("A speaker stands upright with open shoulders.", ["Confidence", "Tiredness", "Embarrassment"], "Confidence"),
                ("A patient keeps looking at the floor while answering questions.", ["Worry or shyness", "Excitement", "Confidence"], "Worry or shyness"),
                ("Someone nods repeatedly during a meeting.", ["Agreement or understanding", "Confusion", "Anger"], "Agreement or understanding"),
                ("A teenager keeps checking their phone while talking to a friend.", ["Distraction or lack of interest", "Deep interest", "Calmness"], "Distraction or lack of interest"),
                ("A teacher folds their arms while listening to a student's explanation.", ["They may be thinking or unsure", "They are laughing", "They are very excited"], "They may be thinking or unsure"),
                ("An athlete smiles confidently before the competition begins.", ["Confidence", "Fear", "Sadness"], "Confidence"),
            ]],
            write(f"Activity 5 – {DISCUSS}", [
                "Can body language sometimes be misunderstood?", "How can culture influence body language?",
            ], min_words=5),
            match("Activity 6 – Read the Signals. Match the body language with the most likely meaning.", [
                ("Smiling", "Friendliness"), ("Avoiding eye contact", "Nervousness or shyness"),
                ("Nodding", "Agreement"), ("Standing confidently", "Confidence"),
                ("Looking at a watch repeatedly", "Impatience"), ("Crossed arms", "Feeling defensive"),
                ("Leaning forward", "Interest"), ("Looking around the room", "Boredom or distraction"),
            ], review=True),
            write("Activity 6 – Now answer the following questions.", [
                "Which body language signals show confidence?", "Which signals may indicate nervousness?",
                "Can the same body language have different meanings in different cultures?",
                "Give one example from your own experience.",
            ], min_words=5),
        ],
        "grammar": [
            heading("Review Corner"),
            plain("From Lesson 3: ✔ First Conditional ✔ Defining Relative Clauses ✔ Environmental Vocabulary "
                  "✔ Cause and Effect ✔ Giving Solutions\nExamples: If people recycle more, the environment will "
                  "become cleaner. · A scientist is someone who studies the natural world.\nToday we will move from "
                  "predicting real future situations to imagining different possibilities and giving advice."),
            cat("Activity 1 – Real Situation or Imaginary Situation? Sort each sentence.", {
                "A. A Real Future Possibility": [
                    "If I recycle more, I will produce less waste.",
                    "If people use renewable energy, pollution will decrease.",
                    "If scientists discover a new vaccine, many lives will be saved.",
                    "If governments reduce plastic production, rivers will become cleaner."],
                "B. An Imaginary Situation": [
                    "If I were the mayor, I would create more parks.",
                    "If I were a doctor, I would help children in rural areas.",
                    "If I had more free time, I would volunteer at an animal shelter.",
                    "If I could travel anywhere, I would visit Antarctica."],
            }, review=True),
            heading("Second Conditional"),
            plain("We use the Second Conditional to talk about imaginary or unlikely situations in the present or "
                  "future.\nStructure: If + Past Simple, would + Base Verb"),
            examples("Examples", ["If I had more free time, I would learn another language.",
                                  "If I were healthier, I would join a hiking club.",
                                  "If everyone were kinder, the world would be a better place.",
                                  "If I were you, I would speak to a counsellor."]),
            plain("Sinhala Help\nIf I were you, I would apologise.\n→ මම ඔයාගේ තැන හිටියා නම් සමාව ඉල්ලනවා.\n"
                  "If I had more confidence, I would speak in public.\n→ මට වැඩි ආත්ම විශ්වාසයක් තිබුණා නම් මම මහජනයා ඉදිරියේ කතා කරනවා."),
            write("Activity 7 – Advice Clinic. Give advice using “If I were you...” and explain why it would help.", [
                "Your friend feels stressed because of university assignments.", "A student cannot manage their time effectively.",
                "Someone spends too much time on social media.", "Your cousin is afraid of speaking English.",
                "A colleague feels exhausted after working long hours.", "A teenager never exercises.",
                "A friend has difficulty sleeping.", "Someone is nervous about attending their first job interview.",
                "A university student feels homesick after moving away from home.",
                "A friend has lost confidence after failing an examination.",
            ], min_words=6),
            write("Activity 8 – Imagine a Better World. Complete the sentences using the Second Conditional.", [
                "If every school had more counsellors, ______.", "If people spent less time on social media, ______.",
                "If everyone exercised regularly, ______.", "If cities had more green spaces, ______.",
                "If I could change one thing about my community, ______.", "If young people volunteered more often, ______.",
                "If I were the Minister of Health, ______.", "If everyone showed more empathy, ______.",
                "If people communicated more openly, ______.", "If every workplace supported mental well-being, ______.",
                "Which idea would create the greatest positive change in society? Explain your answer.",
            ], min_words=4),
            heading("May / Might (Expressing Possibility)"),
            plain("We use may and might to talk about something that is possible but not certain.\n"
                  "Structure: Subject + may/might + base verb"),
            examples("Examples", ["She may be tired because she studied late.", "He might feel nervous before the interview.",
                                  "The meeting may finish early.", "People might misunderstand body language."]),
            plain("Sinhala Help\nShe may be tired.\n→ ඇය වෙහෙසට පත්ව ඇති වෙන්න පුළුවන්.\n"
                  "He might feel nervous.\n→ ඔහු කලබල වෙලා ඇති වෙන්න පුළුවන්."),
            *[mcq(f"Activity 15 – What Might Be Happening? {s}", o, a, review=True) for s, o, a in [
                ("A student is looking out of the classroom window.", ["He might be bored or thinking about something else.", "He must be the teacher.", "He will leave school today."], "He might be bored or thinking about something else."),
                ("Someone is checking their phone repeatedly.", ["She may be waiting for an important message.", "She has no phone.", "She is definitely angry."], "She may be waiting for an important message."),
                ("A friend has been unusually quiet today.", ["He might be worried about something.", "He is always loud.", "He will never speak again."], "He might be worried about something."),
                ("A colleague arrives late to work.", ["She may have missed her bus.", "She lives at the office.", "She always arrives early."], "She may have missed her bus."),
                ("A patient looks worried while waiting outside a doctor's room.", ["He might be nervous about his test results.", "He is the doctor.", "He is on holiday."], "He might be nervous about his test results."),
                ("A teenager avoids joining group activities.", ["She may feel shy or anxious.", "She is the group leader.", "She has joined every group."], "She may feel shy or anxious."),
                ("Someone forgets an important meeting.", ["He might be too busy or stressed.", "He organised the meeting perfectly.", "He has never had a meeting."], "He might be too busy or stressed."),
                ("A neighbour suddenly starts exercising every morning.", ["She may want to improve her health.", "She hates exercise.", "She is moving away tomorrow."], "She may want to improve her health."),
            ]],
            write("Activity 16 – Advice Clinic Challenge. For each case say what may be the reason, what might happen if "
                  "nothing changes, and what advice you would give. Use the Second Conditional, may, might and “If I were you...”.", [
                "Case 1: “I have an important presentation tomorrow, but I cannot stop worrying.”",
                "Case 2: “My best friend has stopped replying to my messages.”",
                "Case 3: “I feel tired all the time.”",
                "Case 4: “I don't think anyone in my class likes me.”",
            ], min_words=15),
        ],
        "pronunciation": [
            phrases("Listen and Repeat", [
                ("Psychology", "සයිකොලජි"), ("Empathetic", "එම්පතෙටික්"), ("Resilient", "රිසිලියන්ට්"),
                ("Overwhelmed", None), ("Motivated", None), ("Confidence", None), ("Communication", None),
                ("Gesture", "ජෙස්චර්"), ("Expression", None), ("Counsellor", "කවුන්සලර්"),
            ]),
            plain("Common Pronunciation Problems\nPsychology — ❌ පයිකොලොජි ✅ සයිකොලජි\n"
                  "Gesture — ❌ ගෙස්චර් ✅ ජෙස්චර්\nResilient — ❌ රෙසිලියන්ට් ✅ රිසිලියන්ට්"),
            *[speak("Tap & Speak: say the word clearly.", w, seconds=5) for w in [
                "Psychology", "Empathetic", "Resilient", "Overwhelmed", "Motivated", "Confidence",
                "Communication", "Gesture", "Expression", "Counsellor"]],
            heading("Sentence Stress Practice"),
            *[speak(f"Say the sentence. Stress the words in capitals: {s}", t, seconds=10) for s, t in [
                ("If I WERE you, I WOULD talk to someone.", "If I were you, I would talk to someone."),
                ("She LOOKS confident because she MAINTAINS eye contact.", "She looks confident because she maintains eye contact."),
                ("People MAY feel anxious before an IMPORTANT interview.", "People may feel anxious before an important interview."),
                ("Helping others CAN improve your own WELL-BEING.", "Helping others can improve your own well-being."),
            ]],
        ],
        "listening": [
            plain("LISTENING TIP\nWhen listening to conversations about emotions and well-being:\n✔ Listen for the "
                  "speaker's feelings.\n✔ Identify the main problem.\n✔ Listen for advice and suggestions.\n✔ Pay "
                  "attention to words that express possibility such as may, might, could, and perhaps.\n✔ Notice how "
                  "tone of voice can help you understand emotions."),
            heading("Listening Text 1 – The Advice Clinic: Feeling Overwhelmed"),
            *[mcq(f"Activity 9 – {q}", o, a, listen=TEXT1) for q, o, a in [
                ("Why was Nuwan feeling stressed?", ["He could not balance his responsibilities.", "He disliked university.", "He wanted to change courses."], "He could not balance his responsibilities."),
                ("What did his lecturer recommend?", ["Visiting the counselling centre", "Leaving university", "Finding another job"], "Visiting the counselling centre"),
                ("Which unhealthy habit did Nuwan mention?", ["Skipping breakfast", "Eating too much", "Sleeping too early"], "Skipping breakfast"),
                ("What did he do before going to bed?", ["Used social media for several hours", "Exercised", "Read novels"], "Used social media for several hours"),
                ("What was the counsellor's first piece of advice?", ["Make small changes gradually", "Quit his job", "Stop studying"], "Make small changes gradually"),
                ("According to the counsellor, what might improve his well-being?", ["Better sleep and regular exercise", "More homework", "Watching television"], "Better sleep and regular exercise"),
                ("How did Nuwan feel after following the advice?", ["More confident", "More worried", "More tired"], "More confident"),
                ("What is the main lesson of the listening?", ["Small positive habits can improve well-being.", "University life is impossible.", "Social media should be banned."], "Small positive habits can improve well-being."),
            ]],
            write("Activity 10 – Advice Detective. Listen again and write the advice given for each problem.", [
                "Stayed up late:", "Felt stressed:", "Used social media too much:", "Rarely exercised:",
                "Poor sleeping habits:", "Which advice do you think would help Nuwan the most? Why?",
            ], min_words=3, listen=TEXT1, models=[
                "Organise his day better.", "Make small changes and take short breaks while studying.",
                "Organise his day so he spends less time scrolling at night.", "Exercise regularly.",
                "Get enough sleep.",
            ], review=True),
            write("Activity 11 – Emotion Tracker. How did Nuwan probably feel at each stage? Explain what caused each emotion.", [
                "Before visiting the counsellor:", "During the conversation:", "After making lifestyle changes:",
                "After improving his routine:",
            ], min_words=3, listen=TEXT1, models=[
                "Overwhelmed and exhausted, because he had too much to do.", "Calmer, because the counsellor listened carefully.",
                "More organised, because he had a better plan.", "Confident, because his routine was working.",
            ], review=True),
            write("Activity 12 – If You Were the Counsellor… Suggest three more pieces of advice for Nuwan. Use: If I "
                  "were you... · You might... · You may want to... · It would be a good idea to... Example: “If I were "
                  "you, I would create a weekly study plan.”", ["Advice 1:", "Advice 2:", "Advice 3:"],
                  min_words=6, listen=TEXT1),
            heading("Listening Text 2 – Understanding Body Language"),
            *[mcq(f"Activity 13 – {q}", o, a, listen=TEXT2) for q, o, a in [
                ("What was being discussed?", ["Job interviews", "Sports", "Holidays"], "Job interviews"),
                ("What made the first candidate appear confident?", ["Positive body language", "Expensive clothes", "Speaking loudly"], "Positive body language"),
                ("What did the second candidate avoid?", ["Eye contact", "Questions", "Smiling"], "Eye contact"),
                ("Why did the interviewers misunderstand the second candidate?", ["His body language suggested he lacked confidence.", "He arrived late.", "He answered incorrectly."], "His body language suggested he lacked confidence."),
                ("According to the career adviser, why might someone appear nervous?", ["They may simply be shy or anxious.", "They are always unprepared.", "They dislike interviews."], "They may simply be shy or anxious."),
                ("What advice was given?", ["Practise interviews before attending one.", "Memorise every answer.", "Speak as quickly as possible."], "Practise interviews before attending one."),
                ("Which body language creates a positive first impression?", ["Smiling and maintaining eye contact", "Looking away", "Crossing your arms"], "Smiling and maintaining eye contact"),
                ("What is the main message?", ["Body language influences communication.", "Interviews are easy.", "Qualifications are unimportant."], "Body language influences communication."),
            ]],
            write("Activity 14 – Body Language Interpreter. Listen again and write the possible message of each.", [
                "Smiling:", "Eye contact:", "Crossed arms:", "Looking down:", "Sitting confidently:", "Active listening:",
                "Can body language have different meanings in different cultures? Give one example.",
            ], min_words=2, listen=TEXT2, models=[
                "Friendly and interested.", "Confident and interested.", "Uncomfortable or defensive.",
                "Nervous, shy or uncomfortable.", "Confident.", "Interested and polite.",
            ], review=True),
        ],
        "reading": [
            plain("READING TIP\nWhen reading articles about health and psychology:\n✔ Identify the main idea.\n"
                  "✔ Look for supporting details.\n✔ Notice the writer's opinion.\n✔ Separate facts from advice.\n"
                  "✔ Think about how the information relates to your own life."),
            passage("Reading Passage 1 – Managing Stress in Everyday Life", PASSAGE1,
                    "ආතතිය ජීවිතයේ සාමාන්‍ය කොටසකි.\nඅධික ආතතිය ශාරීරික හා මානසික සෞඛ්‍යයට බලපායි.\n"
                    "ව්‍යායාම කිරීම, හොඳ නින්ද සහ කතා කිරීම ආතතිය පාලනය කිරීමට උපකාරී වේ."),
            *[mcq(f"Activity 17 – {q}", o, a, review=True) for q, o, a in [
                ("Why do students often feel stressed?", ["Because of examinations, assignments or family responsibilities", "Because they have too much free time", "Because they sleep too much"], "Because of examinations, assignments or family responsibilities"),
                ("How can stress affect people's health?", ["It can make it hard to sleep, concentrate or decide", "It always improves health", "It has no effect"], "It can make it hard to sleep, concentrate or decide"),
                ("Which are two healthy ways to reduce stress?", ["Regular exercise and enough sleep", "Skipping meals and staying up late", "Ignoring problems and working more"], "Regular exercise and enough sleep"),
                ("Why is taking short breaks useful?", ["It improves concentration and reduces mental fatigue", "It wastes time", "It makes work harder"], "It improves concentration and reduces mental fatigue"),
                ("Who can people talk to when they need support?", ["Trusted friends, teachers or counsellors", "Nobody", "Only strangers online"], "Trusted friends, teachers or counsellors"),
                ("What misunderstanding do many people have about successful people?", ["That they never feel stressed", "That they work too little", "That they have no friends"], "That they never feel stressed"),
                ("What important life skill does the writer encourage?", ["Managing stress", "Working without breaks", "Avoiding other people"], "Managing stress"),
                ("What is the writer's main purpose?", ["To explain stress and how to manage it", "To sell medicine", "To tell a funny story"], "To explain stress and how to manage it"),
                ("Which title best suits this article?", ["Healthy Ways to Handle Stress", "The History of Universities", "How to Become Famous"], "Healthy Ways to Handle Stress"),
            ]],
            write("Activity 17 – Do you agree with the writer? Why?", ["My answer:"], min_words=15),
            cat("Activity 18 – Advice Evaluator. Is each suggestion very helpful, somewhat helpful or not helpful?", {
                "Very Helpful": ["Create a realistic study timetable.", "Talk to someone you trust.", "Eat healthy meals regularly.",
                                 "Exercise for at least thirty minutes several times a week."],
                "Somewhat Helpful": ["Take short breaks while studying."],
                "Not Helpful": ["Stay awake all night to finish your work.", "Ignore your stress and hope it disappears.",
                                "Spend every evening on social media."],
            }, review=True),
            write("Activity 18 – Now explain your choices.", ["My explanation:"], min_words=20),
            write("Activity 19 – Stress Problem Solver. Choose the best solution and explain why. Use: If I were... · may · might · should · because...", [
                "Situation 1: A university student studies until 2.00 a.m. every night.",
                "Situation 2: A friend becomes anxious before every presentation.",
                "Situation 3: Someone spends twelve hours a day using social media.",
                "Situation 4: A student never asks for help because they feel embarrassed.",
            ], min_words=10),
            passage("Reading Passage 2 – Can Body Language Change the Way People See You?", PASSAGE2,
                    "ශරීර භාෂාව මිනිසුන් අතර සන්නිවේදනයේ වැදගත් කොටසකි.\nනමුත් සෑම ඉරියව්වකටම එකම අර්ථයක් නොමැත.\n"
                    "හොඳ සන්නිවේදකයෙක් සම්පූර්ණ තත්ත්වය සලකා බලයි."),
            cat("Activity 20 – Fact, Opinion or Advice? Sort each statement.", {
                "Fact": ["Body language influences communication.", "Eye contact often shows confidence.",
                         "Body language is sometimes misunderstood.", "Good communicators observe carefully."],
                "Opinion": ["Crossed arms always mean anger."],
                "Advice": ["Everyone should smile during conversations.", "Never judge someone too quickly.",
                           "We should consider the whole situation."],
            }, review=True),
            write("Activity 21 – Psychology Detective. What emotion might the person be feeling, and what body language "
                  "supports your answer? Is another interpretation possible?", [
                "A student keeps looking down while answering questions.", "A football player raises both hands after scoring.",
                "A customer smiles while thanking a shop assistant.", "A teenager sits quietly without joining the conversation.",
                "A manager maintains eye contact during a meeting.",
            ], min_words=8),
        ],
        "speaking": [
            heading("Activity 22 – Advice Clinic Role Play"),
            plain("Imagine you are the counsellor. The app plays the person with the problem — listen, then record "
                  "your advice. Use: ✔ If I were you... ✔ You might... ✔ You may... ✔ Have you considered...? "
                  "✔ Why don't you...?"),
            *[speak(f"{topic}: listen to the person, then record your advice. Model:", model, seconds=45, review=True)
              | {"listen": line} for topic, line, model in ROLE_PLAY],
            speak("The person says: “Thank you, that's helpful. Is there anything else I could try?” Record one more piece of advice. Model:",
                  "You might also talk to a friend you trust, because sharing a problem often makes it feel smaller.",
                  seconds=30, review=True) | {"listen": "Thank you, that's helpful. Is there anything else I could try?"},
            heading("Activity 23 – Well-being Debate"),
            plain("Choose one statement: Social media does more harm than good. · Schools should teach stress "
                  "management. · Exercise is the best way to improve mental health. · Everyone should speak openly "
                  "about their emotions. Give your opinion, two reasons, one example and a conclusion."),
            speak("Record your argument. Model:",
                  "In my opinion, schools should teach stress management. First, many students feel stressed before examinations. Second, students who learn healthy habits may also do better in their studies. For example, my school started a short breathing exercise before tests, and it helped me stay calm. In conclusion, I think every school should teach it.",
                  seconds=60, review=True),
            heading("Activity 24 – Life Coach Challenge"),
            speak("Speak for 2–3 minutes. Topic: “What Would You Do to Live a Healthier and Happier Life?”. Include "
                  "physical health, mental well-being, relationships, daily habits, personal goals and advice for "
                  "others. Use at least three Second Conditional and three may/might sentences. Model:",
                  "If I had more time, I would exercise every morning. If I slept eight hours every night, I would feel more energetic. I might also spend less time on my phone, because it may affect my sleep. If I were braver, I would talk about my feelings more often. I may join a sports club to meet new friends. My advice for others is that small changes might make a big difference.",
                  seconds=150, review=True),
        ],
        "writing": [
            plain("Activity 25 – Read the letter.\nDear Advice Clinic,\nI have recently started university, but I find "
                  "it difficult to manage my studies, part-time job and family responsibilities. I feel tired every "
                  "day and I worry that I might fail my exams. I don't know how to organise my time or reduce my "
                  "stress. What should I do?\n— A Worried Student"),
            write("Activity 25 – Advice Column. Write a reply (180–200 words). Include advice, encouragement, the "
                  "Second Conditional, may/might and practical suggestions.", ["Dear Worried Student,"], min_words=180),
            write("Activity 26 – If I Were... Write 180–200 words. Choose ONE topic: Option A – If I Were the Minister "
                  "of Health... · Option B – If I Were a School Counsellor... Include problems, solutions, the Second "
                  "Conditional and your personal ideas.", ["My essay:"], min_words=180),
            write("Activity 27 – Personal Well-being Action Plan. Write your goal and actions for each area.", [
                "Physical Health — my goal / actions:", "Mental Health — my goal / actions:", "Sleep — my goal / actions:",
                "Exercise — my goal / actions:", "Study-Life Balance — my goal / actions:",
                "Social Relationships — my goal / actions:",
            ], min_words=4),
            write("Activity 27 – Now write a reflection (120–150 words). Explain why you chose these goals, which habit "
                  "will be the hardest to change, how these changes may improve your life, and what you would do if "
                  "you lost motivation.", ["My reflection:"], min_words=120),
            plain("LESSON 4 SIGNATURE CHALLENGE – THE ADVICE CLINIC\nYou are the lead counsellor at the “Well-being "
                  "Advice Clinic.” Choose ONE letter.\nCase 1 – The Overworked Student: “I study all day, but my "
                  "grades are getting worse. I sleep only four hours every night and I don't have time to exercise.”\n"
                  "Case 2 – The Shy New Employee: “I've started a new job, but I'm too nervous to speak during "
                  "meetings. I'm worried that people think I'm unfriendly.”\nCase 3 – The Lonely University Student: "
                  "“I moved away from home for university. I miss my family, and I haven't made many friends yet.”"),
            write("Signature Challenge – Write your response. Include at least three Second Conditional sentences, at "
                  "least three sentences with may or might, practical advice and encouragement, and a positive "
                  "concluding message.", ["My response:"], min_words=100),
            self_check(
                "□ I can describe emotions and body language confidently.\n□ I can use the Second Conditional accurately.\n"
                "□ I can use may and might to express possibility.\n□ I can give practical advice in different situations.\n"
                "□ I can identify facts, opinions and advice in a text.\n□ I can discuss mental health and well-being respectfully.\n"
                "□ I can write an advice column.\n□ I can write a reflective essay using hypothetical situations.\n"
                "□ I can express empathy and support others using appropriate English.\n"
                "□ I can confidently communicate about health and well-being.",
                prompt="Self-assessment",
            ),
            summary(["Second Conditional for imaginary situations and advice", "May and might for possibility",
                     "Emotions and body language vocabulary", "Giving advice with “If I were you…”"]),
        ],
    },
}
