"""app.py - Streamlit chatbot UI. Run with: streamlit run app.py"""
import streamlit as st

from ai import new_chat, chat_ai_safe

st.set_page_config(page_title="My AI Chatbot", page_icon="🤖")
st.title("🤖 My AI Chatbot")
st.caption("Powered by the Gemini API")

# Streamlit re-runs this script on every interaction,
# so we keep the chat and messages in session_state.
if "chat" not in st.session_state:
    st.session_state.chat = new_chat()
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("Options")
    if st.button("🗑️ New conversation"):
        st.session_state.chat = new_chat()
        st.session_state.messages = []
        st.rerun()

# Show the conversation so far
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box at the bottom
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = chat_ai_safe(st.session_state.chat, prompt)
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})