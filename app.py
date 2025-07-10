import streamlit as st

import google.generativeai as genai

# Load environment variables

# Optional: Use os.getenv or hardcoded key
 
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# Initialize Gemini model
# model = genai.GenerativeModel("gemini-1.5-flash")
model = genai.GenerativeModel("gemini-2.0-flash-lite")

# Streamlit page config
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="wide")

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
        float: right;
    }
    .ai {
        background-color: #f3f4f6;
        color: #22223b;
        margin-right: auto;
        float: left;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🤖 Gemini Chatbot")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    css_class = "user" if msg["role"] == "user" else "ai"
    st.markdown(f'<div class="stChatMessage {css_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# User input
user_input = st.chat_input("Type your message and press Enter", key="input")

if user_input:
    # Add user message to history and rerun immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()

# If the last message is from the user, generate bot reply
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    chat_history = [
        {"role": "user", "parts": [msg["content"]]} if msg["role"] == "user"
        else {"role": "model", "parts": [msg["content"]]}
        for msg in st.session_state.messages
    ]
    try:
        response = model.generate_content(chat_history)
        ai_response = response.text
    except Exception as e:
        ai_response = f"⚠️ Error: {e}"
    st.session_state.messages.append({"role": "ai", "content": ai_response})
    st.rerun()

# List available models for debugging
try:
    models = genai.list_models()
    for m in models:
        print(m)
except Exception as e:
    print(f"Error listing models: {e}")

