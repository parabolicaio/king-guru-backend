"""Level 3 Lesson 5 — Work, Business & Success.

Source: LEVEL_3_L5_individual.docx. Follow-up Part C3–C5 solo lines
applied. Activity 20's ranking was written by the King Guru team, not the
experts (follow-up A7), so it is labelled a suggested ranking and marked
for review. review=True marks keys/models by the King Guru team.
"""
from .dsl import (DISCUSS, cat, examples, heading, interview, mcq, order, passage, phrases, plain,
                  self_check, speak, summary, typed, words, write)

TEXT1 = (
    "After completing her university degree, Amaya started her internship at a software company in Colombo. "
    "Although she was excited, she also felt nervous because it was her first experience in a professional "
    "workplace. On her first morning, the Human Resources Manager welcomed all the new interns and explained "
    "the company's policies. \"You must wear your identification card at all times,\" she said. \"You have to "
    "arrive before 8.30 a.m. every day, and you should inform your supervisor if you are unable to come to "
    "work.\" The manager also explained that teamwork was one of the company's most important values. Each "
    "intern was introduced to a mentor who would guide them during the internship. Amaya's mentor showed her "
    "around the office and introduced her to colleagues from different departments. Later that morning, she "
    "attended her first team meeting. Although she did not speak very much, she listened carefully, took "
    "notes and asked a few questions at the end. During lunch, her colleagues encouraged her to share her "
    "ideas and reminded her that everyone had once been a new employee. By the end of the day, Amaya "
    "realised that confidence grows through experience, preparation and a willingness to learn from others."
)
TEXT2 = (
    "Every Monday morning, the marketing department meets to discuss ongoing projects and set goals for the "
    "week. Today's meeting was led by the department manager, Ms. Fernando. She began by thanking everyone "
    "for completing last week's campaign successfully. Next, she reviewed the agenda and explained the team's "
    "priorities. \"We have to prepare a presentation for our new client before Thursday,\" she said. \"The "
    "design team must finish the promotional materials by Wednesday afternoon, while the marketing team "
    "should complete the customer survey by Tuesday evening.\" During the discussion, one employee suggested "
    "creating a short promotional video for social media. Another colleague recommended inviting customers to "
    "complete an online questionnaire. After listening to everyone's ideas, Ms. Fernando assigned "
    "responsibilities to each team member. Before ending the meeting, she reminded everyone that good "
    "communication and teamwork were the keys to success. The employees left the meeting knowing exactly "
    "what they had to accomplish before the next meeting."
)
PASSAGE1 = (
    "Monday, 14th July\nToday was my first day as a marketing intern at a publishing company. Although I had "
    "been excited for weeks, I felt nervous when I entered the office. Everything seemed new, from the office "
    "layout to the way people communicated during meetings.\n\nMy supervisor welcomed me warmly and "
    "introduced me to the rest of the team. Everyone was friendly, which helped me feel more comfortable.\n\n"
    "My first task was to help prepare promotional materials for a new book launch. At first, I worried that "
    "I might make mistakes, but my mentor reminded me that internships are designed for learning.\n\nDuring "
    "the afternoon meeting, I carefully observed how team members shared ideas and solved problems together. "
    "I noticed that everyone listened respectfully before expressing their opinions.\n\nOne of my colleagues "
    "encouraged me to contribute an idea for the advertising campaign. Although I was nervous, I shared my "
    "suggestion, and the team appreciated my contribution.\n\nWhen I returned home, I realised that "
    "confidence grows through experience. I also understood that asking questions is a strength rather than "
    "a weakness.\n\nTomorrow I hope to participate more actively and continue improving my communication skills."
)
PASSAGE2 = (
    "Many graduates believe that excellent academic results alone are enough to secure a good job. Although "
    "qualifications are important, employers usually look for a combination of technical knowledge, "
    "practical skills and positive attitudes.\n\nOne of the most valued qualities is effective communication. "
    "Employees should be able to express their ideas clearly, listen carefully and work respectfully with "
    "colleagues and clients.\n\nProblem-solving is another important skill. Employers appreciate individuals "
    "who can think critically, suggest creative solutions and remain calm under pressure.\n\nAdaptability has "
    "also become essential in today's workplace. As technology continues to change, employees must be "
    "willing to learn new skills throughout their careers.\n\nLeadership is not only about managing other "
    "people. It also means taking responsibility, supporting teammates and making ethical decisions.\n\n"
    "Finally, employers value honesty, punctuality and reliability. These qualities help create trust and "
    "contribute to a positive working environment.\n\nSuccess is achieved not only through intelligence but "
    "also through continuous learning, teamwork and professionalism."
)

CAREERS = ["Architect", "Software Engineer", "Doctor", "Lecturer", "Accountant", "Journalist",
           "Entrepreneur", "Marketing Executive", "Scientist", "Lawyer"]
WORK_WORDS = ["Meeting", "Feedback", "Report", "Client", "Conference", "Deadline", "Negotiation",
              "Agenda", "Colleague", "Presentation"]


def _pick(answer: str, pool: list[str]) -> list[str]:
    others = [w for w in pool if w != answer]
    i = pool.index(answer)
    return [answer, others[(i + 2) % len(others)], others[(i + 5) % len(others)]]


LESSON = {
    "order": 5,
    "title": "Work, Business & Success",
    "title_si": "රැකියාව, ව්‍යාපාර සහ සාර්ථකත්වය",
    "description": "Talk about careers and workplace rules with modals of obligation, gerunds and infinitives (B1).",
    "objectives": [
        "Describe different jobs, careers and workplace responsibilities",
        "Use modals of obligation appropriately (must, have to, should, mustn't, don't have to)",
        "Distinguish between gerunds and infinitives in common contexts",
        "Discuss career ambitions and professional goals confidently",
        "Take part in workplace discussions and meetings",
        "Write professional emails and short workplace communications",
        "Present future career plans using appropriate language",
    ],
    "sections": {
        "vocabulary": [
            words("A. Jobs and Careers", [
                ("Profession", "වෘත්තිය"), ("Occupation", "රැකියාව"), ("Career", "වෘත්තීය ජීවිතය"),
                ("Qualification", "සුදුසුකම"), ("Experience", "පළපුරුද්ද"), ("Internship", "පුහුණු සේවය"),
                ("Promotion", "උසස්වීම"), ("Vacancy", "පුරප්පාඩුව"), ("Responsibility", "වගකීම"),
                ("Productivity", "ඵලදායිතාව"), ("Leadership", "නායකත්වය"), ("Entrepreneur", "ව්‍යවසායකයා"),
            ]),
            *[mcq(f"Activity 3 – Career Explorer: {s}", _pick(a, CAREERS), a, review=True) for s, a in [
                ("This person designs buildings and supervises construction projects.", "Architect"),
                ("This person develops computer software and mobile applications.", "Software Engineer"),
                ("This professional treats patients and diagnoses illnesses.", "Doctor"),
                ("This person teaches students at a university.", "Lecturer"),
                ("This person manages a company's financial records.", "Accountant"),
                ("This professional reports news to the public.", "Journalist"),
                ("This person starts and manages their own business.", "Entrepreneur"),
                ("This professional creates advertisements and marketing campaigns.", "Marketing Executive"),
                ("This person conducts scientific experiments.", "Scientist"),
                ("This professional provides legal advice.", "Lawyer"),
            ]],
            write(f"Activity 3 – {DISCUSS}", [
                "Which careers require teamwork?", "Which careers require creativity?",
                "Which careers require strong communication skills?",
            ], min_words=5),
            write("Activity 4 – Career Path Planner. Choose one: Teacher, Software Engineer, Doctor, Business Owner, "
                  "Lawyer, Environmental Scientist, Graphic Designer or Journalist. Complete the chart.", [
                "The career I chose:", "Education:", "Skills I Need:", "Experience I Should Gain:",
                "Challenges I May Face:", "How I Will Overcome Them:",
            ], min_words=2),
            speak("Activity 4 – Now record a 30-second explanation of your plan. Model:",
                  "I want to become a software engineer. First, I have to complete a degree in computer science. I need programming and teamwork skills, so I should do an internship. A challenge may be learning new technology quickly, but I will practise every day.",
                  seconds=30, review=True),
            words("B. Workplace Communication", [
                ("Deadline", "අවසන් දිනය"), ("Meeting", "රැස්වීම"), ("Agenda", "න්‍යාය පත්‍රය"),
                ("Presentation", "ඉදිරිපත් කිරීම"), ("Feedback", "ප්‍රතිචාර"), ("Report", "වාර්තාව"),
                ("Client", "සේවාදායකයා"), ("Department", "අංශය"), ("Colleague", "සහකාර සේවකයා"),
                ("Manager", "කළමනාකරු"), ("Negotiation", "සාකච්ඡාව"), ("Conference", "සම්මන්ත්‍රණය"),
            ]),
            *[mcq(f"Activity 5 – Workplace Detective: {s}", _pick(a, WORK_WORDS), a, review=True) for s, a in [
                ("Your team meets every Monday to discuss weekly tasks.", "Meeting"),
                ("Your manager gives comments on your presentation.", "Feedback"),
                ("You prepare a document explaining the progress of a project.", "Report"),
                ("A customer requests information about your company's services.", "Client"),
                ("Employees from different countries attend a business event.", "Conference"),
                ("Your supervisor asks you to finish your work before Friday.", "Deadline"),
                ("Two companies discuss the details of a business agreement.", "Negotiation"),
                ("Your team leader explains what will be discussed during the meeting.", "Agenda"),
                ("You work with people from your own office.", "Colleague"),
                ("Your manager asks your department to present next month's plan.", "Presentation"),
            ]],
            cat("Activity 6 – Workplace Decision Maker. You have just started working in a company. Which actions show professionalism?", {
                "Professional": ["Arriving on time", "Respecting deadlines", "Listening during meetings",
                                 "Asking questions politely", "Working well in a team", "Giving constructive feedback",
                                 "Completing tasks carefully", "Accepting responsibility for mistakes"],
                "Needs Improvement": ["Ignoring emails", "Interrupting colleagues"],
            }, review=True),
            write(f"Activity 6 – {DISCUSS}", [
                "Which professional behaviour is the most important in a workplace? Explain your opinion.",
            ], min_words=15),
        ],
        "grammar": [
            heading("Review Corner"),
            plain("From Lesson 4: ✔ Second Conditional ✔ May / Might ✔ Giving Advice ✔ Emotions and Well-being "
                  "✔ Body Language\nExamples: If I were you, I would prepare well before an interview. · You might "
                  "feel nervous on your first day at work.\nToday we move from giving advice to communicating "
                  "professionally in the workplace."),
            write("Activity 1 – Workplace Advice Challenge. For each situation: what should the person do, what might "
                  "happen if they do not change, and if you were the manager, what would you advise?", [
                "A new employee arrives late every morning.", "A team member never replies to emails.",
                "An intern forgets to attend meetings.", "A colleague interrupts others during discussions.",
                "An employee misses an important deadline.", "A new graduate feels nervous before their first presentation.",
                "A worker has too much work and feels overwhelmed.", "A manager notices that teamwork is poor.",
            ], min_words=10),
            write(f"Activity 2 – Career Reflection. {DISCUSS}", [
                "What career would you like to have in the future?", "Which personal qualities are important in your dream job?",
                "Would you prefer working alone or in a team? Why?", "What skills do employers value today?",
                "What motivates people to work hard?", "How can young people prepare for successful careers?",
                "Is earning a high salary the most important part of a job? Why or why not?", "What does success mean to you?",
            ], min_words=5),
            heading("Modals of Obligation"),
            plain("We use must, have to, should, mustn't, and don't have to to talk about rules, responsibilities, "
                  "obligations and advice."),
            examples("Modal · Use · Example", [
                "Must — Strong obligation — Employees must wear their ID cards.",
                "Have to — Necessary obligation — I have to attend the weekly meeting.",
                "Should — Advice — You should arrive early for interviews.",
                "Mustn't — Prohibition — Employees mustn't share confidential information.",
                "Don't have to — No obligation — You don't have to wear formal clothes every Friday.",
            ]),
            plain("Sinhala Help\nYou must wear your ID card.\n→ ඔබ ඔබගේ හැඳුනුම්පත පැළඳිය යුතුය.\n"
                  "Employees mustn't share confidential information.\n→ සේවකයින් රහස්‍ය තොරතුරු බෙදා නොගත යුතුය."),
            *[mcq(f"Activity 7 – Office Rules Challenge: {s}", o, a, review=True) for s, o, a in [
                ("Employees ______ respect all clients.", ["must", "mustn't", "don't have to"], "must"),
                ("Staff ______ arrive at least ten minutes before meetings.", ["should", "mustn't", "don't have to"], "should"),
                ("Visitors ______ enter restricted areas without permission.", ["mustn't", "have to", "should"], "mustn't"),
                ("Employees ______ complete safety training before starting work.", ["have to", "mustn't", "don't have to"], "have to"),
                ("Team members ______ interrupt others during presentations.", ["mustn't", "must", "have to"], "mustn't"),
                ("Workers ______ wear protective equipment in the laboratory.", ["must", "don't have to", "mustn't"], "must"),
                ("Employees ______ check emails after office hours unless it is an emergency.", ["don't have to", "must", "have to"], "don't have to"),
                ("Staff ______ inform their manager if they are unable to attend work.", ["must", "mustn't", "don't have to"], "must"),
                ("Everyone ______ treat colleagues with respect.", ["should", "mustn't", "don't have to"], "should"),
                ("Employees ______ use company computers for illegal activities.", ["mustn't", "should", "have to"], "mustn't"),
            ]],
            write(f"Activity 7 – {DISCUSS}", ["Which workplace rule do you think is the most important? Why?"], min_words=15),
            write("Activity 8 – Career Launch Mission. You have received a job offer from an international company. "
                  "Before accepting the job, identify:", [
                "Three responsibilities you must perform:", "Two things you don't have to do:",
                "Two pieces of advice someone should give you:", "One thing you mustn't do in your new workplace:",
            ], min_words=5),
            speak("Activity 8 – Record a one-minute summary of your ideas. Model:",
                  "In my new job, I must arrive on time, finish my reports and attend the weekly meetings. I don't have to work at weekends or wear a suit every day. My manager should tell me to ask questions and to plan my week. I mustn't share confidential information.",
                  seconds=60, review=True),
            heading("Gerunds & Infinitives"),
            plain("Some verbs are followed by gerunds (-ing), while others are followed by infinitives (to + verb)."),
            examples("Verb · Structure · Example", [
                "Enjoy — Verb + Gerund — I enjoy working in a team.", "Avoid — Verb + Gerund — She avoids arriving late.",
                "Finish — Verb + Gerund — They finished preparing the report.", "Hope — Verb + Infinitive — He hopes to become a manager.",
                "Decide — Verb + Infinitive — We decided to apply for the internship.",
                "Want — Verb + Infinitive — She wants to improve her leadership skills.",
            ]),
            plain("Sinhala Help\nI enjoy working with people.\n→ මම මිනිසුන් සමඟ වැඩ කිරීම රසවිඳිනවා.\n"
                  "She hopes to become a lawyer.\n→ ඇය නීතිඥවරියක් වීමට බලාපොරොත්තු වෙනවා."),
            *[typed(f"Activity 15 – Career Choices: {s}", a, review=True) for s, a in [
                ("I hope __________ (become) a successful entrepreneur.", ["to become"]),
                ("My sister enjoys __________ (work) with children.", ["working"]),
                ("They decided __________ (apply) for the internship programme.", ["to apply"]),
                ("He avoids __________ (arrive) late to meetings.", ["arriving"]),
                ("Our manager encouraged us __________ (share) new ideas.", ["to share"]),
                ("She finished __________ (prepare) the presentation before lunch.", ["preparing"]),
                ("I want __________ (improve) my communication skills.", ["to improve"]),
                ("We practised __________ (answer) interview questions.", ["answering"]),
                ("They agreed __________ (meet) the client next Monday.", ["to meet"]),
                ("My colleague suggested __________ (organise) another team meeting.", ["organising", "organizing"]),
            ]],
            write("Activity 16 – Career Launch Lab. You have graduated and are planning your future career. Complete the chart.", [
                "Dream Career:", "Why do you want this career?", "What qualifications do you need?",
                "What skills do you enjoy developing?", "What skills do you hope to improve?",
                "What responsibilities will you have?", "What challenges might you face?", "How will you overcome them?",
            ], min_words=2),
            speak("Activity 16 – Now record a one-minute presentation of your career plan using must, should, have to, "
                  "gerunds and infinitives. Model:",
                  "I hope to become an architect because I enjoy designing buildings. I have to complete my degree first, and I should improve my communication and leadership skills.",
                  seconds=60),
        ],
        "pronunciation": [
            phrases("Listen and Repeat", [
                ("Profession", "ප්‍රෆෙෂන්"), ("Qualification", "ක්වොලිෆිකේෂන්"), ("Responsibility", None),
                ("Internship", None), ("Entrepreneur", "ඔන්ට්‍රප්‍රනර්"), ("Productivity", None),
                ("Presentation", None), ("Negotiation", "නිගෝෂියේෂන්"), ("Conference", None), ("Colleague", "කොලීග්"),
            ]),
            plain("Common Pronunciation Problems\nEntrepreneur — ❌ එන්ට්‍රප්‍රෙනියර් ✅ ඔන්ට්‍රප්‍රනර්\n"
                  "Colleague — ❌ කොලීගු ✅ කොලීග්\nQualification — ❌ ක්වාලිෆිකේෂන් ✅ ක්වොලිෆිකේෂන්"),
            *[speak("Tap & Speak: say the word clearly.", w, seconds=5) for w in [
                "Profession", "Qualification", "Responsibility", "Internship", "Entrepreneur", "Productivity",
                "Presentation", "Negotiation", "Conference", "Colleague"]],
            heading("Sentence Stress Practice"),
            *[speak(f"Say the sentence. Stress the words in capitals: {s}", t, seconds=10) for s, t in [
                ("Employees MUST respect workplace rules.", "Employees must respect workplace rules."),
                ("You SHOULD prepare before every meeting.", "You should prepare before every meeting."),
                ("I HAVE TO finish this report today.", "I have to finish this report today."),
                ("Successful teams WORK TOGETHER effectively.", "Successful teams work together effectively."),
            ]],
        ],
        "listening": [
            plain("LISTENING TIP\nWhen listening in workplace situations:\n✔ Listen for the main purpose of the "
                  "conversation.\n✔ Identify responsibilities and deadlines.\n✔ Listen for instructions and suggestions.\n"
                  "✔ Pay attention to words that express obligation such as must, have to, should, mustn't.\n"
                  "✔ Listen for opinions, agreements and decisions made during meetings."),
            heading("Listening Text 1 – My First Day at Work"),
            *[mcq(f"Activity 9 – {q}", o, a, listen=TEXT1) for q, o, a in [
                ("Where did Amaya begin her internship?", ["A software company", "A hospital", "A school"], "A software company"),
                ("Why was she nervous?", ["It was her first professional job.", "She was late.", "She did not know English."], "It was her first professional job."),
                ("Who welcomed the new interns?", ["The Human Resources Manager", "The company director", "A client"], "The Human Resources Manager"),
                ("What must employees wear?", ["Their identification card", "A company cap", "A uniform jacket"], "Their identification card"),
                ("What should employees do if they cannot attend work?", ["Inform their supervisor", "Stay at home without telling anyone", "Ask a colleague to explain later"], "Inform their supervisor"),
                ("What important workplace value did the manager mention?", ["Teamwork", "Competition", "Independence"], "Teamwork"),
                ("Who helped Amaya during her internship?", ["A mentor", "A customer", "A teacher"], "A mentor"),
                ("What did Amaya do during the meeting?", ["She listened carefully and took notes.", "She left early.", "She gave a long presentation."], "She listened carefully and took notes."),
                ("What advice did her colleagues give?", ["Share your ideas confidently.", "Avoid asking questions.", "Work alone."], "Share your ideas confidently."),
                ("What did Amaya learn by the end of the day?", ["Confidence develops through experience.", "Internships are easy.", "Meetings are unnecessary."], "Confidence develops through experience."),
            ]],
            write("Activity 10 – Workplace Notes. Complete the orientation notes.", [
                "Company:", "Employee Rules:", "Arrival Time:", "Who supports the interns?",
                "Important Workplace Value:", "One Lesson Amaya Learned:",
            ], min_words=1, listen=TEXT1, models=[
                "A software company in Colombo",
                "Wear your ID card at all times, arrive before 8.30 a.m., and inform your supervisor if you are absent.",
                "Before 8.30 a.m.", "A mentor", "Teamwork",
                "Confidence grows through experience, preparation and learning from others.",
            ], review=True),
            cat("Activity 11 – Workplace Responsibilities. Listen again. Is each responsibility a must, a should or a don't have to?", {
                "Must": ["Wear an ID card", "Work well with others"],
                "Should": ["Inform your supervisor if absent", "Share ideas during meetings"],
                "Have to": ["Arrive before 8.30 a.m."],
                "Don't Have To": ["Know everything on the first day"],
            }, review=True) | {"listen": TEXT1},
            write(f"Activity 11 – {DISCUSS}", [
                "Which responsibility do you think is the most important for a new employee? Explain your answer.",
            ], min_words=15, listen=TEXT1),
            write("Activity 12 – Career Coach. Imagine you are Amaya's mentor. Write five pieces of professional advice "
                  "for her first month and explain why each is important. Use: You should... · You must... · You "
                  "don't have to... · It is important to...",
                  ["Advice 1:", "Advice 2:", "Advice 3:", "Advice 4:", "Advice 5:"], min_words=8, listen=TEXT1),
            heading("Listening Text 2 – The Weekly Team Meeting"),
            *[mcq(f"Activity 13 – {q}", o, a, listen=TEXT2) for q, o, a in [
                ("Which department held the meeting?", ["Marketing", "Finance", "Human Resources"], "Marketing"),
                ("Who led the meeting?", ["Ms. Fernando", "The company owner", "A customer"], "Ms. Fernando"),
                ("What did the manager discuss first?", ["Last week's achievements", "Employee salaries", "Holiday plans"], "Last week's achievements"),
                ("What did the team have to prepare?", ["A presentation", "A report card", "A training course"], "A presentation"),
                ("Which team had to finish promotional materials?", ["The design team", "Finance", "Sales"], "The design team"),
                ("What suggestion was made?", ["Create a promotional video", "Hire new employees", "Change the manager"], "Create a promotional video"),
                ("What did another employee recommend?", ["An online customer questionnaire", "Buying new computers", "Changing offices"], "An online customer questionnaire"),
                ("What did Ms. Fernando do after the discussion?", ["Assigned responsibilities", "Cancelled the project", "Ended the meeting immediately"], "Assigned responsibilities"),
                ("According to the manager, what leads to success?", ["Teamwork and communication", "Working alone", "Long meetings"], "Teamwork and communication"),
                ("How did employees feel after the meeting?", ["They clearly understood their responsibilities.", "They were confused.", "They wanted another meeting."], "They clearly understood their responsibilities."),
            ]],
            write("Activity 14 – Meeting Minutes. Complete the meeting notes.", [
                "Meeting:", "Manager:", "Main Project:", "Deadline:", "Suggestions Made:",
                "Responsibilities Assigned:", "Key Message:",
            ], min_words=1, listen=TEXT2, models=[
                "Weekly marketing team meeting (Monday)", "Ms. Fernando", "A presentation for the new client",
                "Before Thursday (materials by Wednesday afternoon, survey by Tuesday evening)",
                "A short promotional video for social media; an online customer questionnaire",
                "The design team: promotional materials. The marketing team: the customer survey.",
                "Good communication and teamwork are the keys to success.",
            ], review=True),
        ],
        "reading": [
            plain("READING TIP\nWhen reading workplace texts:\n✔ Identify the purpose of the document.\n✔ Recognise "
                  "professional language.\n✔ Distinguish between facts, opinions and recommendations.\n✔ Notice how "
                  "problems are solved.\n✔ Think about how the information can be applied in real workplaces."),
            passage("Reading Passage 1 – My First Internship (Diary Entry)", PASSAGE1,
                    "මෙය නව පුහුණු සේවකයෙකුගේ පළමු දින දිනපොතකි.\nඔහු නව කාර්යාලයක සේවය ආරම්භ කර නව අත්දැකීම් ලබා ගනී.\n"
                    "අදහස් බෙදා ගැනීම, කණ්ඩායම් වැඩ සහ විශ්වාසය වෘත්තීය ජීවිතයේ වැදගත් බව ඔහු ඉගෙන ගනී."),
            *[mcq(f"Activity 17 – {q}", o, a, review=True) for q, o, a in [
                ("Where did the writer begin the internship?", ["At a publishing company", "At a hospital", "At a bank"], "At a publishing company"),
                ("Why did the writer feel nervous?", ["Everything in the office seemed new", "He was very late", "He did not like the team"], "Everything in the office seemed new"),
                ("How did the supervisor help the writer?", ["She welcomed him warmly and introduced him to the team", "She gave him a holiday", "She did his work for him"], "She welcomed him warmly and introduced him to the team"),
                ("What was the writer's first task?", ["Helping prepare promotional materials for a book launch", "Writing a novel", "Cleaning the office"], "Helping prepare promotional materials for a book launch"),
                ("What advice did the mentor give?", ["Internships are designed for learning", "Never make mistakes", "Work alone"], "Internships are designed for learning"),
                ("What did the writer observe during the meeting?", ["Everyone listened respectfully before giving opinions", "People shouted at each other", "Nobody spoke"], "Everyone listened respectfully before giving opinions"),
                ("Why was sharing an idea important?", ["The team appreciated his contribution and he gained confidence", "It ended the meeting", "It made the manager angry"], "The team appreciated his contribution and he gained confidence"),
                ("What lesson did the writer learn at the end of the day?", ["Asking questions is a strength, not a weakness", "Internships are a waste of time", "Meetings are boring"], "Asking questions is a strength, not a weakness"),
                ("Which qualities helped the writer succeed?", ["Listening, courage and willingness to learn", "Speed and silence", "Luck only"], "Listening, courage and willingness to learn"),
            ]],
            write("Activity 17 – If you were the intern, what would you have done differently?", ["My answer:"], min_words=15),
            write("Activity 18 – Workplace Reflection. For each situation write what happened and what we can learn.", [
                "First day at work:", "Meeting participation:", "Receiving feedback:", "Teamwork:", "Asking questions:",
                "Which professional skill is the most important during an internship? Explain your answer.",
            ], min_words=5),
            cat("Activity 19 – Professional Behaviour Evaluation. Is each behaviour professional or unprofessional?", {
                "Professional": ["Arriving at work on time.", "Asking for clarification when unsure.",
                                 "Completing tasks before deadlines.", "Respecting different opinions.",
                                 "Accepting constructive feedback positively.", "Taking responsibility for mistakes."],
                "Unprofessional": ["Ignoring emails from colleagues.", "Interrupting others during meetings.",
                                   "Sharing confidential company information online.", "Refusing to work with team members."],
            }, review=True),
            write("Activity 19 – Now explain why the unprofessional behaviours should be avoided.", ["My explanation:"], min_words=20),
            passage("Reading Passage 2 – What Employers Really Want", PASSAGE2,
                    "සේවායෝජකයන් සුදුසුකම් පමණක් නොව, සන්නිවේදනය, කණ්ඩායම් වැඩ, ගැටලු විසඳීම සහ වගකීමද අගය කරයි.\n"
                    "සාර්ථකත්වය ලබා ගැනීමට නිරන්තර ඉගෙනීම සහ වෘත්තීය ආකල්ප වැදගත් වේ."),
            write("Activity 20 – Skill Ranking Challenge. Work on your own. Rank these workplace skills from 1 (most "
                  "important) to 8 (least important): Communication, Teamwork, Leadership, Creativity, "
                  "Problem-solving, Adaptability, Honesty, Time Management. Then explain why you placed each skill "
                  "where you did.", ["My ranking:", "My reasons:"], min_words=8),
            order("Activity 20 – Now put the skills in the suggested ranking (to be confirmed by our experts), then "
                  "compare it with yours.", [
                "Communication", "Problem-solving", "Teamwork", "Adaptability", "Time Management", "Honesty",
                "Leadership", "Creativity",
            ], review=True),
            write("Activity 20 – Explain the differences between your order and the suggested ranking.", ["My explanation:"], min_words=15),
            cat("Activity 21 – Fact, Opinion or Recommendation? Sort each statement.", {
                "Fact": ["Employers value communication skills.", "Problem-solving is an important workplace skill.",
                         "Honesty creates trust.", "Adaptability is becoming more important."],
                "Opinion": ["Leadership is only for managers.", "Qualifications are the only requirement for success."],
                "Recommendation": ["Every employee should continue learning.", "Employees should arrive on time."],
            }, review=True),
        ],
        "speaking": [
            heading("Activity 22 – Mock Job Interview"),
            *interview(
                "The app is the interviewer. Each question appears on screen and is played as audio. Record your "
                "answer, then compare it with the model answer, useful expressions and key vocabulary.",
                [
                    ("Tell me about yourself.", "My name is …, and I have recently completed my studies. I am hard-working, reliable, and enjoy working with people."),
                    ("Why are you interested in this position?", "I am interested in this position because it matches my skills and gives me a chance to grow in this field."),
                    ("What are your greatest strengths?", "My greatest strengths are communication and problem-solving. I stay calm under pressure and finish my work on time."),
                    ("Describe a challenge you have overcome.", "Once I had to complete a project with a short deadline. I planned my time carefully and asked for help, and I finished it successfully."),
                    ("How do you work in a team?", "I work well in a team. I listen to others, share my ideas, and support my colleagues to reach our goal."),
                    ("What skills would you like to improve?", "I would like to improve my public-speaking and leadership skills so I can present my ideas more confidently."),
                    ("Where do you see yourself in five years?", "In five years, I see myself in a more senior role, leading a small team and still learning new skills."),
                    ("Why should we hire you?", "You should hire me because I am motivated, reliable, and a fast learner who will add value to your team."),
                ],
                expressions=["My strengths are …", "I have experience in …", "I am good at …", "I would like to …",
                             "In five years, I hope to …"],
                vocabulary=["strengths", "teamwork", "reliable", "motivated", "deadline", "confident", "experience"],
            ),
            heading("Activity 23 – Workplace Problem-Solving"),
            plain("For each situation: identify the problem, suggest two solutions and explain which is the most "
                  f"effective. Use must, should, have to, may and might. {DISCUSS}"),
            *[speak(f"Activity 23 – {s} Model:", m, seconds=45, review=True) for s, m in [
                ("Situation 1: Two colleagues disagree about how to complete an important project.",
                 "The problem is a disagreement. They should listen to each other's ideas, or the manager might help them choose. I think talking calmly is the most effective solution."),
                ("Situation 2: An employee regularly misses deadlines.",
                 "The employee has to plan their time better. The manager should check their workload, and they may need training. A weekly plan might work best."),
                ("Situation 3: A team member refuses to participate during meetings.",
                 "The team member may feel shy. The leader should ask for their opinion directly, or they might share ideas by email first."),
                ("Situation 4: A new intern feels too nervous to ask questions.",
                 "The intern must understand that questions are welcome. A mentor should meet them every day, which might help them feel more confident."),
            ]],
            heading("Activity 24 – Elevator Pitch"),
            speak("You are at a career fair and have one minute to introduce yourself to an employer. Include your "
                  "education, skills, strengths, career goals and why you would be a valuable employee. Speak "
                  "confidently. Model:",
                  "Hello, my name is Kasun. I have a degree in business management from the University of Colombo. I am good at communication and teamwork, and I enjoy solving problems. My goal is to become a marketing manager. I would be a valuable employee because I am reliable, I learn quickly and I always finish my work on time.",
                  seconds=60, review=True),
        ],
        "writing": [
            write("Activity 25 – Professional Email. Write an email (150–180 words). You recently attended a job "
                  "interview for an internship. Write a follow-up email to thank the interviewer. Include your "
                  "appreciation for the opportunity, your continued interest, a summary of why you are suitable and "
                  "a polite closing.", ["Dear …,"], min_words=150),
            write("Activity 26 – My Five-Year Career Plan. Write 180–200 words. Include your dream career, educational "
                  "goals, skills you hope to develop, challenges you may face and how you plan to overcome them. Use "
                  "modals of obligation, gerunds, infinitives and career vocabulary.", ["My plan:"], min_words=180),
            write("Activity 27 – Career Launch Lab (Final Mission). You have graduated and received your first job "
                  "offer. Complete the missions.", [
                "Mission 1 – Accept the Job: write three responsibilities you will have.",
                "Mission 2 – Your First Week: list five workplace goals.",
                "Mission 3 – Professional Development: identify three new skills you want to learn.",
                "Mission 4 – Solving a Workplace Problem: one colleague is struggling to complete their tasks. Explain how you would help them.",
            ], min_words=10),
            write("Mission 5 – Looking Ahead. Write a short reflection (120–150 words): “What kind of professional do I want to become?”",
                  ["My reflection:"], min_words=120),
            plain("LESSON 5 SIGNATURE CHALLENGE – CAREER LAUNCH LAB\nYou have been selected as a graduate trainee at "
                  "an international company. Complete your Career Launch Portfolio."),
            write("Signature Challenge – Portfolio tasks.", [
                "Task 1: Write a short self-introduction for your manager.",
                "Task 2: Reply to a workplace email confirming your attendance at a meeting.",
                "Task 3: Prepare a one-minute presentation introducing your career goals.",
                "Task 4: Explain how you would solve a workplace conflict between two colleagues.",
                "Task 5: Write a personal reflection describing the kind of professional you hope to become.",
                "Final Reflection: “Success at work is not only about getting a good job; it is also about...” "
                "Support your answer with examples from your own goals and experiences.",
            ], min_words=15),
            self_check(
                "□ I can describe different careers and workplace responsibilities.\n"
                "□ I can use must, have to, should, mustn't and don't have to correctly.\n"
                "□ I can distinguish between gerunds and infinitives.\n□ I can discuss career ambitions confidently.\n"
                "□ I can participate in workplace meetings and interviews.\n"
                "□ I can identify professional and unprofessional workplace behaviour.\n□ I can write professional emails.\n"
                "□ I can plan my future career using appropriate English.\n"
                "□ I can communicate confidently in common workplace situations.\n□ I can apply professional English in realistic contexts.",
                prompt="Self-assessment",
            ),
            summary(["Modals of obligation: must, have to, should, mustn't, don't have to", "Gerunds and infinitives",
                     "Career and workplace vocabulary", "Job interviews and professional emails"]),
        ],
    },
}
