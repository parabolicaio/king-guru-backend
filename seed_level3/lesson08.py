"""Level 3 Lesson 8 — Sports, Leisure & Lifestyle.

Source: LEVEL_3_L8_individual.docx. The lesson has no separate
pronunciation part, so the Pronunciation section uses its "Pronunciation
Help" words. review=True marks keys/models by the King Guru team.
"""
from .dsl import (DISCUSS, cat, examples, heading, interview, match, mcq, order, passage, phrases,
                  plain, self_check, speak, summary, tf, typed, words, write)

TEXT1 = (
    "Ruwan recently decided to make some positive changes to his lifestyle. In the past, he spent most of his "
    "free time watching television and playing video games. He rarely exercised and often stayed awake until "
    "midnight. After visiting his doctor, he realised that he needed a healthier routine. Now he wakes up "
    "earlier, goes for a thirty-minute walk every morning and drinks more water throughout the day. He has "
    "also joined a badminton club, where he practises twice a week with his friends. At first, he found the "
    "training difficult, but now he enjoys it because it helps him stay active and reduce stress. Although he "
    "still enjoys relaxing at home, he tries to balance work, exercise and leisure. He believes that these "
    "small changes have improved both his physical and mental health."
)
TEXT2 = (
    "Host: Today we're asking people about their favourite hobbies. Let's meet two university students. "
    "Amaya: I spend a lot of time studying, so I wanted a hobby that helps me relax. Last year, I started "
    "gardening with my parents. I enjoy watching plants grow, and it gives me a chance to spend time outdoors. "
    "Nimesh: I prefer more active hobbies. I play basketball every weekend with my friends. It keeps me fit "
    "and teaches me the importance of teamwork. Host: Both hobbies are very different, but they help people "
    "stay happy and healthy in their own way."
)
PASSAGE1 = (
    "Many people believe that exercise is only important for athletes. However, regular physical activity "
    "benefits everyone, regardless of age or fitness level. Even simple activities such as walking, cycling or "
    "stretching can improve overall health.\n\nExercise helps strengthen muscles and bones, improves heart "
    "health and increases energy levels. It can also reduce stress and improve mental well-being. People who "
    "exercise regularly often sleep better and feel more confident in their daily lives.\n\nHealth experts "
    "recommend that adults should be physically active for at least 150 minutes each week. This does not mean "
    "spending hours at the gym. Activities such as dancing, swimming, gardening and even playing with children "
    "all contribute to a healthier lifestyle.\n\nThe most important thing is to choose activities you enjoy. "
    "When exercise becomes part of your daily routine, it is easier to stay motivated and maintain healthy habits."
)
PASSAGE2 = (
    "Modern life is often busy and demanding. Many people spend long hours studying or working and have little "
    "time to relax. As a result, they may experience stress, tiredness and difficulty concentrating.\n\n"
    "Maintaining a healthy work-life balance means giving enough attention to both responsibilities and "
    "personal well-being. This includes making time for hobbies, exercise, family and adequate rest.\n\n"
    "People who achieve a good balance are often more productive and happier. Taking regular breaks, limiting "
    "screen time and planning daily activities can help reduce stress and improve overall quality of life.\n\n"
    "Although everyone's routine is different, small changes can make a big difference over time."
)

LESSON = {
    "order": 8,
    "title": "Sports, Leisure & Lifestyle",
    "title_si": "ක්‍රීඩා, විවේකය සහ ජීවන රටාව",
    "description": "Talk about sports, hobbies and a balanced lifestyle, and review the grammar of Level 3 (B1).",
    "objectives": [
        "Discuss sports, hobbies and leisure activities confidently",
        "Describe sports equipment, rules and participation",
        "Compare different lifestyles and leisure activities",
        "Express opinions about healthy living and work-life balance",
        "Understand spoken and written texts related to sports and healthy lifestyles",
        "Take part in discussions about exercise, hobbies and well-being",
        "Write a short paragraph describing an ideal lifestyle",
    ],
    "sections": {
        "vocabulary": [
            words("A. Sports Vocabulary", [
                ("Athlete", "ක්‍රීඩකයා / ක්‍රීඩිකාව"), ("Competition", "තරඟය"), ("Tournament", "තරඟාවලිය"),
                ("Coach", "පුහුණුකරු"), ("Referee", "විනිසුරු"), ("Spectator", "ප්‍රේක්ෂකයා"),
                ("Teamwork", "කණ්ඩායම් වැඩ"), ("Training", "පුහුණුව"), ("Fitness", "ශාරීරික යෝග්‍යතාව"),
                ("Endurance", "දරාගැනීමේ හැකියාව"), ("Stamina", "ශක්තිය / දරාගැනීමේ ශක්තිය"),
                ("Warm-up", "උණුසුම් කිරීමේ ව්‍යායාම"), ("Stretch", "ඇඟ දිගහැරීම"), ("Championship", "ශූරතාවලිය"),
            ]),
            match("Activity 3 – Match the sport to the equipment.", [
                ("Cricket", "Bat"), ("Tennis", "Racket"), ("Swimming", "Swimming Goggles"), ("Football", "Football"),
                ("Badminton", "Shuttlecock"), ("Table Tennis", "Table Tennis Bat"), ("Rugby", "Rugby Ball"),
                ("Volleyball", "Volleyball"),
            ]),
            cat("Activity 4 – Categorize the sports.", {
                "Indoor Sports": ["Chess", "Carrom", "Table Tennis"],
                "Outdoor Sports": ["Cricket", "Running", "Cycling", "Football"],
                "Can Be Both": ["Swimming", "Basketball", "Badminton", "Volleyball", "Yoga"],
            }, review=True),
            write("Activity 4 – Think Further.", ["Which category contains your favourite activity? Why?"], min_words=8),
            mcq("Activity 5 – Nimal enjoys individual activities. He wants to improve his fitness but dislikes team sports.",
                ["Cricket", "Swimming", "Rugby", "Football"], "Swimming"),
            mcq("Activity 5 – Sithumi enjoys working with others. She likes fast-paced games.",
                ["Chess", "Basketball", "Running", "Yoga"], "Basketball"),
            mcq("Activity 5 – A retired teacher wants gentle exercise that improves flexibility and reduces stress.",
                ["Rugby", "Yoga", "Sprinting", "Boxing"], "Yoga"),
            mcq("Activity 5 – A ten-year-old child enjoys running and kicking a ball with friends.",
                ["Football", "Swimming", "Chess", "Tennis"], "Football"),
            mcq("Activity 5 – An office worker wants an activity that can be done alone after work and improves cardiovascular health.",
                ["Cycling", "Carrom", "Chess", "Volleyball"], "Cycling"),
            write("Activity 5 – Reflection.", [
                "Choose one activity you have never tried. Would you like to learn it? Explain your answer.",
            ], min_words=10),
            write("Activity 6 – Complete the sports advice using your own ideas.", [
                "Before every match, athletes should ______.", "Teamwork is important because ______.",
                "A good coach should ______.", "Spectators should always ______.", "I enjoy sports because ______.",
                "One new sport I would like to learn is ______.", "Regular exercise helps people ______.",
                "Playing sports has taught me ______.",
            ], min_words=3),
            words("B. Hobbies & Leisure", [
                ("Hobby", "විනෝදාංශය"), ("Leisure", "විවේක කාලය"), ("Relaxation", "විවේකය"),
                ("Recreation", "විනෝදාස්වාදය"), ("Gardening", "ගෙවතු වගාව"), ("Photography", "ඡායාරූපකරණය"),
                ("Hiking", "කඳු නැගීම"), ("Painting", "චිත්‍ර ඇඳීම"), ("Volunteering", "ස්වේච්ඡා සේවය"),
                ("Meditation", "භාවනා කිරීම"), ("Camping", "කඳවුරු බැඳීම"), ("Bird Watching", "කුරුල්ලන් නිරීක්ෂණය කිරීම"),
            ]),
            cat("Activity 7 – Hobby Categories. Place each hobby into the correct group.", {
                "Indoor Hobbies": ["Reading", "Painting", "Meditation", "Cooking", "Chess"],
                "Outdoor Hobbies": ["Camping", "Gardening", "Cycling", "Hiking"],
                "Both Indoor & Outdoor": ["Photography", "Swimming", "Volunteering"],
            }, review=True),
            write(f"Activity 7 – {DISCUSS}", ["Which hobby would you recommend to someone who feels stressed? Explain why."], min_words=10),
            write("Activity 8 – Weekend Planner. Choose the most suitable weekend activity for each person and explain why.", [
                "A university student who enjoys nature:", "A retired couple looking for relaxation:",
                "A teenager interested in teamwork:", "A busy office worker with limited free time:",
            ], min_words=5, models=[
                "Hiking or bird watching, because they can spend time in nature.",
                "Gardening or meditation, because they are calm and relaxing.",
                "Playing football or basketball, because they are team sports.",
                "A short walk or cycling, because it does not take much time.",
            ], review=True),
            plain("Lifestyle Tip\nA healthy lifestyle is not only about exercise. It also includes:\n✔ Enough sleep\n"
                  "✔ Healthy food\n✔ Time with family and friends\n✔ Regular physical activity\n✔ Time to relax\n"
                  "✔ Positive mental health"),
        ],
        "grammar": [
            heading("Review Corner"),
            plain("From Lesson 7: ✔ Shopping Vocabulary ✔ Food Vocabulary ✔ Too / Enough ✔ Consumer Decisions "
                  "✔ Healthy Food Choices\nExamples: This backpack is too expensive. · We have enough food for "
                  "everyone. · I always compare prices before buying something.\nToday we move from making healthy "
                  "food choices to maintaining a healthy and balanced lifestyle through sports, hobbies and recreation."),
            cat("Activity 1 – Healthy Choice or Unhealthy Choice?", {
                "Healthy Lifestyle": ["Amal walks to work every morning instead of driving.",
                                      "Kavindu drinks enough water during the day.",
                                      "A group of friends play badminton every Saturday morning.",
                                      "A family enjoys cycling together on weekends.",
                                      "A football player stretches before every practice session.",
                                      "A teacher takes short breaks while working on the computer."],
                "Unhealthy Lifestyle": ["Nethmi spends six hours every evening watching television without taking a break.",
                                        "Sanduni skips breakfast because she wakes up late.",
                                        "Dinuka sleeps only four hours each night.",
                                        "A university student spends every free hour scrolling through social media."],
            }, review=True),
            write("Activity 1 – Reflection.", ["Choose one unhealthy habit from the list. Explain how it could be improved."], min_words=10),
            plain("Activity 2 – Which Lifestyle Would You Choose?\nPerson A: sleeps 8 hours every night, plays basketball "
                  "twice a week, eats home-cooked meals, reads books before bed.\nPerson B: sleeps 5 hours every "
                  "night, eats fast food four times a week, exercises only once a month, uses social media until midnight."),
            mcq("Activity 2 – Which person has the healthier lifestyle?", ["Person A", "Person B"], "Person A"),
            write("Activity 2 – Follow-up questions.", [
                "Explain your reasons.", "What habits would you recommend to Person B?",
                "Which habit would be easiest for you to adopt?",
            ], min_words=5),
            heading("Mixed Review"),
            plain("Throughout this course you have learned to talk about: ✔ Past experiences ✔ Present situations "
                  "✔ Future plans ✔ Advice ✔ Comparisons ✔ Too / Enough\nToday you'll review these grammar points "
                  "while talking about sports and healthy lifestyles."),
            plain("Sinhala Help\nI used to play football every weekend.\n→ මම ඉස්සර සෑම සති අන්තයකම පාපන්දු ක්‍රීඩා කළා.\n"
                  "I have played badminton for three years.\n→ මම අවුරුදු තුනක් තිස්සේ බැඩ්මින්ටන් ක්‍රීඩා කර තිබෙනවා.\n"
                  "I'm going to join a gym next month.\n→ ලබන මාසේ මම ජිම් එකකට සම්බන්ධ වෙන්න යනවා."),
            mcq("Activity 14 – I ______ yoga for two years.", ["practised", "have practised", "practise yesterday"], "have practised"),
            mcq("Activity 14 – My sister ______ basketball when she was younger.", ["used to play", "has played", "is playing"], "used to play"),
            mcq("Activity 14 – Next month, we ______ participate in the school sports festival.", ["are going to", "went", "have"], "are going to"),
            mcq("Activity 14 – This football is ______ heavy for young children.", ["too", "enough"], "too"),
            mcq("Activity 14 – We have ______ players to start the match.", ["enough", "too"], "enough"),
            mcq("Activity 14 – My coach told me I ______ exercise regularly.", ["should", "shouldn't never", "have"], "should"),
            order("Activity 15 – Lifestyle Timeline. Arrange the events in the correct order.", [
                "Started exercising regularly", "Joined a sports club", "Learned the basic rules",
                "Won the first competition", "Became team captain", "Inspired younger players",
            ], review=True),
            write("Activity 16 – Then and Now. Complete the comparisons. Example: I used to spend my evenings watching "
                  "television, but now I go jogging.", [
                "I used to ______, but now ______.", "My weekends used to ______, but now ______.",
                "I used to eat ______, but now ______.", "My family used to ______, but now ______.",
                "Students used to ______, but now ______.", "I used to think ______, but now ______.",
            ], min_words=5),
            write("Activity 17 – Healthy Lifestyle Challenge. Give one piece of advice for each situation. Use should, "
                  "shouldn't, too and enough.", [
                "Situation 1: Your friend studies all day and never exercises.",
                "Situation 2: A teenager sleeps only four hours every night.",
                "Situation 3: A university student eats fast food every day.",
                "Situation 4: Someone spends every weekend indoors using social media.",
                "Situation 5: A child wants to improve fitness before the school sports meet.",
            ], min_words=6),
            write("Reflection – Complete the sentences.", [
                "One healthy habit I already have is...", "One habit I would like to improve is...",
                "One sport or hobby I want to start this year is...",
            ], min_words=3),
        ],
        "pronunciation": [
            phrases("Pronunciation Help", [
                ("Athlete", "ඇත්ලීට්"), ("Tournament", "ටූර්නමන්ට්"), ("Referee", "රෙෆරී"),
                ("Endurance", "එන්ඩියුරන්ස්"), ("Championship", "චැම්පියන්ෂිප්"),
            ]),
            *[speak("Tap & Speak: say the word clearly.", w, seconds=5) for w in [
                "Athlete", "Tournament", "Referee", "Endurance", "Championship", "Spectator", "Stamina",
                "Photography", "Meditation", "Volunteering"]],
            heading("Say It Clearly"),
            *[speak("Say the sentence clearly.", s, seconds=10) for s in [
                "I have played badminton for three years.", "I used to play football every weekend.",
                "I'm going to join a gym next month.", "This football is too heavy for young children.",
            ]],
        ],
        "listening": [
            plain("LISTENING TIP\nWhen listening to conversations about sports and healthy lifestyles:\n✔ Listen for "
                  "routines and habits.\n✔ Listen for opinions and reasons.\n✔ Identify healthy and unhealthy choices.\n"
                  "✔ Listen for advice and recommendations.\n✔ Pay attention to time expressions and frequency words: "
                  "every morning • twice a week • usually • rarely • after work • at weekends"),
            heading("Listening Text 1 – A Healthier Lifestyle"),
            *[mcq(f"Activity 9 – {q}", o, a, listen=TEXT1) for q, o, a in [
                ("What did Ruwan spend most of his free time doing in the past?", ["Playing badminton", "Watching television and playing video games", "Reading books"], "Watching television and playing video games"),
                ("Why did he decide to change his lifestyle?", ["His teacher advised him.", "He visited his doctor.", "He moved to another city."], "He visited his doctor."),
                ("Which new habit did he develop?", ["Walking every morning", "Sleeping less", "Eating fast food"], "Walking every morning"),
                ("Which sport did he join?", ["Football", "Swimming", "Badminton"], "Badminton"),
                ("What benefit does Ruwan mention?", ["He became famous.", "He reduced stress and became healthier.", "He won many competitions."], "He reduced stress and became healthier."),
            ]],
            *[tf(f"Activity 10 – {s}", a, listen=TEXT1, review=True) for s, a in [
                ("Ruwan always exercised regularly before visiting the doctor.", False),
                ("He now wakes up earlier than before.", True), ("He practises badminton every day.", False),
                ("He believes exercise has improved his health.", True), ("He has stopped relaxing completely.", False),
                ("He tries to balance work and leisure.", True), ("His new routine helps him manage stress.", True),
                ("He regrets changing his lifestyle.", False),
            ]],
            *[typed(f"Activity 11 – {s}", [a], listen=TEXT1, review=True) for s, a in [
                ("Ruwan decided to make some positive __________ to his lifestyle.", "changes"),
                ("He goes for a thirty-minute __________ every morning.", "walk"),
                ("He joined a __________ club.", "badminton"),
                ("He practises __________ a week.", "twice"),
                ("He believes that exercise has improved both his __________ and mental health.", "physical"),
            ]],
            heading("Listening Text 2 – Choosing the Right Hobby"),
            match("Activity 12 – Information Matching. Match each person with the correct information.", [
                ("Amaya's hobby", "Gardening"), ("Amaya's reason", "To relax"),
                ("Nimesh's hobby", "Basketball"), ("Nimesh's reason", "To stay fit"),
            ], review=True) | {"listen": TEXT2},
            write("Activity 13 – Compare the Two Speakers. Write three facts about each speaker.", [
                "Amaya:", "Nimesh:", "Whose hobby is more relaxing?", "Whose hobby requires teamwork?",
                "Which hobby would you prefer? Explain why.",
            ], min_words=3, listen=TEXT2, models=[
                "She studies a lot, she started gardening with her parents, and she enjoys being outdoors.",
                "He likes active hobbies, he plays basketball every weekend, and it keeps him fit.",
                "Amaya's hobby, gardening.", "Nimesh's hobby, basketball.",
            ], review=True),
        ],
        "reading": [
            plain("READING TIP\nWhen reading about sports and healthy lifestyles:\n✔ Identify the writer's main idea.\n"
                  "✔ Look for supporting reasons and examples.\n✔ Distinguish between facts and opinions.\n"
                  "✔ Compare different lifestyles.\n✔ Think about how the ideas relate to your own life."),
            passage("Reading Passage 1 – Why Is Regular Exercise Important?", PASSAGE1,
                    "නිතිපතා ව්‍යායාම කිරීම ශරීරයට පමණක් නොව මානසික සෞඛ්‍යයටද ප්‍රයෝජනවත් වේ. තමා කැමති ක්‍රියාකාරකමක් "
                    "තෝරා ගැනීම දිගුකාලීනව එය පවත්වාගෙන යාමට උපකාරී වේ."),
            mcq("Activity 18 – According to the passage, exercise is important for...",
                ["only athletes.", "children only.", "everyone.", "professional sports players."], "everyone."),
            mcq("Activity 18 – Which of the following is NOT mentioned as a benefit of exercise?",
                ["Better sleep", "Increased confidence", "Learning new languages", "Improved heart health"], "Learning new languages"),
            mcq("Activity 18 – How many minutes of physical activity are recommended each week?",
                ["60 minutes", "90 minutes", "150 minutes", "300 minutes"], "150 minutes"),
            mcq("Activity 18 – Which activity is mentioned in the passage?", ["Skiing", "Gardening", "Boxing", "Surfing"], "Gardening"),
            mcq("Activity 18 – What is the writer's main message?",
                ["Exercise should only be done in a gym.", "People should choose activities they enjoy.",
                 "Exercise is difficult.", "Walking is better than swimming."], "People should choose activities they enjoy."),
            write("Activity 19 – Find the Evidence. Find one sentence or phrase that supports each statement.", [
                "Exercise improves mental health.", "Everyone can benefit from exercise.",
                "Physical activity doesn't have to be difficult.", "Enjoyment helps people continue exercising.",
            ], min_words=4, models=[
                "\"It can also reduce stress and improve mental well-being.\"",
                "\"Regular physical activity benefits everyone, regardless of age or fitness level.\"",
                "\"This does not mean spending hours at the gym.\"",
                "\"When exercise becomes part of your daily routine, it is easier to stay motivated.\"",
            ], review=True),
            cat("Activity 20 – Fact or Opinion? Sort each statement.", {
                "Fact": ["Walking is one of the easiest forms of exercise.", "Exercise improves heart health.",
                         "Regular exercise can reduce stress."],
                "Opinion": ["Swimming is the best sport.", "Everyone should find an activity they enjoy.",
                            "Football is more exciting than tennis."],
            }, review=True),
            write("Activity 20 – Now explain one opinion in your own words.", ["My explanation:"], min_words=10),
            passage("Reading Passage 2 – Finding Balance in Everyday Life", PASSAGE2,
                    "වැඩ, අධ්‍යාපනය සහ විවේකය අතර සමබරතාවයක් පවත්වා ගැනීම ශාරීරික හා මානසික සෞඛ්‍යයට වැදගත් වේ."),
            match("Activity 21 – Information Matching. Match each recommendation with its purpose.", [
                ("Exercise regularly", "Stay physically healthy"), ("Take regular breaks", "Improve concentration"),
                ("Spend time with family", "Strengthen relationships"), ("Reduce screen time", "Reduce stress"),
                ("Plan your day", "Manage time effectively"),
            ], review=True),
            cat("Activity 22 – Compare & Categorize. Place each activity in the correct category.", {
                "Healthy Habits": ["Jogging", "Playing Football", "Meditation", "Cycling", "Sleeping 8 Hours"],
                "Habits to Limit": ["Working Late", "Scrolling through Social Media"],
                "Depends on Balance": ["Watching TV", "Reading", "Cooking"],
            }, review=True),
            write(f"Activity 22 – {DISCUSS}", [
                "Which healthy habit is easiest to practise?", "Which habit do you think people find hardest to change?",
            ], min_words=5),
        ],
        "speaking": [
            heading("Activity 23 – Guided Interview"),
            *interview(
                "The app plays each question as audio. Listen and record your answer in full sentences, then "
                "compare it with the model answer.",
                [
                    ("What is your favourite sport or hobby?", "My favourite hobby is playing cricket with my friends."),
                    ("How often do you do it?", "I play it about three times a week, usually in the evening."),
                    ("Why do you enjoy it?", "I enjoy it because it keeps me fit and helps me relax after studying."),
                    ("What equipment do you need?", "You need a bat, a ball, and some basic protective gear."),
                    ("Would you recommend it to others? Why?", "Yes, I would recommend it because it is fun, healthy, and a great way to make friends."),
                ],
                expressions=["My favourite … is …", "I do it … times a week", "I enjoy it because …", "You need …",
                             "I would recommend it because …"],
            ),
            heading("Activity 24 – Lifestyle Choices"),
            mcq("Situation A – After work, would you rather...", ["go for a walk", "watch television for four hours"], "go for a walk"),
            mcq("Situation B – On a free weekend, would you rather...", ["play badminton with friends", "stay indoors all day"], "play badminton with friends"),
            mcq("Situation C – After dinner, would you rather...", ["read a book", "spend three hours on your phone"], "read a book"),
            speak("Explain each choice. Model:",
                  "After work, I would go for a walk because it keeps me active. At the weekend, I would play badminton with friends, because it is healthy and fun. After dinner, I would read a book, because too much time on my phone affects my sleep.",
                  seconds=45, review=True),
            heading("Activity 25 – Mini Debate"),
            plain("Choose one statement: 1 – Schools should provide more time for sports. 2 – Everyone should have at "
                  "least one hobby. 3 – Professional athletes are good role models for young people. Decide whether "
                  "you agree or disagree. Think of two reasons and put them in order, strongest first. Use: In my "
                  "opinion... · I believe... · One reason is... · For example..."),
            speak("Record a one-minute argument using your position and your two reasons, with one example. Model:",
                  "In my opinion, everyone should have at least one hobby. One reason is that hobbies help us relax and reduce stress. Another reason is that we can meet new people. For example, my uncle started photography and now he has many new friends.",
                  seconds=60, review=True),
            heading("Activity 26 – Fluency Challenge"),
            speak("Speak for one minute without stopping. Choose ONE topic: My Favourite Sport · A Hobby I Would Like to "
                  "Learn · How I Stay Healthy · My Weekend Routine. Model:",
                  "I stay healthy by walking to school every day and playing volleyball at the weekend. I try to sleep eight hours and drink enough water. I also eat home-cooked food and fruit. When I feel stressed, I listen to music or help my mother in the garden.",
                  seconds=60, review=True),
        ],
        "writing": [
            write("Activity 27 – Guided Writing: My Ideal Lifestyle. Write a paragraph (120–150 words). Include your "
                  "daily routine, exercise habits, healthy eating, leisure activities, work-life balance and future "
                  "goals. Use First, Then, After that, Finally, However, Therefore.", ["My paragraph:"], min_words=120),
            write("Activity 28 – Sports Review. You recently watched or took part in a sporting event. Write a short "
                  "review (120–150 words): the name of the sport or event, what happened, what you enjoyed, what could "
                  "be improved and whether you would recommend it.", ["My review:"], min_words=120),
            write("Activity 29 – Lifestyle Planner. For each day, write a physical activity, a leisure activity and a healthy habit.", [
                "Monday:", "Tuesday:", "Wednesday:", "Thursday:", "Friday:", "Saturday:", "Sunday:",
                "Which habit will be the most difficult to maintain?", "Which activity are you most excited about?",
                "How will this plan improve your well-being?",
            ], min_words=3),
            plain("HEALTHY LIFESTYLE CHALLENGE – Final Mission: Become a Lifestyle Coach\nYour friend says: “I spend "
                  "most of my day studying. I rarely exercise, sleep only five hours a night and spend my weekends "
                  "using social media. I want to become healthier, but I don't know where to start.”"),
            write("Create a Healthy Lifestyle Plan.", [
                "Step 1 – Daily Routine: recommend a better daily schedule.",
                "Step 2 – Exercise Plan: suggest at least three physical activities and explain why they are suitable.",
                "Step 3 – Healthy Habits: recommend healthy eating, sleep and relaxation habits.",
                "Step 4 – Leisure Time: suggest hobbies that help reduce stress.",
                "Step 5 – Your Advice: write five pieces of advice with You should... · You shouldn't... · Try to... · It's important to... · Don't forget to...",
                "Reflection: “A balanced lifestyle is important because...” Give three reasons.",
            ], min_words=10),
            self_check(
                "□ I can discuss different sports and hobbies confidently.\n□ I can describe sports equipment and basic rules.\n"
                "□ I can compare different lifestyles.\n□ I can express my opinions about healthy living.\n"
                "□ I can understand texts about sports and well-being.\n□ I can participate in conversations about leisure activities.\n"
                "□ I can write about my ideal lifestyle.\n□ I can recommend healthy habits to others.",
                prompt="Self-assessment — tick the statements that are true for you.",
            ),
            summary(["Sports and hobby vocabulary", "Mixed review: past, present, future, advice, too / enough",
                     "Healthy lifestyles and work-life balance", "Giving lifestyle advice"]),
        ],
    },
}
