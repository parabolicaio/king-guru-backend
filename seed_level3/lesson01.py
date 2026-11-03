"""Level 3 Lesson 1 — Life Stories, Relationships & Modern Communication.

Source: Lesson Contents/Kingguru L3 Activities/LEVEL_3_L1_individual (1).docx
(solo version, 5 Oct 2026). review=True marks keys/models by the King Guru
team, for the experts to check.
"""
from .dsl import (cat, examples, fbo, heading, interview, match, mcq, order, passage, phrases,
                  plain, self_check, speak, summary, tf, typed, words, write)

L1_TEXT1 = (
    "Hello. My name is Nadeesha. I am twenty-four years old and I work as a graphic designer. "
    "When I was younger, I used to be very shy. I didn't enjoy speaking in front of people and I rarely "
    "shared my opinions. However, things slowly changed when I entered university. I joined several "
    "student clubs and started meeting new people. Over time, I became more confident and independent. "
    "I have made many close friends and learned valuable communication skills. Today, I enjoy working "
    "with people and presenting ideas. I have also travelled to different parts of Sri Lanka through my "
    "work. Looking back, I am proud of how much I have changed. Next year, I am going to start my own "
    "design business."
)
L1_TEXT2 = (
    "Today, social media plays a major role in people's lives. Many people use social media to "
    "communicate with friends and family. It allows users to share ideas, photos, and experiences "
    "instantly. Students often use social media to discuss assignments and share educational resources. "
    "Businesses use social media to promote products and connect with customers. However, social media "
    "also has disadvantages. Some people spend too much time online and become less active in real life. "
    "Privacy is another important concern. Users should think carefully before sharing personal "
    "information online. In my opinion, social media is useful if people use it responsibly."
)
L1_PASSAGE1 = (
    "When I was in school, I was a quiet student who rarely spoke in class. I used to spend most of my "
    "time reading books and working alone. Although I had a few close friends, I often felt nervous when "
    "meeting new people. After leaving school, I entered university and joined several student "
    "organizations. These experiences helped me become more confident and independent. I learned how to "
    "work with different people and communicate effectively. Over the past few years, I have participated "
    "in workshops, community projects, and leadership programmes. As a result, I have developed many "
    "valuable skills. Today, I enjoy public speaking and teamwork. Looking back, I realise that personal "
    "growth often happens when we challenge ourselves."
)
L1_PASSAGE2 = (
    "Social media has transformed the way people communicate. Supporters believe that it helps people "
    "stay connected regardless of distance. It allows individuals to share ideas, learn new information, "
    "and build communities. Many students use social media to collaborate on projects and access "
    "educational content. On the other hand, critics argue that social media can become addictive. "
    "Excessive use may reduce face-to-face communication and affect mental health. There are also "
    "concerns about misinformation and privacy. In reality, social media is neither completely good nor "
    "completely bad. Its impact depends on how people choose to use it. Responsible use can provide many "
    "benefits while reducing potential risks."
)

LESSON = {
    "order": 1,
    "title": "Life Stories, Relationships & Modern Communication",
    "title_si": "ජීවන කතා, සබඳතා සහ නවීන සන්නිවේදනය",
    "description": "Talk about life experiences, past habits, people's personalities and social media (B1).",
    "objectives": [
        "Distinguish between Present Perfect and Past Simple when talking about life experiences",
        "Describe past habits using \"used to\"",
        "Discuss social media and modern communication methods",
        "Describe people's personalities using character adjectives",
        "Use common relationship phrasal verbs appropriately",
        "Speak about important people and experiences in your life",
        "Write a short personal narrative combining past and present experiences",
    ],
    "sections": {
        "vocabulary": [
            words("Life Experience Vocabulary", [
                ("Achievement", "ජයග්‍රහණය"), ("Experience", "අත්දැකීම"), ("Challenge", "අභියෝගය"),
                ("Success", "සාර්ථකත්වය"), ("Failure", "අසාර්ථකත්වය"), ("Opportunity", "අවස්ථාව"),
                ("Decision", "තීරණය"), ("Goal", "ඉලක්කය"), ("Memory", "මතකය"),
                ("Childhood", "ළමා කාලය"), ("Journey", "ගමන"), ("Milestone", "වැදගත් සන්ධිස්ථානය"),
            ], meanings={
                "Achievement": "Something you successfully completed", "Challenge": "A difficult situation",
                "Goal": "Something you want to achieve", "Memory": "Something remembered from the past",
                "Opportunity": "A chance to do something", "Success": "A positive result",
                "Failure": "Lack of success", "Decision": "A choice you make",
            }),
            match("Activity 3 – Match the word and meaning.", [
                ("Achievement", "Something you successfully completed"), ("Challenge", "A difficult situation"),
                ("Goal", "Something you want to achieve"), ("Memory", "Something remembered from the past"),
                ("Opportunity", "A chance to do something"), ("Success", "A positive result"),
                ("Failure", "Lack of success"), ("Decision", "A choice you make"),
            ]),
            cat("Activity 4 – Categorize the vocabulary.", {
                "Positive Experiences": ["Achievement", "Success", "Opportunity", "Goal"],
                "Life Events": ["Memory", "Journey", "Milestone"],
                "Personal Growth": ["Challenge", "Decision", "Experience"],
            }),
            write("Activity 5 – Complete the sentences about your own life.", [
                "One important achievement in my life was ______.", "A challenge I overcame was ______.",
                "My biggest goal is ______.", "One childhood memory I will never forget is ______.",
                "An important decision I made was ______.", "I would like the opportunity to ______.",
                "Success means ______ to me.", "A valuable experience I had was ______.",
                "One milestone in my life was ______.", "I learned an important lesson from ______.",
            ], min_words=2),
            words("Character Adjectives", [
                ("Friendly", "මිත්‍රශීලී"), ("Honest", "අවංක"), ("Reliable", "විශ්වාසවන්ත"),
                ("Patient", "ඉවසීම ඇති"), ("Confident", "ආත්ම විශ්වාසයෙන් යුතු"), ("Generous", "දානශීලී"),
                ("Supportive", "සහයෝගය දක්වන"), ("Responsible", "වගකීම් සහිත"), ("Creative", "නිර්මාණශීලී"),
                ("Independent", "ස්වාධීන"), ("Kind", "කරුණාවන්ත"), ("Hard-working", "මහන්සි වන"),
            ], meanings={
                "Friendly": "Enjoys meeting and talking to people", "Honest": "Always tells the truth",
                "Reliable": "Can be trusted", "Creative": "Has many original ideas",
                "Responsible": "Takes duties seriously", "Patient": "Can wait calmly",
                "Independent": "Likes doing things alone", "Supportive": "Helps others when needed",
            }),
            match("Activity 6 – Match the adjective to the description.", [
                ("Friendly", "Enjoys meeting and talking to people"), ("Honest", "Always tells the truth"),
                ("Reliable", "Can be trusted"), ("Creative", "Has many original ideas"),
                ("Responsible", "Takes duties seriously"), ("Patient", "Can wait calmly"),
                ("Independent", "Likes doing things alone"), ("Supportive", "Helps others when needed"),
            ]),
            mcq("Activity 7 – My best friend always helps me when I have a problem.", ["supportive", "careless", "selfish"], "supportive"),
            mcq("Activity 7 – My teacher always tells the truth.", ["honest", "lazy", "rude"], "honest"),
            mcq("Activity 7 – My sister studies hard and completes her work on time.", ["responsible", "careless", "impatient"], "responsible"),
            mcq("Activity 7 – My cousin writes stories and creates artwork.", ["creative", "shy", "dishonest"], "creative"),
            mcq("Activity 7 – My grandfather listens carefully and never gets angry quickly.", ["patient", "rude", "selfish"], "patient"),
            mcq("Activity 7 – My friend can always be trusted.", ["reliable", "careless", "dishonest"], "reliable"),
            mcq("Activity 7 – My brother enjoys meeting new people.", ["friendly", "lazy", "unfriendly"], "friendly"),
            mcq("Activity 7 – My aunt believes in herself and tries new things.", ["confident", "nervous", "weak"], "confident"),
            mcq("Activity 7 – My neighbour helps everyone in the community.", ["kind", "selfish", "impatient"], "kind"),
            mcq("Activity 7 – My classmate studies without needing much help.", ["independent", "dependent", "careless"], "independent"),
            words("Communication Vocabulary", [
                ("Social Media", "සමාජ මාධ්‍ය"), ("Online Profile", "මාර්ගගත පැතිකඩ"), ("Follower", "අනුගාමිකයා"),
                ("Post", "පළ කිරීම"), ("Comment", "අදහස"), ("Share", "බෙදාගැනීම"),
                ("Privacy", "පෞද්ගලිකත්වය"), ("Notification", "දැනුම්දීම"), ("Message", "පණිවිඩය"),
                ("Video Call", "වීඩියෝ ඇමතුම"), ("Influencer", "බලපෑම් ඇති කරන පුද්ගලයා"),
                ("Digital Footprint", "ඩිජිටල් සලකුණ"),
            ]),
            cat("Activity 8 – Categorize the vocabulary.", {
                "Communication Tools": ["Message", "Video Call", "Comment", "Post"],
                "Social Media Features": ["Follower", "Share", "Notification", "Online Profile"],
                "Safety & Privacy": ["Privacy", "Digital Footprint"],
                "People": ["Influencer"],
            }),
            typed("Activity 9 – I send a ______ when I want to communicate privately.", ["message"], review=True),
            typed("Activity 9 – I receive a ______ when someone likes my post.", ["notification"], review=True),
            typed("Activity 9 – A famous online content creator is called an ______.", ["influencer"], review=True),
            typed("Activity 9 – People can leave a ______ under a post.", ["comment"], review=True),
            typed("Activity 9 – Your online activities create a ______.", ["digital footprint"], review=True),
            typed("Activity 9 – Many people use ______ to connect with friends.", ["social media"], review=True),
            typed("Activity 9 – A ______ allows you to talk face-to-face online.", ["video call"], review=True),
            typed("Activity 9 – I can ______ a post if I want others to see it.", ["share"], review=True),
            typed("Activity 9 – My personal information should be protected through ______ settings.", ["privacy"], review=True),
            typed("Activity 9 – An ______ contains information about a user.", ["online profile"], review=True),
        ],
        "grammar": [
            heading("Review Corner"),
            mcq("I ______ to Anuradhapura during the school holidays.", ["went", "have gone", "go"], "went"),
            mcq("She ______ never travelled by plane.", ["has", "is", "was"], "has"),
            mcq("Next month, we ______ visit our relatives.", ["are going to", "went", "have"], "are going to"),
            mcq("The internet is ______ than traditional mail.", ["faster", "fast", "fastest"], "faster"),
            mcq("My father ______ a new smartphone last week.", ["bought", "buy", "buying"], "bought"),
            mcq("Have you ever ______ a famous person?", ["met", "meet", "meeting"], "met"),
            mcq("We ______ to the museum yesterday.", ["went", "have gone", "going"], "went"),
            mcq("My sister ______ travelled abroad twice.", ["has", "have", "was"], "has"),
            mcq("Technology has made communication ______.", ["easier", "easy", "easiest"], "easier"),
            mcq("I ______ going to start a new course next month.", ["am", "was", "have"], "am"),
            mcq("They ______ many interesting people during their trip.", ["met", "have met", "meeting"], "met"),
            mcq("She ______ a video call with her friend yesterday.", ["had", "has", "having"], "had"),
            heading("A. Present Perfect vs Past Simple"),
            plain("We use the Present Perfect to talk about experiences, achievements, and actions connected "
                  "to the present.\nStructure: Subject + have/has + past participle"),
            examples("Present Perfect", ["I have visited many places in Sri Lanka.", "She has learned three languages.",
                                         "We have met many interesting people."]),
            plain("We use the Past Simple for actions that happened at a specific time in the past.\n"
                  "Structure: Subject + past verb"),
            examples("Past Simple", ["I visited Kandy last year.", "She learned French in school.",
                                     "We met our teacher yesterday."]),
            plain("IMPORTANT\nPresent Perfect: ✔ Experience ✔ No specific time ✔ Life events\n"
                  "Past Simple: ✔ Finished action ✔ Specific time mentioned ✔ Yesterday, last year, in 2023"),
            examples("Compare", ["I have visited Galle. - (Experience)", "I visited Galle in 2024. - (Specific time)"]),
            plain("Sinhala Help\nI have travelled abroad. → මම විදේශයකට ගොස් තිබෙනවා.\n"
                  "I travelled abroad last year. → මම ගිය අවුරුද්දේ විදේශයකට ගියා."),
            mcq("Activity 10 – I ______ to Ella in 2023.", ["travelled", "have travelled"], "travelled"),
            mcq("Activity 10 – She ______ many interesting people in her life.", ["has met", "met"], "has met"),
            mcq("Activity 10 – We ______ that movie last weekend.", ["watched", "have watched"], "watched"),
            mcq("Activity 10 – I ______ never travelled by ship.", ["have", "travelled"], "have"),
            mcq("Activity 10 – My father ______ in Colombo for ten years.", ["has worked", "worked"], "has worked"),
            mcq("Activity 10 – They ______ to Kandy last month.", ["went", "have gone"], "went"),
            mcq("Activity 10 – I ______ many useful skills.", ["have learned", "learned yesterday"], "have learned"),
            mcq("Activity 10 – She ______ her best friend in school.", ["met", "has met"], "met"),
            mcq("Activity 10 – We ______ several workshops this year.", ["have attended", "attended last year"], "have attended"),
            mcq("Activity 10 – He ______ a new job in January.", ["started", "has started"], "started"),
            mcq("Activity 10 – I ______ this book before.", ["have read", "read yesterday"], "have read"),
            mcq("Activity 10 – They ______ to Jaffna during the holidays.", ["travelled", "have travelled in 2022"], "travelled"),
            mcq("Activity 11 – I (have visited / visited) Kandy three times.", ["have visited", "visited"], "have visited", review=True),
            mcq("Activity 11 – She (has travelled / travelled) to India last year.", ["has travelled", "travelled"], "travelled", review=True),
            mcq("Activity 11 – We (met / have met) many people during our lives.", ["met", "have met"], "have met", review=True),
            mcq("Activity 11 – I (have completed / completed) my project yesterday.", ["have completed", "completed"], "completed", review=True),
            mcq("Activity 11 – My parents (have lived / lived) here since 2015.", ["have lived", "lived"], "have lived", review=True),
            mcq("Activity 11 – He (went / has gone) to Galle last weekend.", ["went", "has gone"], "went", review=True),
            mcq("Activity 11 – I (have never seen / never saw) snow.", ["have never seen", "never saw"], "have never seen", review=True),
            mcq("Activity 11 – They (have achieved / achieved) many goals this year.", ["have achieved", "achieved"], "have achieved", review=True),
            mcq("Activity 11 – She (received / has received) an award in 2022.", ["received", "has received"], "received", review=True),
            mcq("Activity 11 – We (have improved / improved) our English a lot.", ["have improved", "improved"], "have improved", review=True),
            order("Activity 12 – Life Story Timeline. Place the events in order.", [
                "Learned English", "Graduated from school", "Started university", "Got first job",
                "Completed a professional course", "Received promotion",
            ]),
            heading("B. Used to – Past Habits & Past States"),
            plain("We use \"used to\" for: ✔ Past habits ✔ Past routines ✔ Situations that are no longer true"),
            examples("Examples", ["I used to play cricket every evening.", "We used to write letters to friends.",
                                  "People used to use landline phones.", "I used to be shy.", "She used to live in Kandy."]),
            examples("Compare", ["Past - I used to play outside.", "Present - Now I spend more time online."]),
            plain("Sinhala Help\nI used to play outside. → මම ඉස්සර එළියේ සෙල්ලම් කළා.\n"
                  "People used to send letters. → මිනිස්සු ඉස්සර ලිපි යැව්වා."),
            write("Activity 13 – Complete the sentences.", [
                "When I was younger, I used to ______.", "My family used to ______ every weekend.",
                "We used to communicate by ______.", "I used to spend most of my free time ______.",
                "My friends and I used to ______ after school.", "I used to think that ______.",
                "People used to ______ before smartphones became popular.", "My school used to ______.",
                "I used to be ______.", "My parents used to ______.",
            ], min_words=2),
            match("Activity 14 – Past and Present Comparison. Match the ideas.", [
                ("Used to send letters", "Use messaging apps"), ("Used to buy newspapers", "Read online news"),
                ("Used to use maps", "Use GPS"), ("Used to watch DVDs", "Stream movies"),
                ("Used to use landline phones", "Use smartphones"),
            ]),
            write("Activity 15 – Complete the comparison. Example: I used to play outside every day, but now I spend more time online.", [
                "I used to ____________, but now I ____________.",
                "My family used to ____________, but now we ____________.",
                "People used to ____________, but now they ____________.",
                "Students used to ____________, but now they ____________.",
                "I used to believe ____________, but now I think ____________.",
                "We used to communicate through ____________, but now we use ____________.",
                "I used to spend my weekends ____________, but now I ____________.",
                "My friends and I used to ____________, but now we ____________.",
            ], min_words=4),
            heading("C. Relationship Phrasal Verbs"),
            phrases(None, [
                ("Get Along With", "හොඳින් එකට ඉන්නවා"), ("Look Up To", "ගෞරව කරනවා"), ("Grow Up", "වැඩෙනවා"),
                ("Break Up", "සම්බන්ධතාවයක් අවසන් කරනවා"), ("Make Up", "රණ්ඩුවකින් පසු සමථයට පත්වෙනවා"),
                ("Take After", "කෙනෙකු වගේ වීම"), ("Bring Up", "ඇති දැඩි කරනවා"),
                ("Catch Up With", "කාලයකට පසු නැවත හමුවී කතා කරනවා"),
            ]),
            match("Activity 16 – Match the phrasal verb.", [
                ("Get Along With", "Have a good relationship"), ("Look Up To", "Admire someone"),
                ("Grow Up", "Become an adult"), ("Break Up", "End a relationship"),
                ("Make Up", "Become friends again"), ("Take After", "Be similar to a family member"),
                ("Bring Up", "Raise a child"), ("Catch Up With", "Talk after a long time"),
            ]),
            mcq("Activity 17 – I really ______ my older sister because she is hardworking.", ["look up to", "break up", "make up"], "look up to"),
            mcq("Activity 17 – My brother and I ______ very well.", ["get along", "break up", "grow up"], "get along"),
            mcq("Activity 17 – After the argument, they decided to ______.", ["make up", "grow up", "take after"], "make up"),
            mcq("Activity 17 – My nephew ______ his father.", ["takes after", "breaks up", "catches up"], "takes after"),
            mcq("Activity 17 – We ______ together in the same neighbourhood.", ["grew up", "looked up", "made up"], "grew up"),
            mcq("Activity 17 – My grandparents ______ six children.", ["brought up", "broke up", "took after"], "brought up"),
            mcq("Activity 17 – I met my school friend yesterday and we ______ for two hours.", ["caught up", "broke up", "looked up"], "caught up"),
            mcq("Activity 17 – The couple decided to ______ after many disagreements.", ["break up", "make up", "get along"], "break up"),
            mcq("Activity 18 – Two friends had an argument but became friends again.", ["make up", "take after", "grow up"], "make up", review=True),
            mcq("Activity 18 – A child behaves very similarly to her mother.", ["take after", "bring up", "break up"], "take after", review=True),
            mcq("Activity 18 – A student admires his teacher greatly.", ["look up to", "catch up with", "make up"], "look up to", review=True),
            mcq("Activity 18 – Brothers have a positive relationship.", ["get along with", "break up", "grow up"], "get along with", review=True),
            mcq("Activity 18 – Friends meet after five years and talk about their lives.", ["catch up with", "look up to", "bring up"], "catch up with", review=True),
            mcq("Activity 18 – Parents raise their children with care.", ["bring up", "take after", "make up"], "bring up", review=True),
            mcq("Activity 18 – A teenager becomes an adult.", ["grow up", "break up", "catch up with"], "grow up", review=True),
            mcq("Activity 18 – A couple ends their relationship.", ["break up", "make up", "get along with"], "break up", review=True),
        ],
        "pronunciation": [
            phrases("Listen & Repeat", [
                ("Achievement", "අචීව්මන්ට්"), ("Experience", "එක්ස්පීරියන්ස්"), ("Challenge", None),
                ("Childhood", "චයිල්ඩ්හුඩ්"), ("Reliable", "රිලයබල්"), ("Supportive", "සපෝටිව්"),
                ("Independent", "ඉන්ඩිපෙන්ඩන්ට්"), ("Communication", "කමියුනිකේෂන්"),
                ("Influencer", "ඉන්ෆ්ලුවන්සර්"), ("Relationship", "රිලේෂන්ෂිප්"),
            ]),
            *[speak("Tap & Speak: say the word clearly.", w, seconds=5) for w in [
                "Achievement", "Experience", "Challenge", "Childhood", "Reliable", "Supportive",
                "Independent", "Communication", "Influencer", "Relationship"]],
            heading("Sentence Stress Practice"),
            *[speak(f"Say the sentence. Stress the word in capitals: {s}", t, seconds=10) for s, t in [
                ("I HAVE achieved many goals.", "I have achieved many goals."),
                ("She HAS learned a new skill.", "She has learned a new skill."),
                ("We USED TO play outside every day.", "We used to play outside every day."),
                ("My best friend is VERY supportive.", "My best friend is very supportive."),
                ("Social media has CHANGED communication.", "Social media has changed communication."),
            ]],
        ],
        "listening": [
            plain("LISTENING TIP\nWhen listening to people talk about their lives:\n✔ Listen for time expressions.\n"
                  "✔ Listen for life experiences.\n✔ Listen for opinions.\n✔ Listen for words that show change.\n"
                  "Examples: when I was younger • in the past • nowadays • recently • over the years"),
            heading("Listening Text 1 – My Life Has Changed a Lot"),
            *[mcq(f"Activity 19 – {q}", o, a, listen=L1_TEXT1) for q, o, a in [
                ("What is Nadeesha's job?", ["Graphic Designer", "Teacher", "Engineer"], "Graphic Designer"),
                ("What was she like when she was younger?", ["Shy", "Outgoing", "Confident"], "Shy"),
                ("Where did her life begin to change?", ["University", "School", "Workplace"], "University"),
                ("What did she join?", ["Student Clubs", "Sports Teams", "Music Groups"], "Student Clubs"),
                ("What skills has she learned?", ["Communication Skills", "Driving Skills", "Cooking Skills"], "Communication Skills"),
                ("Has she travelled around Sri Lanka?", ["Yes", "No"], "Yes"),
                ("How does she feel about her progress?", ["Proud", "Disappointed", "Uncertain"], "Proud"),
                ("What is she going to do next year?", ["Start a business", "Move abroad", "Change careers"], "Start a business"),
                ("Which adjective best describes her now?", ["Confident", "Shy", "Nervous"], "Confident"),
                ("What is the main message of the story?", ["People can grow and change", "University is difficult", "Work is stressful"], "People can grow and change"),
            ]],
            *[tf(f"Activity 20 – {s}", a, listen=L1_TEXT1) for s, a in [
                ("Nadeesha is twenty-four years old.", True), ("She used to be very confident.", False),
                ("She joined clubs at university.", True), ("She has learned communication skills.", True),
                ("She dislikes working with people.", False), ("She has travelled for work.", True),
                ("She is planning to start a business.", True), ("She regrets her university experience.", False),
            ]],
            *[typed(f"Activity 21 – {s}", [a], listen=L1_TEXT1) for s, a in [
                ("When I was younger, I used to be very ______.", "shy"),
                ("I joined several student ______.", "clubs"),
                ("Over time, I became more ______ and independent.", "confident"),
                ("I have made many close ______.", "friends"),
                ("Next year, I am going to start my own ______ business.", "design"),
            ]],
            heading("Listening Text 2 – Social Media in Modern Life"),
            *[mcq(f"Activity 22 – {q}", o, a, listen=L1_TEXT2) for q, o, a in [
                ("Why do people use social media?", ["To communicate", "To travel", "To cook"], "To communicate"),
                ("What do students share?", ["Educational Resources", "Tickets", "Furniture"], "Educational Resources"),
                ("Why do businesses use social media?", ["Promote products", "Teach lessons", "Build houses"], "Promote products"),
                ("What is one disadvantage?", ["Too much screen time", "Faster communication", "Easy sharing"], "Too much screen time"),
                ("What is another concern?", ["Privacy", "Transport", "Weather"], "Privacy"),
                ("Should people share personal information carelessly?", ["No", "Yes"], "No"),
                ("Does the speaker think social media is useful?", ["Yes", "No"], "Yes"),
                ("What is the speaker's advice?", ["Use it responsibly", "Avoid it completely", "Use it all day"], "Use it responsibly"),
            ]],
        ],
        "reading": [
            plain("READING TIP\nWhen reading opinion texts:\n✔ Identify facts.\n✔ Identify opinions.\n"
                  "✔ Look for reasons and examples.\n✔ Notice linking words.\n"
                  "Examples: because • however • although • therefore"),
            passage("Reading Passage 1 – My Life Has Changed Since School", L1_PASSAGE1,
                    "පාසල් කාලයේ ලේඛකයා නිහඬ ශිෂ්‍යයෙක් විය.\nවිශ්වවිද්‍යාලයේ අත්දැකීම් ඔහුට විශ්වාසය ලබා දුන්නා.\n"
                    "අද ඔහු වඩා සමාජශීලී හා විශ්වාසවන්තය."),
            *[mcq(f"Activity 23 – {q}", o, a, review=True) for q, o, a in [
                ("What was the writer like at school?", ["Quiet and nervous with new people", "Loud and popular", "Always a leader"], "Quiet and nervous with new people"),
                ("What did the writer use to do?", ["Read books and work alone", "Play sports every day", "Speak in public"], "Read books and work alone"),
                ("What helped the writer change?", ["University and student organizations", "A new school", "Moving abroad"], "University and student organizations"),
                ("What skills did the writer develop?", ["Working with people and communicating effectively", "Cooking and driving", "Drawing and painting"], "Working with people and communicating effectively"),
                ("What does the writer enjoy today?", ["Public speaking and teamwork", "Reading alone", "Staying at home"], "Public speaking and teamwork"),
                ("What lesson did the writer learn?", ["Personal growth happens when we challenge ourselves", "School is the most important time", "It is better to work alone"], "Personal growth happens when we challenge ourselves"),
                ("Was personal growth immediate?", ["No, it happened over a few years", "Yes, it happened in one day"], "No, it happened over a few years"),
                ("What role did university play?", ["It gave the writer new experiences", "It made the writer more shy", "It was not important"], "It gave the writer new experiences"),
                ("How did teamwork help?", ["It helped the writer communicate with different people", "It made the writer nervous", "It did not help"], "It helped the writer communicate with different people"),
                ("What is the main message of the passage?", ["People grow when they challenge themselves", "University is difficult", "Books are better than people"], "People grow when they challenge themselves"),
            ]],
            match("Activity 24 – Information matching.", [
                ("School Years", "Quiet and shy"), ("University", "New experiences"),
                ("Workshops", "Skill development"), ("Teamwork", "Communication skills"),
                ("Leadership Programmes", "Personal growth"),
            ]),
            write("Activity 25 – Find evidence. Answer in complete sentences.", [
                "Why did the writer feel nervous?", "How did university help?",
                "What activities did the writer participate in?", "What skills were developed?",
                "What advice can we learn from the passage?",
            ], min_words=5, models=[
                "The writer felt nervous when meeting new people because he was a quiet student.",
                "University helped because the writer joined student organizations and became more confident and independent.",
                "The writer participated in workshops, community projects and leadership programmes.",
                "The writer developed skills such as working with different people, communicating effectively, public speaking and teamwork.",
                "We can learn that personal growth often happens when we challenge ourselves.",
            ], review=True),
            passage("Reading Passage 2 – Social Media: Helpful or Harmful?", L1_PASSAGE2,
                    "සමාජ මාධ්‍යට වාසි සහ අවාසි දෙකම ඇත.\nඑය මිනිසුන් සම්බන්ධ කරයි.\nනමුත් අධික භාවිතය ගැටලු ඇති කළ හැක."),
            cat("Activity 26 – Fact or Opinion? Sort each statement.", {
                "Fact": ["Social media helps people communicate.", "Many students use social media for learning.",
                         "Privacy concerns exist online.", "Social media can help communities grow."],
                "Opinion": ["Social media is the best invention ever.", "Social media is harmful for everyone.",
                            "Responsible use is important.", "Everyone should delete social media."],
            }, review=True),
            cat("Activity 27 – Compare the arguments.", {
                "Advantages": ["Communication", "Learning", "Sharing information", "Building communities"],
                "Disadvantages": ["Addiction", "Privacy concerns", "Misinformation", "Reduced face-to-face interaction"],
            }),
        ],
        "speaking": [
            heading("A. Life Experience Interview"),
            *interview(
                "The app is your interviewer. Each question is shown on screen and played as audio. Listen, then "
                "record your answer in full sentences. (ප්‍රශ්නවලට සම්පූර්ණ වාක්‍යවලින් පිළිතුරු දෙන්න.) After you "
                "answer, compare with the model answer, key vocabulary, and useful expressions.",
                [
                    ("What experience has changed your life the most?", "The experience that changed my life the most was starting my first job. I have learned how to work with different people and manage my time."),
                    ("What did you use to be like as a child?", "When I was younger, I used to be very shy and quiet. I used to spend most of my time reading alone."),
                    ("Have you achieved any important goals?", "Yes, I have achieved a few important goals. For example, I have completed an English course and improved my speaking."),
                    ("Who has influenced your life the most?", "The person who has influenced my life the most is my mother, because she is hard-working and kind."),
                    ("What valuable lesson have you learned?", "One valuable lesson I have learned is that failure is part of success, so I never give up."),
                    ("How have you changed over the years?", "Over the years, I have become more confident and independent than before."),
                    ("What challenge have you overcome?", "One challenge I have overcome is my fear of speaking in public. I used to feel nervous, but now I enjoy it."),
                    ("What are your future goals?", "In the future, I am going to start my own small business and keep learning new skills."),
                ],
                expressions=["I have + past participle … (experience) — I have travelled to many places.",
                             "I used to … (past habit) — I used to be very shy.",
                             "The person who has influenced me most is …", "One lesson I have learned is …",
                             "In the future, I am going to …"],
                vocabulary=["experience", "achievement", "challenge", "confident", "independent", "influence", "goal"],
            ),
            heading("B. Social Media Debate"),
            plain("Step 1 — Read the statement: “Social media does more good than harm.” "
                  "(සමාජ මාධ්‍ය හානියට වඩා යහපත වැඩිය.)\nStep 2 — Choose your position: Agree or Disagree.\n"
                  "Step 3 — Select two or three reasons that support your position."),
            examples("If you AGREE", ["It helps people stay connected across long distances.",
                                      "Students can learn and share educational resources.",
                                      "Businesses can reach and connect with customers.",
                                      "Useful information and news spread quickly.",
                                      "People can build communities with shared interests."]),
            examples("If you DISAGREE", ["It can become addictive and reduce real-life activity.",
                                         "It creates privacy and personal-data concerns.",
                                         "It can spread false information (misinformation).",
                                         "It reduces face-to-face communication.",
                                         "Too much use can affect mental health."]),
            speak("Step 4 — Record a 30-second opinion. Begin with “In my opinion …”, give at least two reasons, "
                  "and add one example from your own experience. Model (Agree):",
                  "In my opinion, social media does more good than harm. First, it helps people stay connected with family and friends who live far away. Second, students can share notes and learn new things online. For example, I have joined study groups on social media that helped me improve my English. If we use it responsibly, the benefits are greater than the risks.",
                  seconds=45, review=True),
            speak("Step 5 — Now give the other side. Model (Disagree):",
                  "In my opinion, social media does more harm than good. First, many people spend too much time online and become less active. Second, there are serious privacy concerns and a lot of misinformation. For example, false news can spread very quickly and cause panic. Although it connects people, the risks are greater when it is not used carefully.",
                  seconds=45, review=True),
            heading("C. Fluency Challenge"),
            speak("Speak for 2 minutes. Topic: “My Journey So Far”. Include: childhood, past habits, important "
                  "experiences, relationships, achievements, future goals. Model:",
                  "When I was a child, I used to live in a small village and I was very shy. I used to spend my free time reading and playing with my cousins. An important experience in my life was going to university, where I have met many good friends. My best friend is very supportive and I really look up to my older sister. I have completed an English course and I have started my first job. In the future, I am going to keep learning and travel to new places.",
                  seconds=120, review=True),
        ],
        "writing": [
            write("Activity 28 – Guided writing. Complete the sentences.", [
                "One experience that changed my life was ______.", "I used to ______ when I was younger.",
                "Today, I am more ______ because ______.", "Someone I look up to is ______.",
                "They influenced me by ______.", "Social media helps me ______.",
                "One challenge I overcame was ______.", "My future goal is ______.",
            ], min_words=2),
            write("Activity 29 – Personal narrative. Write 150–180 words.", [
                "Topic: “My Life Story So Far”. Include: childhood, important experiences, challenges, "
                "achievements, present life, future plans.",
            ], min_words=150),
            write("Activity 30 – Opinion essay. Write 150–180 words.", [
                "Topic: “Is Social Media Helpful or Harmful?”. Include: your opinion, at least two reasons, "
                "one example, a conclusion.",
            ], min_words=150),
            self_check(
                "□ I can distinguish between Present Perfect and Past Simple.\n□ I can use \"used to\" accurately.\n"
                "□ I can describe people's personalities.\n□ I can discuss relationships and communication.\n"
                "□ I can understand longer listening texts.\n□ I can identify facts and opinions.\n"
                "□ I can express and justify my opinions.\n□ I can write a personal narrative.\n"
                "□ I can write an opinion paragraph.\n□ I can speak confidently about my experiences.",
                prompt="Self-assessment",
            ),
            summary(["Present Perfect vs Past Simple", "Used to for past habits", "Character adjectives",
                     "Relationship phrasal verbs", "Talking about social media"]),
        ],
    },
}
