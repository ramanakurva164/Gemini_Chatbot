import streamlit as st

st.set_page_config(page_title="Welcome to Agent Ramana", layout="centered")

st.title("👋 Welcome to Agent Ramana")

# Embed the Spline scene
spline_url = (
    "https://my.spline.design/community/file/"
    "8cfb6748‑f3dd‑44dd‑89fb‑f46c7ab4186e/"
)
st.markdown(
    f'''
    <iframe src="{spline_url}" frameborder="0" width="100%" height="500px" allowfullscreen></iframe>
    ''',
    unsafe_allow_html=True
)

st.markdown(
    """
    ### Meet Ramana
    Your friendly AI companion 🤖

    Ready to chat? Tap the button below to begin.
    """
)

if st.button("💬 Start Chatting"):
    st.switch_page("app.py")
