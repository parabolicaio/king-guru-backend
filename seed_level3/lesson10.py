"""Level 3 Lesson 10 — My World Today & My Future (capstone review).

Source: LEVEL_3_L10_individual.docx (answer keys from the file).
Follow-up A21: Activity 23 is individual planning. review=True marks
keys/models by the King Guru team.
"""
from .dsl import (cat, heading, interview, match, mcq, order, passage, phrases, plain, self_check, speak,
                  summary, tf, typed, write)

TEXT1 = (
    "Hello everyone. My name is Nadeesha, and I recently graduated from university. Looking back, I realise how "
    "much my life has changed over the last few years. When I was a first-year student, I used to spend most of "
    "my free time with friends and rarely thought about my future career. However, as I progressed through "
    "university, I became more interested in technology, communication and professional development. Last "
    "year, I completed an internship at an international company. At first, I was nervous because it was my "
    "first professional experience. However, my colleagues were supportive, and I quickly learned how to work "
    "as part of a team. Now, I work as a marketing assistant while continuing my studies. My job has helped me "
    "improve my communication skills and confidence. In the future, I hope to complete a master's degree and "
    "work with people from different countries. I believe that learning never stops. Every experience teaches "
    "us something valuable, and every challenge helps us become stronger."
)
TEXT2 = (
    "Our town has changed significantly over the past ten years. New schools, hospitals and public parks have "
    "improved the quality of life for many residents. However, some challenges still remain. Traffic congestion "
    "has increased because more people own private vehicles. Environmental groups have suggested planting more "
    "trees, improving public transport and creating bicycle lanes to reduce pollution. Young people have also "
    "started volunteering in community projects. They organise recycling campaigns, clean public spaces and "
    "educate children about protecting the environment. The local council plans to introduce smart technology "
    "to improve traffic management and public services in the near future. Everyone believes that small "
    "actions can create a better community for future generations."
)
PASSAGE1 = (
    "Over the past twenty years, the world has changed dramatically. Technology has transformed the way people "
    "communicate, work and learn. Today, students can attend online classes, professionals can work remotely, "
    "and families can stay connected through video calls regardless of where they live.\n\nAt the same time, "
    "many countries face global challenges such as climate change, pollution and rapid urbanisation. "
    "Governments, businesses and individuals are working together to develop cleaner energy sources, improve "
    "public transport and protect natural resources. These efforts aim to create healthier and more sustainable "
    "communities.\n\nEducation has also changed significantly. Instead of depending only on textbooks, learners "
    "now have access to digital libraries, language-learning applications and online courses. These tools allow "
    "people to continue learning throughout their lives and prepare for careers that may not even exist today.\n\n"
    "Although change can sometimes be challenging, it also creates new opportunities. People who are adaptable, "
    "willing to learn and open to different cultures are more likely to succeed in an increasingly connected world."
)
PASSAGE2 = (
    "When I think about my future, I feel both excited and curious. By 2035, I hope to have completed my "
    "education and established a successful career in a field that allows me to make a positive contribution to "
    "society.\n\nI would like to work in an international environment where I can communicate with people from "
    "different cultures and continue improving my English. I also hope to travel to several countries to learn "
    "about their traditions, architecture and ways of life.\n\nIn my personal life, maintaining a healthy "
    "work-life balance will be important. I want to exercise regularly, spend time with my family and continue "
    "learning new skills throughout my life. I believe that lifelong learning is one of the keys to personal and "
    "professional success.\n\nI also hope to contribute to my community by participating in environmental "
    "projects and encouraging others to protect natural resources. Small actions, such as recycling and reducing "
    "waste, can make a significant difference.\n\nAlthough I know the future is unpredictable, I believe that "
    "determination, hard work and a positive attitude will help me achieve my goals."
)

LESSON = {
    "order": 10,
    "title": "My World Today & My Future",
    "title_si": "අද මගේ ලෝකය සහ මගේ අනාගතය",
    "description": "Level 3 capstone: review the grammar and topics of Lessons 1–9 and plan your future (B1).",
    "objectives": [
        "Integrate grammar and vocabulary from Lessons 1–9 in spoken and written communication",
        "Express opinions, experiences and future plans with confidence",
        "Apply a variety of grammar structures accurately in meaningful contexts",
        "Demonstrate comprehension of authentic reading and listening texts",
        "Take part confidently in discussions, interviews and debates",
        "Produce connected paragraphs and short multi-paragraph texts",
        "Demonstrate readiness to progress to the Upper-Intermediate level",
    ],
    "sections": {
        "vocabulary": [
            heading("Level 3 Vocabulary Review"),
            *[mcq("Activity 4 – Vocabulary Mission. Choose the odd one out.", o, a) for o, a in [
                (["Museum", "Temple", "Library", "Password"], "Password"),
                (["Budget", "Warranty", "Receipt", "Volleyball"], "Volleyball"),
                (["Pollution", "Recycling", "Conservation", "Tournament"], "Tournament"),
                (["Coach", "Referee", "Spectator", "Apartment"], "Apartment"),
                (["Bridge", "Monument", "Heritage Site", "Recipe"], "Recipe"),
                (["Research", "Laboratory", "Scientist", "Marketplace"], "Marketplace"),
            ]],
            cat("Activity 5 – Build the Theme. Put each word in the correct category.", {
                "Health": ["Fitness", "Meditation"], "Cities": ["Architecture", "Infrastructure", "Tourism"],
                "Shopping": ["Budget", "Customer Review", "Recipe"], "Work": ["Career"],
                "Environment": ["Recycling"], "Technology": ["Innovation", "Technology"],
            }),
            *[typed(f"Activity 6 – Quick Challenge. Use one word from the box (heritage, budget, innovation, fitness, career, community): {s}", [a])
              for s, a in [
                ("Regular exercise improves your __________.", "fitness"),
                ("We should protect our cultural __________.", "heritage"),
                ("The company introduced a new __________ to reduce pollution.", "innovation"),
                ("She carefully planned her monthly __________.", "budget"),
                ("Teaching is a rewarding __________.", "career"),
                ("Everyone should contribute to their __________.", "community"),
            ]],
            match("Activity 2 – Which Lesson Does It Belong To?", [
                ("I have visited many historical places.", "Lesson 2 – Travel & Culture"),
                ("If everyone recycled more, pollution would decrease.", "Lesson 3 – Environment"),
                ("This article was published yesterday.", "Lesson 6 – Technology"),
                ("The backpack offers good value for money.", "Lesson 7 – Consumerism"),
                ("Yoga helps reduce stress.", "Lesson 8 – Sports & Lifestyle"),
                ("The museum attracts thousands of tourists.", "Lesson 9 – Cities & Tourism"),
                ("A good employee should be punctual.", "Lesson 5 – Work & Business"),
            ]),
        ],
        "grammar": [
            heading("Review Corner"),
            plain("Grammar reviewed in Level 3: ✔ Present Perfect ✔ Past Simple ✔ Narrative Tenses ✔ First "
                  "Conditional ✔ Second Conditional ✔ Relative Clauses ✔ Passive Voice ✔ Gerunds & Infinitives "
                  "✔ Modals ✔ Comparatives"),
            *[mcq(f"Activity 1 – Grammar Master Challenge: {s}", o, a) for s, o, a in [
                ("I ______ to Kandy several times.", ["visited", "have visited", "visiting", "visit"], "have visited"),
                ("Last December we ______ Galle Fort.", ["have visited", "visited", "visit", "visiting"], "visited"),
                ("While we ______ around the museum, our guide explained the history.", ["walked", "were walking", "have walked", "walk"], "were walking"),
                ("If people recycle more, ...", ["pollution decreases yesterday", "pollution will decrease", "pollution decrease", "pollution has decreased tomorrow"], "pollution will decrease"),
                ("If I were the mayor, ...", ["I improve public transport.", "I would improve public transport.", "I improved public transport.", "I improving public transport."], "I would improve public transport."),
                ("This bridge ______ in 2023.", ["built", "was built", "build", "building"], "was built"),
                ("I enjoy ______ English.", ["learn", "learning", "learned", "learns"], "learning"),
                ("Employees ______ arrive on time.", ["should", "should to", "should be", "should arriving"], "should"),
                ("Colombo is ______ than my hometown.", ["busy", "busier", "busiest", "more busier"], "busier"),
                ("Technology has made communication much ______.", ["easier", "easiest", "easy", "easily"], "easier"),
            ]],
            *[typed(f"Activity 3 – Grammar Detective. Correct the sentence: {s}", [a]) for s, a in [
                ("I have visited Anuradhapura last year.", "I visited Anuradhapura last year."),
                ("If I were rich, I will travel around the world.", "If I were rich, I would travel around the world."),
                ("The report published yesterday.", "The report was published yesterday."),
                ("She enjoys to read travel blogs.", "She enjoys reading travel blogs."),
                ("The park is enough large for children.", "The park is large enough for children."),
                ("People should to protect wildlife.", "People should protect wildlife."),
                ("This is the person which helped me.", "This is the person who helped me."),
                ("My father used to travelled by train.", "My father used to travel by train."),
            ]],
            *[mcq(f"Activity 13 – Ultimate Grammar Challenge: {s}", o, a) for s, o, a in [
                ("She ______ at the company since January.", ["worked", "has worked", "working", "work"], "has worked"),
                ("While they ______ the museum, the guide explained its history.", ["visited", "were visiting", "visit", "have visited"], "were visiting"),
                ("If everyone used public transport, ...", ["pollution will reduce", "pollution would decrease", "pollution decreased", "pollution decreases yesterday"], "pollution would decrease"),
                ("The new bridge ______ last year.", ["built", "was built", "building", "has build"], "was built"),
                ("I enjoy ______ documentaries.", ["watch", "watching", "watched", "watches"], "watching"),
                ("This park is ______ than the old one.", ["more beautiful", "beautiful", "most beautiful", "beautifully"], "more beautiful"),
                ("Students ______ respect different opinions.", ["should", "should to", "should be", "should being"], "should"),
                ("The scientist ______ discovered the medicine received an award.", ["who", "which", "where", "whose"], "who"),
            ]],
            *[mcq("Activity 14 – Grammar Mix-Up. Choose the correct sentence.", o, a) for o, a in [
                (["She has visited Anuradhapura yesterday.", "She visited Anuradhapura yesterday."], "She visited Anuradhapura yesterday."),
                (["The bridge was built in 2020.", "The bridge built in 2020."], "The bridge was built in 2020."),
                (["If I were you, I'd apply for the job.", "If I was you, I will apply."], "If I were you, I'd apply for the job."),
                (["I enjoy reading historical novels.", "I enjoy to read historical novels."], "I enjoy reading historical novels."),
                (["Colombo is busier than Galle.", "Colombo is more busier than Galle."], "Colombo is busier than Galle."),
            ]],
            plain("Activity 15 – Integrated Language Mission. Words: has improved • who • should • recycling • going to • learning"),
            *[typed(f"Activity 15 – {s}", [a]) for s, a in [
                ("Our community ______ significantly over the past few years.", "has improved"),
                ("Many volunteers, ______ care about the environment, organise campaigns every month.", "who"),
                ("Volunteers organise ______ campaigns every month.", "recycling"),
                ("Next year, the local council is ______ build a new public library.", "going to"),
                ("Everyone ______ protect public spaces because they belong to the whole community.", "should"),
                ("I enjoy ______ about different cultures.", "learning"),
            ]],
            match("Activity 16 – Quick Review Challenge. Match each sentence with its lesson topic.", [
                ("Online learning has changed education.", "Technology"), ("Healthy eating improves well-being.", "Health"),
                ("Ancient cities attract many tourists.", "Cities"), ("A successful career requires responsibility.", "Work"),
                ("Recycling protects the environment.", "Environment"),
            ]),
        ],
        "pronunciation": [
            phrases("Listen and Repeat", [
                ("Achievement", None), ("Architecture", "AR-chi-tec-ture"), ("Biodiversity", "bio-di-VER-si-ty"),
                ("Championship", "CHAM-pi-on-ship"), ("Consumer", None), ("Cybersecurity", None), ("Heritage", None),
                ("Infrastructure", "IN-fra-struc-ture"), ("Innovation", None), ("Qualification", "qua-li-fi-CA-tion"),
                ("Sustainability", None), ("Tournament", None),
            ]),
            *[mcq(f"Activity 7 – Word Stress Challenge. Which syllable is stressed in “{w}”?", o, a) for w, o, a in [
                ("Architecture", ["AR", "chi", "tec", "ture"], "AR"),
                ("Qualification", ["qua", "li", "fi", "CA", "tion"], "CA"),
                ("Infrastructure", ["IN", "fra", "struc", "ture"], "IN"),
                ("Sustainability", ["sus", "tain", "a", "BI", "li", "ty"], "BI"),
                ("Innovation", ["in", "no", "VA", "tion"], "VA"),
                ("Consumer", ["con", "SU", "mer"], "SU"),
                ("Heritage", ["HER", "i", "tage"], "HER"),
                ("Biodiversity", ["bi", "o", "di", "VER", "si", "ty"], "VER"),
            ]],
            *[speak("Tap & Speak: say the word clearly.", w, seconds=5) for w in [
                "Achievement", "Architecture", "Biodiversity", "Championship", "Consumer", "Cybersecurity",
                "Heritage", "Infrastructure", "Innovation", "Qualification", "Sustainability", "Tournament"]],
        ],
        "listening": [
            plain("LISTENING TIP\nWhen listening to longer conversations:\n✔ Listen for the speaker's purpose.\n"
                  "✔ Identify opinions and supporting reasons.\n✔ Listen for changes in time (past, present and future).\n"
                  "✔ Pay attention to linking words: however • although • because • therefore • in the future • recently"),
            heading("Listening Text 1 – From Student to Professional"),
            *[mcq(f"Activity 8 – {q}", o, a, listen=TEXT1) for q, o, a in [
                ("What did Nadeesha use to do during her first year?", ["Work full time", "Spend most of her free time with friends", "Travel abroad", "Teach English"], "Spend most of her free time with friends"),
                ("What helped her gain professional experience?", ["A holiday", "A university competition", "An internship", "A training course"], "An internship"),
                ("How did she feel at first?", ["Excited", "Nervous", "Angry", "Confused"], "Nervous"),
                ("What is her current job?", ["Teacher", "Marketing Assistant", "Engineer", "Journalist"], "Marketing Assistant"),
                ("What is one of her future goals?", ["Start a business", "Learn French", "Complete a master's degree", "Move to another country"], "Complete a master's degree"),
            ]],
            order("Activity 9 – Timeline Builder. Arrange the events.", [
                "Started university", "Completed an internship", "Began working", "Plans to complete a master's degree",
            ]) | {"listen": TEXT1},
            write("Activity 10 – Complete the Notes.", ["Past Habit:", "Internship:", "Current Job:", "Future Goal:"],
                  min_words=1, listen=TEXT1, models=[
                "Spent most of her free time with friends", "International company", "Marketing Assistant",
                "Complete a master's degree"]),
            heading("Listening Text 2 – Building a Better Community"),
            *[tf(f"Activity 11 – {s}", a, listen=TEXT2) for s, a in [
                ("The town has remained exactly the same.", False), ("New public parks have been built.", True),
                ("Traffic congestion has decreased.", False), ("Young people organise recycling campaigns.", True),
                ("The council plans to introduce smart technology.", True), ("Everyone believes communities can improve.", True),
            ]],
            match("Activity 12 – Match the problem with the solution.", [
                ("Traffic congestion", "Bicycle lanes"), ("Pollution", "Recycling campaigns"),
                ("Dirty public spaces", "Community clean-up projects"),
                ("Lack of environmental awareness", "Environmental education"),
            ]) | {"listen": TEXT2},
        ],
        "reading": [
            plain("READING TIP\nAs an intermediate learner, you should be able to:\n✔ Identify the writer's purpose.\n"
                  "✔ Distinguish facts from opinions.\n✔ Infer meaning from context.\n✔ Connect ideas across paragraphs.\n"
                  "✔ Express your own opinion using evidence from the text."),
            passage("Reading Passage 1 – The World Is Changing", PASSAGE1,
                    "තාක්ෂණය, අධ්‍යාපනය සහ පරිසරය යන ක්ෂේත්‍රවල සිදුවන වෙනස්කම් මිනිසුන්ගේ ජීවිතය වෙනස් කර ඇති අතර, "
                    "අනාගතයට සූදානම් වීමට අඛණ්ඩ ඉගෙනීම වැදගත් බව මෙම පාඨය පෙන්වා දෙයි."),
            *[mcq(f"Activity 17 – {q}", o, a) for q, o, a in [
                ("According to the passage, technology has changed the way people...", ["only travel.", "communicate, work and learn.", "play sports.", "build houses."], "communicate, work and learn."),
                ("Which global challenge is mentioned?", ["Population decline", "Climate change", "Space exploration", "Desert tourism"], "Climate change"),
                ("What allows learners to continue learning throughout their lives?", ["Newspapers", "Digital learning tools", "Television only", "Printed dictionaries"], "Digital learning tools"),
                ("According to the writer, successful people are...", ["adaptable and willing to learn.", "physically stronger.", "wealthier.", "older."], "adaptable and willing to learn."),
            ]],
            cat("Activity 18 – Fact or Opinion?", {
                "Fact": ["Technology has changed communication.", "Climate change affects many countries.",
                         "Online learning provides new opportunities."],
                "Opinion": ["Everyone should learn a second language.", "People who continue learning are more likely to succeed."],
            }),
            write("Activity 19 – Find the Evidence. Find one sentence that supports each statement.", [
                "Technology has improved communication.", "Education is becoming more flexible.",
                "Environmental problems require cooperation.",
            ], min_words=4, models=[
                "\"Families can stay connected through video calls regardless of where they live.\"",
                "\"Learners now have access to digital libraries, language-learning applications and online courses.\"",
                "\"Governments, businesses and individuals are working together to develop cleaner energy sources.\"",
            ], review=True),
            passage("Reading Passage 2 – My Future in 2035", PASSAGE2,
                    "අනාගත අරමුණු, වෘත්තිය, සංචාර, පරිසරය සහ පෞද්ගලික සංවර්ධනය පිළිබඳව මෙම පාඨය විස්තර කරයි."),
            write("Activity 20 – Information Hunt. Answer the questions.", [
                "What career goal does the writer have?", "Why does the writer want to travel?",
                "Which healthy habits are mentioned?", "How does the writer hope to help the community?",
                "What qualities does the writer believe are important for success?",
            ], min_words=3, models=[
                "To establish a successful career.", "To learn about different cultures, traditions and architecture.",
                "Regular exercise, spending time with family and lifelong learning.",
                "By participating in environmental projects and encouraging recycling.",
                "Determination, hard work and a positive attitude.",
            ]),
        ],
        "speaking": [
            heading("Activity 21 – Personal Interview"),
            *interview(
                "The app plays each question as audio. Listen and record your answer in full sentences, then "
                "compare it with the model answer.",
                [
                    ("What achievement are you most proud of?", "The achievement I am most proud of is finishing my English course, because I worked very hard for it."),
                    ("Which place would you most like to visit? Why?", "I would most like to visit Japan, because I am interested in its culture and technology."),
                    ("How has technology changed your daily life?", "Technology has made my daily life easier. I can study online, keep in touch with friends, and find information quickly."),
                    ("What career would you like to have in the future?", "In the future, I would like to have a career in software development, because I enjoy solving problems."),
                    ("What can young people do to protect the environment?", "Young people can protect the environment by reducing plastic, saving energy, and planting trees."),
                ],
                expressions=["The achievement I am most proud of is …", "I would like to visit … because …",
                             "Technology has helped me to …", "In the future, I would like to …",
                             "We can … to protect the environment."],
            ),
            heading("Activity 22 – Opinion Carousel"),
            speak("Choose ONE topic and give a one-minute response: A – Technology has improved our lives. B – Cities "
                  "should have more green spaces. C – Travelling is one of the best ways to learn. D – Everyone should "
                  "learn a second language. Use: In my opinion... · Firstly... · Furthermore... · Finally... Model:",
                  "In my opinion, everyone should learn a second language. Firstly, it helps us communicate with people from other countries. Furthermore, it gives us better job opportunities. Finally, it helps us understand other cultures.",
                  seconds=60, review=True),
            heading("Activity 23 – Problem Solving"),
            speak("Your town has received Rs. 100 million. Decide how you will spend it (new school, public library, "
                  "sports centre, hospital, public park, bicycle lanes, technology centre, environmental projects). "
                  "Present your plan and explain your reasons. Model:",
                  "I would spend most of the money on a hospital, because everyone needs good health care. I would also build bicycle lanes to reduce traffic and pollution, and a public library so that students have a quiet place to study.",
                  seconds=60, review=True),
            heading("Activity 24 – Fluency Challenge"),
            speak("Speak for two minutes: “My World Today and My Future.” Include your life today, your achievements, "
                  "your future career, travel plans, personal goals and how you will help your community. Model:",
                  "Today I am a student, and I have completed Level 3 of my English course. I am proud of this achievement. In the future, I would like to work in technology. I hope to travel to Japan and learn about its culture. I want to stay healthy and keep learning. I will also help my community by joining recycling projects.",
                  seconds=120, review=True),
        ],
        "writing": [
            write("Activity 25 – Multi-Paragraph Writing: My World Today & My Future. Write 220–250 words about your "
                  "life today, education, career goals, technology, health, travel, community and future ambitions. "
                  "Use a variety of grammar structures from Level 3.", ["My essay:"], min_words=220),
            write("Activity 26 – Opinion Essay. Write 180–200 words: “Technology has improved our lives more than it has "
                  "created problems.” Give your opinion, support it with examples and conclude with your own view.",
                  ["My essay:"], min_words=180),
            write("Activity 27 – Reflection Journal. Complete the sentences.", [
                "This year I learned...", "The most useful lesson was...", "I still want to improve...",
                "In the future I hope to...", "The biggest challenge I overcame was...",
            ], min_words=3),
            write("LEVEL 3 CAPSTONE PROJECT – My World Today & My Future (a written portfolio of 500–600 words, or "
                  "prepare a 3–5 minute presentation).", [
                "Part 1 – About Me: introduce yourself, your interests and achievements.",
                "Part 2 – My Learning Journey: what have you learned during Level 3?",
                "Part 3 – My Future: your goals for education, career, travel and personal development.",
                "Part 4 – My Community: how would you improve your town (environment, technology, education, public services)?",
                "Part 5 – Final Reflection: “How has learning English changed my life?”",
            ], min_words=40),
            self_check(
                "□ I can describe experiences using a variety of tenses.\n□ I can express my opinions confidently.\n"
                "□ I can understand extended reading texts.\n□ I can understand longer listening passages.\n"
                "□ I can participate in discussions and interviews.\n□ I can compare ideas and support my opinions.\n"
                "□ I can write organised multi-paragraph texts.\n□ I feel ready for Upper-Intermediate English.",
                prompt="Self-assessment — tick the statements that are true for you.",
            ),
            summary(["Level 3 completed!", "Express opinions confidently", "Tell detailed stories using different tenses",
                     "Understand extended spoken and written texts", "Write organised multi-paragraph texts"]),
        ],
    },
}
