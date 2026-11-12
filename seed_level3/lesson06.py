"""Level 3 Lesson 6 — Technology, Media & the Digital Age.

Source: LEVEL_3_L6_individual.docx. Follow-up Part C6 (Activity 12 solo
version) applied. review=True marks keys/models by the King Guru team.
"""
from .dsl import (DISCUSS, cat, examples, heading, mcq, passage, phrases, plain, self_check, speak,
                  summary, typed, words, write)

TEXT1 = (
    "Last month, a photograph of a flooded city was widely shared on social media. Thousands of people "
    "believed that the picture showed a recent disaster in Sri Lanka. Within a few hours, the image had been "
    "shared by hundreds of users. Many people began posting messages asking for donations and warning others "
    "about the situation. Later that day, professional journalists investigated the story. They discovered "
    "that the photograph had actually been taken in another country more than five years earlier. The "
    "original image had been copied from an old news website and shared without proper context. Several "
    "fact-checking organisations quickly published articles explaining the truth. Social media platforms were "
    "informed, and many misleading posts were removed. Although the false story spread rapidly, the correct "
    "information was eventually shared by reliable news organisations. Experts reminded the public that "
    "information should always be verified before it is shared online."
)
TEXT2 = (
    "Many schools are now teaching students about digital safety because technology has become an important "
    "part of everyday life. During an Internet Safety Week programme, students attended a workshop led by a "
    "cybersecurity specialist. The speaker explained that personal information should never be shared with "
    "strangers online. Strong passwords should be created using a combination of letters, numbers and "
    "symbols. Students were also reminded that suspicious links should not be opened because they may "
    "contain harmful software. The specialist demonstrated how fake websites are created to steal personal "
    "information. Finally, students learned that online friendships should be approached carefully because "
    "people are not always who they claim to be. At the end of the workshop, every participant received a "
    "digital safety guide prepared by the school."
)
PASSAGE1 = (
    "Over the past two decades, social media has transformed the way people communicate, learn and share "
    "information. Today, millions of people use platforms such as Facebook, Instagram, TikTok, LinkedIn and X "
    "to connect with family members, friends and colleagues around the world.\n\nOne of the greatest "
    "advantages of social media is that information can be shared almost instantly. News, educational "
    "resources and emergency announcements can reach thousands of people within minutes. During natural "
    "disasters, social media has helped emergency services provide important updates and safety "
    "instructions.\n\nHowever, not everything shared online is accurate. False information can spread just as "
    "quickly as true information, especially when users share posts without checking reliable sources.\n\n"
    "Another concern is the amount of personal information people share online. Many users publish "
    "photographs, locations and personal details without considering possible risks. Cybersecurity experts "
    "advise users to protect their privacy by creating strong passwords and carefully selecting what they "
    "share.\n\nDespite these challenges, social media continues to play an important role in modern "
    "communication. Responsible users understand that technology should be used thoughtfully and that every "
    "post shared online has the potential to influence others."
)
PASSAGE2 = (
    "Every day, thousands of news stories are published on websites, blogs and social media platforms. While "
    "many reports are prepared by professional journalists, others are written by people with little "
    "experience or without checking reliable sources.\n\nAs a result, readers need to think carefully before "
    "accepting information as true.\n\nOne useful strategy is to compare several trustworthy sources. If "
    "different organisations report the same facts, the information is more likely to be accurate.\n\n"
    "Readers should also check whether evidence is provided. Reliable articles often include interviews, "
    "official reports or expert opinions.\n\nSensational headlines are another warning sign. Some websites "
    "use dramatic titles simply to attract more readers. These headlines may exaggerate or misrepresent the "
    "real story.\n\nDigital literacy has become one of the most important skills in today's world. People who "
    "think critically are less likely to believe false information and more likely to make informed "
    "decisions.\n\nInstead of asking, \"Is this interesting?\", responsible readers ask, \"Is this true?\""
)

TECH = ["Password", "Video Conference", "Notification", "Cloud Storage", "Artificial Intelligence (AI)",
        "Social Media", "Application (App)", "Cybersecurity", "Online Platform"]
MEDIA = ["Broadcast", "Journalist", "Editor", "Interview", "Fake News", "Headline", "Reporter",
         "Rumour", "Source", "Opinion"]


def _pick(answer: str, pool: list[str]) -> list[str]:
    others = [w for w in pool if w != answer]
    i = pool.index(answer)
    return [answer, others[(i + 1) % len(others)], others[(i + 4) % len(others)]]


LESSON = {
    "order": 6,
    "title": "Technology, Media & the Digital Age",
    "title_si": "තාක්ෂණය, මාධ්‍ය සහ ඩිජිටල් යුගය",
    "description": "Judge online information, stay safe on the internet and use the Passive Voice (B1).",
    "objectives": [
        "Discuss the impact of technology on everyday life",
        "Identify facts and opinions in news and media texts",
        "Use introductory Passive Voice structures in spoken and written English",
        "Discuss internet safety and responsible digital behaviour",
        "Evaluate information from digital media critically",
        "Take part in discussions and debates about technology and communication",
        "Write short opinion texts and simple news reports",
    ],
    "sections": {
        "vocabulary": [
            words("A. Technology & Internet Vocabulary", [
                ("Technology", "තාක්ෂණය"), ("Device", "උපකරණය"), ("Smartphone", "ස්මාර්ට් දුරකථනය"),
                ("Application (App)", "යෙදුම"), ("Artificial Intelligence (AI)", "කෘත්‍රිම බුද්ධිය"),
                ("Cloud Storage", "ක්ලවුඩ් ගබඩාව"), ("Social Media", "සමාජ මාධ්‍ය"),
                ("Digital Communication", "ඩිජිටල් සන්නිවේදනය"), ("Video Conference", "වීඩියෝ සම්මන්ත්‍රණය"),
                ("Online Platform", "මාර්ගගත වේදිකාව"), ("Notification", "දැනුම්දීම"), ("Password", "මුරපදය"),
                ("Privacy", "පෞද්ගලිකත්වය"), ("Cybersecurity", "සයිබර් ආරක්ෂාව"),
            ]),
            *[mcq(f"Activity 3 – Digital Toolbox: {s}", _pick(a, TECH), a, review=True) for s, a in [
                ("You create a secret code to protect your email account.", "Password"),
                ("Students join an English lesson through Zoom.", "Video Conference"),
                ("Your phone informs you that a new message has arrived.", "Notification"),
                ("You save your university assignment online so you can access it anywhere.", "Cloud Storage"),
                ("A company uses computer systems that learn from data.", "Artificial Intelligence (AI)"),
                ("Friends communicate using Instagram and WhatsApp.", "Social Media"),
                ("You install a new mobile programme to edit photographs.", "Application (App)"),
                ("A business protects customer information from hackers.", "Cybersecurity"),
                ("Employees work together using Microsoft Teams.", "Online Platform"),
                ("You upload files to Google Drive.", "Cloud Storage"),
            ]],
            write("Activity 3 – Now answer.", [
                "Which of these technologies do you use most often?", "Which technology has made your life easier?",
            ], min_words=5),
            cat("Activity 4 – Digital Detective. Is each action safe or unsafe online behaviour?", {
                "Safe": ["Using a strong password", "Checking whether a website is secure", "Updating antivirus software",
                         "Logging out after using a public computer", "Downloading files from trusted websites",
                         "Reporting suspicious online behaviour"],
                "Unsafe": ["Sharing your password with friends", "Clicking unknown links",
                           "Posting your home address publicly", "Accepting friend requests from strangers"],
            }, review=True),
            write(f"Activity 4 – {DISCUSS}", [
                "Which unsafe behaviour is most common among teenagers?", "How can people protect themselves online?",
                "Have you ever experienced an online scam or suspicious message?",
            ], min_words=5),
            words("B. News & Media", [
                ("Headline", "ප්‍රධාන සිරස්තලය"), ("Journalist", "මාධ්‍යවේදියා"), ("Reporter", "වාර්තාකරු"),
                ("Editor", "සංස්කාරක"), ("Article", "ලිපිය"), ("Broadcast", "විකාශනය"),
                ("Interview", "සම්මුඛ සාකච්ඡාව"), ("Source", "මූලාශ්‍රය"), ("Fact", "සත්‍යය"), ("Opinion", "මතය"),
                ("Evidence", "සාක්ෂි"), ("Rumour", "කටකතාව"), ("Fake News", "ව්‍යාජ ප්‍රවෘත්ති"),
                ("Reliable", "විශ්වාසදායක"),
            ]),
            *[mcq(f"Activity 5 – Newsroom Challenge: {s}", _pick(a, MEDIA), a, review=True) for s, a in [
                ("A television programme announces today's top stories.", "Broadcast"),
                ("Someone writes an article for tomorrow's newspaper.", "Journalist"),
                ("A news organisation checks information before publishing it.", "Editor"),
                ("A famous athlete answers questions during a television programme.", "Interview"),
                ("A social media post spreads false information.", "Fake News"),
                ("A newspaper prints today's biggest story in large letters.", "Headline"),
                ("A reporter interviews local residents after a flood.", "Reporter"),
                ("A website publishes information without checking its accuracy.", "Rumour"),
                ("A journalist uses official documents before writing an article.", "Source"),
                ("A reader expresses personal views in an opinion column.", "Opinion"),
            ]],
            write(f"Activity 5 – {DISCUSS}", ["Why is it important to verify information before sharing it?"], min_words=10),
            cat("Activity 6 – Fact or Opinion? Sort each statement.", {
                "Fact": ["Sri Lanka is an island nation.", "The Internet connects millions of users worldwide.",
                         "Cybercrime has increased in many countries.", "Many universities use online learning platforms.",
                         "Passwords help protect online accounts."],
                "Opinion": ["Smartphones have improved people's lives.", "Online learning is more effective than classroom learning.",
                            "Social media is the best invention of the century.", "Artificial intelligence will completely replace teachers.",
                            "Everyone should limit their screen time."],
            }, review=True),
            write("Activity 6 – Now explain which opinions you agree or disagree with and give reasons.", ["My answer:"], min_words=20),
        ],
        "grammar": [
            heading("Review Corner"),
            plain("From Lesson 5: ✔ Workplace Vocabulary ✔ Professional Communication ✔ Modals of Obligation "
                  "✔ Gerunds and Infinitives ✔ Writing Professional Emails\nExamples: Employees must respect company "
                  "rules. · I hope to become an engineer. · We enjoy working in teams.\nToday we move from workplace "
                  "communication to digital communication, online information, and responsible technology use."),
            cat("Activity 1 – Career or Technology? Is each sentence mainly about work & business or technology & media?", {
                "A. Work & Business": ["Employees should attend weekly meetings.", "A professional email should be polite and clear.",
                                       "Employees have to complete safety training before starting work."],
                "B. Technology & Media": ["Many people now read newspapers online.",
                                          "Companies use artificial intelligence to improve customer service.",
                                          "You must protect your online passwords.", "Social media allows people to communicate instantly.",
                                          "Journalists report news through television and websites.",
                                          "Video conferencing has changed the way businesses communicate.",
                                          "Many students use online learning platforms every day."],
            }, review=True),
            write("Activity 1 – Explain why technology has become important in modern workplaces.", ["My answer:"], min_words=15),
            heading("Activity 2 – My Digital Life"),
            write("Answer these questions on your own as a survey. Type a short answer for each.", [
                "Which digital device do you use most often?", "How many hours do you spend online every day?",
                "Which apps help you learn something new?", "What are the advantages of online learning?",
                "Have you ever received false information online?", "How do you decide whether a website is trustworthy?",
                "What are the dangers of sharing too much personal information online?",
                "Do you think people depend too much on technology? Why?",
                "What technological invention has changed your life the most?",
                "Could you live for one week without the Internet? Explain your answer.",
            ], min_words=1),
            speak("Short speaking task – Choose two questions above and record a 30–40 second answer for each. Model:",
                  "The device I use most often is my smartphone. I use it for messages, music and learning English. I spend about three hours online every day, and I think that is enough.",
                  seconds=40, review=True),
            write("Reflection journal – Write 3–4 sentences about your own digital habits: what is healthy, and what you "
                  "would like to change. (ඔබේ ඩිජිටල් පුරුදු ගැන වාක්‍ය 3–4ක් ලියන්න.)", ["My journal:"], min_words=25),
            heading("Introduction to the Passive Voice"),
            plain("We use the Passive Voice when the action is more important than the person who performs it.\n"
                  "Present Simple Passive: Subject + am/is/are + Past Participle"),
            examples("Examples", ["The news is reported every evening.", "Emails are sent automatically.",
                                  "Personal information is protected by secure passwords.",
                                  "Many articles are published online every day."]),
            plain("Sinhala Help\nThe news is reported every evening.\n→ ප්‍රවෘත්ති සෑම සවසකම වාර්තා කරනු ලැබේ.\n"
                  "Personal information is protected.\n→ පෞද්ගලික තොරතුරු ආරක්ෂා කරනු ලැබේ.\n"
                  "Emails are sent automatically.\n→ ඊමේල් ස්වයංක්‍රීයව යවනු ලැබේ."),
            *[typed(f"Activity 7 – Digital Newsroom: {s}", a, review=True) for s, a in [
                ("News articles __________ (publish) every hour.", ["are published"]),
                ("Passwords __________ (protect) by encryption.", ["are protected"]),
                ("Online classes __________ (conduct) using digital platforms.", ["are conducted"]),
                ("Important emails __________ (send) to all employees.", ["are sent"]),
                ("Videos __________ (upload) every day.", ["are uploaded"]),
                ("Personal information __________ (store) securely.", ["is stored"]),
                ("Fake news __________ (share) quickly on social media.", ["is shared"]),
                ("New mobile applications __________ (develop) every year.", ["are developed"]),
                ("Digital payments __________ (use) by millions of people.", ["are used"]),
                ("Online meetings __________ (organise) every week.", ["are organised", "are organized"]),
            ]],
            write("Activity 8 – Become a Digital Detective. A social media story is spreading rapidly. Before sharing "
                  "it, go through the checklist: Is the source reliable? Is evidence provided? Has another news "
                  "organisation reported the same story? Could the headline be misleading? Is the information based "
                  "on facts or opinions? Should you verify the information first?", [
                "“If every person checked information before sharing it, how would social media change?” Use the "
                "First Conditional and the Passive Voice. Example: If information is checked carefully, fewer "
                "rumours will be shared online.",
            ], min_words=20),
            heading("Passive Voice in Context"),
            plain("The Passive Voice is commonly used in news reports because the action is more important than the "
                  "person performing it."),
            examples("Compare", ["Active: Journalists reported the story yesterday. → Passive: The story was reported yesterday.",
                                 "Active: People share millions of videos online every day. → Passive: Millions of videos are shared online every day."]),
            plain("Sinhala Help\nThe article was published yesterday.\n→ ලිපිය ඊයේ ප්‍රකාශයට පත් කරන ලදී.\n"
                  "Personal information is protected by secure systems.\n→ පෞද්ගලික තොරතුරු ආරක්ෂිත පද්ධති මගින් ආරක්ෂා කරනු ලැබේ."),
            *[typed(f"Activity 15 – Newsroom Editor. Rewrite in the Passive Voice: {s}", a, review=True) for s, a in [
                ("Journalists publish thousands of articles every day.",
                 ["Thousands of articles are published every day.", "Thousands of articles are published by journalists every day.", "Thousands of articles are published every day by journalists."]),
                ("Experts verify important information.",
                 ["Important information is verified by experts.", "Important information is verified."]),
                ("Schools organise Internet safety programmes.",
                 ["Internet safety programmes are organised by schools.", "Internet safety programmes are organized by schools.", "Internet safety programmes are organised."]),
                ("Engineers develop new technology.",
                 ["New technology is developed by engineers.", "New technology is developed."]),
                ("Companies protect customer information.",
                 ["Customer information is protected by companies.", "Customer information is protected."]),
                ("Scientists create new software.",
                 ["New software is created by scientists.", "New software is created."]),
                ("Teachers use online learning platforms.",
                 ["Online learning platforms are used by teachers.", "Online learning platforms are used."]),
                ("Police investigate cybercrime cases.",
                 ["Cybercrime cases are investigated by police.", "Cybercrime cases are investigated by the police.", "Cybercrime cases are investigated."]),
                ("Social media users share millions of photographs.",
                 ["Millions of photographs are shared by social media users.", "Millions of photographs are shared."]),
                ("Developers update mobile applications regularly.",
                 ["Mobile applications are updated regularly by developers.", "Mobile applications are updated by developers regularly.", "Mobile applications are updated regularly."]),
            ]],
            write("Activity 16 – Digital Detective Mission. You work for a national fact-checking organisation and a "
                  "viral post has appeared online. Complete your investigation.", [
                "Claim:", "Possible Evidence:", "Reliable Sources You Would Check:", "How Would You Verify the Information?",
                "Final Decision (Reliable / Misleading / False):",
                "Now write a short report (80–100 words) using at least three Passive Voice sentences. Examples: The "
                "information was verified by several news organisations. · The original photograph was published in "
                "2020. · The false claim was removed from social media.",
            ], min_words=2),
        ],
        "pronunciation": [
            phrases("Listen and Repeat", [
                ("Technology", "ටෙක්නොලජි"), ("Journalist", "ජර්නලිස්ට්"), ("Cybersecurity", "සයිබර් සිකියුරිටි"),
                ("Artificial Intelligence", "ආටිෆිෂල් ඉන්ටෙලිජන්ස්"), ("Reliable", "රිලයබල්"), ("Evidence", "එවිඩන්ස්"),
                ("Headline", None), ("Broadcast", "බ්‍රෝඩ්කාස්ට්"), ("Privacy", "ප්‍රයිවසි"),
                ("Encryption", "එන්ක්‍රිප්ෂන්"), ("Notification", "නෝටිෆිකේෂන්"),
            ]),
            *[speak("Tap & Speak: say the word clearly.", w, seconds=5) for w in [
                "Technology", "Journalist", "Cybersecurity", "Artificial Intelligence", "Reliable", "Evidence",
                "Headline", "Broadcast", "Privacy", "Encryption"]],
            heading("Sentence Stress Practice"),
            *[speak(f"Say the sentence. Stress the words in capitals: {s}", t, seconds=10) for s, t in [
                ("Personal information IS PROTECTED online.", "Personal information is protected online."),
                ("News IS REPORTED every hour.", "News is reported every hour."),
                ("Fake news SHOULD NOT BE SHARED without checking the facts.", "Fake news should not be shared without checking the facts."),
                ("Reliable sources ARE USED by professional journalists.", "Reliable sources are used by professional journalists."),
            ]],
        ],
        "listening": [
            plain("LISTENING TIP\nWhen listening to news reports and discussions about technology:\n✔ Listen for the "
                  "main event.\n✔ Identify facts and opinions.\n✔ Listen for evidence supporting a claim.\n✔ Notice "
                  "whether the information comes from a reliable source.\n✔ Pay attention to passive voice expressions "
                  "such as: was reported • was shared • is published • was discovered"),
            heading("Listening Text 1 – Fake News Spreads Fast"),
            *[mcq(f"Activity 9 – {q}", o, a, listen=TEXT1) for q, o, a in [
                ("What was widely shared online?", ["A photograph", "A video game", "A sports article"], "A photograph"),
                ("What did many people believe?", ["The picture showed a recent disaster.", "It showed a concert.", "It showed a political meeting."], "The picture showed a recent disaster."),
                ("Who investigated the story?", ["Professional journalists", "Police officers", "Teachers"], "Professional journalists"),
                ("What did they discover?", ["The photograph was old.", "The picture was edited yesterday.", "The event happened last week."], "The photograph was old."),
                ("Where had the photograph originally appeared?", ["On an old news website", "In a school magazine", "On television"], "On an old news website"),
                ("Who published the correct information?", ["Fact-checking organisations", "Bloggers", "Tourists"], "Fact-checking organisations"),
                ("What happened to many misleading posts?", ["They were removed.", "They became advertisements.", "They won awards."], "They were removed."),
                ("What lesson does the listening teach?", ["Always verify information before sharing it.", "Never use social media.", "Newspapers are always wrong."], "Always verify information before sharing it."),
            ]],
            write("Activity 10 – Digital Detective Notebook. Complete the investigation report.", [
                "Headline:", "What happened?", "What evidence proved the story was false?", "Who verified the information?",
                "What action was taken?", "What lesson can we learn?",
            ], min_words=2, listen=TEXT1, models=[
                "Old Flood Photo Shared as a Recent Sri Lankan Disaster",
                "A photograph of a flooded city was shared by thousands of people as a recent disaster in Sri Lanka.",
                "It had been taken in another country more than five years earlier and copied from an old news website.",
                "Professional journalists and fact-checking organisations.",
                "Articles explaining the truth were published and many misleading posts were removed.",
                "Information should always be verified before it is shared online.",
            ], review=True),
            cat("Activity 11 – Fact Check Investigation. Listen again. Is each statement a fact or an opinion?", {
                "Fact": ["The photograph was widely shared.", "Journalists investigated the story.",
                         "The image was more than five years old."],
                "Opinion": ["Social media is dangerous.", "Everyone believes fake news.", "Information should be verified."],
            }, review=True) | {"listen": TEXT1},
            write("Activity 11 – Now explain why facts and opinions should not be confused.", ["My answer:"], min_words=15, listen=TEXT1),
            heading("Activity 12 – Before You Share..."),
            write("Imagine that someone sends you a shocking news story. Before sharing it, think about the following questions.", [
                "Who published the story?", "Is there enough evidence?", "Can another reliable source confirm it?",
                "Could the headline be misleading?", "What might happen if the information is false?",
            ], min_words=4, listen=TEXT1),
            speak("Decide: will you share it or not? Record your decision and give two reasons. Model:",
                  "I will not share the story. First, it was published by an unknown website. Second, no reliable news organisation has reported it, so it might be false and could frighten people.",
                  seconds=40, review=True) | {"listen": TEXT1},
            heading("Listening Text 2 – Staying Safe Online"),
            *[mcq(f"Activity 13 – {q}", o, a, listen=TEXT2) for q, o, a in [
                ("Why did the school organise the programme?", ["To teach digital safety", "To introduce a new subject", "To celebrate a festival"], "To teach digital safety"),
                ("Who conducted the workshop?", ["A cybersecurity specialist", "A police officer", "A university student"], "A cybersecurity specialist"),
                ("What should never be shared online?", ["Personal information", "Homework", "Music"], "Personal information"),
                ("What should strong passwords include?", ["Letters, numbers and symbols", "Only numbers", "Only names"], "Letters, numbers and symbols"),
                ("Why should suspicious links be avoided?", ["They may contain harmful software.", "They waste time.", "They use too much data."], "They may contain harmful software."),
                ("What did students learn about fake websites?", ["They are created to steal information.", "They are always colourful.", "They are legal websites."], "They are created to steal information."),
                ("What did every participant receive?", ["A digital safety guide", "A certificate", "A laptop"], "A digital safety guide"),
                ("What is the main purpose of the workshop?", ["To encourage responsible Internet use.", "To promote social media.", "To teach programming."], "To encourage responsible Internet use."),
            ]],
            cat("Activity 14 – Safe or Unsafe? Listen again and sort each action.", {
                "Safe": ["Creating strong passwords", "Updating security software", "Checking website addresses",
                         "Reporting suspicious accounts", "Using two-factor authentication"],
                "Unsafe": ["Sharing passwords", "Clicking unknown links", "Sharing personal details publicly"],
            }, review=True) | {"listen": TEXT2},
            write(f"Activity 14 – {DISCUSS}", ["Which online safety rule is the most important? Why?"], min_words=15, listen=TEXT2),
        ],
        "reading": [
            plain("READING TIP\nWhen reading online articles and news reports:\n✔ Identify the main idea.\n"
                  "✔ Distinguish between facts and opinions.\n✔ Consider whether the source is reliable.\n"
                  "✔ Look for supporting evidence.\n✔ Ask yourself: \"Can I trust this information?\""),
            passage("Reading Passage 1 – How Social Media Has Changed the Way We Communicate", PASSAGE1,
                    "සමාජ මාධ්‍ය සන්නිවේදනය ඉතා වේගවත් කර ඇත.\nනමුත් වැරදි තොරතුරුද ඉක්මනින් පැතිර යා හැකිය.\n"
                    "එබැවින් තොරතුරු පරීක්ෂා කර බෙදාගැනීම සහ පෞද්ගලිකත්වය ආරක්ෂා කිරීම වැදගත්ය."),
            *[mcq(f"Activity 17 – {q}", o, a, review=True) for q, o, a in [
                ("How has social media changed communication?", ["Information can be shared almost instantly around the world", "People now write more letters", "It has made communication slower"], "Information can be shared almost instantly around the world"),
                ("Which two advantages are mentioned in the passage?", ["Instant sharing and help during emergencies", "Free phones and faster internet", "More jobs and higher salaries"], "Instant sharing and help during emergencies"),
                ("Why does false information spread easily?", ["Users share posts without checking reliable sources", "Journalists always lie", "The internet is slow"], "Users share posts without checking reliable sources"),
                ("What risks come with sharing personal information?", ["Photographs, locations and details may be misused", "You will get more followers", "There are no risks"], "Photographs, locations and details may be misused"),
                ("What advice do cybersecurity experts give?", ["Use strong passwords and choose carefully what you share", "Share everything publicly", "Never use the internet"], "Use strong passwords and choose carefully what you share"),
                ("How can social media help during emergencies?", ["Emergency services can share updates and safety instructions", "It stops natural disasters", "It sends money automatically"], "Emergency services can share updates and safety instructions"),
                ("What does the writer mean by \"technology should be used thoughtfully\"?", ["We should think before we post or share", "We should use technology as much as possible", "We should stop using technology"], "We should think before we post or share"),
                ("What is the writer's overall opinion of social media?", ["It is important but must be used responsibly", "It is completely bad", "It is perfect"], "It is important but must be used responsibly"),
            ]],
            write("Activity 17 – Your view.", [
                "Do you agree with the writer? Explain your answer.",
                "Suggest one additional way people can use social media responsibly.",
            ], min_words=10),
            write("Activity 18 – Evidence Detective. Find evidence from the passage for each statement.", [
                "Social media helps people communicate quickly.", "False information spreads rapidly.",
                "Privacy should be protected online.", "Social media can help during emergencies.",
                "Responsible users think before sharing information.",
                "Why is evidence important when reading news online?",
            ], min_words=5, models=[
                "\"News, educational resources and emergency announcements can reach thousands of people within minutes.\"",
                "\"False information can spread just as quickly as true information.\"",
                "\"Cybersecurity experts advise users to protect their privacy by creating strong passwords.\"",
                "\"During natural disasters, social media has helped emergency services provide important updates.\"",
                "\"Responsible users understand that technology should be used thoughtfully.\"",
            ], review=True),
            write("Activity 19 – Pros and Cons Analysis.", [
                "Advantages of social media (at least three):", "Disadvantages of social media (at least three):",
                "Do the advantages outweigh the disadvantages? Explain your opinion.",
            ], min_words=8),
            passage("Reading Passage 2 – Can We Trust Everything We Read Online?", PASSAGE2,
                    "අන්තර්ජාලයේ ඇති සියලුම තොරතුරු විශ්වාස කළ නොහැක.\nවිශ්වාසදායක මූලාශ්‍ර, සාක්ෂි සහ විවිධ වාර්තා පරීක්ෂා කිරීම වැදගත්ය.\n"
                    "විවේචනාත්මකව සිතීම ඩිජිටල් යුගයේ අත්‍යවශ්‍ය කුසලතාවකි."),
            cat("Activity 20 – Fact, Opinion or Recommendation? Sort each statement.", {
                "Fact": ["Thousands of articles are published every day.", "Evidence improves credibility.",
                         "Sensational headlines attract attention.", "Digital literacy is an important life skill."],
                "Opinion": ["Every online article is trustworthy.", "Professional journalism is always perfect."],
                "Recommendation": ["Readers should compare different sources.", "Everyone should question online information."],
            }, review=True),
            plain("Activity 21 – Media Detective. Read the headlines.\nHeadline A: “Scientists Discover a New Method to "
                  "Reduce Plastic Waste.” (Source: National Science Institute)\nHeadline B: “You Won't Believe This "
                  "Amazing Secret That Will Save the Planet Overnight!” (Source: Unknown Website)\nHeadline C: "
                  "“Government Announces New Recycling Programme Beginning Next Month.” (Source: National News Network)"),
            mcq("Activity 21 – Which headline is designed to attract attention rather than inform?",
                ["Headline B", "Headline A", "Headline C"], "Headline B", review=True),
            write(f"Activity 21 – {DISCUSS}", [
                "Which headlines seem trustworthy, and why?",
                "What evidence would you look for before believing each story?",
            ], min_words=10),
        ],
        "speaking": [
            heading("Activity 22 – Technology Debate"),
            plain("Choose ONE topic. Topic A: Social media does more good than harm. Topic B: Artificial Intelligence "
                  "will improve education. Topic C: Students should have limited screen time.\nStep 1 — Pick your "
                  "viewpoint: Agree or Disagree.\nStep 2 — Choose two or three pieces of supporting evidence."),
            examples("Topic A — Social media does more good than harm", [
                "It connects people and helps them share ideas. (Agree)", "Useful information and news spread quickly. (Agree)",
                "It can spread misinformation. (Disagree)", "Too much screen time can affect mental health. (Disagree)"]),
            examples("Topic B — Artificial Intelligence will improve education", [
                "It personalises learning for each student. (Agree)", "It gives instant feedback and help. (Agree)",
                "It can reduce students' critical thinking. (Disagree)", "Not every student has equal access to it. (Disagree)"]),
            examples("Topic C — Students should have limited screen time", [
                "It protects health and sleep. (Agree)", "It improves focus on studies. (Agree)",
                "It limits access to useful learning tools. (Disagree)", "It is hard to enforce fairly. (Disagree)"]),
            speak("Step 3 — Record a short opinion (about one minute) with your viewpoint, your evidence and one example. Model:",
                  "I agree that students should have limited screen time. First, it protects their health and sleep. Second, it improves focus on studies. For example, when I stopped using my phone after nine o'clock, I slept better and did better in my tests.",
                  seconds=60, review=True),
            heading("Activity 23 – Newsroom Discussion"),
            plain("Imagine you are the chief news editor of a television news channel. A story has become popular "
                  "online. Before broadcasting it, think carefully: Is the source reliable? Has the information been "
                  "verified? Is there enough evidence? Could the story create unnecessary panic? Should it be "
                  "broadcast immediately?"),
            speak("Speaking Task – Record a 1–2 minute news-meeting summary: would you broadcast the story, why, and "
                  "what steps should be taken first? Model:",
                  "I would not broadcast the story yet. The source is a single social media account, and the information has not been verified. There is not enough evidence, and the story could create unnecessary panic. First, our reporters should contact the police and check official reports. If the facts are confirmed, we will broadcast it tonight.",
                  seconds=90, review=True),
            heading("Activity 24 – Digital Detective Challenge"),
            speak("Speak for 2–3 minutes. Topic: “How Can We Become Responsible Digital Citizens?”. Include internet "
                  "safety, fake news, privacy, responsible communication, technology in education and the future of "
                  "digital media. Use the Passive Voice, facts and opinions, and your own examples. Model:",
                  "Responsible digital citizens protect themselves and others. Strong passwords should be used, and personal information should not be shared with strangers. Before a story is shared, it should be checked with reliable sources. I think schools should teach digital literacy, because many students are online every day. For example, I once received a fake message about a prize, and I deleted it. In the future, more information will be shared online, so these skills will be even more important.",
                  seconds=150, review=True),
        ],
        "writing": [
            write("Activity 25 – News Report. Write 180–200 words. Your school organised a Digital Safety Awareness "
                  "Week. Write a news report. Include the date and location, activities organised, guest speakers, "
                  "students' participation and the main message. Use at least five Passive Voice sentences.",
                  ["Headline and report:"], min_words=180),
            write("Activity 26 – Opinion Essay. Write 180–200 words. Topic: “Has Technology Improved Our Lives?”. "
                  "Include an introduction, advantages, disadvantages, your opinion and a conclusion. Use facts, "
                  "opinions, the Passive Voice and linking words (however, therefore, furthermore, in conclusion).",
                  ["My essay:"], min_words=180),
            write("Activity 27 – Digital Detective Final Mission. A news story has gone viral. Complete the investigation.", [
                "Step 1 – Identify the claim.", "Step 2 – List three reliable sources you would consult.",
                "Step 3 – Explain how the information would be verified.",
                "Step 4 – Write a short news report (120–150 words) with the Passive Voice, facts only and a suitable headline.",
                "Step 5 – Reflection (80–100 words): “Why is digital literacy an essential skill in today's world?”",
            ], min_words=5),
            write("LESSON 6 SIGNATURE CHALLENGE – DIGITAL DETECTIVE. Investigate a breaking online story before it is published.", [
                "Mission 1 – Examine the Headline: is it informative, misleading or sensational? Explain.",
                "Mission 2 – Verify the Information: list the steps you would take to check whether the story is accurate.",
                "Mission 3 – Write the Report: a short, objective news report using the Passive Voice.",
                "Mission 4 – Public Safety Message: a short announcement (80–100 words) encouraging people to think critically before sharing.",
                "Mission 5 – Final Reflection: “Responsible digital citizens are people who...” Support your answer with examples from the lesson.",
            ], min_words=10),
            self_check(
                "□ I can discuss technology and digital communication confidently.\n□ I can identify facts and opinions in media texts.\n"
                "□ I can recognise reliable and unreliable sources.\n□ I can use introductory Passive Voice accurately.\n"
                "□ I can analyse online information critically.\n□ I can participate in debates about technology and media.\n"
                "□ I can write a short news report.\n□ I can write an opinion essay using supporting evidence.\n"
                "□ I can explain how to stay safe online.\n□ I can use English confidently in digital communication.",
                prompt="Self-assessment",
            ),
            summary(["Present Simple and Past Simple Passive", "Facts, opinions and reliable sources",
                     "Internet safety vocabulary", "Writing a news report"]),
        ],
    },
}
