"""Level 3 Lesson 2 — Travel, Culture & Traditions.

Source: LEVEL_3_L2_individual.docx. review=True marks keys/models by the
King Guru team. "Discuss" instructions use the follow-up Part D rule.
"""
from .dsl import (DISCUSS, cat, examples, heading, mcq, order, passage, phrases, plain,
                  self_check, speak, summary, tf, typed, words, write)

TEXT1 = (
    "Last July, my family and I travelled to Polonnaruwa during the school holidays. Before the trip, we "
    "planned our itinerary carefully because we wanted to visit several important historical sites. The "
    "weather was warm and sunny when we arrived. While we were walking through the ancient city, our guide "
    "explained how Polonnaruwa became one of Sri Lanka's most important kingdoms. As we were exploring the "
    "ruins of the Royal Palace, we noticed the impressive stone walls and ancient architecture. Many tourists "
    "were taking photographs while the guide was describing the history of the site. Later, we visited Gal "
    "Vihara, where we admired the beautiful stone statues of the Buddha. While we were listening to the "
    "guide's explanation, I realised how advanced the ancient civilisation had been. In the afternoon, we "
    "cycled around several archaeological sites and learned about irrigation systems that were built "
    "hundreds of years ago. The trip was both educational and enjoyable because it helped us understand "
    "Sri Lanka's rich cultural heritage."
)
TEXT2 = (
    "Every year, thousands of people visit Kandy to witness the Esala Perahera, one of the most famous "
    "cultural festivals in Sri Lanka. Last year, my family and I attended the festival for the first time. "
    "As we were walking through the crowded streets, traditional drummers were performing energetic rhythms. "
    "Decorated elephants were moving slowly through the procession while dancers performed around them. "
    "Many visitors were taking photographs as the parade passed by. The atmosphere was exciting because "
    "everyone was celebrating together. While we were watching the performances, a guide explained the "
    "history of the festival and its connection to Sri Lankan heritage. We learned that the festival has "
    "been celebrated for centuries and remains an important symbol of cultural identity. At the end of the "
    "evening, we felt proud of our traditions and grateful for the opportunity to experience such an "
    "important event."
)
PASSAGE1 = (
    "Two years ago, I had the opportunity to visit Jaffna with my family during the December holidays. "
    "Although I had travelled to many places in Sri Lanka before, this trip felt completely different. As we "
    "were driving through the Northern Province, I noticed how the landscape, language, and culture "
    "gradually changed. When we arrived in Jaffna, we visited several famous landmarks, including the Jaffna "
    "Fort and the Nallur Kandaswamy Temple. While we were exploring the temple grounds, a religious ceremony "
    "was taking place. Many worshippers were offering flowers and participating in traditional rituals. Our "
    "guide explained the history of the temple and its importance to the local community. Later, we tried "
    "several traditional Jaffna dishes. At first, some of the food seemed unfamiliar, but I soon discovered "
    "that the flavours were unique and delicious. One evening, we spoke with local residents who shared "
    "stories about the region's history and traditions. These conversations helped me understand the "
    "culture beyond what I could learn from books or websites. By the end of the trip, I realised that "
    "travelling is not only about visiting new places. It is also about understanding different people, "
    "traditions, and ways of life."
)
PASSAGE2 = (
    "Festivals play an important role in preserving culture and bringing communities together. Across the "
    "world, people celebrate festivals for religious, historical, and social reasons. These events often "
    "include music, dance, food, ceremonies, and traditional clothing. For many communities, festivals help "
    "pass traditions from one generation to another. Young people learn about their heritage while older "
    "generations share their knowledge and experiences. Festivals also encourage social unity. People from "
    "different backgrounds often come together to participate in celebrations and cultural events. In "
    "addition, festivals attract tourists, creating economic opportunities for local businesses. Hotels, "
    "restaurants, and craft sellers often benefit when visitors attend major festivals. However, some people "
    "argue that modern celebrations are becoming too commercial. They believe that traditional values may be "
    "lost when festivals focus mainly on entertainment or tourism. Others argue that change is natural and "
    "that festivals must evolve to remain relevant. Regardless of these opinions, most people agree that "
    "festivals remain an important part of cultural identity."
)
MODEL_SPEAKER = (
    "I would like to compare the Sinhala and Tamil New Year in Sri Lanka with the New Year celebration in "
    "Japan. Both festivals are about new beginnings and family. In Sri Lanka, people clean their houses, light "
    "the oil lamp at the auspicious time, and prepare kiribath and sweets such as kokis and kavum. In Japan, "
    "families also clean their homes before the New Year, and they eat special food called osechi. One "
    "difference is the date: our New Year is in April, but the Japanese New Year is on the first of January. "
    "Another difference is that we play traditional games in the village, while many Japanese people visit a "
    "shrine to pray. However, in both cultures, children receive money from their elders. I think both "
    "traditions teach us to respect our families and to start the year with hope."
)

TRAVEL_WORDS = ["Itinerary", "Souvenir", "Sightseeing", "Local Guide", "Exploration", "Accommodation",
                "Destination", "Landmark"]
CULTURE_WORDS = ["Festival", "Tradition", "Heritage", "Procession", "Performance", "Ceremony",
                 "Cultural Identity", "Preserve"]


def _pick(answer: str, pool: list[str]) -> list[str]:
    """The answer and two other words from the same list."""
    others = [w for w in pool if w != answer]
    i = pool.index(answer)
    return [answer, others[i % len(others)], others[(i + 3) % len(others)]]


LESSON = {
    "order": 2,
    "title": "Travel, Culture & Traditions",
    "title_si": "සංචාරය, සංස්කෘතිය සහ සම්ප්‍රදායන්",
    "description": "Describe journeys and festivals with narrative tenses and compare cultural traditions (B1).",
    "objectives": [
        "Describe travel experiences using narrative tenses",
        "Talk about cultural traditions and festivals",
        "Sequence past events using appropriate time markers",
        "Compare traditions and customs from different cultures",
        "Understand spoken and written travel narratives",
        "Speak confidently about memorable journeys and cultural experiences",
        "Write a descriptive paragraph about a cultural event or travel experience",
    ],
    "sections": {
        "vocabulary": [
            words("A. Travel Adventures", [
                ("Destination", "ගමනාන්තය"), ("Expedition", "ගවේෂණ චාරිකාව"), ("Landmark", "ප්‍රසිද්ධ ස්ථානය"),
                ("Itinerary", "සංචාර සැලැස්ම"), ("Sightseeing", "දර්ශන නැරඹීම"), ("Accommodation", "නවාතැන්"),
                ("Backpacker", "බෑගයක් රැගෙන සංචාරය කරන පුද්ගලයා"), ("Souvenir", "සිහිවටන තෑග්ග"),
                ("Local Guide", "ප්‍රාදේශීය මාර්ගෝපදේශකයා"), ("Journey", "ගමන"), ("Adventure", "වික්‍රමය"),
                ("Exploration", "ගවේෂණය"),
            ]),
            cat("Activity 3 – Travel Planner. You are planning a three-day trip. Place the items into the correct category.", {
                "Planning": ["Destination", "Itinerary", "Local Guide"],
                "During the Trip": ["Sightseeing", "Exploration", "Adventure"],
                "After the Trip": ["Souvenir", "Travel Photos", "Travel Journal"],
            }),
            *[mcq(f"Activity 4 – {s}", _pick(a, TRAVEL_WORDS), a, review=True) for s, a in [
                ("You are creating a day-by-day schedule for your trip.", "Itinerary"),
                ("You buy a small gift to remember your holiday.", "Souvenir"),
                ("You visit famous attractions in a city.", "Sightseeing"),
                ("Someone helps you understand local history.", "Local Guide"),
                ("You travel to discover new places and experiences.", "Exploration"),
                ("You need a place to stay overnight.", "Accommodation"),
                ("You decide where your trip will end.", "Destination"),
                ("You visit an ancient historical site.", "Landmark"),
            ]],
            words("B. Culture & Traditions", [
                ("Heritage", "උරුමය"), ("Custom", "චාරිත්‍රය"), ("Tradition", "සම්ප්‍රදාය"),
                ("Ceremony", "උත්සව චාරිත්‍රය"), ("Festival", "උත්සවය"), ("Procession", "පෙරහැර"),
                ("Ritual", "චාරිත්‍රානුකූල ක්‍රියාව"), ("Celebration", "සැමරුම"), ("Community", "ප්‍රජාව"),
                ("Cultural Identity", "සංස්කෘතික අනන්‍යතාවය"), ("Performance", "ප්‍රසංගය"),
                ("Preserve", "ආරක්ෂා කර පවත්වාගෙන යාම"),
            ]),
            cat("Activity 5 – Heritage Explorer. Sort the words into the correct categories.", {
                "Cultural Events": ["Festival", "Celebration", "Performance"],
                "Traditional Practices": ["Ritual", "Ceremony", "Custom"],
                "Cultural Values": ["Heritage", "Cultural Identity", "Preserve"],
                "Community Activities": ["Procession", "Community"],
            }),
            *[mcq(f"Activity 6 – {s}", _pick(a, CULTURE_WORDS), a, review=True) for s, a in [
                ("A community gathers every year to celebrate an important event.", "Festival"),
                ("People follow a practice that has existed for generations.", "Tradition"),
                ("A country protects ancient buildings and traditions.", "Heritage"),
                ("A large group walks through the streets during a religious event.", "Procession"),
                ("Traditional dances are shown to visitors.", "Performance"),
                ("A special event marks an important occasion.", "Ceremony"),
                ("People feel connected through shared traditions.", "Cultural Identity"),
                ("Historical sites are protected for future generations.", "Preserve"),
            ]],
        ],
        "grammar": [
            heading("Review Corner"),
            plain("From Lesson 1: ✔ Present Perfect ✔ Past Simple ✔ Used To ✔ Life Experiences ✔ Communication Skills"),
            examples("Examples", ["I have visited many historical places.", "I travelled to Kandy last year.",
                                  "I used to spend my holidays with my grandparents."]),
            mcq("Activity 1 – Your friend asks if you have ever visited a UNESCO World Heritage Site.",
                ["Yes, I have visited Sigiriya twice.", "Yes, I visit.", "Yes, I visiting."], "Yes, I have visited Sigiriya twice."),
            mcq("Activity 1 – A tourist asks about a place you visited last year.",
                ["I visited Anuradhapura last August.", "I have visited last August.", "I visiting last August."], "I visited Anuradhapura last August."),
            mcq("Activity 1 – Your teacher asks about an important cultural experience.",
                ["I attended the Kandy Esala Perahera and learned about Sri Lankan traditions.", "I attend.", "I attending."],
                "I attended the Kandy Esala Perahera and learned about Sri Lankan traditions."),
            mcq("Activity 1 – Someone asks how communication has changed for travellers.",
                ["Travellers can now share experiences instantly through social media.", "Travellers instant.", "Share travelling."],
                "Travellers can now share experiences instantly through social media."),
            mcq("Activity 1 – You are describing a memorable trip.",
                ["I travelled with my family and explored several historical sites.", "I travel family.", "I exploring."],
                "I travelled with my family and explored several historical sites."),
            write(f"Activity 2 – Cultural Reflection. {DISCUSS}", [
                "What is the most interesting place you have visited?", "Which festival in Sri Lanka do you enjoy the most?",
                "Why do people travel?", "What can travellers learn from different cultures?",
                "Should tourists respect local traditions? Why?", "What makes a journey memorable?",
                "What cultural tradition should future generations protect?",
                "Have you ever learned something important while travelling?",
            ], min_words=5),
            heading("Narrative Tenses: Past Simple + Past Continuous"),
            plain("We often use Past Continuous to describe a longer action in progress. We use Past Simple for a "
                  "shorter action that interrupted it."),
            examples("Examples", ["While we were exploring the ancient city, we discovered a hidden temple.",
                                  "As the musicians were performing, the crowd started cheering.",
                                  "The tourists were taking photographs when the rain suddenly began."]),
            plain("Sinhala Help\nWhile we were exploring the city, we discovered a hidden temple.\n"
                  "→ අපි නගරය ගවේෂණය කරමින් සිටියදී සැඟවුණු පන්සලක් සොයාගත්තා.\n"
                  "The tourists were taking photographs when it started raining.\n"
                  "→ සංචාරකයන් ඡායාරූප ගනිමින් සිටියදී වැස්ස පටන් ගත්තා."),
            typed("Activity 7 – Complete the story: Last year, my family ______ (travel) to Kandy.", ["travelled", "traveled"], review=True),
            typed("Activity 7 – While we ______ (walk) around the city, we suddenly ______ (hear) traditional drums. Type both verbs, with a comma between them.",
                  ["were walking, heard"], review=True),
            typed("Activity 7 – Many performers ______ (dance) in the streets when the procession ______ (arrive). Type both verbs, with a comma between them.",
                  ["were dancing, arrived"], review=True),
            typed("Activity 7 – As we ______ (watch) the event, a local guide ______ (explain) its history. Type both verbs, with a comma between them.",
                  ["were watching, explained"], review=True),
            typed("Activity 7 – People ______ (celebrate) enthusiastically while musicians ______ (play) traditional music. Type both verbs, with a comma between them.",
                  ["were celebrating, were playing"], review=True),
            typed("Activity 7 – Later, we ______ (visit) a museum and ______ (learn) more about the festival. Type both verbs, with a comma between them.",
                  ["visited, learned", "visited, learnt"], review=True),
            mcq("Activity 8 – While the tourists were exploring the temple...",
                ["they discovered an ancient painting.", "they exploring.", "they discovery."], "they discovered an ancient painting."),
            mcq("Activity 8 – As the ceremony was beginning...",
                ["hundreds of visitors arrived.", "hundreds arriving.", "hundreds arrival."], "hundreds of visitors arrived."),
            mcq("Activity 8 – While we were travelling through the mountains...",
                ["we saw a beautiful waterfall.", "we seeing.", "we sawed."], "we saw a beautiful waterfall."),
            mcq("Activity 8 – As the guide was speaking...",
                ["everyone listened carefully.", "everyone listening.", "everyone listen."], "everyone listened carefully."),
            mcq("Activity 8 – While the dancers were performing...",
                ["the audience took photographs.", "audience taking.", "audience photograph."], "the audience took photographs."),
        ],
        "pronunciation": [
            phrases("Listen & Repeat", [
                ("Destination", None), ("Heritage", "හෙරිටිජ්"), ("Tradition", None), ("Ceremony", "සෙරමනි"),
                ("Procession", "ප්‍රොසෙෂන්"), ("Exploration", "එක්ස්ප්ලොරේෂන්"), ("Adventure", None),
                ("Accommodation", "අකොමඩේෂන්"), ("Performance", "පර්ෆෝමන්ස්"), ("Cultural Identity", None),
            ]),
            plain("Common Pronunciation Problems\nHeritage — Wrong: හෙරිටේජ් · Correct: හෙරිටිජ්\n"
                  "Procession — Wrong: ප්‍රොසෙසන් · Correct: ප්‍රොසෙෂන්\n"
                  "Accommodation — Wrong: අකොමඩේශන් · Correct: අකොමඩේෂන්"),
            *[speak("Tap & Speak: say the word clearly.", w, seconds=5) for w in [
                "Destination", "Heritage", "Tradition", "Ceremony", "Procession", "Exploration",
                "Adventure", "Accommodation", "Performance", "Cultural Identity"]],
            heading("Sentence Stress Practice"),
            *[speak(f"Say the sentence. Stress the words in capitals: {s}", t, seconds=10) for s, t in [
                ("We were EXPLORING the city when we FOUND a hidden temple.", "We were exploring the city when we found a hidden temple."),
                ("The dancers were PERFORMING while the musicians were PLAYING.", "The dancers were performing while the musicians were playing."),
                ("The procession was MOVING through the streets when the rain STARTED.", "The procession was moving through the streets when the rain started."),
            ]],
        ],
        "listening": [
            plain("LISTENING TIP\nWhen listening to travel stories and cultural descriptions:\n✔ Listen for where "
                  "events happened.\n✔ Listen for what was happening.\n✔ Listen for unexpected events.\n"
                  "✔ Listen for sequence words: first • then • later • while • as • suddenly • eventually\n"
                  "These words help you follow the story."),
            heading("Listening Text 1 – Exploring Ancient Polonnaruwa"),
            *[mcq(f"Activity 9 – {q}", o, a, listen=TEXT1) for q, o, a in [
                ("Where did the family travel?", ["Polonnaruwa", "Sigiriya", "Anuradhapura"], "Polonnaruwa"),
                ("Why did they plan their itinerary carefully?", ["They wanted to visit many historical sites", "They wanted to go shopping", "They wanted to visit relatives"], "They wanted to visit many historical sites"),
                ("What was the weather like?", ["Warm and sunny", "Rainy", "Windy"], "Warm and sunny"),
                ("Who explained the history of the city?", ["A guide", "A teacher", "A tourist"], "A guide"),
                ("What were tourists doing while the guide was speaking?", ["Taking photographs", "Eating lunch", "Buying souvenirs"], "Taking photographs"),
                ("Which famous site did they visit?", ["Gal Vihara", "Nine Arches Bridge", "Galle Fort"], "Gal Vihara"),
                ("How did they travel around some archaeological sites?", ["By bicycle", "By train", "By boat"], "By bicycle"),
                ("What did they learn about?", ["Ancient irrigation systems", "Modern farming", "Wildlife"], "Ancient irrigation systems"),
                ("How did the speaker describe the trip?", ["Educational and enjoyable", "Tiring and boring", "Short and disappointing"], "Educational and enjoyable"),
                ("What was the main purpose of the trip?", ["To learn about Sri Lankan heritage", "To attend a festival", "To go hiking"], "To learn about Sri Lankan heritage"),
            ]],
            *[tf(f"Activity 10 – {s}", a, listen=TEXT1) for s, a in [
                ("The family travelled to Polonnaruwa.", True), ("They travelled during the school holidays.", True),
                ("The weather was rainy.", False), ("A guide explained the history of the ancient city.", True),
                ("They visited Gal Vihara.", True), ("They learned about ancient irrigation systems.", True),
                ("They travelled around the sites by train.", False), ("The trip helped them understand Sri Lankan heritage.", True),
            ]],
            order("Activity 11 – Timeline Reconstruction. Arrange the events in order.", [
                "Travelled to Polonnaruwa", "Explored the Royal Palace", "Visited Gal Vihara",
                "Cycled around archaeological sites", "Learned about ancient irrigation systems",
            ]) | {"listen": TEXT1},
            write("Activity 12 – Heritage Explorer. Answer the questions.", [
                "Why is Polonnaruwa considered an important historical city?", "What did the guide help visitors understand?",
                "Why do you think Gal Vihara is famous?", "What can modern people learn from ancient irrigation systems?",
                "Which part of the trip sounds most interesting to you? Why?", "Why is it important to preserve historical sites?",
            ], min_words=5, listen=TEXT1),
            heading("Listening Text 2 – The Kandy Esala Perahera"),
            *[mcq(f"Activity 13 – {q}", o, a, listen=TEXT2) for q, o, a in [
                ("Which festival is described?", ["Esala Perahera", "Vesak", "Thai Pongal"], "Esala Perahera"),
                ("Where is the festival held?", ["Kandy", "Galle", "Jaffna"], "Kandy"),
                ("What were the drummers doing?", ["Performing rhythms", "Teaching visitors", "Singing songs"], "Performing rhythms"),
                ("What were the elephants doing?", ["Moving through the procession", "Resting", "Running"], "Moving through the procession"),
                ("What were visitors doing?", ["Taking photographs", "Leaving early", "Buying food"], "Taking photographs"),
                ("Who explained the history of the festival?", ["A guide", "A teacher", "A performer"], "A guide"),
                ("What did the family learn about?", ["Sri Lankan heritage", "Modern technology", "Business"], "Sri Lankan heritage"),
                ("How long has the festival existed?", ["For centuries", "For ten years", "For one generation"], "For centuries"),
                ("How did the family feel at the end?", ["Proud", "Bored", "Confused"], "Proud"),
                ("What does the festival represent?", ["Cultural identity", "Sports", "Politics"], "Cultural identity"),
            ]],
            typed("Activity 14 – Festival Fact Finder. Festival:", ["Esala Perahera", "the Esala Perahera", "Kandy Esala Perahera", "the Kandy Esala Perahera"], listen=TEXT2, review=True),
            typed("Activity 14 – Festival Fact Finder. Location:", ["Kandy"], listen=TEXT2, review=True),
            write("Activity 14 – Festival Fact Finder. Complete the information.", [
                "Main Attractions:", "Historical Importance:", "Feelings of Visitors:",
            ], min_words=2, listen=TEXT2, models=[
                "Traditional drummers, decorated elephants and dancers in the procession.",
                "It has been celebrated for centuries and is an important symbol of cultural identity.",
                "They felt proud of their traditions and grateful for the opportunity.",
            ], review=True),
            *[typed(f"Activity 15 – Complete with the Past Continuous: {s}", a, listen=TEXT2, review=True) for s, a in [
                ("As the family __________ through the streets, they heard the drums.", ["was walking", "were walking"]),
                ("The elephants __________ through the procession while dancers performed.", ["were moving"]),
                ("Many visitors __________ photographs as the parade passed.", ["were taking"]),
                ("The guide __________ the history while people listened.", ["was explaining"]),
                ("The crowd __________ together during the celebration.", ["was celebrating", "were celebrating"]),
            ]],
            write("Activity 16 – Cultural Detective. Compare the Esala Perahera with another Sri Lankan festival.", [
                "Purpose:", "Activities:", "Traditional Clothing:", "Music:", "Community Participation:", "Historical Significance:",
            ], min_words=3, listen=TEXT2),
            cat("Activity 17 – Fact, Opinion or Cultural Value? Label each statement.", {
                "Fact": ["The Esala Perahera is held in Kandy.", "The festival has existed for centuries.",
                         "Many visitors attend the festival every year.", "The procession includes decorated elephants."],
                "Opinion": ["It is the most spectacular festival in Sri Lanka.", "Everyone should experience the Perahera at least once."],
                "Cultural Value": ["Cultural traditions should be preserved.", "Festivals strengthen community identity."],
            }, review=True) | {"listen": TEXT2},
        ],
        "reading": [
            plain("READING TIP\nGood readers do more than find answers. They also:\n✔ Identify the writer's purpose.\n"
                  "✔ Understand feelings and opinions.\n✔ Notice cultural information.\n✔ Connect ideas across a text.\n"
                  "✔ Compare information with their own experiences."),
            passage("Reading Passage 1 – A Journey I Will Never Forget", PASSAGE1,
                    "කතුවරයා ජාෆ්නාවට සංචාරය කළා.\nඔහු සංස්කෘතිය, ආහාර සහ සම්ප්‍රදායන් ගැන ඉගෙන ගත්තා.\n"
                    "ප්‍රදේශයේ ජනතාව සමඟ කතා කිරීමෙන් ඔහුට ගැඹුරු සංස්කෘතික අවබෝධයක් ලැබුණා."),
            *[mcq(f"Activity 18 – {q}", o, a, review=True) for q, o, a in [
                ("When did the journey take place?", ["Two years ago, in the December holidays", "Last July", "Last month"], "Two years ago, in the December holidays"),
                ("Which province did the writer visit?", ["The Northern Province", "The Southern Province", "The Central Province"], "The Northern Province"),
                ("Which temple is mentioned in the passage?", ["The Nallur Kandaswamy Temple", "The Temple of the Tooth", "Gal Vihara"], "The Nallur Kandaswamy Temple"),
                ("What was happening at the temple?", ["A religious ceremony", "A cricket match", "A music concert"], "A religious ceremony"),
                ("What did the guide explain?", ["The history of the temple and its importance", "How to cook Jaffna food", "The route to Colombo"], "The history of the temple and its importance"),
                ("How did the writer feel about the food?", ["Unfamiliar at first, then unique and delicious", "Too spicy to eat", "Exactly like home"], "Unfamiliar at first, then unique and delicious"),
                ("Who shared stories about local traditions?", ["Local residents", "Other tourists", "The writer's teacher"], "Local residents"),
                ("What helped the writer understand the culture better?", ["Talking with local people", "Reading websites", "Watching television"], "Talking with local people"),
                ("What lesson did the writer learn from travelling?", ["Travel is about understanding people and ways of life", "Travel is only about famous places", "Travel is too expensive"], "Travel is about understanding people and ways of life"),
                ("What is the main message of the passage?", ["Travelling helps us understand other cultures", "Jaffna is far from Colombo", "Temples are crowded"], "Travelling helps us understand other cultures"),
            ]],
            write("Activity 19 – Travel Detective. Find evidence from the passage.", [
                "How do we know the writer was interested in culture?", "Which sentence shows that the writer changed his opinion?",
                "What evidence shows that local people were welcoming?", "Which activities helped the writer learn about history?",
                "Why was this trip different from previous journeys?",
            ], min_words=5, models=[
                "He visited a temple, watched a ceremony and spoke with local residents about traditions.",
                "\"At first, some of the food seemed unfamiliar, but I soon discovered that the flavours were unique and delicious.\"",
                "Local residents shared stories about the region's history and traditions with them.",
                "Visiting the Jaffna Fort and the temple, listening to the guide and talking with local residents.",
                "He noticed the landscape, language and culture change, and he learned about people, not only places.",
            ], review=True),
            write(f"Activity 20 – Travel Reflection. {DISCUSS}", [
                "Would you like to visit Jaffna? Why?", "What can travellers learn from local communities?",
                "Is food an important part of culture?", "How can travel reduce misunderstandings between people?",
                "What region of Sri Lanka would you like to explore next?",
            ], min_words=5),
            passage("Reading Passage 2 – Why Festivals Matter", PASSAGE2,
                    "උත්සව සංස්කෘතිය ආරක්ෂා කිරීමට උපකාරී වේ.\nඒවා ප්‍රජාවන් එකට එක් කරයි.\n"
                    "නමුත් සමහරුන් විශ්වාස කරන්නේ නවීන උත්සව වාණිජකරණය වී ඇති බවයි."),
            cat("Activity 21 – Fact, Opinion & Argument. Label each statement.", {
                "Fact": ["Festivals bring communities together.", "Some festivals attract tourists.",
                         "Hotels often benefit from tourism.", "Festivals help preserve culture."],
                "Opinion": ["Festivals are the most important cultural events.", "Traditional values should always remain unchanged."],
                "Argument": ["Modern celebrations are becoming too commercial.", "Change is natural and necessary."],
            }, review=True),
            write("Activity 22 – Compare the Perspectives. Viewpoint A: Festivals should remain traditional. "
                  "Viewpoint B: Festivals should evolve with modern society.", [
                "Advantages of Viewpoint A:", "Advantages of Viewpoint B:", "Your Opinion:",
            ], min_words=5),
            write("Activity 23 – Cultural Comparison. Compare two festivals you know.", [
                "Purpose:", "Traditions:", "Clothing:", "Food:", "Activities:", "Importance:",
            ], min_words=3),
        ],
        "speaking": [
            heading("A. Festival Ambassador Challenge"),
            plain("Imagine that a group of international tourists is visiting Sri Lanka. Recommend one festival, one "
                  "historical site and one traditional food. Explain why they should visit, what they will learn, "
                  "and what makes it special."),
            speak("Record your recommendation. Model:",
                  "I recommend the Kandy Esala Perahera, Sigiriya and kiribath. You should see the Perahera because the decorated elephants, drummers and dancers show our culture. At Sigiriya you will learn about an ancient king and his rock fortress. Kiribath is special because we eat it to celebrate new beginnings, such as the New Year.",
                  seconds=60, review=True),
            heading("B. Cultural Comparison Discussion"),
            plain("Answer these questions on your own. The app plays each question — listen, then record your "
                  "answer in full sentences."),
            *[speak(f"Answer out loud: {q}", m, seconds=45, review=True) for q, m in [
                ("Which cultural tradition in Sri Lanka should be preserved most carefully?", "I think the Sinhala and Tamil New Year traditions should be preserved most carefully, because they bring families together."),
                ("Are traditions changing today?", "Yes, traditions are changing today. For example, many people now send greetings online instead of visiting relatives."),
                ("Is cultural change always positive?", "No, cultural change is not always positive. Some changes are useful, but we can lose important values."),
                ("How can young people protect heritage?", "Young people can protect heritage by learning traditional arts, visiting historical sites and sharing them with others."),
                ("What can tourists learn from local communities?", "Tourists can learn about local food, customs and the history of the people who live there."),
            ]],
            write("Complete the comparison table. Compare a Sri Lankan tradition with a tradition from another culture you know.", [
                "Festival or celebration — Sri Lankan tradition / another culture's tradition:",
                "Food — Sri Lankan tradition / another culture's tradition:",
                "Clothing — Sri Lankan tradition / another culture's tradition:",
                "Music or dance — Sri Lankan tradition / another culture's tradition:",
                "A value it teaches — Sri Lankan tradition / another culture's tradition:",
                "Describe the similarities and differences in 4–5 sentences.",
            ], min_words=3),
            phrases("Listen to a model speaker, then compare it with your own answer.", [(MODEL_SPEAKER, None)]),
            write("Reflect on another culture. In your journal, write 2–3 sentences: Which tradition from another "
                  "culture do you admire, and why? (ඔබ අගය කරන වෙනත් සංස්කෘතියක සම්ප්‍රදායක් ගැන ලියන්න.)",
                  ["My journal:"], min_words=20),
            heading("C. Travel Story Challenge"),
            speak("Speak for 2–3 minutes. Topic: “A Journey That Changed My Perspective”. Include: destination, "
                  "people, cultural experience, unexpected event, what you learned, how you felt. Model:",
                  "Last year, I travelled to Jaffna with my family. While we were exploring the Nallur temple, a ceremony was taking place, and a local family invited us to watch. Suddenly it started raining, so we waited with them and talked about their traditions. I learned that people in different regions have different customs, but they are just as welcoming. I felt surprised and happy, and the journey changed the way I think about my country.",
                  seconds=150, review=True),
        ],
        "writing": [
            write("Activity 24 – Travel Blog Entry. Write 180–200 words.", [
                "Topic: “A Journey I Will Never Forget”. Include: destination, activities, cultural experiences, "
                "narrative tenses, personal reflection.",
            ], min_words=180),
            write("Activity 25 – Cultural Article. Write 180–200 words.", [
                "Topic: “A Festival That Represents My Culture”. Include: history, activities, traditions, "
                "importance, personal opinion.",
            ], min_words=180),
            write("Activity 26 – Opinion Writing. Write 180–200 words.", [
                "Topic: “Should Traditional Festivals Change with Modern Society?”. Include: your opinion, two "
                "supporting reasons, one counterargument, a conclusion.",
            ], min_words=180),
            self_check(
                "□ I can describe travel experiences using narrative tenses.\n□ I can talk about cultural traditions and festivals.\n"
                "□ I can sequence events clearly.\n□ I can compare cultural practices.\n□ I can understand travel narratives.\n"
                "□ I can identify facts, opinions, and arguments.\n□ I can express and justify my opinions.\n"
                "□ I can write a travel blog.\n□ I can write about culture and traditions.\n"
                "□ I can speak confidently about travel and cultural experiences.",
                prompt="Self-assessment",
            ),
            summary(["Narrative tenses: Past Simple + Past Continuous", "Travel and culture vocabulary",
                     "Describing festivals and traditions", "Comparing cultures"]),
        ],
    },
}
