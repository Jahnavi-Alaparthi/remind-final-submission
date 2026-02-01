import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL = "gemini-2.5-flash"
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.title("🧠 Socratic Tutor")

if "chat" not in st.session_state:
    st.session_state.chat = []


for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask a question...")

if user_input:
 
    st.session_state.chat.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    prompt = f"""
    You are a Socratic tutor.
    Respond only with guiding questions.
    Do not give direct answers.

    User question:
    {user_input}
    """

    response = client.models.generate_content(
        model=MODEL,
        contents=[types.Content(role="user", parts=[types.Part(text=prompt)])]
    )

    st.session_state.chat.append(
        {"role": "assistant", "content": response.text}
    )
    with st.chat_message("assistant"):
        st.markdown(response.text)
