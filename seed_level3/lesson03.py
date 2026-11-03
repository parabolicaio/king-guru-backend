"""Level 3 Lesson 3 — Environment, Science & the Future.

Source: LEVEL_3_L3_individual.docx. review=True marks keys/models by the
King Guru team. "Discuss" instructions use the follow-up Part D rule.
"""
from .dsl import (DISCUSS, cat, examples, heading, match, mcq, passage, phrases, plain, self_check,
                  speak, summary, typed, words, write)

TEXT1 = (
    "Last month, a group of university students visited Wilpattu National Park to take part in an "
    "environmental awareness programme. Before entering the park, wildlife officers explained why forests "
    "are important for protecting biodiversity. While the students were walking through the forest, they "
    "observed many native birds, deer, monkeys and several rare butterflies. The officers also showed them "
    "areas where illegal activities had damaged the environment. Many trees had been cut down, and some "
    "natural habitats had disappeared because of human activities. As the students were discussing these "
    "problems, one of the officers explained how conservation projects had already helped several "
    "endangered species recover. The students realised that protecting forests is not only about saving "
    "animals. Healthy forests also provide clean water, improve air quality and reduce the effects of "
    "climate change. Before leaving, each student planted a tree. They also promised to organise awareness "
    "campaigns in their own communities. The trip inspired them to become more responsible citizens."
)
TEXT2 = (
    "Nimali is a young environmental scientist who works at a research centre in Colombo. Her team has been "
    "studying ways to reduce plastic pollution in rivers. Recently, they developed a biodegradable material "
    "made from seaweed. The material looks like ordinary plastic, but it naturally breaks down after a short "
    "time without harming the environment. While the researchers were testing the new material in the "
    "laboratory, they discovered that it was stronger than they had expected. Several local businesses have "
    "already shown interest in using it instead of traditional plastic packaging. Nimali believes that "
    "scientific innovation can solve many environmental problems if governments, businesses and communities "
    "work together. She also says that education is just as important as new technology. \"If people "
    "continue to throw rubbish into rivers,\" she says, \"even the best inventions will not be enough.\" Her "
    "research team hopes that their discovery will encourage more sustainable lifestyles in the future."
)
PASSAGE1 = (
    "Many people believe that solving environmental problems is the responsibility of governments and large "
    "organisations. However, history has shown that individuals can also make a significant difference.\n\n"
    "Several years ago, a university student named Dilan noticed that large amounts of plastic waste were "
    "collecting near a river close to his hometown. Instead of ignoring the problem, he invited a few friends "
    "to organise a weekend clean-up programme.\n\n"
    "At first, only a small group of volunteers participated. However, as local residents saw the positive "
    "results, more people decided to join. Within a few months, schools, businesses, and community "
    "organisations were supporting the project.\n\n"
    "While the volunteers were cleaning the riverbanks, they also educated local families about recycling "
    "and responsible waste disposal. They explained how plastic pollution affects wildlife, drinking water, "
    "and even human health.\n\n"
    "Today, the project has expanded into several neighbouring towns. Thousands of kilograms of plastic have "
    "been collected, and recycling centres have been established in many communities.\n\n"
    "Dilan believes that meaningful change begins with one simple decision. \"If every person takes "
    "responsibility for one small action,\" he says, \"our environment will become healthier for future "
    "generations.\"\n\n"
    "His story reminds us that ordinary people can create extraordinary change when they work together."
)
PASSAGE2 = (
    "Scientists around the world agree that climate change is one of the greatest challenges facing "
    "humanity. Rising temperatures, changing weather patterns, floods, droughts, and the loss of biodiversity "
    "are already affecting millions of people. Although governments have introduced environmental policies, "
    "experts believe that lasting change requires cooperation from everyone. Technology is helping "
    "researchers develop cleaner sources of energy, smarter transportation systems, and environmentally "
    "friendly products. At the same time, schools are encouraging young people to develop sustainable "
    "habits from an early age. Simple actions such as reducing waste, planting trees, saving electricity, "
    "and protecting wildlife can make a significant difference if millions of people work together. Some "
    "people believe that technology alone will solve environmental problems. Others argue that changing "
    "human behaviour is equally important. In reality, both scientific innovation and responsible lifestyles "
    "are necessary for creating a sustainable future. Every generation has the responsibility to protect "
    "the planet for those who will live here after us."
)

SCIENCE = ["Research", "Discovery", "Innovation", "Technology", "Experiment", "Laboratory",
           "Medical Breakthrough", "Artificial Intelligence"]


def _pick(answer: str) -> list[str]:
    others = [w for w in SCIENCE if w != answer]
    i = SCIENCE.index(answer)
    return [answer, others[i % len(others)], others[(i + 4) % len(others)]]


LESSON = {
    "order": 3,
    "title": "Environment, Science & the Future",
    "title_si": "පරිසරය, විද්‍යාව සහ අනාගතය",
    "description": "Discuss environmental problems and solutions with the First Conditional and relative clauses (B1).",
    "objectives": [
        "Discuss environmental issues and possible solutions",
        "Use the First Conditional to talk about future consequences",
        "Describe scientific and medical developments using defining relative clauses (who, which, that)",
        "Express opinions about environmental responsibility",
        "Understand texts about science, innovation, and sustainability",
        "Take part in discussions about future environmental challenges",
        "Write a short article suggesting solutions to environmental problems",
    ],
    "sections": {
        "vocabulary": [
            words("A. Environment", [
                ("Environment", "පරිසරය"), ("Pollution", "දූෂණය"), ("Climate Change", "දේශගුණික වෙනස්වීම"),
                ("Deforestation", "වන විනාශය"), ("Recycling", "ප්‍රතිචක්‍රීකරණය"),
                ("Renewable Energy", "පුනර්ජනනීය බලශක්තිය"), ("Conservation", "සංරක්ෂණය"),
                ("Biodiversity", "ජෛව විවිධත්වය"), ("Ecosystem", "පරිසර පද්ධතිය"),
                ("Natural Resources", "ස්වභාවික සම්පත්"), ("Carbon Emissions", "කාබන් විමෝචනය"),
                ("Sustainability", "තිරසාර සංවර්ධනය"),
            ]),
            cat("Activity 3 – Green Mission. A town wants to become environmentally friendly. Place each word under the correct heading.", {
                "Environmental Problems": ["Pollution", "Deforestation", "Carbon Emissions"],
                "Environmental Solutions": ["Recycling", "Renewable Energy", "Conservation"],
                "Natural Systems": ["Ecosystem", "Biodiversity", "Natural Resources"],
                "Long-term Goals": ["Sustainability"],
            }),
            match("Activity 4 – Cause and Effect Builder. Match each problem with its most likely consequence.", [
                ("Cutting down forests", "Loss of biodiversity"), ("Throwing plastic into rivers", "Water pollution"),
                ("Burning fossil fuels", "Climate change"), ("Wasting electricity", "Increased carbon emissions"),
                ("Destroying wildlife habitats", "Animal extinction"),
            ], review=True),
            write("Activity 4 – Now explain your answers in complete sentences. Example: Cutting down forests causes "
                  "the loss of biodiversity because many animals lose their habitats.", [
                "Throwing plastic into rivers …", "Burning fossil fuels …", "Wasting electricity …",
                "Destroying wildlife habitats …",
            ], min_words=6),
            words("B. Science & Innovation", [
                ("Research", "පර්යේෂණ"), ("Discovery", "සොයාගැනීම"), ("Innovation", "නවෝත්පාදනය"),
                ("Technology", "තාක්ෂණය"), ("Experiment", "පරීක්ෂණය"), ("Scientist", "විද්‍යාඥයා"),
                ("Laboratory", "රසායනාගාරය"), ("Medicine", "ඖෂධය"), ("Vaccine", "එන්නත"),
                ("Treatment", "ප්‍රතිකාරය"), ("Artificial Intelligence", "කෘත්‍රිම බුද්ධිය"),
                ("Medical Breakthrough", "වෛද්‍ය විද්‍යාත්මක විශාල සොයාගැනීම"),
            ]),
            *[mcq(f"Activity 5 – {s}", _pick(a), a, review=True) for s, a in [
                ("A team develops a new vaccine that protects children from a disease.", "Medical Breakthrough"),
                ("A scientist studies plants to discover new medicines.", "Research"),
                ("Engineers create a robot that helps doctors during surgery.", "Technology"),
                ("Researchers test a new medicine before hospitals use it.", "Experiment"),
                ("A laboratory studies viruses.", "Laboratory"),
                ("Artificial intelligence helps doctors identify diseases more quickly.", "Artificial Intelligence"),
                ("A researcher makes an important discovery after years of work.", "Discovery"),
                ("Scientists design environmentally friendly technology.", "Innovation"),
            ]],
            match("Activity 6 – Innovation Challenge. Match each problem with the best innovation.", [
                ("Plastic waste", "Recycling machines"), ("Water shortages", "Water purification systems"),
                ("Air pollution", "Electric vehicles"), ("Disease outbreaks", "New vaccines"),
                ("Traffic congestion", "Smart traffic management"),
            ], review=True),
            write("Activity 6 – Which innovation do you think is the most important, and why?", ["My answer:"], min_words=15),
        ],
        "grammar": [
            heading("Review Corner"),
            plain("From Lesson 2: ✔ Narrative Tenses ✔ Travel Vocabulary ✔ Cultural Vocabulary ✔ Sequencing Events "
                  "✔ Expressing Experiences\nExample: While we were visiting Polonnaruwa, our guide explained the "
                  "history of the ancient city.\nToday we move from telling stories to predicting future outcomes "
                  "and proposing solutions."),
            typed("Activity 1 – Last month, my classmates and I ______ (travel) to Galle Fort.", ["travelled", "traveled"], review=True),
            typed("Activity 1 – While we ______ (walk) around the old streets, our guide suddenly ______ (show) us an underground tunnel. Type both verbs, with a comma between them.",
                  ["were walking, showed"], review=True),
            typed("Activity 1 – As everyone ______ (listen), we ______ (learn) many interesting facts about Sri Lanka's colonial history. Type both verbs, with a comma between them.",
                  ["was listening, learned", "was listening, learnt", "were listening, learned"], review=True),
            typed("Activity 1 – Later, we ______ (watch) a traditional dance performance before we returned home.", ["watched"], review=True),
            cat("Activity 2 – Then and Now. Does each statement refer to a past experience, the present situation or a future possibility?", {
                "Past Experience": ["I have visited several national parks.", "We travelled to Yala last December.",
                                    "While we were hiking, we discovered a rare bird.", "My family has planted many trees over the years."],
                "Present Situation": ["Scientists are developing new medical treatments."],
                "Future Possibility": ["If we protect forests, more animals will survive.",
                                       "I am going to volunteer for a beach clean-up next month.",
                                       "People will enjoy cleaner cities if everyone recycles."],
            }, review=True),
            heading("First Conditional"),
            plain("We use the First Conditional to talk about real and possible future situations.\n"
                  "Structure: If + Present Simple + will + base verb"),
            examples("Examples", ["If people recycle more, the environment will become cleaner.",
                                  "If we protect forests, more animals will survive.",
                                  "If scientists discover a better treatment, many lives will improve."]),
            plain("Sinhala Help\nIf people recycle more, the environment will become cleaner.\n"
                  "→ මිනිසුන් වැඩිපුර ප්‍රතිචක්‍රීකරණය කළොත් පරිසරය වඩා පිරිසිදු වේවි.\n"
                  "If we save water, future generations will benefit.\n→ අපි ජලය ඉතිරි කළොත් අනාගත පරම්පරාවට ප්‍රයෝජන ලැබේවි."),
            write("Activity 7 – Green Solutions Challenge. Complete the sentences.", [
                "If everyone plants one tree every year, ______.", "If factories reduce pollution, ______.",
                "If people stop using plastic bags, ______.", "If students recycle paper, ______.",
                "If we waste less electricity, ______.", "If governments invest in renewable energy, ______.",
                "If more people use bicycles, ______.", "If communities protect forests, ______.",
                "Are your ideas realistic? Think about it, then write two or three sentences.",
            ], min_words=4),
            write("Activity 8 – Mission: Save the Planet. Your city has funding for only THREE projects: build more "
                  "parks, plant 10,000 trees, improve public transport, ban single-use plastics, install solar "
                  "panels, organise community recycling programmes, protect wildlife habitats, build more "
                  "factories. Choose the best three and explain your reasons with First Conditional sentences. "
                  "Example: If we improve public transport, fewer people will use private vehicles and air "
                  "pollution will decrease.", ["Project 1 and why:", "Project 2 and why:", "Project 3 and why:"], min_words=10),
            heading("Defining Relative Clauses"),
            plain("We use defining relative clauses to give essential information about a person, place or thing.\n"
                  "who → for people · which → for things or animals · that → for people or things"),
            examples("Examples", ["A scientist is a person who studies the natural world.",
                                  "Wilpattu is a national park which protects many endangered animals.",
                                  "Recycling is an activity that helps reduce waste.",
                                  "A vaccine is a medicine that protects people from disease."]),
            plain("Sinhala Help\nA scientist is a person who studies nature.\n→ විද්‍යාඥයෙක් කියන්නේ ස්වභාවය අධ්‍යයනය කරන පුද්ගලයෙකි.\n"
                  "A forest is a place which provides homes for animals.\n→ වනයක් කියන්නේ සතුන්ට වාසස්ථාන සපයන ස්ථානයකි."),
            *[typed(f"Activity 16 – {s}", a, review=True) for s, a in [
                ("A researcher is a person ______ develops new ideas.", ["who", "that"]),
                ("Recycling is a process ______ helps reduce waste.", ["which", "that"]),
                ("A laboratory is a place ______ scientists carry out experiments.", ["where", "in which"]),
                ("An inventor is someone ______ creates new products.", ["who", "that"]),
                ("National parks are places ______ protect wildlife.", ["which", "that"]),
                ("Renewable energy is energy ______ comes from natural sources.", ["which", "that"]),
                ("A community is a group of people ______ live in the same area.", ["who", "that"]),
                ("A vaccine is a medicine ______ protects people from diseases.", ["which", "that"]),
            ]],
            plain("Activity 17 – Combine the sentences using who, which, or that.\nExample: The student won the science "
                  "competition. She developed a water filter. → The student who developed a water filter won the "
                  "science competition."),
            *[typed(f"Activity 17 – {s}", a, review=True) for s, a in [
                ("We visited a research centre. It studies renewable energy.",
                 ["We visited a research centre which studies renewable energy.", "We visited a research centre that studies renewable energy."]),
                ("I met a scientist. She works on climate change.",
                 ["I met a scientist who works on climate change.", "I met a scientist that works on climate change."]),
                ("They planted trees. The trees improve air quality.",
                 ["They planted trees which improve air quality.", "They planted trees that improve air quality."]),
                ("We watched a documentary. It explained biodiversity.",
                 ["We watched a documentary which explained biodiversity.", "We watched a documentary that explained biodiversity."]),
                ("The organisation protects endangered animals. It needs volunteers.",
                 ["The organisation which protects endangered animals needs volunteers.", "The organisation that protects endangered animals needs volunteers."]),
                ("The students organised a campaign. It encouraged recycling.",
                 ["The students organised a campaign which encouraged recycling.", "The students organised a campaign that encouraged recycling."]),
            ]],
        ],
        "pronunciation": [
            phrases("Listen and Repeat", [
                ("Environment", "එන්වයරන්මන්ට්"), ("Sustainability", None), ("Biodiversity", "බයෝඩයිවර්සිටි"),
                ("Conservation", "කොන්සර්වේෂන්"), ("Renewable", "රිනියුවබල්"), ("Innovation", None),
                ("Laboratory", "ලැබොරටරි"), ("Research", None), ("Scientist", None),
                ("Artificial Intelligence", "ආටිෆිෂල් ඉන්ටෙලිජන්ස්"),
            ]),
            *[speak("Tap & Speak: say the word clearly.", w, seconds=5) for w in [
                "Environment", "Sustainability", "Biodiversity", "Conservation", "Renewable", "Innovation",
                "Laboratory", "Research", "Scientist", "Artificial Intelligence"]],
            heading("Sentence Stress Practice"),
            *[speak(f"Say the sentence. Stress the words in capitals: {s}", t, seconds=10) for s, t in [
                ("If we PROTECT forests, animals WILL survive.", "If we protect forests, animals will survive."),
                ("Scientists are DEVELOPING new treatments.", "Scientists are developing new treatments."),
                ("Renewable ENERGY will reduce pollution.", "Renewable energy will reduce pollution."),
                ("Communities SHOULD work together to protect the environment.", "Communities should work together to protect the environment."),
            ]],
        ],
        "listening": [
            plain("LISTENING TIP\nWhen listening to discussions about the environment or science:\n✔ Listen for problems.\n"
                  "✔ Listen for causes and effects.\n✔ Listen for possible solutions.\n✔ Listen for opinions and "
                  "supporting reasons.\n✔ Notice words such as: because • therefore • however • if • unless • as a result\n"
                  "These words help you understand relationships between ideas."),
            heading("Listening Text 1 – Saving Wilpattu National Park"),
            *[mcq(f"Activity 9 – {q}", o, a, listen=TEXT1) for q, o, a in [
                ("Why did the students visit Wilpattu National Park?", ["To attend an environmental programme", "To play sports", "To study history"], "To attend an environmental programme"),
                ("Who explained the importance of forests?", ["Wildlife officers", "Tourists", "Teachers"], "Wildlife officers"),
                ("Which animals did the students observe?", ["Birds, deer and monkeys", "Elephants only", "Whales"], "Birds, deer and monkeys"),
                ("What environmental problem did they see?", ["Illegal deforestation", "Flooding", "Heavy traffic"], "Illegal deforestation"),
                ("What had disappeared?", ["Natural habitats", "Schools", "Roads"], "Natural habitats"),
                ("What helped endangered species recover?", ["Conservation projects", "Tourism", "Factories"], "Conservation projects"),
                ("According to the officers, forests help improve ______.", ["Air quality", "Television signals", "Internet speed"], "Air quality"),
                ("What did every student do before leaving?", ["Planted a tree", "Bought souvenirs", "Fed the animals"], "Planted a tree"),
                ("What promise did the students make?", ["To organise awareness campaigns", "To visit another country", "To build a hotel"], "To organise awareness campaigns"),
                ("What is the main message of the listening text?", ["Everyone has a responsibility to protect nature.", "National parks are expensive.", "Travelling is difficult."], "Everyone has a responsibility to protect nature."),
            ]],
            write("Activity 10 – Cause & Effect Listening. Write the effect of each cause.", [
                "Trees were cut down. →", "Conservation projects were introduced. →",
                "Students visited the national park. →", "Students planted trees. →",
                "Communities become environmentally aware. →",
            ], min_words=3, listen=TEXT1, models=[
                "Natural habitats disappeared.", "Several endangered species recovered.",
                "They learned why forests and biodiversity are important.", "The forest will grow and the air will be cleaner.",
                "More people will protect nature.",
            ], review=True),
            write("Activity 11 – Audio Note Completion. Complete the notes.", [
                "Location:", "Environmental Problems:", "Animals Mentioned:", "Solutions Suggested:",
                "Students' Promise:", "Lesson Learned:",
            ], min_words=1, listen=TEXT1, models=[
                "Wilpattu National Park", "Illegal deforestation and loss of natural habitats",
                "Native birds, deer, monkeys and rare butterflies", "Conservation projects and planting trees",
                "To organise awareness campaigns in their own communities",
                "Protecting forests also gives people clean water, better air and less climate change.",
            ], review=True),
            write(f"Activity 12 – Think Beyond the Audio. {DISCUSS}", [
                "Why are forests important for people as well as animals?", "What would happen if national parks disappeared?",
                "Which environmental problem is most serious in your area?", "What can young people do to protect biodiversity?",
                "Would you like to volunteer for an environmental campaign? Why?",
            ], min_words=5, listen=TEXT1),
            heading("Listening Text 2 – A Young Scientist's Discovery"),
            *[mcq(f"Activity 13 – {q}", o, a, listen=TEXT2) for q, o, a in [
                ("What is Nimali's profession?", ["Environmental scientist", "Doctor", "Engineer"], "Environmental scientist"),
                ("What problem is her team studying?", ["Plastic pollution", "Traffic", "Climate"], "Plastic pollution"),
                ("What material did they create?", ["Biodegradable material", "Metal", "Glass"], "Biodegradable material"),
                ("What is the material made from?", ["Seaweed", "Wood", "Paper"], "Seaweed"),
                ("Where was it tested?", ["Laboratory", "School", "Museum"], "Laboratory"),
                ("What surprised the researchers?", ["The material was stronger than expected.", "It was expensive.", "It changed colour."], "The material was stronger than expected."),
                ("Who is interested in using the invention?", ["Local businesses", "Tourists", "Farmers"], "Local businesses"),
                ("According to Nimali, what is as important as technology?", ["Education", "Entertainment", "Advertising"], "Education"),
                ("What warning does Nimali give?", ["People must change their behaviour.", "Technology will solve every problem.", "Plastic is harmless."], "People must change their behaviour."),
                ("What is the main purpose of her research?", ["To promote sustainable living", "To earn money", "To increase plastic production"], "To promote sustainable living"),
            ]],
            cat("Activity 14 – Fact or Opinion? Listen again and sort each statement.", {
                "Fact": ["Nimali works in Colombo.", "The new material is made from seaweed.",
                         "The material was stronger than expected.", "Local businesses are interested in the invention."],
                "Opinion": ["Scientific innovation can solve many environmental problems.", "Education is just as important as technology.",
                            "Everyone should stop using plastic immediately.", "Sustainable living is important for the future."],
            }, review=True) | {"listen": TEXT2},
            write("Activity 15 – Green Innovation Challenge. Imagine you are part of Nimali's research team. Choose one "
                  f"problem: plastic pollution, air pollution, water pollution, food waste or deforestation. {DISCUSS} "
                  "Use at least three First Conditional sentences. Example: If people use biodegradable packaging, "
                  "plastic pollution will decrease.", [
                "What is the problem?", "Why is it dangerous?", "What invention could solve it?", "Who would use it?",
                "If your invention is successful, what will happen?",
            ], min_words=5, listen=TEXT2),
        ],
        "reading": [
            plain("READING TIP\nWhen reading articles about environmental or scientific issues:\n✔ Identify the main "
                  "problem.\n✔ Look for the causes and effects.\n✔ Distinguish between facts and opinions.\n"
                  "✔ Identify proposed solutions.\n✔ Ask yourself: \"What is the writer trying to convince me to do or think?\""),
            passage("Reading Passage 1 – Can One Person Change the World?", PASSAGE1,
                    "ඩිලන් නම් විශ්වවිද්‍යාල ශිෂ්‍යයෙක් ගඟක් පිරිසිදු කිරීමේ වැඩසටහනක් ආරම්භ කළා.\n"
                    "කුඩා කණ්ඩායමක් ලෙස ආරම්භ වූ එය පසුව විශාල ප්‍රජා ව්‍යාපෘතියක් බවට පත්වුණා.\n"
                    "එය පරිසර ආරක්ෂාව සඳහා පුද්ගලයෙකුගේ දායකත්වය කොතරම් වැදගත්ද යන්න පෙන්වයි."),
            *[mcq(f"Activity 18 – {q}", o, a) for q, o, a in [
                ("What problem did Dilan notice?", ["Plastic pollution near a river", "Air pollution", "Water shortages"], "Plastic pollution near a river"),
                ("How did he respond to the problem?", ["He organised a clean-up programme.", "He wrote a book.", "He moved away."], "He organised a clean-up programme."),
                ("Who joined the project later?", ["Schools, businesses and local communities", "Foreign tourists", "Scientists only"], "Schools, businesses and local communities"),
                ("Besides cleaning the river, what did volunteers do?", ["Educated people about recycling", "Built roads", "Sold plastic"], "Educated people about recycling"),
                ("What happened after several months?", ["The project expanded.", "The project ended.", "The volunteers left."], "The project expanded."),
                ("Why is plastic pollution dangerous?", ["It affects wildlife, water and human health.", "It creates more parks.", "It increases rainfall."], "It affects wildlife, water and human health."),
                ("What does Dilan believe?", ["Small actions create big change.", "Only governments can help.", "Recycling is expensive."], "Small actions create big change."),
                ("Which sentence best describes the writer's message?", ["Everyone has a role in protecting the environment.", "Pollution cannot be stopped.", "Communities cannot work together."], "Everyone has a role in protecting the environment."),
                ("What type of text is this?", ["Inspirational environmental article", "Advertisement", "News report"], "Inspirational environmental article"),
                ("Which word best describes Dilan?", ["Responsible", "Careless", "Selfish"], "Responsible"),
            ]],
            write("Activity 19 – Reading Detective. Find evidence from the passage.", [
                "Which sentence shows that the project started on a small scale?",
                "What evidence suggests that the community supported the project?",
                "Which sentence explains why recycling education was important?",
                "What evidence shows that the project became successful?",
                "Which sentence expresses the writer's main message?",
            ], min_words=5, models=[
                "\"At first, only a small group of volunteers participated.\"",
                "\"Within a few months, schools, businesses, and community organisations were supporting the project.\"",
                "\"They explained how plastic pollution affects wildlife, drinking water, and even human health.\"",
                "\"Thousands of kilograms of plastic have been collected, and recycling centres have been established in many communities.\"",
                "\"His story reminds us that ordinary people can create extraordinary change when they work together.\"",
            ], review=True),
            write("Activity 20 – Cause, Effect & Solution. Write the cause and a solution for each problem.", [
                "Plastic waste — cause / solution:", "River pollution — cause / solution:",
                "Low community awareness — cause / solution:", "Harm to wildlife — cause / solution:",
                "Waste disposal — cause / solution:",
                "Which solution do you think would have the greatest long-term impact? Why?",
            ], min_words=5),
            passage("Reading Passage 2 – The Future Starts Today", PASSAGE2,
                    "දේශගුණික වෙනස්වීම ලෝකයේ විශාල අභියෝගයකි.\nතාක්ෂණය සහ මිනිසුන්ගේ වගකීම දෙකම පරිසරය ආරක්ෂා කිරීමට අවශ්‍ය වේ.\n"
                    "කුඩා ක්‍රියාකාරකම්ද විශාල වෙනසක් ඇති කළ හැකිය."),
            write("Activity 21 – Critical Reading. Write the solution the passage gives for each challenge.", [
                "Climate Change:", "Pollution:", "Energy Use:", "Biodiversity Loss:", "Waste:",
            ], min_words=2, models=[
                "Cooperation from everyone, plus scientific innovation and responsible lifestyles.",
                "Environmentally friendly products and smarter transportation systems.",
                "Cleaner sources of energy and saving electricity.",
                "Protecting wildlife and planting trees.",
                "Reducing waste.",
            ], review=True),
            cat("Activity 22 – Fact, Opinion or Recommendation? Sort each statement.", {
                "Fact": ["Climate change affects millions of people.", "Floods and droughts are increasing.",
                         "Cleaner energy sources are being developed."],
                "Opinion": ["Technology will solve every environmental problem.", "Responsible lifestyles are necessary."],
                "Recommendation": ["People should reduce waste.", "Everyone should protect wildlife.",
                                   "Schools should teach environmental education."],
            }, review=True),
            write("Activity 23 – Think Like a Scientist. Suggest the best solution. Use at least one First Conditional "
                  "sentence in each answer. Example: If schools organise recycling programmes, students will become "
                  "more environmentally responsible.", [
                "Situation 1: A town produces too much plastic waste. What should the local council do?",
                "Situation 2: Many people waste electricity. What could schools do?",
                "Situation 3: A forest is disappearing because of illegal logging. How can the government and local communities work together?",
                "Situation 4: Young people know very little about biodiversity. How can technology help?",
            ], min_words=10),
        ],
        "speaking": [
            heading("Activity 24 – Green Solutions Forum"),
            plain(f"You are attending a Youth Environmental Conference. {DISCUSS}"),
            *[speak(f"Answer out loud: {q}", m, seconds=45, review=True) for q, m in [
                ("What is the biggest environmental problem in Sri Lanka?", "I think the biggest environmental problem in Sri Lanka is plastic pollution."),
                ("Why is this problem becoming more serious?", "It is becoming more serious because people use more plastic and do not recycle it."),
                ("How does it affect people's daily lives?", "Plastic blocks drains, so roads flood when it rains, and it pollutes our water."),
                ("What can individuals do?", "Individuals can carry their own bags and bottles and recycle their waste."),
                ("What should governments do?", "Governments should ban single-use plastics and build more recycling centres."),
                ("What role should schools play?", "Schools should teach students about the environment and organise clean-up programmes."),
                ("How can technology help protect nature?", "Technology can help us create biodegradable materials and cleaner energy."),
                ("Which environmental habit have you already changed?", "I have stopped using plastic bags, and now I always carry a cloth bag."),
            ]],
            heading("Activity 25 – Climate Action Challenge"),
            plain("Your school has received funding for one environmental project. Choose ONE: plant a mini forest, "
                  "build a recycling centre, install solar panels, organise a zero-plastic campaign, create a school "
                  "garden, introduce rainwater harvesting. Present your proposal. Explain why you chose it, how it "
                  "will help, who will benefit, and what challenges you might face. Use at least four First "
                  "Conditional sentences."),
            speak("Record your proposal. Model:",
                  "I choose to install solar panels. If we install solar panels, the school will use less electricity from fossil fuels. If we save money on electricity, we will be able to buy more books. Students, teachers and the community will benefit. If it is cloudy for many days, we will need a backup, but if we plan carefully, the project will succeed.",
                  seconds=60, review=True),
            heading("Activity 26 – Future Earth Presentation"),
            speak("Speak for 2–3 minutes. Topic: “What Will Our World Be Like in 2050?”. Include climate, technology, "
                  "science, environment, education, transportation, personal responsibility and predictions using "
                  "the First Conditional. Model:",
                  "In 2050, the climate will be warmer, but if we use renewable energy, we will reduce the damage. Technology will help doctors treat diseases faster. Most cars will be electric, so if more people use public transport, our cities will be cleaner. Students will learn online and in school. If every person takes responsibility for small actions, our planet will be healthier.",
                  seconds=150, review=True),
            heading("Lesson 3 Challenge"),
            speak("You have one minute at an international youth conference. Complete the sentence: “If every person "
                  "made one positive environmental change today, our future would...” Give three practical examples "
                  "and end with a message encouraging others to take action. Model:",
                  "If every person made one positive environmental change today, our future would be cleaner and safer. For example, we could carry reusable bags, save electricity and plant trees. Small actions like these add up when millions of people do them. So please start today, because our planet needs all of us.",
                  seconds=60, review=True),
        ],
        "writing": [
            write("Activity 27 – Community Action Plan. Write 180–200 words.", [
                "Topic: “How Can My Community Become More Environmentally Friendly?”. Include: current environmental "
                "problems, possible solutions, First Conditional sentences, your opinion, a conclusion.",
            ], min_words=180),
            write("Activity 28 – Magazine Article. Write 180–200 words. Use at least four defining relative clauses.", [
                "Topic: “A Young Scientist Who Changed the World”. Include: who the scientist is, what problem they "
                "solved, their discovery, how it helps people, why their work is important.",
            ], min_words=180),
            write("Activity 29 – Environmental Campaign Project. Imagine your class is launching an environmental "
                  "awareness campaign. Create a campaign plan.", [
                "Campaign Name:", "Main Environmental Issue:", "Target Audience:", "Three Activities:", "Campaign Slogan:",
                "Write a short speech (120–150 words) encouraging people to join your campaign. Use the First "
                "Conditional, relative clauses and persuasive language.",
            ], min_words=2),
            self_check(
                "□ I can discuss environmental problems confidently.\n□ I can explain scientific discoveries.\n"
                "□ I can use the First Conditional accurately.\n□ I can use defining relative clauses correctly.\n"
                "□ I can identify causes, effects, and solutions.\n□ I can distinguish facts, opinions, and recommendations.\n"
                "□ I can participate in discussions about environmental issues.\n□ I can write proposals and informative articles.\n"
                "□ I can suggest practical solutions to real-world problems.\n"
                "□ I can communicate confidently about science and sustainability.",
                prompt="Self-assessment",
            ),
            summary(["First Conditional for future results", "Defining relative clauses: who, which, that",
                     "Environment and science vocabulary", "Causes, effects and solutions"]),
        ],
    },
}
