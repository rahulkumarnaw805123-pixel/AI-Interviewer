# AI-Interviewer
AI-powered technical interview platform with voice interaction, speech-to-text, intelligent answer evaluation, feedback, and automated PDF reports.
# 🎤 AI Interviewer

An AI-powered technical interview platform designed to simulate real-world technical interviews through **text and voice interaction**.

The application asks technical questions, accepts spoken or typed answers, evaluates responses using AI, provides feedback and scores, and generates interview reports.

## ✨ Features

* 🎤 Voice-based interview answers
* ⌨️ Text-based answers
* 🔊 AI question reading
* 🧠 AI-powered answer evaluation
* 📊 Score and feedback
* 💡 Correct/ideal answer suggestions
* 🤖 Offline evaluation fallback
* 📄 Automated interview report generation
* 🗂️ Multiple technical subjects
* 🔄 Random interview questions
* 💾 Interview data management

## 📚 Subjects

The project currently includes questions for:

* Python
* SQL
* Data Science
* Data Analyst
* Software Engineering
* Cyber Security

## 🛠️ Technologies Used

* **Python**
* **Streamlit**
* **Google Gemini API**
* **Speech Recognition**
* **Text-to-Speech**
* **HTML/CSS**
* **SQLite / Database**
* **ReportLab**
* **python-dotenv**

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
├── assets/
├── reports/
├── app.py
├── questions.json
├── requirements.txt
└── .gitignore
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/AI-Interviewer.git
cd AI-Interviewer
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 🔐 API Key Setup

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

**Never upload your `.env` file or API key to GitHub.**

The project uses `.gitignore` to prevent sensitive files such as `.env` from being committed.

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## 🎯 How It Works

1. Enter your name.
2. Select an interview subject.
3. Start the interview.
4. The AI interviewer presents a technical question.
5. Answer using **voice or text**.
6. Submit your answer.
7. The AI evaluates your response.
8. Receive a score, feedback, and ideal answer.
9. Continue to the next question.
10. Generate an interview report.

## 🤖 AI Evaluation

The application primarily uses the Gemini API for evaluating technical answers.

If the online AI service is unavailable, the project includes an **offline evaluation fallback** so the interview experience can continue.

## 📄 Interview Reports

The application can generate an interview report containing information such as:

* Candidate details
* Interview questions
* Candidate answers
* Scores
* Feedback
* Evaluation results

## 🔒 Security

Sensitive configuration is stored using environment variables.

The repository excludes:

```text
.env
venv/
.venv/
__pycache__/
*.pyc
test_api.py
mic_test.py
```

**Important:** Never commit an API key directly inside Python source files.

## 🚀 Future Improvements

Possible future improvements include:

* Real-time voice waveform visualization
* More advanced speech recognition
* Interview difficulty levels
* Timer-based interviews
* Detailed performance analytics
* Interview history dashboard
* More technical subjects
* Improved AI feedback
* Deployment as a public web application

## 👨‍💻 Developers

**Rahul Kumar & Gaurav Kumar**

Minor Project — **AI Interviewer**

## ⭐ Project Goal

The goal of this project is to provide students and job seekers with an interactive platform for practicing technical interviews and improving their interview performance through AI-powered evaluation and feedback.
