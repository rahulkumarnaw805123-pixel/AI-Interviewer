# 🎤 AI Interviewer

> AI-powered technical interview practice platform with voice interaction, speech-to-text, AI-based answer evaluation, feedback, scoring, and automated PDF reports.

## 📌 Overview

**AI Interviewer** is a technical interview practice platform designed to simulate real-world interview experiences.

The application allows candidates to:

- Answer technical questions using **voice or text**
- Listen to interview questions using **text-to-speech**
- Receive **AI-powered evaluation**
- Get a **score and detailed feedback**
- View an **ideal/correct answer**
- Continue through randomly selected technical questions
- Generate an **automated interview report in PDF format**

The project also includes an **offline evaluation fallback** so that the interview experience can continue when the online AI service is unavailable.

---

## ✨ Features

- 🎤 Voice-based interview answers
- ⌨️ Text-based answers
- 🔊 AI question reading
- 🧠 AI-powered answer evaluation
- 📊 Score and feedback
- 💡 Ideal answer suggestions
- 🤖 Offline evaluation fallback
- 📄 Automated PDF interview reports
- 🗂️ Multiple technical subjects
- 🔄 Random interview questions
- 💾 Interview data management

---

## 📚 Available Subjects

The project currently includes technical questions for:

- Python
- SQL
- Data Science
- Data Analyst
- Software Engineering
- Cyber Security

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Web application interface |
| Google Gemini API | AI-powered answer evaluation |
| Speech Recognition | Voice answer processing |
| Text-to-Speech | Reading interview questions |
| HTML/CSS | Voice recorder component |
| SQLite / Database | Interview data management |
| ReportLab | PDF report generation |
| python-dotenv | Environment variable management |

---

## 📁 Project Structure

```text
AI-Interviewer/
│
├── ai/
│   ├── clear_voice.py
│   ├── gemini.py
│   ├── listener.py
│   ├── offline_ai.py
│   ├── speech.py
│   └── speech_to_text.py
│
├── data/
│   ├── python.json
│   ├── sql.json
│   ├── data_science.json
│   ├── data_analyst.json
│   ├── software_engineering.json
│   └── cyber_security.json
│
├── database/
│   └── database.py
│
├── utils/
│   ├── helper.py
│   ├── pdf_report.py
│   └── question_manager.py
│
├── voice_recorder_component/
│   ├── __init__.py
│   └── frontend/
│       └── index.html
│
├── app.py
├── questions.json
├── requirements.txt
└── .gitignore```


## 🖥️ Application Screenshots

### 1. Candidate Setup

![Candidate Setup](screenshots/AI_Interviewer_Setup_Combined.jpg)

### 2. Interview

![Interview](screenshots/AI_Interviewer_Interview_Combined.jpg)

### 3. AI Evaluation

![AI Evaluation](screenshots/AI_Interviewer_Evaluation_Combined.jpg)


## 🚀 Live Demo

https://ai-interviewer-eje4hjgkvagvcqrf9lp3rc.streamlit.app/
