import streamlit as st
import random

# Page config
st.set_page_config(page_title="Health Buddy AI", page_icon="💬")

# Sidebar – Customization
with st.sidebar:
    st.header("🎨 Customize Your Buddy")
    ai_name = st.text_input("AI Name", value="Health Buddy")
    ai_personality = st.selectbox("Personality Style", ["Friendly", "Encouraging", "Playful", "Professional"])

# Page Title
st.title(f"💬 {ai_name}")
st.info("🧘 This is a private, judgement-free space. Ask me anything — I'm here to help!")

# Session State Setup
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "new_message" not in st.session_state:
    st.session_state.new_message = ""

# Chatbot Logic with Personality + High-Risk Detection + Navigation Support
def get_bot_reply(user_input):
    user_input_lower = user_input.lower()

    high_risk_keywords = ["suicide", "kill myself", "end it all", "self harm", "can't go on", "overdose", "hopeless"]
    mental_keywords = ["anxious", "depressed", "stress", "sad", "lonely", "panic", "burnout","anxiety"]
    physical_keywords = ["fever", "headache", "sore throat", "vomit", "nausea", "cough", "flu", "tired", "rash", "fatigue", "back pain"]
    navigation_keywords = ["programme", "navigate", "app", "find", "book", "appointment", "menu", "feature", "section"]

    # Store user intent between messages (for navigation)
    if "awaiting_navigation_detail" not in st.session_state:
        st.session_state.awaiting_navigation_detail = False

    # 1. High-risk: comfort → suggest consult
    if any(k in user_input_lower for k in high_risk_keywords):
        return (
            "\nI'm really sorry you're feeling this way 💚 You're not alone — I'm here for you.\n\n"
            "\nThis might be something that needs a little more support than I can give.\n"
            "\nWould you like to book a *virtual* or *in-person* consultation with a healthcare professional through the app?\n"
            "\nJust go to **Health Services → Appointments** to start.\n"
            "\n Dont worry your data will not be shared <3\n"
            "\n Our 24/7 virtual and/or in-person consultation will be able to provide you with professional help :)\n"
        )

    # 2. Navigation flow — Step 1: Detect general navigation query
    if any(k in user_input_lower for k in navigation_keywords) or st.session_state.awaiting_navigation_detail:
        if not st.session_state.awaiting_navigation_detail:
            st.session_state.awaiting_navigation_detail = True
            return "Sure! Which feature or part of the app do you need help navigating?"

        # Step 2: Handle user reply
        st.session_state.awaiting_navigation_detail = False
        if "consult" in user_input_lower or "book" in user_input_lower:
            return (
                "You can book a consult by going to **Health Services → Appointments**. "
                "Choose 'Virtual' or 'In-Person' based on your preference. Let me know if you need help deciding!"
            )
        elif "programme" in user_input_lower or "events" in user_input_lower:
            return (
                "To explore programmes, tap **Wellness** in the main menu. You’ll see upcoming events and workshops there!"
            )
        else:
            return (
                "Got it! Try going to the main menu, then select the tab that matches what you're looking for. "
                "Let me know if you need help finding something specific."
            )

    if "high fever" in user_input_lower:
        return (
           "Hey, I see you've been having a high fever for a while. That sounds really uncomfortable, and I'm here to support you.\n"
           "\nHigh fevers can feel scary and exhausting. You're doing the right thing by reaching out and paying attention to your body. \n"
           "\nLet's try to understand more about what's going on, and I’ll guide you based on your symptoms.\n"
            "\n🔎 Can you tell me a bit more?\n"
            "\nTo help better, could you answer a few quick questions:\n"
            "\nHow high is the fever? (e.g., above 38°C / 100.4°F?)\n"

            "\nHow long has it been ongoing? (e.g., more than 2 days?)\n"
            "\nAny other symptoms? (e.g., sore throat, cough, rash, body aches, vomiting, difficulty breathing?)\n"
            "\nHave you taken anything? (e.g., Panadol, ibuprofen, antibiotics?)\n"

            "\nAny recent travel, exposure to sick people, or medical conditions?\n"
        )
    if "wont go away" in user_input_lower:
        return(
            "\n🧭 Based on what you said so far (high fever that won’t go away):\n"
            "\nHere’s some general guidance:\n"
            "\n✅ You can try for now:\n"
            "\nStay hydrated: Fever dehydrates the body fast. Drink water, isotonic drinks, or warm fluids regularly.\n"

            "\nTake fever-reducing medication: If not already, you can take Paracetamol (Panadol) every 4–6 hours as needed (but not more than 4 times a day).\n"

            "\nRest: Your body needs full rest to fight off infection.\n"

            "\nCool down: Light clothing, a fan, or a lukewarm sponge bath can help regulate body temperature.\n"

            "\n🚩 But please be alert for these signs:\n"
            "\nIf you have any of the following, please consider seeking medical help promptly:\n"

            "\nFever above 39.5°C (103°F) consistently\n"

            "\nFever lasting more than 48–72 hours\n"

            "\nSevere sore throat, chest pain, or trouble breathing\n"

            "\nConfusion, dizziness, or a persistent headache\n"

            "\nRash or neck stiffness\n"

            "\nNot eating/drinking at all or vomiting everything\n"
        )
    # 3. Physical health symptoms (realistic advice)
    if any(k in user_input_lower for k in physical_keywords):
        return (
            "Thanks for sharing. For these symptoms:\n"
            "\n- Stay hydrated and rest\n"
            "\n- Monitor your symptoms for 48 hours\n"
            "\n- Take paracetamol if you have a fever\n\n"
            "If things don’t improve after 2–3 days, it’s best to book a consult through the app.\n"
            "(Health Info from: HealthHub SG)"
        )

    # 4. Mental health support
    if any(k in user_input_lower for k in mental_keywords):
        if ai_personality == "Friendly":
            return random.choice([
                "That sounds really heavy. Want to take a moment and try a breathing exercise together?",
                "You’re not alone — talking about this is already a strong first step 💚",
                "Sometimes journaling or even just naming your feeling helps. Want a simple tip?"
            ])
        elif ai_personality == "Encouraging":
            return random.choice([
                "You’ve taken a strong first step. Let’s keep going, one breath at a time 💪",
                "That took courage. I'm here to walk through it with you 💚",
                "Let’s find something today that makes you feel a little lighter 🌈"
            ])
        elif ai_personality == "Playful":
            return random.choice([
                "You sound low — want to try a 3-min feel-good dance challenge? 🕺",
                "Feeling bleh? I prescribe memes, naps, and snacks 🍕🧸",
                "Mood = 🫠 but you're still showing up. That’s kinda amazing"
            ])
        elif ai_personality == "Professional":
            return random.choice([
                "Acknowledged. You may benefit from journaling and a mindfulness exercise. Would you like guidance?",
                "Consider logging your thoughts or speaking to a professional if symptoms persist.",
                "Mental health is just as important as physical health. Let me know how I can assist further."
            ])
    


    # 5. Catch-all fallback
    return random.choice([
        "I'm here to listen, guide, or just chat. What would help you right now?",
        "Need help with your health, emotions, or navigating the app? I’ve got you.",
        "You can talk to me about anything — this is a safe and private space 🌱"
    ])
 



    # 4. Health advice (verified tone)
    if any(k in user_input for k in physical_keywords):
        return (
            "🩺 That sounds like a common symptom. Here's general advice:\n"
            "- Stay hydrated\n"
            "- Get 7–9 hours of rest\n"
            "- Monitor temperature and symptoms\n\n"
            "If symptoms last >3 days or worsen, consult a doctor. (Source: HealthHub SG)"
        )

    # 5. Default casual check-ins (judgment-free tone)
    if ai_personality == "Friendly":
        return random.choice([
            "Hey hey 👋 How’s your head and heart today?",
            "Just checking in. Want to chat, get tips, or chill a bit?",
            "I’m here if you want to talk — no pressure 💕"
        ])
    elif ai_personality == "Encouraging":
        return random.choice([
            "Let’s focus on what you *can* do today. Tiny steps 💪",
            "One moment at a time. I believe in you 🌈",
            "You got this. Want to start with a small goal?"
        ])
    elif ai_personality == "Playful":
        return random.choice([
            "Wanna talk about life or why socks disappear in the dryer? 🧦",
            "Drop your feels here 🫠 I’m your emotional trash bin 🗑️❤️",
            "Rawr 🐉 What’s got you spiraling today?"
        ])
    elif ai_personality == "Professional":
        return (
            "Feel free to ask me anything — health, mental wellbeing, or how to use the app. I’ll do my best to assist."
        )

    # Just in case fallback
    return "I'm here for anything you need. Ask me about health, mood, or using the app!"
    user_input = user_input.lower()

    high_risk_keywords = ["suicide", "kill myself", "end it all", "chest pain", "shortness of breath", "can't breathe", "severe", "overdose", "fainted"]
    mental_keywords = ["anxious", "depressed", "stress", "sad", "lonely", "tired", "panic"]
    physical_keywords = ["headache", "fever", "pain", "cough", "sore", "cold", "throat", "nausea", "dizzy", "vomit"]
    navigation_keywords = ["programme", "navigate", "app", "find", "book", "appointment", "menu", "service"]

    # High-risk handling
    if any(keyword in user_input for keyword in high_risk_keywords):
        return (
            "⚠️ I'm really concerned about what you've shared. "
            "Please speak to a doctor or mental health professional immediately.\n\n"
            "[🚨 Click here for 24/7 support (SOS SG)](https://www.sos.org.sg/)"
        )

    # Navigation
    if any(keyword in user_input for keyword in navigation_keywords):
        return (
            "To explore programmes, tap on the 'Services' tab in the main menu. "
            "To book a virtual consult, go to 'Appointments' → 'Schedule'. Let me know if you need a walkthrough!"
        )

    # Mental health
    if any(keyword in user_input for keyword in mental_keywords):
        responses = {
            "Friendly": [
                "That sounds rough. Try deep breathing or a short break. Want a grounding tip?",
                "You're not alone. Want to chat more about it?",
                "I’m here to listen. Let's figure this out together 💚"
            ],
            "Encouraging": [
                "You’re doing better than you think. One step at a time, okay?",
                "Proud of you for opening up. Let’s keep going 💪",
                "It’s okay to feel this way. Want a motivational quote?"
            ],
            "Playful": [
                "Big feelings detected 🥺 Wanna smash a stress ball or something?",
                "Let’s get through this — with snacks, memes, and naps?",
                "Scream into a pillow then tell me how you're doing 😅"
            ],
            "Professional": [
                "It may help to log your thoughts and establish a routine. Would you like a resource?",
                "Mental fatigue is real. Prioritize rest and talk to a counsellor if it persists.",
                "Noted. I recommend tracking your mood and exploring mindfulness exercises."
            ]
        }
        return random.choice(responses[ai_personality])

    # Physical symptoms
    if any(keyword in user_input for keyword in physical_keywords):
        return (
            "Your symptoms may be mild. Rest, hydrate, and monitor for 48 hours. "
            "If symptoms worsen or persist, consult a GP. (Source: HealthHub SG)"
        )

    # Default fallback
    generic_responses = {
        "Friendly": [
            "Hey, I’m here for you 😊",
            "Thanks for sharing. Want advice or just someone to listen?",
            "Tell me more whenever you’re ready!"
        ],
        "Encouraging": [
            "You're doing your best and that’s enough 💛",
            "Let’s tackle this together — one small win at a time!",
            "Keep going! You’re stronger than you think."
        ],

        "Professional": [
            "Please describe your concern so I can guide you appropriately.",
            "Understood. Would you like me to provide advice or navigation support?",
            "Acknowledged. Feel free to ask a health or mental wellness question."
        ]
    }
    return random.choice(generic_responses[ai_personality])

# Styling
st.markdown("""
    <style>
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main {
            background-color: #e8f5e9;
        }
        .chat-container {
            font-family: 'Segoe UI', sans-serif;
        }
        .user-bubble {
            text-align: right;
            background-color: whitesmoke;
            color: black;
            padding: 10px;
            border-radius: 12px;
            margin: 6px 0;
            width: fit-content;
            float: right;
            clear: both;
        }
        .bot-bubble {
            text-align: left;
            background-color: white;
            color: black;
            padding: 10px;
            border-radius: 12px;
            margin: 6px 0;
            width: fit-content;
            float: left;
            clear: both;
        }
    </style>
""", unsafe_allow_html=True)

# Display chat history
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for sender, msg in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"<div class='user-bubble'>{msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-bubble'><strong>{ai_name}:</strong> {msg}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# Input Form
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", key="input_text", placeholder="Type your message here...")
    submitted = st.form_submit_button("Send")
    if submitted and user_input.strip() != "":
        st.session_state.chat_history.append(("You", user_input))
        reply = get_bot_reply(user_input)
        st.session_state.chat_history.append((ai_name, reply))
        st.rerun()

st.caption("⚠️ This chatbot is for general wellness support only. It does not provide medical advice.")
