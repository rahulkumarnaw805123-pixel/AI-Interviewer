import os
import re
import time
from dotenv import load_dotenv
from google import genai
from ai.offline_ai import evaluate_offline

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Primary + Backup Models
MODELS = [
    "models/gemini-3.5-flash",
    "models/gemini-3.1-flash-lite",
    "models/gemini-flash-lite-latest"
]


# ---------------- OFFLINE AI ----------------

def offline_evaluation(question, answer):

    answer = answer.lower()

    keywords = {
        "variable": ["memory", "store", "value", "data", "name"],
        "list": ["ordered", "mutable", "collection"],
        "tuple": ["ordered", "immutable"],
        "dictionary": ["key", "value"],
        "sql": ["database", "query"],
        "select": ["retrieve", "data"],
        "where": ["condition", "filter"],
        "group by": ["group"],
        "having": ["group", "aggregate"],
        "join": ["table"],
        "excel": ["spreadsheet"],
        "data analysis": ["clean", "transform", "analyze", "visualize"]
    }

    score = 5

    for topic, words in keywords.items():
        if topic in question.lower():
            matches = sum(1 for w in words if w in answer)
            score += matches

    if score > 10:
        score = 10

    return f"""
Score: {score}/10

Feedback:

Offline AI Evaluation was used because the online AI service was unavailable.

Your answer covers some important points.
Try adding more technical details and examples for a stronger interview response.

Correct Answer:

Please retry later for a detailed AI-generated answer.
"""


# ---------------- GEMINI ----------------

def ask_gemini(subject, question, answer):

    prompt = f"""
You are an expert technical interviewer.

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer fairly.

Rules:

1. Don't deduct marks for wording.
2. Give score out of 10.
3. Explain strengths.
4. Explain missing points.
5. Give ideal answer.

Return exactly like this.

Score: X/10

Feedback:
...

Correct Answer:
...
"""

    for model_name in MODELS:

        for attempt in range(3):

            try:

                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )

                return response.text

            except Exception as e:

                error = str(e)

                # Server Busy
                if "503" in error or "UNAVAILABLE" in error:
                    time.sleep(5)
                    continue

                # Quota Exceeded
                elif "429" in error or "RESOURCE_EXHAUSTED" in error:
                    break

                # Model Not Found
                elif "404" in error:
                    break

                else:
                    break

    # ✅ All Gemini models failed → Offline AI
    return evaluate_offline(
    subject,
    question,
    answer
)
