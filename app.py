import streamlit as st
from chatbot import chatbot_response

st.set_page_config(page_title="Chatbot do Edu 🤖", page_icon="💬")
st.title("🤖 Chatbot Inteligente do Edu")
st.write("Converse comigo! Pergunte qualquer coisa 👇")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Você:", "")

if user_input:
    response = chatbot_response(user_input)
    st.session_state.history.append(("Você", user_input))
    st.session_state.history.append(("Bot", response))

for speaker, text in st.session_state.history:
    st.markdown(f"**{speaker}:** {text}")