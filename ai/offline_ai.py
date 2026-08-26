import json
import os


def evaluate_offline(subject, question, answer):

    # Subject -> File Mapping
    subject_files = {
        "Python": "python.json",
        "SQL": "sql.json",
        "Data Analyst": "data_analyst.json",
        "Data Science": "data_science.json",
        "Software Engineering": "software_engineering.json",
        "Cyber Security": "cyber_security.json"
    }

    filename = subject_files.get(subject)

    if filename is None:
        return f"""
Score: 0/10

Feedback:
Offline AI does not support this subject.

Correct Answer:
Not Available.
"""

    json_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        filename
    )

    with open(json_path, "r", encoding="utf-8") as file:
        questions = json.load(file)

    for q in questions:

        if q["question"].strip().lower() == question.strip().lower():

            keywords = q["keywords"]

            answer_lower = answer.lower()

            matched = 0

            for word in keywords:

                if word.lower() in answer_lower:
                    matched += 1

            score = round((matched / len(keywords)) * 10)

            if score >= 9:
                feedback = "Excellent answer."
            elif score >= 7:
                feedback = "Good answer. Few points are missing."
            elif score >= 5:
                feedback = "Average answer. Add more technical details."
            else:
                feedback = "Poor answer. Please study this topic."

            return f"""
⚠ Online AI unavailable.

✅ Offline AI Evaluation

Score: {score}/10

Feedback:
{feedback}

Correct Answer:
{q['correct_answer']}
"""

    return f"""
⚠ Online AI unavailable.

Score: 0/10

Feedback:
Question not found in Offline AI database.

Correct Answer:
Not Available.
"""