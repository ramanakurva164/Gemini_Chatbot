import streamlit as st
import google.generativeai as genai

# ✅ Configure Gemini API
api_key = st.secrets["GEMINI_API_KEY"]  # or use st.secrets or os.getenv
genai.configure(api_key=api_key)

# ✅ Load Gemini model (You can also use: "gemini-1.5-flash" or "gemini-pro")
model = genai.GenerativeModel("gemini-2.0-flash-lite")

# ✅ Set Streamlit Page Config
st.set_page_config(page_title="🤖 Agent Ramana", page_icon="🤖", layout="wide")

# ✅ Add basic CSS for style
st.markdown(
    """
    <style>
    .stChatMessage {
        display: inline-block;
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        max-width: 70%;
        word-break: break-word;
    }
    .user {
        background-color: #2563eb;
        color: #fff;
        text-align: right;
        margin-left: auto;
    }
    .ai {
        background-color: #f3f4f6;
        color: #22223b;
        text-align: left;
        margin-right: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🤖 Agent Ramana")

# ✅ Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "ai",
            "content": (
                "Hey, I'm Ramana — your friendly personal companion 🤗. "
                "You can share anything with me — your thoughts, dreams, problems, or just chat casually. "
                "I'm always here to listen and talk like a friend 💬"
            )
        }
    ]

# ✅ Display previous messages
for msg in st.session_state.messages:
    css_class = "user" if msg["role"] == "user" else "ai"
    st.markdown(f'<div class="stChatMessage {css_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# ✅ User input
user_input = st.chat_input("Type your message and press Enter", key="input")

# ✅ Handle new user message
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()

# ✅ Generate Gemini response only if last message is from user
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    # Format history for Gemini
    chat_history = []
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            chat_history.append({"role": "user", "parts": [msg["content"]]})
        else:
            chat_history.append({"role": "model", "parts": [msg["content"]]})

    # Get Gemini's reply
    try:
        response = model.generate_content(chat_history)
        ai_response = response.text
    except Exception as e:
        ai_response = f"⚠️ Error: {e}"

    # Store response
    st.session_state.messages.append({"role": "ai", "content": ai_response})
    st.rerun()
