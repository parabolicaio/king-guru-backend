"""Level 3 Lesson 9 — Architecture, Cities & Global Living.

Source: LEVEL_3_L9_individual.docx. Follow-up Part C9/C10 (solo versions and
the C10 model answers) applied. Activity 2's recommended ranking was
written by the King Guru team (follow-up A17). review=True marks
keys/models by the King Guru team.
"""
from .dsl import (DISCUSS, cat, examples, heading, interview, match, mcq, order, passage, phrases,
                  plain, self_check, speak, summary, tf, typed, words, write)

TEXT1 = (
    "Welcome to today's city walking tour of Colombo. Our tour begins at Independence Square, one of the "
    "city's most important historical landmarks. Many visitors come here to enjoy the peaceful surroundings and "
    "learn about Sri Lanka's independence. Next, we'll visit the National Museum, where you can explore "
    "fascinating collections of art, history and archaeology. After that, we'll walk through Viharamahadevi "
    "Park, the largest public park in Colombo. It's a popular place for families, joggers and tourists who want "
    "to relax. Finally, we'll end our tour at Galle Face Green, where people gather to enjoy the sea breeze, "
    "street food and beautiful sunset. Whether you're interested in history, culture or nature, Colombo has "
    "something for everyone."
)
TEXT2 = (
    "The Green City Council is planning a new community park. During a public meeting, residents shared their "
    "ideas. Some people suggested building a children's playground because families need more safe places for "
    "recreation. Others wanted walking paths and bicycle lanes so that people could exercise safely. Several "
    "residents recommended planting more trees and flowers to improve the environment. Some people also "
    "requested benches, drinking water facilities and better lighting for evening visitors. At the end of the "
    "meeting, everyone agreed that the park should be clean, safe and accessible for people of all ages."
)
KANDY_GUIDE = (
    "Kandy is one of Sri Lanka's most famous cities. It is well known for its beautiful scenery, cultural "
    "heritage and historical landmarks. Visitors often begin their journey at the Temple of the Sacred Tooth "
    "Relic before walking around Kandy Lake. The Royal Botanical Gardens in Peradeniya attract thousands of "
    "visitors every year with their colourful flowers and peaceful environment. Kandy also offers local "
    "markets, museums and traditional cultural performances, making it an excellent destination for both "
    "local and international tourists."
)
PASSAGE1 = (
    "Every city has its own identity, but the best cities have something in common. They provide safe public "
    "spaces, reliable transport, clean environments and opportunities for people to work, learn and relax.\n\n"
    "Modern cities are designed to meet the needs of different groups of people. Families need parks and "
    "playgrounds, students need libraries and schools, while visitors often look for museums, historical "
    "landmarks and cultural experiences.\n\nA successful city also protects its natural environment. Green "
    "spaces improve air quality, reduce noise and provide places where people can exercise or spend time with "
    "family and friends.\n\nGood urban planning is not only about constructing new buildings. It is also about "
    "creating communities where people feel safe, connected and proud of where they live."
)
PASSAGE2 = (
    "Located in the dry zone of Anuradhapura District, Ritigala is one of Sri Lanka's most fascinating yet "
    "lesser-known archaeological sites. Unlike many popular tourist attractions, Ritigala offers visitors a "
    "peaceful environment where history, architecture and nature exist together in perfect harmony.\n\nThe "
    "site is believed to have been an ancient Buddhist monastery that dates back more than two thousand years. "
    "Hidden within a dense forest reserve, the ruins include stone pathways, meditation platforms, reservoirs "
    "and beautifully constructed bridges that demonstrate the remarkable engineering skills of ancient Sri "
    "Lankan builders. Although many of the buildings have been damaged over time, visitors can still admire the "
    "careful planning and unique architectural design of the monastery.\n\nRitigala is also surrounded by "
    "legends and local folklore. According to one popular story from the Ramayana, the mountain became home to "
    "rare medicinal plants after a fragment of the Himalayas fell here. While historians continue to study "
    "these stories, the area remains an important place for both archaeological research and biodiversity "
    "conservation.\n\nToday, Ritigala attracts travellers who enjoy history, hiking and eco-tourism rather than "
    "crowded tourist destinations. Visitors are encouraged to respect the peaceful atmosphere, protect the "
    "archaeological remains and preserve the surrounding forest for future generations. For those looking to "
    "experience a quieter side of Sri Lanka's cultural heritage, Ritigala offers a memorable journey through "
    "history and nature."
)

LESSON = {
    "order": 9,
    "title": "Architecture, Cities & Global Living",
    "title_si": "ගෘහ නිර්මාණය, නගර සහ ගෝලීය ජීවිතය",
    "description": "Describe buildings, landmarks and cities, and discuss city planning and tourism (B1).",
    "objectives": [
        "Describe buildings, landmarks and public spaces using appropriate vocabulary",
        "Discuss city planning and modern living environments",
        "Compare cities and public spaces using descriptive language",
        "Express opinions about urban development and tourism",
        "Understand spoken and written texts related to architecture and city life",
        "Take part in discussions about improving communities and cities",
        "Write a descriptive paragraph about a city or famous building",
    ],
    "sections": {
        "vocabulary": [
            words("A. Buildings & Landmarks", [
                ("Landmark", "ප්‍රසිද්ධ ස්ථානය"), ("Monument", "ස්මාරකය"), ("Skyscraper", "උස ගොඩනැගිල්ල"),
                ("Apartment", "මහල් නිවාසය"), ("Bridge", "පාලම"), ("Tower", "කුළුණ"), ("Temple", "පන්සල / දේවාලය"),
                ("Museum", "කෞතුකාගාරය"), ("Stadium", "ක්‍රීඩාංගණය"), ("Library", "පුස්තකාලය"),
                ("Heritage Site", "උරුම ස්ථානය"), ("Architecture", "ගෘහ නිර්මාණ ශිල්පය"),
                ("Structure", "ව්‍යුහය / ගොඩනැගිල්ල"), ("Construction", "ඉදිකිරීම"),
            ]),
            match("Activity 3 – Match each place with its purpose.", [
                ("Hospital", "Receive medical treatment"), ("Museum", "Learn about history"),
                ("Library", "Study and borrow books"), ("Stadium", "Watch or play sports"),
                ("Bridge", "Cross a river"), ("School", "Receive education"),
            ], review=True),
            cat("Activity 4 – Categorize the places.", {
                "Public Buildings": ["Library", "Hospital", "Railway Station", "Airport"],
                "Tourist Attractions": ["Temple", "Museum", "Sports Stadium", "Hotel"],
                "Everyday Places": ["Shopping Mall", "Playground", "Apartment", "Park"],
            }, review=True),
            write("Activity 4 – Think Further.", ["Which place belongs in more than one category? Explain."], min_words=10),
            mcq("Activity 5 – A tourist wants to learn about local culture.", ["Museum", "Office", "Factory", "Supermarket"], "Museum"),
            mcq("Activity 5 – A family wants to enjoy nature and fresh air.", ["Public Park", "Car Park", "Warehouse", "Cinema"], "Public Park"),
            mcq("Activity 5 – Students need a quiet place to prepare for examinations.", ["Library", "Stadium", "Market", "Restaurant"], "Library"),
            mcq("Activity 5 – A visitor wants to stay overnight near a famous landmark.", ["Hotel", "Bus Station", "Museum", "Playground"], "Hotel"),
            mcq("Activity 5 – Engineers are planning to reduce traffic congestion. Which structure should they improve?",
                ["Bridge", "Temple", "Cinema", "Hotel"], "Bridge"),
            write("Activity 5 – Reflection.", ["Which place do you think is most important in every city? Why?"], min_words=10),
            words("B. City Life & Urban Planning", [
                ("Public Transport", "පොදු ප්‍රවාහනය"), ("Pedestrian", "පදිකයා"), ("Traffic Congestion", "රථවාහන තදබදය"),
                ("Green Space", "හරිත ප්‍රදේශය"), ("Residential Area", "නේවාසික ප්‍රදේශය"),
                ("Commercial Area", "ව්‍යාපාරික ප්‍රදේශය"), ("Pedestrian Crossing", "පදික මාරුව"),
                ("Bicycle Lane", "පාපැදි මංතීරුව"), ("Community", "ප්‍රජාව"), ("Infrastructure", "යටිතල පහසුකම්"),
                ("Sustainable", "තිරසාර"), ("Tourism", "සංචාරක කර්මාන්තය"),
            ]),
            mcq("Activity 6 – There is heavy traffic every morning. What would help?",
                ["More bicycle lanes", "Fewer roads", "More traffic lights that never change", "Closing schools"], "More bicycle lanes"),
            mcq("Activity 6 – Families say there are not enough places for children to play. What should the city build?",
                ["More parks", "More factories", "More car parks", "More office buildings"], "More parks"),
            mcq("Activity 6 – Tourists find it difficult to travel around the city. What would help most?",
                ["Better public transport", "Fewer buses", "More traffic", "Closing museums"], "Better public transport"),
            mcq("Activity 6 – The city has very few trees. What is the best solution?",
                ["Create more green spaces", "Build more shopping malls", "Remove parks", "Build more car parks"], "Create more green spaces"),
            mcq("Activity 6 – Older people find it difficult to cross busy roads safely. Which improvement would help?",
                ["More pedestrian crossings", "More billboards", "More shops", "More apartments"], "More pedestrian crossings"),
            write("Activity 6 – Reflection.", [
                "If you were the mayor of your town, what is the first improvement you would make? Why?",
            ], min_words=10),
            plain("City Planning Tip\nA well-designed city should include:\n✔ Safe public transport\n✔ Green spaces\n"
                  "✔ Hospitals and schools\n✔ Tourist attractions\n✔ Public libraries\n✔ Sports and recreation areas\n"
                  "✔ Clean streets\n✔ Accessible public services"),
            speak("Mini Speaking Challenge – A tourist asks: “What is the one place I should definitely visit in your "
                  "city?” Recommend one place for one minute: why it is special, what visitors can do there, the best "
                  "time to visit and one interesting fact. Model:",
                  "You should definitely visit Galle Fort. It is special because it is a UNESCO World Heritage Site with old Dutch buildings. Visitors can walk on the walls, visit museums and eat in small cafés. The best time to visit is in the late afternoon, when you can watch the sunset. One interesting fact is that people still live inside the fort.",
                  seconds=60, review=True),
            words("C. Public Spaces & Tourism", [
                ("Tourist Attraction", "සංචාරක ආකර්ෂණය"), ("Guided Tour", "මාර්ගෝපදේශක සංචාරය"),
                ("Sightseeing", "දර්ශන නැරඹීම"), ("Entrance Fee", "ඇතුල්වීමේ ගාස්තුව"),
                ("Local Market", "ප්‍රාදේශීය වෙළඳපොළ"), ("Souvenir", "සිහිවටන භාණ්ඩය"),
                ("Visitor Centre", "සංචාරක තොරතුරු මධ්‍යස්ථානය"), ("Landmark", "ප්‍රසිද්ධ ස්ථානය"),
                ("Public Square", "මහජන චතුරශ්‍රය"), ("Walking Trail", "ඇවිදින මාර්ගය"),
                ("Guided Map", "මාර්ග සිතියම"), ("Information Board", "තොරතුරු පුවරුව"),
            ]),
            mcq("Activity 7 – You have just arrived in a new city and want information about famous places.",
                ["Visitor Centre", "Stadium", "Apartment", "Library"], "Visitor Centre"),
            mcq("Activity 7 – You want to buy a small gift to remember your holiday.",
                ["Souvenir Shop", "Railway Station", "Hospital", "Office"], "Souvenir Shop"),
            mcq("Activity 7 – You want to learn about the history of an ancient building with the help of an expert.",
                ["Guided Tour", "Shopping Centre", "Car Park", "Sports Complex"], "Guided Tour"),
            mcq("Activity 7 – You would like to explore the city by following a marked path.",
                ["Walking Trail", "Factory", "Airport Runway", "Warehouse"], "Walking Trail"),
            mcq("Activity 7 – You are looking for directions to nearby attractions.",
                ["Information Board", "Playground", "Petrol Station", "Cinema"], "Information Board"),
            *[typed(f"Activity 8 – City Explorer. Identify the place: {s}", a, review=True) for s, a in [
                ("People come here to admire famous buildings and learn about history.", ["landmark", "heritage site", "a landmark", "a heritage site", "museum"]),
                ("Visitors usually buy small gifts for friends and family here.", ["souvenir shop", "a souvenir shop", "local market", "market"]),
                ("It provides maps, brochures and travel advice.", ["visitor centre", "a visitor centre", "visitor center"]),
                ("It is a safe place where people can walk while enjoying nature.", ["walking trail", "a walking trail", "park"]),
                ("It displays useful information about attractions and directions.", ["information board", "an information board"]),
            ]],
            write("Activity 9 – Plan the Best Day Trip. Your friend is visiting your town for one day. Choose four places "
                  "(museum, temple, public park, local market, beach, library, art gallery, shopping centre, botanical "
                  "garden, historical monument).", [
                "My four places:", "Why did you choose these places?", "Which place should your friend visit first?",
                "Which place would you leave until the evening?", "Which place best represents your town?",
            ], min_words=3),
            passage("Activity 10 – Read the City Guide: Welcome to Kandy!", KANDY_GUIDE),
            mcq("Activity 10 – Which attraction do many visitors explore first?",
                ["The Temple of the Sacred Tooth Relic", "Kandy Lake", "The Royal Botanical Gardens"],
                "The Temple of the Sacred Tooth Relic"),
            write("Activity 10 – Answer the questions.", [
                "Why is Kandy famous?", "What can tourists enjoy at Peradeniya?",
                "Name two other attractions mentioned in the passage.", "Would you like to visit Kandy? Explain why.",
            ], min_words=4, models=[
                "It is famous for its beautiful scenery, cultural heritage and historical landmarks.",
                "Colourful flowers and a peaceful environment at the Royal Botanical Gardens.",
                "Kandy Lake, local markets, museums and traditional cultural performances.",
            ], review=True),
            write("Activity 11 – Tourist Advice. Complete the conversation.", [
                "Tourist: I'm visiting Sri Lanka for the first time. Which city should I visit? — You: I recommend ______.",
                "Tourist: Why should I visit there? — You: Because ______.",
                "Tourist: What can I do there? — You: You can ______.",
                "Tourist: What's the best time to visit? — You: I think ______.",
            ], min_words=3),
            write("Quick Reflection – Complete the sentences.", [
                "The most beautiful place I have visited is ______.", "I would like to visit ______ because ______.",
                "One place every tourist should visit in Sri Lanka is ______.", "A well-planned city should always have ______.",
            ], min_words=3),
        ],
        "grammar": [
            heading("Review Corner"),
            plain("From Lesson 8: ✔ Sports & Leisure Vocabulary ✔ Healthy Lifestyle Expressions ✔ Giving Advice "
                  "✔ Mixed Grammar Review ✔ Comparing Lifestyles\nExamples: I usually go jogging before work. · "
                  "Everyone should have enough time to relax. · Playing sports helps people stay healthy."),
            mcq("Activity 1 – A tourist wants to learn about Sri Lankan history.", ["Museum", "Airport", "Bus Stop", "Shopping Centre"], "Museum"),
            mcq("Activity 1 – Children want to play safely after school.", ["Playground", "Car Park", "Railway Station", "Market"], "Playground"),
            mcq("Activity 1 – You want to borrow books and study quietly.", ["Library", "Cinema", "Stadium", "Café"], "Library"),
            mcq("Activity 1 – A family wants to relax on Sunday morning.", ["Public Park", "Highway", "Office Building", "Factory"], "Public Park"),
            mcq("Activity 1 – Visitors want to enjoy beautiful views of the city.", ["Observation Tower", "Warehouse", "Petrol Station", "Hospital"], "Observation Tower"),
            write("Activity 1 – Reflection.", ["Which public place do you visit most often? Why?"], min_words=8),
            write("Activity 2 – Build Your Perfect City. Rank these places on your own from 1 (most important) to 8 "
                  "(least important): Hospital, Public Park, School, Sports Complex, Shopping Centre, Library, "
                  "Museum, Railway Station.", [
                "My ranking:", "Which three places are the most important? Explain your reasons.",
            ], min_words=8),
            order("Activity 2 – Now put the places in the recommended ranking (to be confirmed by our experts), then "
                  "compare it with yours.", [
                "Hospital", "School", "Railway Station", "Public Park", "Shopping Centre", "Library",
                "Sports Complex", "Museum",
            ], review=True),
            write("Activity 2 – Explain why your choices are similar to or different from the recommended ranking.",
                  ["My explanation:"], min_words=15),
            heading("Mixed Review"),
            plain("In this lesson you will review grammar you have already learned while talking about cities, "
                  "landmarks and travel: ✔ Present Perfect vs Past Simple ✔ Used to ✔ Too / Enough ✔ Modals of "
                  "Advice (should / shouldn't) ✔ Future Plans (going to)"),
            examples("Present Perfect — experiences or actions connected to the present",
                     ["I have visited Sigiriya twice.", "We have never travelled by train to Ella."]),
            examples("Past Simple — completed actions at a definite time",
                     ["We visited Galle Fort last December.", "They stayed in Kandy for three days."]),
            examples("Used to — past habits or situations that no longer happen",
                     ["My grandparents used to live in the village.", "This area used to be a forest."]),
            examples("Too / Enough", ["The road is too narrow.", "The park is large enough for families."]),
            examples("Should / Shouldn't — advice", ["Cities should have more green spaces.",
                                                     "Tourists shouldn't leave litter in public places."]),
            examples("Going to — future plans", ["We are going to visit the National Museum tomorrow.",
                                                 "They are going to build a new bridge."]),
            plain("Sinhala Help\nI have visited Anuradhapura many times. → මම අනුරාධපුරයට බොහෝ වාර ගොස් තිබෙනවා.\n"
                  "This road is too busy. → මේ මාර්ගය වැඩියෙන් කාර්යබහුලයි.\n"
                  "The park is big enough for children. → මෙම උද්‍යානය ළමයින්ට ප්‍රමාණවත් තරම් විශාලයි.\n"
                  "People should protect historical places. → මිනිසුන් ඓතිහාසික ස්ථාන ආරක්ෂා කළ යුතුය."),
            *[mcq(f"Activity 12 – {s}", o, a) for s, o, a in [
                ("We __________ the Lotus Tower last weekend.", ["have visited", "visited", "visit"], "visited"),
                ("My family __________ travel by train every holiday when I was a child.", ["used to", "have", "going to"], "used to"),
                ("The museum is __________ crowded today.", ["too", "enough"], "too"),
                ("The city has __________ public parks for children.", ["enough", "too"], "enough"),
                ("We __________ visit Jaffna during the next school vacation.", ["are going to", "visited", "have visited"], "are going to"),
                ("Visitors __________ respect historical monuments.", ["should", "shouldn't never", "too"], "should"),
                ("I __________ to Galle Fort three times.", ["have been", "went yesterday", "am going"], "have been"),
                ("The bridge isn't wide __________ for heavy traffic.", ["enough", "too"], "enough"),
            ]],
            order("Activity 13 – City Timeline. A family is planning a holiday. Arrange the events in the correct order.", [
                "Book the hotel", "Arrive in Kandy", "Explore the city", "Visit the museum", "Buy souvenirs", "Travel home",
            ], review=True),
            write("Activity 13 – Now tell the story using sequence words: First... Next... Then... After that... Finally...",
                  ["My story:"], min_words=25),
            write("Activity 14 – Then and Now. Complete the sentences.", [
                "My hometown used to ______, but now ______.", "This street used to ______, but today ______.",
                "Tourists used to ______, but now ______.", "The city centre used to ______, but today ______.",
                "Public transport used to ______, but now ______.",
                "My favourite holiday destination used to ______, but now ______.",
            ], min_words=5),
            write("Activity 15 – Advice for a Better City. Give one piece of advice for each situation. Use should, "
                  "shouldn't and going to where appropriate.", [
                "Situation 1: There are very few trees in the city.", "Situation 2: Tourists cannot find directions easily.",
                "Situation 3: Traffic congestion is becoming worse every year.",
                "Situation 4: Many historical buildings are not properly maintained.",
                "Situation 5: Children have very few places to play.",
            ], min_words=6),
            plain("Activity 16 – Complete the Conversation. Use the words in the box: have visited • should • too • "
                  "enough • going to\nMaya: Have you ever __________ Sigiriya?\nKasun: Yes, I have. It was amazing!\n"
                  "Maya: We're __________ visit it next month.\nKasun: That's great. You __________ take a camera "
                  "because the views are beautiful.\nMaya: Is it difficult to climb?\nKasun: Some parts are "
                  "__________ steep, but most people can manage the climb.\nMaya: Is one day __________ to explore "
                  "everything?\nKasun: Yes, if you start early."),
            *[typed(f"Activity 16 – {s}", [a], review=True) for s, a in [
                ("Maya: Have you ever __________ Sigiriya?", "visited"),
                ("Maya: We're __________ visit it next month.", "going to"),
                ("Kasun: You __________ take a camera because the views are beautiful.", "should"),
                ("Kasun: Some parts are __________ steep, but most people can manage the climb.", "too"),
                ("Maya: Is one day __________ to explore everything?", "enough"),
            ]],
            *[typed(f"Activity 17 – Spot the Mistake. Rewrite correctly: {s}", a, review=True) for s, a in [
                ("We have visited Kandy yesterday.", ["We visited Kandy yesterday."]),
                ("This bridge is enough strong.", ["This bridge is strong enough."]),
                ("They used to travelled by train.", ["They used to travel by train."]),
                ("People should to protect heritage sites.", ["People should protect heritage sites."]),
                ("We are going visit Colombo tomorrow.", ["We are going to visit Colombo tomorrow."]),
                ("The museum is too small enough.", ["The museum is too small.", "The museum is small enough."]),
            ]],
            write("Quick Reflection – Complete the sentences.", [
                "A city I would like to visit is ______ because ______.", "One thing my town should improve is ______.",
                "I think tourists should always ______.", "One famous building I have visited is ______.",
            ], min_words=3),
            heading("Mixed Review in Context"),
            examples("When talking about cities and travel, we often use different grammar structures together.", [
                "I have visited Kandy twice.", "We visited Anuradhapura last year.", "People should protect historical buildings.",
                "The park is big enough for families.", "The road is too narrow for buses.",
            ]),
            plain("Sinhala Help\nThe museum is big enough for school groups. → මෙම කෞතුකාගාරය පාසල් කණ්ඩායම් සඳහා ප්‍රමාණවත් තරම් විශාලයි.\n"
                  "People should protect historical buildings. → මිනිසුන් ඓතිහාසික ගොඩනැගිලි ආරක්ෂා කළ යුතුය."),
            *[mcq(f"Activity 25 – {s}", o, a) for s, o, a in [
                ("I __________ Sigiriya three times.", ["visited", "have visited", "am visit"], "have visited"),
                ("The streets are __________ crowded during the festival.", ["too", "enough"], "too"),
                ("We __________ visit Jaffna next month.", ["are going to", "visited", "have"], "are going to"),
                ("This park is large __________ for community events.", ["enough", "too"], "enough"),
                ("Visitors __________ respect local customs.", ["should", "shouldn't never", "are"], "should"),
                ("My grandparents __________ live in this neighbourhood.", ["used to", "have", "going to"], "used to"),
            ]],
            plain("Activity 26 – Complete the Travel Blog. Use the words in the box: have visited • should • enough • "
                  "going to • used to"),
            *[typed(f"Activity 26 – {s}", a, review=True) for s, a in [
                ("Last weekend, I ______ Galle Fort with my cousins.", ["visited", "have visited"]),
                ("The streets were wide ______ for visitors to walk comfortably.", ["enough"]),
                ("Local people told us that the fort ______ be much quieter many years ago.", ["used to"]),
                ("Next year, we are ______ visit Jaffna because we've heard it's beautiful.", ["going to"]),
                ("I think everyone ______ explore Sri Lanka's historical cities at least once.", ["should"]),
            ]],
            write("Activity 27 – What Would You Improve? Write one suggestion for each problem. Use should, going to, "
                  "enough and too.", [
                "Situation 1: The city has very few public parks.", "Situation 2: Tourists cannot understand the road signs.",
                "Situation 3: Traffic congestion is increasing every year.",
                "Situation 4: Many historical buildings are covered with litter.",
                "Situation 5: There are not enough bicycle lanes.",
            ], min_words=6),
            write("Quick Reflection – Complete the sentences.", [
                "The most interesting city I have visited is ______.", "A good city should always have ______.",
                "If I could improve one thing in my town, I would ______.",
            ], min_words=3),
        ],
        "pronunciation": [
            phrases("Listen and Repeat", [
                ("Architecture", "AR-chi-tec-ture · ආකිටෙක්චර්"), ("Landmark", "ලෑන්ඩ්මාර්ක්"),
                ("Monument", "මොන්‍යුමන්ට්"), ("Museum", None), ("Heritage", "HER-i-tage · හෙරිටිජ්"),
                ("Infrastructure", "IN-fra-struc-ture"), ("Pedestrian", "pe-DES-tri-an"),
                ("Boulevard", "BOO-le-vard"), ("Tourism", None), ("Community", None), ("Apartment", None),
                ("Skyscraper", "ස්කයිස්ක්‍රේපර්"), ("Souvenir", "සුවනියර්"), ("Sightseeing", "සයිට්සීඉං"),
            ]),
            *[mcq(f"Activity 18 – Word Stress. Which syllable is stressed in “{w}”?", o, a, review=True) for w, o, a in [
                ("Architecture", ["AR", "chi", "tec", "ture"], "AR"),
                ("Community", ["com", "MU", "ni", "ty"], "MU"),
                ("Pedestrian", ["pe", "DES", "tri", "an"], "DES"),
                ("Infrastructure", ["IN", "fra", "struc", "ture"], "IN"),
                ("Monument", ["MON", "u", "ment"], "MON"),
                ("Apartment", ["a", "PART", "ment"], "PART"),
            ]],
            *[speak("Tap & Speak: say the word clearly.", w, seconds=5) for w in [
                "Architecture", "Landmark", "Monument", "Heritage", "Infrastructure", "Pedestrian", "Skyscraper",
                "Souvenir"]],
            heading("Activity 19 – Functional English"),
            *[speak("Practise the expression: listen, then record it.", e, seconds=8) for e in [
                "Excuse me, how can I get to the museum?", "Is the railway station far from here?",
                "Which bus goes to the city centre?", "This building is famous for its architecture.",
                "The park is popular because it is peaceful.", "I recommend visiting Galle Fort.",
                "You should visit early in the morning.", "Don't forget to bring water.", "It's worth visiting.",
            ]],
        ],
        "listening": [
            plain("LISTENING TIP\nWhen listening to conversations about cities and tourism:\n✔ Listen for landmarks "
                  "and place names.\n✔ Pay attention to directions and locations.\n✔ Identify opinions and "
                  "recommendations.\n✔ Listen for sequence words such as first, next, finally.\n✔ Notice descriptive "
                  "words used for places."),
            heading("Listening Text 1 – A Walking Tour Around Colombo"),
            *[mcq(f"Activity 20 – {q}", o, a, listen=TEXT1) for q, o, a in [
                ("Where does the walking tour begin?", ["National Museum", "Galle Face Green", "Independence Square", "Viharamahadevi Park"], "Independence Square"),
                ("Which place is famous for history and archaeology?", ["Galle Face Green", "National Museum", "Park", "Railway Station"], "National Museum"),
                ("Why do many people visit Viharamahadevi Park?", ["To go shopping", "To relax and exercise", "To watch sports", "To study"], "To relax and exercise"),
                ("Where does the tour end?", ["Lotus Tower", "Galle Face Green", "Dutch Hospital", "Library"], "Galle Face Green"),
                ("Which sentence best describes Colombo?", ["It only has historical places.", "It offers something for different interests.", "It is only suitable for tourists.", "It has very few parks."], "It offers something for different interests."),
            ]],
            order("Activity 21 – Route Builder. Listen again and put the places in the correct order.", [
                "Independence Square", "National Museum", "Viharamahadevi Park", "Galle Face Green",
            ]) | {"listen": TEXT1},
            write("Activity 22 – Tourist Notes. Listen again. Why visit each place?", [
                "Independence Square:", "National Museum:", "Viharamahadevi Park:", "Galle Face Green:",
            ], min_words=3, listen=TEXT1, models=[
                "To enjoy the peaceful surroundings and learn about Sri Lanka's independence.",
                "To explore collections of art, history and archaeology.",
                "To relax; it is the largest public park in Colombo and popular with families and joggers.",
                "To enjoy the sea breeze, street food and the beautiful sunset.",
            ], review=True),
            heading("Listening Text 2 – Planning a New Community Park"),
            *[tf(f"Activity 23 – {s}", a, listen=TEXT2, review=True) for s, a in [
                ("The meeting was about building a shopping mall.", False), ("Families wanted a children's playground.", True),
                ("Residents suggested adding bicycle lanes.", True), ("Everyone wanted to remove the trees.", False),
                ("Better lighting was one recommendation.", True), ("The park should be accessible to everyone.", True),
            ]],
            match("Activity 24 – Community Planner. Match each suggestion with its purpose.", [
                ("Children's Playground", "Help children play safely"), ("Bicycle Lane", "Encourage cycling"),
                ("Trees and Flowers", "Make the park greener"), ("Benches", "Provide places to rest"),
                ("Street Lights", "Improve safety at night"),
            ], review=True) | {"listen": TEXT2},
        ],
        "reading": [
            plain("READING TIP\nWhen reading about cities and architecture:\n✔ Identify the writer's purpose.\n"
                  "✔ Notice descriptive words and opinions.\n✔ Compare places using evidence from the text.\n"
                  "✔ Think about how places meet people's needs."),
            passage("Reading Passage 1 – What Makes a Great City?", PASSAGE1,
                    "හොඳ නගරයක් යනු ගොඩනැගිලි පමණක් නොව, මිනිසුන්ට ආරක්ෂිතව ජීවත් වීමට, වැඩ කිරීමට සහ විවේක ගැනීමට "
                    "සුදුසු පරිසරයක් සපයන නගරයකි."),
            mcq("Activity 28 – According to the passage, a successful city should...",
                ["only have modern buildings.", "meet the needs of different people.", "attract tourists only.", "have many shopping centres."],
                "meet the needs of different people."),
            mcq("Activity 28 – Why are green spaces important?",
                ["They reduce traffic.", "They improve the environment.", "They create more buildings.", "They increase pollution."],
                "They improve the environment."),
            mcq("Activity 28 – Which group is mentioned as needing libraries?", ["Tourists", "Families", "Students", "Athletes"], "Students"),
            mcq("Activity 28 – What is the writer's main message?",
                ["Cities should continue building taller buildings.", "Good cities balance development with people's needs.",
                 "Tourism is the most important part of city life.", "Parks are more important than schools."],
                "Good cities balance development with people's needs."),
            write("Activity 29 – Find the Evidence. Find one sentence or phrase that supports each idea.", [
                "Cities should include green spaces.", "Public places are important for families.",
                "Urban planning is about more than buildings.", "Different people have different needs.",
            ], min_words=4, models=[
                "\"A successful city also protects its natural environment.\"",
                "\"Families need parks and playgrounds.\"",
                "\"Good urban planning is not only about constructing new buildings.\"",
                "\"Modern cities are designed to meet the needs of different groups of people.\"",
            ], review=True),
            cat("Activity 30 – Compare & Categorize. Place each feature in the correct category.", {
                "Positive Features": ["Museums", "Playgrounds", "Libraries", "Public Parks", "Pedestrian Crossings",
                                      "Green Spaces", "Historical Landmarks", "Cycling Lanes"],
                "Problems Cities Face": ["Traffic Congestion", "Air Pollution"],
            }, review=True),
            write("Activity 30 – Now answer.", [
                "Which problem affects your town the most?", "Which positive feature do you appreciate most?",
            ], min_words=5),
            passage("Reading Passage 2 – Discover Ritigala: Sri Lanka's Hidden Forest Monastery", PASSAGE2,
                    "රිටිගල යනු අනුරාධපුර දිස්ත්‍රික්කයේ පිහිටි අද්විතීය පුරාවිද්‍යාත්මක හා ස්වභාවික උරුමයකි. එහි පැරණි "
                    "ආරාම නටබුන්, වනාන්තර පරිසරය සහ ජනප්‍රවාද එකට එක්ව සංචාරකයන්ට සුවිශේෂී අත්දැකීමක් ලබා දෙයි."),
            *[mcq(f"Activity 31 Part A – {q}", o, a, review=True) for q, o, a in [
                ("Where is Ritigala located?", ["In the dry zone of Anuradhapura District", "Near Colombo", "In the hill country near Kandy"], "In the dry zone of Anuradhapura District"),
                ("Why is Ritigala different from many other tourist destinations in Sri Lanka?", ["It is peaceful and lesser-known", "It is very crowded", "It is a modern city"], "It is peaceful and lesser-known"),
                ("What architectural features can visitors still see today?", ["Stone pathways, meditation platforms, reservoirs and bridges", "Skyscrapers and shopping malls", "Only one small temple"], "Stone pathways, meditation platforms, reservoirs and bridges"),
                ("What does the passage say about the engineering skills of ancient Sri Lankans?", ["They were remarkable", "They were very poor", "They are unknown"], "They were remarkable"),
                ("Which legend is associated with Ritigala?", ["A piece of the Himalayas fell there, bringing medicinal plants", "A king built it in one night", "It was built by giants"], "A piece of the Himalayas fell there, bringing medicinal plants"),
                ("Why is Ritigala important for biodiversity conservation?", ["It is a forest reserve with rare plants", "It has a zoo", "It has no plants"], "It is a forest reserve with rare plants"),
                ("What type of travellers are most likely to enjoy visiting Ritigala?", ["People who enjoy history, hiking and eco-tourism", "People who want nightlife", "People who want to shop"], "People who enjoy history, hiking and eco-tourism"),
                ("Why are visitors encouraged to protect the site?", ["To preserve it for future generations", "To make it more crowded", "To build a hotel there"], "To preserve it for future generations"),
            ]],
            *[typed(f"Activity 31 Part B – Scan and Find. Find the word or phrase in the passage for: {m}", a, review=True) for m, a in [
                ("Very old remains of buildings", ["ruins", "the ruins", "archaeological remains"]),
                ("A place where monks live", ["monastery", "a monastery", "buddhist monastery"]),
                ("Plants used for healing", ["medicinal plants", "rare medicinal plants"]),
                ("Rich variety of living organisms", ["biodiversity"]),
                ("Travelling in ways that protect nature", ["eco-tourism", "ecotourism"]),
            ]],
            write("Activity 31 Part C – Think Critically. Answer the following questions. You can record your answers or "
                  "write them in full sentences.", [
                "Why do you think some historical places receive fewer visitors than famous tourist attractions?",
                "Should countries promote lesser-known heritage sites as tourist destinations? Why or why not?",
                "How can tourists help protect archaeological sites and natural environments?",
                "Would you like to visit Ritigala? Explain your answer using at least three reasons.",
            ], min_words=10),
            write("Activity 31 Part D – Complete the Visitor Information Card.", [
                "Place:", "Province:", "Main Attraction:", "Best For:", "Interesting Fact:", "Advice for Visitors:",
            ], min_words=1, models=[
                "Ritigala", "North Central Province (Anuradhapura District)",
                "The ruins of an ancient forest monastery", "History, hiking and eco-tourism",
                "A legend says a piece of the Himalayas fell here, bringing medicinal plants.",
                "Respect the peaceful atmosphere and protect the ruins and the forest.",
            ], review=True),
        ],
        "speaking": [
            heading("Activity 32 – Guided Interview"),
            *interview(
                "The app plays each question as audio. Listen and record your answer in full sentences. After "
                "recording, compare yours with the model answer.",
                [
                    ("Which city in Sri Lanka have you enjoyed visiting the most?", "I have enjoyed visiting Galle the most because of the old fort, the beach and the colonial buildings."),
                    ("Which famous building would you recommend to a tourist?", "I would recommend the Temple of the Tooth in Kandy because it is an important religious and historical building."),
                    ("What public place do you visit most often?", "The public place I visit most often is the library, because I can study there in a quiet place."),
                    ("What improvements would you like to see in your town?", "I would like to see more green spaces, cleaner roads and better public transport in my town."),
                    ("Do you prefer living in a city or a village? Why?", "I prefer living in a village because it is quieter and less polluted, although cities have more facilities."),
                ],
            ),
            heading("Activity 33 – Compare Two Cities"),
            speak("Choose two cities you know (for example Colombo & Kandy, Galle & Jaffna, or your hometown & Colombo). "
                  "Compare their size, transport, tourist attractions, public spaces, environment and lifestyle, using "
                  "comparative language. Model:",
                  "Colombo is bigger and busier than Kandy. Colombo has more buses and trains, but the traffic is worse. Kandy has more natural beauty, with the lake and the hills, and the air is cleaner. Colombo has more shopping centres, while Kandy has more cultural attractions. Life in Kandy is slower and more relaxed than in Colombo.",
                  seconds=90, review=True),
            heading("Activity 34 – Council Debate"),
            speak("Choose ONE topic: A – Every city should have more green spaces. B – Historical buildings should always "
                  "be protected. C – Public transport should be improved before building more roads. State your "
                  "opinion with two reasons and one example. Use: In my opinion... · I believe... · One advantage is... "
                  "· For example... Model:",
                  "In my opinion, public transport should be improved before building more roads. One advantage is that fewer people will drive, so there will be less traffic. I also believe it is better for the environment. For example, the new buses in Colombo help many workers reach their offices quickly.",
                  seconds=60, review=True),
            heading("Activity 35 – Fluency Challenge"),
            speak("Speak for one minute without stopping. Choose ONE topic: My Favourite City · A Place Every Tourist "
                  "Should Visit · My Dream Neighbourhood · A Famous Building I Admire. Model:",
                  "My favourite city is Galle. I have visited it many times with my family. The old fort is beautiful, and you can walk on the walls and watch the sea. There are small cafés, museums and shops. I think every tourist should visit Galle at least once.",
                  seconds=60, review=True),
        ],
        "writing": [
            write("Activity 36 – Guided Writing: My Ideal City. Write a paragraph (150–180 words) about public "
                  "buildings, transport, green spaces, tourist attractions, community facilities and why you would "
                  "enjoy living there. Use First, In addition, Furthermore, However, Finally.", ["My paragraph:"], min_words=150),
            write("Activity 37 – Famous Building Description. Choose a famous building or landmark (for example "
                  "Sigiriya, Lotus Tower, Temple of the Sacred Tooth Relic, Galle Fort, Nine Arches Bridge) and describe "
                  "where it is, its history, its appearance, why it is famous and why people should visit it.",
                  ["My description:"], min_words=100),
            write("Activity 38 – Create a Tourist Brochure for your town or city.", [
                "A title:", "Three attractions:", "Things to do:", "Local food to try:", "Best time to visit:",
                "A short welcome message:",
            ], min_words=3),
            write("DREAM CITY CHALLENGE – Final Mission: Become an Urban Planner. Your town has received funding to "
                  "build a new community. Create a proposal.", [
                "Step 1 – Choose at least six facilities (for example school, hospital, public library, sports centre, museum, park, bus station, shopping area).",
                "Step 2 – Explain why each facility is important.",
                "Step 3 – Describe how your city will be safe, clean, environmentally friendly and tourist-friendly.",
                "Step 4 – Write a 2-minute speech introducing your city to international visitors.",
                "Reflection: “A great city is one where...” Support your answer with three ideas from today's lesson.",
            ], min_words=10),
            self_check(
                "□ I can describe buildings and landmarks confidently.\n□ I can discuss city planning and public spaces.\n"
                "□ I can compare different cities.\n□ I can express opinions about tourism.\n"
                "□ I can understand texts about architecture and city life.\n□ I can recommend places to visit.\n"
                "□ I can write about cities and famous buildings.\n□ I can discuss how communities can be improved.",
                prompt="Self-assessment — tick the statements that are true for you.",
            ),
            summary(["Buildings, landmarks and city vocabulary", "Mixed review: Present Perfect, Past Simple, used to, "
                     "too / enough, should, going to", "City planning and tourism", "Describing a city or building"]),
        ],
    },
}
