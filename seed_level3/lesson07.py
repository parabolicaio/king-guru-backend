"""Level 3 Lesson 7 — Consumerism, Money & Global Food.

Source: LEVEL_3_L7_individual.docx. Follow-up Part B2/B3 (the app's lines in
the role plays) and Part C7/C8 solo lines applied. review=True marks
keys/models by the King Guru team.
"""
from .dsl import (DISCUSS, cat, examples, heading, mcq, open_answer, passage, phrases, plain,
                  self_check, speak, summary, typed, words, write)

TEXT1 = (
    "Nadeesha and her brother are shopping for groceries before the weekend. Nadeesha: We only have Rs. 8,000 "
    "today, so we need to be careful with our spending. Brother: I think we should buy fresh vegetables first. "
    "Nadeesha: I agree. They aren't too expensive, and they're healthier than processed food. Brother: What "
    "about these apples? Nadeesha: They're fresh enough, but they're quite expensive. Let's compare the prices "
    "with another shop. Brother: Good idea. We also need rice, milk and eggs. Nadeesha: Yes, but we don't have "
    "enough money to buy everything on our list today. Brother: Then let's leave the snacks for next week. "
    "Nadeesha: That's probably the smartest decision. When they finished shopping, they stayed within their "
    "budget and bought everything they really needed."
)
TEXT2 = (
    "Welcome to today's Food Review Podcast! This week we visited The Spice Garden, a family restaurant that "
    "serves both traditional Sri Lankan dishes and international meals. The restaurant was clean and "
    "comfortable. The staff were friendly and welcomed every customer warmly. The chicken rice was delicious "
    "and the portion was large enough for one person. However, the seafood pasta was slightly too salty. The "
    "fresh fruit juice was refreshing, and the desserts were beautifully presented. Although the prices were a "
    "little higher than those of nearby restaurants, the food quality and excellent service made the "
    "experience worthwhile. Overall, we would happily recommend this restaurant to anyone looking for "
    "authentic flavours and a relaxing atmosphere."
)
PASSAGE1 = (
    "Many people make shopping decisions based on emotions rather than necessity. Have you ever bought "
    "something simply because it was on sale or because everyone else seemed to have it? This type of buying "
    "is often called impulse buying.\n\nAdvertisements, social media and special promotions encourage "
    "consumers to spend more money. Bright colours, limited-time offers and phrases such as \"Only Today!\" or "
    "\"Buy One, Get One Free!\" often create a sense of urgency. As a result, people sometimes purchase "
    "products they never intended to buy.\n\nOnline shopping has also made impulse buying easier. With just a "
    "few clicks, customers can compare products, read reviews and place orders without leaving home. Although "
    "this is convenient, it can also encourage unnecessary spending.\n\nFinancial experts recommend creating a "
    "shopping list and setting a budget before shopping. They also suggest waiting a day before buying "
    "expensive items. This gives consumers time to think carefully about whether they really need the "
    "product.\n\nBeing a smart shopper does not mean buying the cheapest product. It means making informed "
    "decisions based on quality, value for money and personal needs."
)
PASSAGE2 = (
    "Food plays an important role in every culture. Traditional meals are often prepared using fresh "
    "ingredients and recipes that have been passed down through generations. These meals usually take more "
    "time to prepare but are often richer in nutrients.\n\nFast food, on the other hand, is convenient and "
    "quick. Many busy people choose fast food because it saves time. However, eating fast food regularly may "
    "increase the risk of health problems if it becomes part of a daily diet.\n\nIn recent years, many "
    "restaurants have started offering healthier options. Customers can now choose grilled dishes, fresh "
    "salads and fruit instead of fried food.\n\nRather than avoiding fast food completely, nutritionists "
    "recommend maintaining a balanced diet by making healthier choices most of the time."
)

# Follow-up Part B2/B3: (what the app says, what the learner does, model reply).
SUPERMARKET = [
    ("Good morning! Can I help you find anything?", "Say what you are looking for.",
     "Yes, please. I'm looking for rice. Where can I find it?"),
    ("The rice is in aisle three. There is a ten per cent discount on this brand today.", "Ask about the price or the size.",
     "That's great. How much is the five-kilo bag?"),
    ("The five-kilo bag is Rs. 1,450, and the ten-kilo bag is Rs. 2,700.", "Choose one and give a reason (use too or enough).",
     "I'll take the five-kilo bag. The ten-kilo bag is too heavy for me to carry, and five kilos is enough for my family."),
    ("Would you like anything else?", "Ask about one more item.",
     "Yes. Do you have fresh milk? Is it on sale?"),
    ("Will you pay by cash or by card?", "Answer and ask for the receipt.",
     "Can I pay by card, please? Could I have the receipt, please?"),
]
RESTAURANT = [
    ("Good evening, and welcome! Here is the menu. Can I get you something to drink first?", "Order a drink.",
     "Thank you. I'd like a fresh lime juice, please."),
    ("Today's special is grilled fish with garlic rice.", "Ask about the ingredients.",
     "That sounds nice. What is it made with?"),
    ("It's made with fresh seer fish, garlic, lime and a little chilli. It isn't too spicy.", "Ask about the price.",
     "How much does the grilled fish cost?"),
    ("It's Rs. 2,200. If you would like something lighter, I recommend the vegetable curry.",
     "Ask for or respond to the recommendation, then order.",
     "Thank you for the recommendation. I'd like to order the vegetable curry with rice, please."),
    ("Excellent choice. Would you like a dessert as well?", "Answer politely.",
     "No, thank you. That's enough for me."),
]
GIFT = [
    ("Hello! Are you looking for something special today?", "Say who the present is for and your budget.",
     "Yes, I'm looking for a birthday present for my brother. My budget is about Rs. 12,000."),
    ("These two headphones are very popular. The SoundMax is Rs. 8,500, and the BeatPro is Rs. 12,000.", "Ask about the quality.",
     "Which one has better quality?"),
    ("The BeatPro has better sound and a longer battery life, but the SoundMax is lighter.", "Ask about the warranty.",
     "Is there a warranty on these headphones?"),
    ("The SoundMax has a one-year warranty, and the BeatPro has a two-year warranty.",
     "Compare them: which is better value for money?",
     "The BeatPro is more expensive, but it has better sound and a longer warranty, so I think it is better value for money."),
    ("So, which one would you like to take?", "Choose one and explain why.",
     "I'll take the BeatPro, because my brother listens to music every day and it will last longer."),
]
RESTAURANT_2 = [
    ("Good afternoon! A table for one? Please have a seat.", "Ask for the menu.",
     "Thank you. Could I see the menu, please?"),
    ("Here you are. Are you ready to order, or do you need a few minutes?", "Order your food.",
     "I'm ready. I'd like to order the chicken curry with rice, please."),
    ("Certainly. Is there anything you would like to know about the dish?", "Ask about the ingredients.",
     "Yes, what ingredients are in the chicken curry?"),
    ("It has chicken, coconut milk, onions and curry spices. If you like spicy food, I also recommend our devilled prawns.",
     "Respond to the recommendation.",
     "Thank you, but devilled prawns are too spicy for me. The chicken curry is enough."),
    ("How was your meal?", "Answer politely and ask for the bill.",
     "It was delicious, thank you. Could I have the bill, please?"),
    ("Here is your bill. It's Rs. 3,150, including the service charge.", "Pay and thank the waiter.",
     "Here you are. Can I pay by card? Thank you very much for the excellent service."),
]


def _role_play(lines: list[tuple[str, str, str]]) -> list[dict]:
    return [speak(f"Listen, then record your reply: {task} Model:", model, seconds=30, review=True) | {"listen": says}
            for says, task, model in lines]


SHOP_WORDS = ["Warranty", "Budget", "Receipt", "Discount", "Refund", "Customer Review", "Value for Money", "Online Purchase"]

LESSON = {
    "order": 7,
    "title": "Consumerism, Money & Global Food",
    "title_si": "පාරිභෝගිකත්වය, මුදල් සහ ලෝක ආහාර",
    "description": "Shop and spend wisely, talk about food from around the world and use too and enough (B1).",
    "objectives": [
        "Discuss shopping habits and consumer choices confidently",
        "Use too and enough accurately in different contexts",
        "Compare products and make informed purchasing decisions",
        "Describe food, cooking methods and recipes using appropriate vocabulary",
        "Discuss budgeting and responsible spending habits",
        "Compare food cultures from different countries",
        "Write simple recipes and consumer advice texts",
    ],
    "sections": {
        "vocabulary": [
            words("A. Consumer & Shopping Vocabulary", [
                ("Consumer", "පාරිභෝගිකයා"), ("Budget", "අයවැය"), ("Discount", "වට්ටම"), ("Receipt", "රිසිට්පත"),
                ("Warranty", "වගකීම් සහතිකය"), ("Brand", "වෙළඳ නාමය"), ("Quality", "ගුණාත්මකභාවය"),
                ("Refund", "මුදල් ආපසු ලබාදීම"), ("Value for Money", "මුදලට වටිනාකම"), ("Bargain", "ලාභදායී මිලදී ගැනීම"),
                ("Expense", "වියදම"), ("Savings", "ඉතිරිකිරීම්"), ("Customer Review", "පාරිභෝගික අදහස"),
                ("Online Purchase", "මාර්ගගත මිලදී ගැනීම"),
            ]),
            *[mcq(f"Activity 4 – Shopping Detective: {s}", o, a, review=True) for s, o, a in [
                ("You buy a washing machine. If it stops working within two years, the company promises to repair it free of charge.", ["Receipt", "Warranty", "Discount", "Bargain"], "Warranty"),
                ("Before going shopping, your family decides how much money can be spent this month.", ["Expense", "Brand", "Budget", "Refund"], "Budget"),
                ("After paying for a pair of shoes, the cashier gives you a printed document showing the amount you paid.", ["Receipt", "Savings", "Customer Review", "Quality"], "Receipt"),
                ("A supermarket reduces the price of cooking oil by 25% for one weekend only.", ["Bargain", "Refund", "Discount", "Expense"], "Discount"),
                ("You return a damaged electric kettle and receive all your money back.", ["Value for Money", "Refund", "Budget", "Brand"], "Refund"),
                ("Before buying a mobile phone, you read what other buyers have written about it online.", ["Customer Review", "Receipt", "Warranty", "Discount"], "Customer Review"),
                ("Two bags cost the same, but one is stronger, lasts longer and has a better warranty. It offers better...", ["Expense", "Quality", "Value for Money", "Savings"], "Value for Money"),
                ("You order a book using an online shopping website. This is called an...", ["Online Purchase", "Refund", "Discount", "Bargain"], "Online Purchase"),
            ]],
            write("Activity 4 – Now answer.", [
                "Which of these shopping terms do you use most often?", "Have you ever returned a product? What happened?",
            ], min_words=5),
            write("Activity 5 – Smart Shopping Decisions. You have Rs. 8,000 to buy a backpack. Backpack A: waterproof, "
                  "laptop compartment, Rs. 7,950. Backpack B: ordinary fabric, no laptop compartment, Rs. 5,200.",
                  ["Which backpack would you choose? Why?"], min_words=10),
            mcq("Activity 5 – A pair of sports shoes is advertised as 50% OFF. Before buying them, what should you check first?",
                ["Whether you actually need them", "The colour", "What your friend thinks", "Whether the shop is crowded"],
                "Whether you actually need them", review=True),
            write("Activity 5 – Two online stores sell the same smartwatch. Store A: Rs. 14,500, rated 4.5. Store B: "
                  "Rs. 13,900, rated 2.8.", ["Which store would you buy from? Explain your decision."], min_words=10),
            mcq("Activity 5 – You want to buy a birthday present for your friend. Which is the most important factor?",
                ["Best quality", "Lowest price", "Attractive packaging", "Most expensive brand"], "Best quality", review=True),
            mcq("Activity 5 – You have enough money to buy only one item today. Which would be the best investment?",
                ["English Dictionary", "Designer Sunglasses", "Video Game", "Decorative Lamp"], "English Dictionary", review=True),
            plain("Activity 6 – Read Before You Buy.\nProduct Review 1 ⭐⭐⭐⭐⭐ “This backpack is comfortable, waterproof "
                  "and spacious enough for my university books. I've used it for nearly a year, and it still looks "
                  "new. I would definitely recommend it.”\nProduct Review 2 ⭐⭐☆☆☆ “The headphones looked stylish, but "
                  "the battery lasted only two hours. They were too expensive for the quality they offered.”\n"
                  "Product Review 3 ⭐⭐⭐⭐☆ “The rice cooker was easy to use, and the instructions were clear. Although "
                  "it cost a little more than other models, it was worth buying because it saves both time and electricity.”"),
            mcq("Activity 6 – Which product received the highest rating?", ["The backpack", "The headphones", "The rice cooker"], "The backpack", review=True),
            mcq("Activity 6 – Why was the customer disappointed with the headphones?",
                ["The battery lasted only two hours", "They were the wrong colour", "They arrived late"],
                "The battery lasted only two hours", review=True),
            mcq("Activity 6 – Which review uses a positive recommendation?", ["Review 1", "Review 2", "Review 3"], "Review 1", review=True),
            write("Activity 6 – Answer the questions.", [
                "Which product offers good value for money?", "Which review would most influence your decision?",
                "Do you usually read customer reviews before buying something? Why or why not?",
                "Find one sentence that describes quality.", "Would you recommend any of these products? Explain.",
            ], min_words=4),
            plain("Consumer Tip\nBefore buying an expensive product, ask yourself:\n✔ Do I really need it?\n✔ Is the "
                  "quality good?\n✔ Have I compared prices?\n✔ What do other customers say?\n✔ Is it worth the money?\n"
                  "A smart consumer doesn't always buy the cheapest product—they buy the product that offers the best value."),
            speak("Mini Speaking Challenge – Your friend wants to buy a new laptop. Give your advice for one minute. Use: "
                  "I think you should... · In my opinion... · It would be better to... · You should compare... · "
                  "Don't forget to check... Model:",
                  "I think you should make a budget first. In my opinion, the cheapest laptop is not always the best. You should compare the prices in two or three shops and read customer reviews. Don't forget to check the warranty.",
                  seconds=60, review=True),
            write("Quick Reflection – Complete the sentences.", [
                "Before I buy something expensive, I usually ______.", "One shopping mistake I have made is ______.",
                "Next time I go shopping, I will ______.",
            ], min_words=3),
            words("B. Global Food", [
                ("Cuisine", "ආහාර සංස්කෘතිය"), ("Ingredient", "අමුද්‍රව්‍ය"), ("Recipe", "වට්ටෝරුව"),
                ("Appetiser", "ආරම්භක ආහාරය"), ("Main Course", "ප්‍රධාන ආහාරය"), ("Dessert", "අතුරුපස"),
                ("Boil", "තම්බනවා"), ("Fry", "බැදනවා"), ("Bake", "උඳුනේ පිසිනවා"), ("Grill", "ග්‍රිල් කරනවා"),
                ("Steam", "වාෂ්පයෙන් පිසිනවා"), ("Roast", "පුළුස්සනවා"), ("Spices", "කුළුබඩු"),
                ("Nutrition", "පෝෂණය"), ("Vegetarian", "නිර්මාංශ"), ("Seafood", "මුහුදු ආහාර"),
            ]),
            *[mcq(f"Activity 7 – Around the World on a Plate: {s}", o, a, review=True) for s, o, a in [
                ("A dish made with vinegared rice, seafood and seaweed.", ["Japan", "Italy", "Sri Lanka", "Mexico"], "Japan"),
                ("A spicy rice dish often served with chicken, seafood or vegetables.", ["Spain", "China", "India", "Thailand"], "India"),
                ("A traditional meal prepared with hoppers, coconut sambol and dhal curry.", ["Sri Lanka", "Nepal", "Korea", "Greece"], "Sri Lanka"),
                ("A baked dish made with pasta, cheese and tomato sauce.", ["Italy", "Malaysia", "Japan", "Turkey"], "Italy"),
                ("Soft tortillas filled with meat, vegetables and salsa.", ["Mexico", "France", "Vietnam", "Australia"], "Mexico"),
                ("A noodle dish commonly eaten using chopsticks and often served in broth.", ["China", "Brazil", "Egypt", "Canada"], "China"),
            ]],
            write(f"Activity 7 – Let's Talk. {DISCUSS}", [
                "Which of these dishes have you tasted?", "Which cuisine would you like to try?",
                "What makes Sri Lankan food unique?",
            ], min_words=5),
            *[mcq(f"Activity 8 – What's the Cooking Method? {s}", o, a) for s, o, a in [
                ("Chicken is cooked over hot charcoal.", ["Boil", "Grill", "Steam", "Bake"], "Grill"),
                ("Potatoes are cooked in hot oil until they become crispy.", ["Roast", "Fry", "Steam", "Boil"], "Fry"),
                ("Bread is prepared inside an oven.", ["Bake", "Grill", "Fry", "Steam"], "Bake"),
                ("Rice is cooked in boiling water.", ["Steam", "Boil", "Roast", "Fry"], "Boil"),
                ("Fish is slowly cooked over hot coals without oil.", ["Grill", "Steam", "Fry", "Boil"], "Grill"),
                ("Vegetables are cooked using hot steam instead of oil.", ["Steam", "Bake", "Fry", "Roast"], "Steam"),
            ]],
            write("Activity 8 – Challenge. Think of another food for each cooking method. Example: Boil → Eggs",
                  ["Grill →", "Bake →", "Steam →", "Fry →", "Roast →"], min_words=1),
            write("Activity 9 – Build the Perfect Meal. Choose one appetiser (vegetable soup, garlic bread, fresh salad), "
                  "one main course (chicken rice, vegetable noodles, grilled fish), one dessert (fruit salad, ice "
                  "cream, chocolate cake) and one drink (water, fresh juice, lemon tea).", [
                "My meal:", "Why did you choose these dishes?", "Is your meal healthy? Explain.",
                "Which dish would you recommend to a tourist visiting Sri Lanka?",
                "Would you change anything to make your meal healthier?",
            ], min_words=3),
            plain("Activity 10 – Read the Menu. Sunrise Café – Breakfast Menu\nString Hoppers & Curry — Rs. 650\n"
                  "Egg Sandwich — Rs. 580\nVegetable Rice — Rs. 750\nChicken Fried Rice — Rs. 1,150\n"
                  "Fresh Fruit Juice — Rs. 450\nTea — Rs. 180\nCoffee — Rs. 250\nFruit Salad — Rs. 550"),
            mcq("Activity 10 – Which meal is the most expensive?", ["Chicken Fried Rice", "Vegetable Rice", "String Hoppers & Curry"], "Chicken Fried Rice"),
            mcq("Activity 10 – Which drink costs the least?", ["Tea", "Coffee", "Fresh Fruit Juice"], "Tea"),
            write("Activity 10 – Answer the questions.", [
                "You have Rs. 1,300. Choose a breakfast and a drink. How much money will you have left?",
                "Which meal would you recommend to a vegetarian?",
                "Which breakfast would give you the healthiest start to the day? Explain.",
                "Which meal would you order? Why?",
            ], min_words=3),
            cat("Activity 11 – Healthy or Unhealthy? Sort each food.", {
                "Healthy": ["Fresh fruit", "Grilled chicken", "Steamed vegetables", "Brown rice", "Fresh fruit juice"],
                "Less Healthy": ["Soft drinks", "French fries", "Chocolate cake", "Fried chicken", "Potato chips"],
            }, review=True),
            write(f"Activity 11 – {DISCUSS}", [
                "Do you think it is possible to eat healthy food on a small budget?", "Which healthy food do you eat most often?",
                "What changes could people make to improve their eating habits?",
            ], min_words=5),
            examples("Useful Expressions", ["I'd like to order the grilled fish, please.", "What's today's special?",
                                            "Could I have the menu, please?", "I'm allergic to peanuts.",
                                            "Could you recommend a vegetarian dish?", "This looks delicious!"]),
            speak("Mini Speaking Challenge – A friend from another country is visiting Sri Lanka for the first time. "
                  "Recommend one traditional dish, one dessert and one drink, and say why. Use: I recommend... · You "
                  "should try... · It's made with... · It's popular because... Model:",
                  "I recommend rice and curry, because it's made with many different vegetables and spices. You should try watalappan for dessert. It's made with coconut milk and jaggery. For a drink, I recommend king coconut water. It's popular because it's fresh and healthy.",
                  seconds=60, review=True),
        ],
        "grammar": [
            heading("Review Corner"),
            plain("From Lesson 6: ✔ Passive Voice ✔ Technology and Media Vocabulary ✔ Facts vs Opinions ✔ News "
                  "Reporting ✔ Internet Safety\nExamples: The article was published yesterday. · Personal "
                  "information is protected online. · Fake news should not be shared without checking reliable sources."),
            cat("Activity 1 – Smart Consumer or Impulse Buyer?", {
                "Smart Consumer": ["Maya compares prices in three supermarkets before buying a microwave.",
                                   "Nadeesha reads customer reviews before ordering a mobile phone online.",
                                   "Sahan checks the expiry date before purchasing milk and yoghurt.",
                                   "A family prepares a shopping list before visiting the supermarket.",
                                   "A university student waits until the weekend to take advantage of a discount.",
                                   "A shopper checks whether a product has a warranty before making a purchase."],
                "Impulse Buyer": ["Kasun buys an expensive pair of shoes simply because they are popular on social media.",
                                  "Amal buys three shirts during a sale even though he only needs one.",
                                  "Dilini buys the first laptop she sees without comparing the specifications.",
                                  "A customer purchases a product because the advertisement says \"Limited Time Only!\""],
            }, review=True),
            write("Activity 1 – Follow-up. Short answers.", [
                "Which shopping habits help people save money?",
                "Have you ever bought something you didn't really need? What happened?",
                "Why do advertisements sometimes influence our decisions?",
            ], min_words=5),
            write("Activity 2 – Spending Choices. Choose the best decision and explain your reason.", [
                "Situation 1: You have Rs. 4,000. Would you buy a reference book for your studies, a fashionable T-shirt, or movie tickets and snacks? Explain.",
                "Situation 2: Your headphones stopped working. Pair A: Rs. 5,500, 2-year warranty, excellent reviews. Pair B: Rs. 4,500, no warranty, mixed reviews. Which would you choose? Why?",
                "Situation 3: Your shopping basket is already over your budget. Would you remove unnecessary items, borrow more money, buy everything anyway, or compare prices in another shop? Why?",
                "Situation 4: A supermarket advertises “Buy 2 Get 1 Free!” You only need one bottle of juice. Would you still buy three bottles? Why or why not?",
                "Situation 5: Restaurant A: Rs. 1,250, rated 4.8/5. Restaurant B: Rs. 950, rated 3.2/5. Which would you choose, and what besides price influenced you?",
            ], min_words=8),
            *[mcq(f"Activity 3 – Think Like a Smart Shopper: {s}", o, a) for s, o, a in [
                ("Before buying an expensive electronic item, I usually...", ["compare prices.", "buy it immediately.", "ignore customer reviews.", "choose the most colourful one."], "compare prices."),
                ("When I see a large discount, I should first...", ["check whether I really need the item.", "buy several products immediately.", "ignore the price completely.", "spend all my money."], "check whether I really need the item."),
                ("When shopping online, the safest thing to do is...", ["read customer reviews.", "share my bank details with anyone who asks.", "click every advertisement.", "buy from unknown websites."], "read customer reviews."),
                ("Which statement shows responsible spending?", ["\"I plan my monthly budget.\"", "\"I always spend my entire salary.\"", "\"I never compare prices.\"", "\"I buy things because my friends have them.\""], "\"I plan my monthly budget.\""),
                ("Which quality is most important when buying food?", ["Freshness", "Colourful packaging", "Expensive advertising", "Famous celebrities promoting it"], "Freshness"),
                ("A product offers good value for money when...", ["it is useful, durable and reasonably priced.", "it is the most expensive product in the shop.", "everyone else buys it.", "it has attractive packaging."], "it is useful, durable and reasonably priced."),
            ]],
            write("Activity 3 – Reflection. Think about your own shopping habits.", [
                "One thing I always compare before buying is ______.", "I sometimes waste money on ______.",
                "The next time I go shopping, I will ______.",
            ], min_words=2),
            heading("Too / Enough"),
            plain("We use too to show that something is more than necessary, more than acceptable, or more than we "
                  "want. Structure: too + adjective.\nWe use enough to show that something is sufficient. Structure: "
                  "adjective + enough, or enough + noun."),
            examples("Too", ["The bag is too heavy.", "The coffee is too hot to drink.", "The dress is too expensive for my budget."]),
            examples("Enough", ["The soup is hot enough to eat.", "This laptop is fast enough for online classes.",
                                "The restaurant is close enough to walk to.", "We have enough money to buy the groceries.",
                                "There is enough food for everyone."]),
            plain("Sinhala Help\nThe shoes are too expensive. → මෙම සපත්තු වැඩියෙන් මිල අධිකයි.\n"
                  "The tea isn't hot enough. → මෙම තේ ප්‍රමාණවත් තරම් උණු නැහැ.\n"
                  "We have enough money. → අපට ප්‍රමාණවත් මුදල් තිබෙනවා.\nThere isn't enough rice. → ප්‍රමාණවත් හාල් නැහැ."),
            plain("Common Mistakes\n❌ This phone is enough expensive. ✅ This phone is too expensive.\n"
                  "❌ The bag is enough big. ✅ The bag is big enough.\n❌ We have money enough. ✅ We have enough money.\n"
                  "Grammar Tip: Is it MORE than necessary? ➡ Use too. Is it SUFFICIENT? ➡ Use enough."),
            *[typed(f"Activity 12 – Smart Shopping Grammar. Write too or enough: {s}", [a], review=True) for s, a in [
                ("This jacket is __________ expensive for my budget.", "too"),
                ("The shopping bag isn't strong __________ to carry these groceries.", "enough"),
                ("We have __________ money to buy fresh vegetables.", "enough"),
                ("The restaurant is __________ crowded, so let's come back later.", "too"),
                ("This recipe is easy __________ for beginners.", "enough"),
                ("The tea is __________ hot to drink right now.", "too"),
                ("There isn't __________ cheese to make another pizza.", "enough"),
                ("These shoes are comfortable __________ for long walks.", "enough"),
                ("The supermarket is __________ far to walk, so we'll take the bus.", "too"),
                ("We bought __________ fruit for everyone at the picnic.", "enough"),
            ]],
            *[mcq(f"Activity 13 – Choose the Best Option. {s}", o, a, review=True) for s, o, a in [
                ("You want to buy a laptop. It costs Rs. 350,000. You only have Rs. 200,000. The laptop is...", ["enough expensive", "too expensive", "expensive enough", "enough"], "too expensive"),
                ("The soup has finished because everyone ate it. There isn't...", ["too soup", "enough soup", "soup enough", "too much enough"], "enough soup"),
                ("Your backpack can hold your books, laptop and lunch. The backpack is...", ["enough big", "too big", "big enough", "enough"], "big enough"),
                ("The noodles are still cold. They aren't...", ["hot enough", "enough hot", "too enough", "enough"], "hot enough"),
                ("The queue at the supermarket has over fifty people. The queue is...", ["enough long", "too long", "long enough", "enough"], "too long"),
                ("Your phone battery lasts two full days. The battery is...", ["too good", "good enough", "enough good", "too enough"], "good enough"),
            ]],
            *[typed(f"Activity 14 – Fix the Mistake. Rewrite correctly: {s}", a, review=True) for s, a in [
                ("This coffee is enough hot.", ["This coffee is hot enough.", "This coffee is too hot."]),
                ("The television is too small enough.", ["The television is too small.", "The television is small enough."]),
                ("We have fruits enough for everyone.", ["We have enough fruit for everyone.", "We have enough fruits for everyone."]),
                ("This restaurant is enough expensive.", ["This restaurant is too expensive.", "This restaurant is expensive enough."]),
                ("My bag isn't enough light.", ["My bag isn't light enough.", "My bag is not light enough."]),
                ("There isn't money enough.", ["There isn't enough money.", "There is not enough money."]),
                ("The classroom is too noisy enough to study.", ["The classroom is too noisy to study.", "The classroom is too noisy to study in."]),
                ("The cake is enough sweet.", ["The cake is sweet enough.", "The cake is too sweet."]),
            ]],
            *[open_answer(f"Activity 15 – Real-Life Decisions. Complete the sentence: {s}", e) for s, e in [
                ("Your suitcase weighs 35 kg. The airline allows only 25 kg. “My suitcase is ______.”", "My suitcase is too heavy."),
                ("You have Rs. 8,000. The headphones cost Rs. 7,500. “I have ______.”", "I have enough money for the headphones."),
                ("The restaurant serves very small portions. “There isn't ______.”", "There isn't enough food."),
                ("The hotel room has fast Wi-Fi, a comfortable bed and a quiet environment. “The room is ______.”", "The room is comfortable enough."),
                ("Your friend wants to cook dinner. There are only two tomatoes. “There aren't ______.”", "There aren't enough tomatoes."),
                ("The bus is completely full. “It is ______.”", "It is too crowded."),
            ]],
            plain("Activity 16 – Grammar Challenge. Complete the conversation.\nNimal: What do you think of this jacket?\n"
                  "Amaya: It's nice, but I think it's ______.\nNimal: Really? Why?\nAmaya: It costs Rs. 18,000. I don't "
                  "have ______ money today.\nNimal: What about this one?\nAmaya: It's cheaper and it's stylish ______ "
                  "for work.\nNimal: Shall we buy it?\nAmaya: Yes! I think it's good value for money."),
            typed("Activity 16 – Amaya: It's nice, but I think it's ______.", ["too expensive"], review=True),
            typed("Activity 16 – Amaya: I don't have ______ money today.", ["enough"], review=True),
            typed("Activity 16 – Amaya: It's cheaper and it's stylish ______ for work.", ["enough"], review=True),
            write("Activity 16 – Now write your own short shopping conversation (6–8 lines) between a customer and a shop "
                  "assistant, using too, enough, budget, discount and quality.", ["My conversation:"], min_words=40),
            write("Grammar in Everyday Life – Complete the sentences about yourself. Try to use too or enough in every answer.", [
                "I have ______.", "My favourite restaurant is ______ enough.", "I think online shopping is ______.",
                "My school bag is ______.", "I don't have ______.", "My hometown has ______.",
            ], min_words=3),
            write("Grammar Challenge – Look around you and write five original sentences using too or enough, about objects, "
                  "food, places, people and daily situations. Examples: My water bottle is big enough for a whole day. · "
                  "My desk is too small for all my books.", ["1.", "2.", "3.", "4.", "5."], min_words=5),
            heading("Too & Enough in Real Life"),
            plain("Too = more than necessary: The soup is too hot. · The bag is too heavy.\nEnough = sufficient: The "
                  "room is big enough. · We have enough money.\nSinhala Help: This coffee is too hot. → මෙම කෝපි එක "
                  "වැඩියෙන් උණුයි. · The pizza is big enough for two people. → මෙම පීසා එක දෙදෙනෙකුට ප්‍රමාණවත් තරම් විශාලයි."),
            *[typed(f"Activity 26 – Restaurant Conversations. Write too or enough: {s}", [a], review=True) for s, a in [
                ("Customer: The soup is ______ hot to eat right now.", "too"),
                ("Friend: Yes, I have ______ money.", "enough"),
                ("Customer: The table isn't large ______ for six people.", "enough"),
                ("Customer: Yes! It's ______ spicy for me.", "too"),
                ("Customer: No thanks. This one is strong ______.", "enough"),
            ]],
            plain("Activity 27 – Complete the Review.\n“We visited a new café yesterday. The restaurant wasn't (1) ______ "
                  "crowded, so we found a table quickly. The sandwiches were fresh (2) ______, but the coffee was (3) "
                  "______ sweet for my taste. The portions were large (4) ______ for two people to share. Overall, we "
                  "had (5) ______ time to enjoy our meal, and we would definitely visit again.”"),
            *[typed(f"Activity 27 – Blank ({n}): write too or enough.", [a], review=True) for n, a in [
                (1, "too"), (2, "enough"), (3, "too"), (4, "enough"), (5, "enough")]],
            write("Activity 28 – Smart Shopper Mission. You have Rs. 6,500 to buy ingredients for dinner: rice Rs. 1,600, "
                  "chicken Rs. 2,200, vegetables Rs. 900, fruit Rs. 850, ice cream Rs. 1,400, soft drinks Rs. 950, "
                  "bread Rs. 350. Choose your items, then answer. Try to use too and enough.", [
                "My shopping basket:", "Did you have enough money?", "Which item was too expensive?",
                "Which items were necessary?", "Which items could you buy next time?",
                "Explain why you chose your final shopping basket.",
            ], min_words=3),
        ],
        "pronunciation": [
            phrases("Listen to the audio and repeat each word.", [
                ("Consumer", "කන්සියුමර්"), ("Budget", "බජට්"), ("Receipt", "රිසීට් (the 'p' is silent)"),
                ("Warranty", "වොරන්ටි"), ("Discount", None), ("Cuisine", "ක්විසීන්"),
                ("Ingredient", "ඉන්ග්‍රීඩියන්ට්"), ("Recipe", "රෙසිපි"), ("Nutrition", "නියුට්‍රිෂන්"),
                ("Vegetarian", "වෙජිටේරියන්"), ("Affordable", "අෆෝඩබල්"), ("Bargain", "බාර්ගේන්"),
                ("Purchase", None), ("Quality", None), ("Refund", None),
            ]),
            plain("Common Pronunciation Problems\nReceipt — ❌ Re-ceipt ✅ Receipt (silent “p”)\nVegetable — ❌ "
                  "Ve-ge-ta-ble (4 syllables) ✅ Veg-ta-ble (3 syllables)\nComfortable — ❌ Com-for-ta-ble ✅ "
                  "Comf-ta-ble\nRestaurant — ❌ Res-tau-rant ✅ Res-trənt\nChocolate — ❌ Cho-co-late ✅ Choc-late\n"
                  "Word Stress: conSUMer · disCOUNT · warRANty · nuTRItion · inGREdient · afFORDable · reCIPE"),
            *[speak("Tap & Speak: say the word clearly.", w, seconds=5) for w in [
                "Consumer", "Budget", "Receipt", "Warranty", "Cuisine", "Ingredient", "Recipe", "Nutrition",
                "Vegetarian", "Affordable"]],
            *[mcq("Activity 17 – Which Word Do You Hear? Listen carefully and tap the word you hear.", o, a, listen=a)
              for o, a in [
                (["Budget", "Bargain"], "Budget"), (["Receipt", "Recipe"], "Recipe"), (["Quality", "Quantity"], "Quality"),
                (["Cuisine", "Kitchen"], "Cuisine"), (["Discount", "Customer"], "Customer"),
                (["Ingredient", "Restaurant"], "Ingredient"), (["Affordable", "Comfortable"], "Affordable"),
                (["Refund", "Receipt"], "Refund"),
            ]],
            heading("Activity 18 – Sentence Stress"),
            *[speak(f"Listen and repeat. Notice the stressed words: {s}", t, seconds=10) for s, t in [
                ("THIS jacket is TOO EXPENSIVE for me.", "This jacket is too expensive for me."),
                ("We have ENOUGH MONEY to buy fresh vegetables.", "We have enough money to buy fresh vegetables."),
                ("I'd like to COMPARE PRICES before buying.", "I'd like to compare prices before buying."),
                ("This restaurant offers GOOD VALUE FOR MONEY.", "This restaurant offers good value for money."),
                ("The recipe is EASY ENOUGH to follow.", "The recipe is easy enough to follow."),
                ("Could I have the RECEIPT, please?", "Could I have the receipt, please?"),
                ("The vegetables are FRESH ENOUGH to cook today.", "The vegetables are fresh enough to cook today."),
                ("This laptop comes with a TWO-YEAR WARRANTY.", "This laptop comes with a two-year warranty."),
            ]],
            heading("Activity 19 – Useful Shopping Expressions"),
            plain("Listen to the recording and repeat each expression aloud. Then record yourself and compare your "
                  "pronunciation with the model."),
            *[speak("Listen, repeat, then record yourself.", e, seconds=8) for e in [
                "How much does this cost?", "Is this item on sale?", "Do you have this in another colour?",
                "Can I compare these two products?", "I'd like to buy this, please.", "Can I pay by card?",
                "Could I have the receipt, please?", "Is there a warranty?", "Could I see the menu, please?",
                "What do you recommend?", "I'd like to order the grilled chicken.", "Could I have the bill, please?",
                "This dish is too spicy.", "The soup isn't hot enough.", "This meal is delicious.",
                "I'd like to try something traditional.",
            ]],
        ],
        "listening": [
            plain("LISTENING TIP\nWhen listening to conversations about shopping and food:\n✔ Listen for prices and "
                  "numbers.\n✔ Identify the speaker's purpose.\n✔ Notice opinions and recommendations.\n✔ Listen for "
                  "expressions about quantity and quality.\n✔ Pay attention to words like too and enough."),
            heading("Listening Text 1 – Shopping Within a Budget"),
            *[mcq(f"Activity 21 – {q}", o, a, listen=TEXT1, review=True) for q, o, a in [
                ("How much money did they have?", ["Rs. 5,000", "Rs. 8,000", "Rs. 10,000"], "Rs. 8,000"),
                ("Which items did they decide to buy first?", ["Snacks", "Vegetables", "Soft drinks"], "Vegetables"),
                ("Why didn't they buy the apples immediately?", ["They weren't fresh.", "They were too expensive.", "They didn't like apples."], "They were too expensive."),
                ("What did they decide to leave for next week?", ["Rice", "Eggs", "Snacks"], "Snacks"),
                ("What helped them stay within their budget?", ["Buying everything", "Comparing prices and buying only what they needed", "Borrowing money"], "Comparing prices and buying only what they needed"),
            ]],
            cat("Activity 22 – Shopping Notes. Listen again. Which items did they buy?", {
                "Bought": ["Vegetables", "Rice", "Milk", "Eggs"],
                "Not Bought": ["Apples", "Snacks"],
            }, review=True) | {"listen": TEXT1},
            write("Activity 22 – Now answer.", [
                "Why is preparing a shopping list useful?", "Have you ever bought something that wasn't on your shopping list?",
            ], min_words=5, listen=TEXT1),
            cat("Activity 23 – Budget Decisions. Do you agree or disagree?", {
                "Agree": ["Comparing prices saves money.", "A shopping list helps people avoid unnecessary purchases.",
                          "Buying only what you need is a smart habit."],
                "Disagree": ["Buying snacks is more important than buying vegetables.", "Expensive products are always better."],
            }, review=True) | {"listen": TEXT1},
            write("Activity 23 – Explain one of your answers.", ["My explanation:"], min_words=10, listen=TEXT1),
            heading("Listening Text 2 – A Restaurant Review Podcast"),
            *[mcq(f"Activity 24 – {q}", o, a, listen=TEXT2, review=True) for q, o, a in [
                ("What kind of restaurant was reviewed?", ["Fast food restaurant", "Family restaurant", "Street food stall"], "Family restaurant"),
                ("Which meal received positive comments?", ["Chicken rice", "Seafood pasta", "Pizza"], "Chicken rice"),
                ("Why wasn't the seafood pasta perfect?", ["It was cold.", "It was too salty.", "It was too small."], "It was too salty."),
                ("What did the reviewer think about the prices?", ["Very cheap", "Reasonable considering the quality", "Too low"], "Reasonable considering the quality"),
                ("Would the reviewer recommend the restaurant?", ["Yes", "No", "Not sure"], "Yes"),
            ]],
            write("Activity 25 – Restaurant Rating. Listen again. Give each category 1 to 5 stars and explain your ratings.", [
                "Food:", "Service:", "Cleanliness:", "Price:", "Atmosphere:",
            ], min_words=3, listen=TEXT2, models=[
                "4 stars — the chicken rice was delicious, but the pasta was a little too salty.",
                "5 stars — the staff were friendly and welcomed every customer.",
                "5 stars — the restaurant was clean and comfortable.",
                "3 stars — a little higher than nearby restaurants, but worth it.",
                "5 stars — relaxing, with authentic flavours.",
            ], review=True),
        ],
        "reading": [
            plain("READING TIP\nWhen reading articles about shopping and food:\n✔ Identify the writer's purpose.\n"
                  "✔ Separate facts from opinions.\n✔ Look for reasons and supporting examples.\n✔ Compare different "
                  "viewpoints.\n✔ Think about how the information relates to your own life."),
            passage("Reading Passage 1 – Why Do We Buy Things We Don't Need?", PASSAGE1,
                    "ප්‍රචාරණය සහ වට්ටම් නිසා මිනිසුන් සමහර විට අවශ්‍ය නොවන දේවල් මිලදී ගනී.\n"
                    "හොඳ පාරිභෝගිකයෙක් අයවැය සැලසුම් කර අවශ්‍ය දේ පමණක් මිලදී ගනී."),
            *[mcq(f"Activity 29 – {q}", o, a, review=True) for q, o, a in [
                ("What is impulse buying?", ["Buying because of emotions, not need", "Buying only from a list", "Buying the cheapest item"], "Buying because of emotions, not need"),
                ("Which two techniques do advertisers use to attract customers?", ["Bright colours and limited-time offers", "Long instructions and small print", "High prices and no discounts"], "Bright colours and limited-time offers"),
                ("Why has online shopping increased impulse buying?", ["You can order with just a few clicks", "Shops are always closed", "It is more expensive"], "You can order with just a few clicks"),
                ("What advice do financial experts give?", ["Make a list, set a budget and wait a day before buying expensive items", "Buy everything on sale", "Never read reviews"], "Make a list, set a budget and wait a day before buying expensive items"),
                ("According to the writer, what makes someone a smart shopper?", ["Making informed decisions about quality, value and needs", "Always buying the cheapest product", "Shopping every day"], "Making informed decisions about quality, value and needs"),
                ("Which sentence best expresses the main idea of the article?", ["Being a smart shopper means making informed decisions.", "Online shopping is always bad.", "Advertisements are illegal."], "Being a smart shopper means making informed decisions."),
            ]],
            write("Activity 29 – Your view.", [
                "Have you ever bought something you later regretted? Why?", "Do you think advertisements influence teenagers? Explain.",
            ], min_words=8),
            cat("Activity 30 – Fact or Opinion? Sort each statement.", {
                "Fact": ["Online shopping is convenient.", "Advertisements encourage consumers to buy products.",
                         "Smart shoppers compare quality before buying.", "Creating a shopping list helps people manage their spending.",
                         "Social media influences many consumers."],
                "Opinion": ["Everyone spends too much money.", "Discounts are always a good idea.", "Expensive products are always better."],
            }, review=True),
            plain("Activity 31 – Advertisement Detective.\nSUPER SALE! THIS WEEKEND ONLY!\n✔ 50% OFF selected products\n"
                  "✔ Buy 2 Get 1 FREE\n✔ Free delivery for orders above Rs. 5,000\n✔ Limited Stock Available!\n"
                  "Don't Miss Out! Shop Today!"),
            write("Activity 31 – Answer the questions.", [
                "Which words are designed to attract customers?", "Which offer interests you most?",
                "Would this advertisement encourage you to buy something? Why?",
                "What information is missing from the advertisement?", "Should consumers believe every advertisement? Explain.",
            ], min_words=4),
            passage("Reading Passage 2 – Traditional Food or Fast Food?", PASSAGE2,
                    "සාම්ප්‍රදායික ආහාර සහ ක්ෂණික ආහාර දෙකටම වාසි සහ අවාසි ඇත.\nසෞඛ්‍ය සම්පන්න ජීවිතයක් සඳහා සමබර ආහාර වේලක් වැදගත් වේ."),
            cat("Activity 32 – Compare the Ideas. Sort each idea from the passage.", {
                "Traditional Food": ["Fresh ingredients", "Recipes passed down through generations", "Takes more time to prepare", "Richer in nutrients"],
                "Fast Food": ["Convenient and quick", "Saves time", "May cause health problems if eaten daily"],
            }, review=True),
            write("Activity 32 – Now answer.", [
                "Which type of food do you prefer?", "Why do many people choose fast food?",
                "What healthier choices are available today?", "How can people maintain a balanced diet?",
            ], min_words=5),
        ],
        "speaking": [
            heading("Activity 20 – Mini Role Play"),
            plain("Listen to the other speaker's lines and respond by recording your own. Use at least four "
                  "expressions from the lesson."),
            heading("Situation A — At a Supermarket (you are the customer; the app is the shop assistant)"),
            *_role_play(SUPERMARKET),
            heading("Situation B — At a Restaurant (you are ordering dinner; the app is the waiter or waitress)"),
            *_role_play(RESTAURANT),
            heading("Situation C — Shopping for a Gift (the app helps you compare two products)"),
            *_role_play(GIFT),
            heading("Activity 33 – Restaurant Role Play"),
            plain("Imagine you are dining at a restaurant. The app plays the waiter or waitress. Listen to each prompt "
                  "and record your responses using polite expressions: ask for the menu, order food, ask about "
                  "ingredients, respond to a recommendation and ask for the bill."),
            *_role_play(RESTAURANT_2),
            heading("Activity 34 – Budget Challenge"),
            speak("You have Rs. 4,000 to prepare lunch for four people. What would you buy? Which foods are essential? "
                  "Which are too expensive? How can you stay within your budget? Present your final shopping plan. Model:",
                  "With Rs. 4,000, I would buy rice, vegetables, eggs and some fruit. Rice and vegetables are essential. Chicken is too expensive today, so I would use eggs instead. To stay within my budget, I would make a list and compare prices before buying.",
                  seconds=60, review=True),
            heading("Activity 35 – Food Culture Discussion"),
            speak("Choose one topic: A – Should schools encourage students to eat healthier food? B – Are traditional Sri "
                  "Lankan meals healthier than fast food? C – Should supermarkets reduce plastic packaging? Give your "
                  "opinion, two reasons, one example and a conclusion. Model:",
                  "In my opinion, traditional Sri Lankan meals are healthier than fast food. First, they use fresh vegetables and spices. Second, they are usually not fried. For example, rice and curry with dhal and green leaves gives us many nutrients. In conclusion, we should eat traditional food more often.",
                  seconds=60, review=True),
        ],
        "writing": [
            write("Activity 36 – Recipe Writing. Write a recipe for one of your favourite dishes. Include the name, "
                  "ingredients, cooking method, step-by-step instructions and a serving suggestion. Use First, Next, "
                  "Then, After that, Finally.", [
                "Name of the dish:", "Ingredients:", "Cooking method:", "Step-by-step instructions:", "Serving suggestion:",
            ], min_words=2),
            write("Activity 37 – Consumer Advice. Your younger cousin spends money carelessly and buys many unnecessary "
                  "things online. Write a short advice article (150–180 words) on why budgeting is important, tips for "
                  "saving money, shopping wisely and avoiding impulse buying. Use: You should... · It's important to... "
                  "· Don't forget to... · Always...", ["My article:"], min_words=150),
            write("Activity 38 – Restaurant Review. Write a review (150–180 words) of your favourite restaurant: its name, "
                  "atmosphere, food quality, service, prices, and whether you would recommend it. Use too and enough "
                  "where appropriate.", ["My review:"], min_words=150),
            write("SMART SHOPPER CHALLENGE – FINAL MISSION. You have Rs. 10,000 to organise a healthy family dinner.", [
                "Mission 1 – Plan Your Shopping: list the ingredients you need.",
                "Mission 2 – Stay Within Your Budget: explain how you decided what to buy and what not to buy.",
                "Mission 3 – Prepare the Menu: one appetiser, one main course, one dessert, one drink.",
                "Mission 4 – Write a Recommendation: why is your meal healthy, affordable and good value for money?",
                "Mission 5 – Reflection: “Being a smart consumer means...” Give at least three reasons from the lesson.",
            ], min_words=10),
            self_check(
                "□ I can discuss shopping habits confidently.\n□ I can compare products before buying.\n"
                "□ I can use too and enough correctly.\n□ I can understand advertisements and shopping information.\n"
                "□ I can describe cooking methods and recipes.\n□ I can order food politely in a restaurant.\n"
                "□ I can discuss healthy eating and budgeting.\n□ I can write a recipe and a restaurant review.\n"
                "□ I can make informed consumer decisions.\n"
                "□ I can communicate confidently in shopping and food-related situations.",
                prompt="Self-assessment",
            ),
            summary(["Too and enough", "Shopping and consumer vocabulary", "Food and cooking methods",
                     "Ordering in a restaurant", "Budgeting and smart shopping"]),
        ],
    },
}
