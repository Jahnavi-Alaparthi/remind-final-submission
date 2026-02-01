import streamlit as st
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")


client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash"
HISTORY_FILE = "question_history_11_2.json"

# Base intervals per level (in minutes)
BASE_INTERVALS = {1: 10, 2: 30, 3: 60, 4: 180, 5: 360}


if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r") as f:
        question_history = json.load(f)
else:
    question_history = {}

def save_history():
    with open(HISTORY_FILE, "w") as f:
        json.dump(question_history, f, indent=4)



def get_due_questions():
    due = []
    now = datetime.now()
    for q, info in question_history.items():
        last = datetime.fromisoformat(info["last_reviewed"])
        interval = info.get("interval", BASE_INTERVALS.get(info["level"], 30))
        if now >= last + timedelta(minutes=interval):
            due.append(q)
    return due

# Call Gemini to get an answer
def get_gemini_answer(prompt_text):
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[types.Content(role="user", parts=[types.Part(text=prompt_text)])]
    )
    return response.text.strip()


def calculate_interval(level):
    return BASE_INTERVALS.get(level, 30)


st.title("Spaced repetition chatbot")

mode = st.radio("Mode", ["Ask a Question", "Take Quiz"])

if mode == "Ask a Question":
    user_question = st.text_input("Enter your question here:")

    if st.button("Get Answer"):
        if user_question:
            # Get bot answer
            bot_answer = get_gemini_answer(user_question)
            st.markdown(f"**Bot:** {bot_answer}")

            # Store question if new
            if user_question not in question_history:
                question_history[user_question] = {
                    "level": 1,
                    "interval": BASE_INTERVALS[1],
                    "last_reviewed": datetime.now().isoformat()
                }
            else:
                # Reset last_reviewed so next quiz is spaced
                question_history[user_question]["last_reviewed"] = datetime.now().isoformat()

            save_history()

elif mode == "Take Quiz":
    due_questions = get_due_questions()
    if not due_questions:
        st.write("No questions are due for review right now.")
    else:
        for q in due_questions:
            info = question_history[q]
            st.markdown(f"**Review Question:** {q}")

            user_answer = st.text_input(f"Your answer for: {q}", key=q)

            if st.button(f"Submit Answer for: {q}", key=f"btn_{q}"):
                correct_answer = get_gemini_answer(q).lower().strip()
                user_ans_lower = user_answer.lower().strip()

                if user_ans_lower == correct_answer:
                    st.success("Correct!")
                    info["level"] = min(info["level"] + 1, 5)
                else:
                    st.error(f"Incorrect! Correct answer: {correct_answer}")
                    info["level"] = max(info["level"] - 1, 1)

                # Update review timing
                info["interval"] = calculate_interval(info["level"])
                info["last_reviewed"] = datetime.now().isoformat()

                question_history[q] = info
                save_history()
