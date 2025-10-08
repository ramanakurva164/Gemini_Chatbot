import streamlit as st
import google.generativeai as genai
import os
import requests

# --------------------------
# API keys
# --------------------------
GENIE_API_KEY = os.getenv("GEMINI_API_KEY")
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
genai.configure(api_key=GENIE_API_KEY)

# Load Gemini model
model = genai.GenerativeModel("gemini-2.0-flash-lite")

# --------------------------
# Streamlit page settings & CSS
# --------------------------
st.set_page_config(page_title="FlavorFussion Assistant", page_icon="🤖", layout="wide")

st.markdown(
    """
    <style>
    .chat-message { max-width: 75%; padding: 12px 16px; margin: 10px 0; border-radius: 12px; font-size: 16px; line-height: 1.5; display: inline-block; word-break: break-word; }
    .user-container { display: flex; justify-content: flex-end; }
    .user-message { background-color: #2563eb; color: white; text-align: right; }
    .ai-container { display: flex; justify-content: flex-start; }
    .ai-message { background-color: #f3f4f6; color: #111827; text-align: left; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🤖 FlavorFussion Assistant")

# --------------------------
# Session state
# --------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "ai", "content": "👋 Hi! I'm your FlavorFussion Assistant. I can help you explore cuisines and dishes. Try asking: 'Show me Indian dishes', or 'What cuisines do you have?' "}
    ]

# --------------------------
# Function: fetch dishes from Spoonacular
# --------------------------
def fetch_dishes(cuisine, number=5):
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {"query": cuisine, "number": number, "apiKey": SPOONACULAR_API_KEY}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        dishes = [{"name": d["title"], "image": d["image"]} for d in data.get("results", [])]
        return dishes
    except:
        return []

# --------------------------
# Show chat history
# --------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-container"><div class="chat-message user-message">{msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-container"><div class="chat-message ai-message">{msg["content"]}</div></div>', unsafe_allow_html=True)

# --------------------------
# User input
# --------------------------
user_input = st.chat_input("Ask me about dishes or cuisines...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()

# --------------------------
# Generate reply
# --------------------------
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_msg = st.session_state.messages[-1]["content"]

    # --- Simple keyword detection for cuisines ---
    cuisines = ["indian", "italian", "mexican", "chinese", "japanese", "french"]
    found_cuisine = None
    for cuisine in cuisines:
        if cuisine.lower() in last_msg.lower():
            found_cuisine = cuisine
            break

    if found_cuisine:
        # Fetch dishes from Spoonacular
        dishes = fetch_dishes(found_cuisine)
        if dishes:
            content = f"Here are some **{found_cuisine.title()} dishes**:\n"
            for d in dishes:
                content += f"- {d['name']}\n"
            st.session_state.messages.append({"role": "ai", "content": content})
            
            # Show images inline
            for d in dishes:
                st.image(d["image"], caption=d["name"], width=200)
        else:
            st.session_state.messages.append({"role": "ai", "content": f"Sorry, I couldn't fetch {found_cuisine.title()} dishes right now."})
        st.rerun()

    else:
        # --- Fallback: Gemini for general site-related questions ---
        system_prompt = (
            "You are FlavorFussion Assistant. "
            "Help users explore the website. "
            "Talk about cuisines, dishes, and site features. "
            "Do not answer unrelated questions."
        )
        chat_history = [
            {"role": "user", "parts": [m["content"]]} if m["role"] == "user"
            else {"role": "model", "parts": [m["content"]]}
            for m in st.session_state.messages
        ]
        try:
            response = model.generate_content(chat_history)
            ai_reply = response.text
        except Exception as e:
            ai_reply = f"⚠️ Error: {e}"

        st.session_state.messages.append({"role": "ai", "content": ai_reply})
        st.rerun()
