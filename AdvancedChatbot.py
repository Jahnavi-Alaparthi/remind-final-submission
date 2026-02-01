import streamlit as st
import json, os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.5-flash"
DATA_FILE = "memory_11_3.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def review_time(item):
    base = {1: 20, 2: 90, 3: 360, 4: 1440}
    return datetime.fromisoformat(item["last_seen"]) + timedelta(
        minutes=base[item["level"]] / item["forgetting_speed"]
    )

memory = load_data()

st.title("🧠 Advanced Chatbot")

question = st.chat_input("Ask a question")

if question:
    with st.chat_message("user"):
        st.markdown(question)

    response = client.models.generate_content(
        model=MODEL,
        contents=[types.Content(
            role="user",
            parts=[types.Part(text=question)]
        )]
    )

    answer = response.text

    with st.chat_message("assistant"):
        st.markdown(answer)

    memory.append({
        "question": question,
        "level": 1,
        "memory_strength": 0.5,
        "forgetting_speed": 1.0,
        "last_seen": datetime.now().isoformat()
    })

    save_data(memory)

# ---------- QUIZ SELECTION ----------
due = [q for q in memory if datetime.now() >= review_time(q)]

if due:
    st.divider()
    st.subheader("📝 Quick Quiz")

    quiz = sorted(
        due,
        key=lambda x: (x["memory_strength"], x["level"])
    )[0]

    st.markdown(f"**Question:** {quiz['question']}")
    user_ans = st.text_input("Your answer", key="quiz_ans")

    if user_ans and st.button("Submit Answer"):
        eval_prompt = f"""
Question: {quiz['question']}
Student Answer: {user_ans}

Respond with:
Correct or Incorrect.
One-line explanation.
"""

        evaluation = client.models.generate_content(
            model=MODEL,
            contents=[types.Content(
                role="user",
                parts=[types.Part(text=eval_prompt)]
            )]
        ).text

        st.markdown(evaluation)

        if evaluation.lower().startswith("correct"):
            quiz["memory_strength"] = min(1.0, quiz["memory_strength"] + 0.25)
            quiz["forgetting_speed"] = max(0.5, quiz["forgetting_speed"] - 0.15)
            quiz["level"] = min(quiz["level"] + 1, 4)
        else:
            quiz["memory_strength"] = max(0.1, quiz["memory_strength"] - 0.35)
            quiz["forgetting_speed"] += 0.25
            quiz["level"] = max(1, quiz["level"] - 1)

        quiz["last_seen"] = datetime.now().isoformat()
        save_data(memory)


with st.expander("📂 Memory State"):
    st.json(memory)
