import re
import streamlit as st

# Voice-answer input: records from the browser microphone and converts speech to text.
try:
    from streamlit_mic_recorder import mic_recorder
    import speech_recognition as sr
except ImportError:
    mic_recorder = None
    sr = None

from ai.clear_voice import speak_clear
from ai.gemini import ask_gemini
from utils.question_manager import QuestionManager
from utils.pdf_report import generate_pdf

st.set_page_config(
    page_title="AI Interviewer | Rahul Kumar",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- PROFESSIONAL UI ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: linear-gradient(135deg, #f8fbff 0%, #eef4ff 55%, #f7f9fc 100%); }
.block-container { max-width: 1180px; padding-top: 2rem; padding-bottom: 3rem; }
.hero { padding: 28px 32px; border-radius: 22px; background: linear-gradient(135deg, #111827, #1e3a8a); color: white; box-shadow: 0 14px 35px rgba(30,58,138,.18); margin-bottom: 24px; }
.hero h1 { margin: 0; font-size: 34px; font-weight: 800; }
.hero p { margin: 8px 0 0; opacity: .86; font-size: 15px; }
.card { background: white; border: 1px solid #e6eaf0; border-radius: 18px; padding: 22px; box-shadow: 0 8px 24px rgba(15,23,42,.06); margin-bottom: 18px; }
.metric { background: white; border: 1px solid #e6eaf0; border-radius: 16px; padding: 18px; text-align:center; box-shadow: 0 6px 18px rgba(15,23,42,.05); }
.metric .value { font-size: 28px; font-weight: 800; color: #1d4ed8; }
.metric .label { color: #64748b; font-size: 13px; margin-top: 4px; }
.question { background: #eff6ff; border-left: 5px solid #2563eb; padding: 20px 22px; border-radius: 14px; font-size: 18px; line-height: 1.6; color: #172033; }
.badge { display:inline-block; padding: 6px 11px; border-radius: 999px; background:#dbeafe; color:#1d4ed8; font-size:12px; font-weight:700; }
.footer { text-align:center; color:#64748b; font-size:12px; padding:24px 0 4px; }
div.stButton > button { border-radius: 12px; font-weight: 700; min-height: 44px; }
textarea { border-radius: 14px !important; }
[data-testid="stSidebar"] { background: #111827; }
[data-testid="stSidebar"] * { color: #f8fafc !important; }

/* Premium UI additions */
[data-testid="stHeader"] { background: rgba(0,0,0,0); }
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 12px;
}
.stProgress > div > div > div > div { border-radius: 20px; }
button[kind="primary"] {
    box-shadow: 0 8px 18px rgba(37,99,235,.18);
}
.profile-strip {
    display:flex; justify-content:space-between; align-items:center;
    gap:14px; padding:14px 18px; border-radius:16px;
    background:rgba(255,255,255,.86); border:1px solid #e5e7eb;
    margin:10px 0 20px;
}
.profile-title { font-weight:800; color:#0f172a; font-size:16px; }
.profile-sub { color:#64748b; font-size:12px; margin-top:2px; }
.section-label {
    color:#2563eb; font-size:11px; font-weight:800;
    letter-spacing:1.1px; text-transform:uppercase; margin-bottom:7px;
}
.result-card {
    background:linear-gradient(135deg,#ffffff,#f8fbff);
    border:1px solid #dbeafe; border-radius:18px; padding:20px;
    box-shadow:0 8px 24px rgba(15,23,42,.05);
}



/* VOICE ANSWER */
.voice-answer-box {
    margin-top: 12px;
    padding: 14px 16px;
    border: 1px solid #dbeafe;
    border-radius: 16px;
    background: linear-gradient(135deg,#f8fbff,#eef6ff);
}
.voice-answer-title {
    font-size: 14px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 4px;
}
.voice-answer-sub {
    font-size: 12px;
    color: #64748b;
}

/* AI VOICE INDICATOR */
.ai-voice-panel {
    display:flex;
    align-items:center;
    gap:14px;
    padding:14px 18px;
    margin:0 0 18px;
    border-radius:18px;
    background:linear-gradient(135deg,#0f172a,#1d4ed8);
    color:white;
    box-shadow:0 10px 28px rgba(15,23,42,.14);
}
.ai-avatar {
    width:52px;
    height:52px;
    min-width:52px;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    background:linear-gradient(135deg,#38bdf8,#2563eb);
    font-size:27px;
    box-shadow:0 0 0 5px rgba(255,255,255,.10);
}
.ai-avatar.speaking {
    animation:aiPulse 1.2s infinite;
}
.ai-voice-title {
    font-size:15px;
    font-weight:800;
}
.ai-voice-status {
    font-size:12px;
    color:#bfdbfe;
    margin-top:2px;
}
.ai-wave {
    display:flex;
    align-items:center;
    gap:3px;
    margin-left:auto;
}
.ai-wave span {
    width:4px;
    height:14px;
    border-radius:5px;
    background:#93c5fd;
    animation:aiWave .9s infinite ease-in-out;
}
.ai-wave span:nth-child(2){animation-delay:.12s}
.ai-wave span:nth-child(3){animation-delay:.24s}
.ai-wave span:nth-child(4){animation-delay:.36s}
.ai-wave span:nth-child(5){animation-delay:.48s}
@keyframes aiWave {
    0%,100% { transform:scaleY(.55); opacity:.55; }
    50% { transform:scaleY(1.55); opacity:1; }
}
@keyframes aiPulse {
    0%,100% {
        box-shadow:0 0 0 5px rgba(255,255,255,.10),0 0 0 0 rgba(96,165,250,.35);
    }
    50% {
        box-shadow:0 0 0 5px rgba(255,255,255,.10),0 0 0 12px rgba(96,165,250,0);
    }
}

/* PROFESSIONAL VOICE ANSWER CONTROL */
.voice-listening {
    display:flex;
    align-items:center;
    justify-content:center;
    gap:14px;
    min-height:72px;
    margin:14px auto 10px;
    padding:10px 18px;
    border:1px solid #dbeafe;
    border-radius:18px;
    background:linear-gradient(135deg,#ffffff,#f8fbff);
    box-shadow:0 8px 22px rgba(15,23,42,.06);
}
.voice-mic-icon {
    width:52px;
    height:52px;
    min-width:52px;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:25px;
    background:linear-gradient(135deg,#7c3aed,#2563eb);
    color:#fff;
    box-shadow:0 0 0 5px rgba(124,58,237,.10),0 8px 20px rgba(37,99,235,.20);
}
.voice-listening > div:nth-child(2) {
    font-size:13px;
    font-weight:700;
    color:#475569;
    min-width:78px;
}
.voice-wave {
    display:flex;
    align-items:center;
    justify-content:center;
    gap:3px;
    height:40px;
    flex:1;
    max-width:620px;
}
.voice-wave span {
    width:3px;
    height:10px;
    border-radius:8px;
    background:linear-gradient(180deg,#7c3aed,#2563eb);
    animation:voiceWave 1s ease-in-out infinite;
    transform-origin:center;
}
.voice-wave span:nth-child(2){animation-delay:.08s}
.voice-wave span:nth-child(3){animation-delay:.16s}
.voice-wave span:nth-child(4){animation-delay:.24s}
.voice-wave span:nth-child(5){animation-delay:.32s}
.voice-wave span:nth-child(6){animation-delay:.40s}
.voice-wave span:nth-child(7){animation-delay:.48s}
.voice-wave span:nth-child(8){animation-delay:.56s}
@keyframes voiceWave {
    0%,100% { transform:scaleY(.45); opacity:.45; }
    50% { transform:scaleY(2.8); opacity:1; }
}
/* Keep the actual recorder compact; the component remains fully functional. */
div[data-testid="stCustomComponentV1"] {
    display:flex;
    justify-content:center;
    margin-top:-8px;
    margin-bottom:6px;
}
/* ===== FIX MAIN CONTENT TEXT VISIBILITY ===== */

[data-testid="stAppViewContainer"] .main {
    color: #0f172a !important;
}

[data-testid="stAppViewContainer"] .main
[data-testid="stMarkdownContainer"] {
    color: #0f172a !important;
}

/* Normal headings and paragraphs */
[data-testid="stAppViewContainer"] .main h1,
[data-testid="stAppViewContainer"] .main h2,
[data-testid="stAppViewContainer"] .main h3,
[data-testid="stAppViewContainer"] .main h4,
[data-testid="stAppViewContainer"] .main p,
[data-testid="stAppViewContainer"] .main li {
    color: #0f172a !important;
}

/* AI Evaluation result */
[data-testid="stAppViewContainer"] .main
[data-testid="stMarkdownContainer"] p {
    color: #0f172a !important;
}

/* Keep AI voice panel white */
.ai-voice-panel,
.ai-voice-panel * {
    color: white !important;
}

.ai-voice-status {
    color: #bfdbfe !important;
}

/* Keep sidebar white */
[data-testid="stSidebar"],
[data-testid="stSidebar"] * {
    color: #f8fafc !important;
}

/* Success / warning messages */
[data-testid="stAlert"] p {
    color: inherit !important;
}
</style>
""", unsafe_allow_html=True)

manager = QuestionManager()

# ---------------- AI VOICE ----------------
def ai_say(text):
    """Clear deep male AI voice using Microsoft Edge neural TTS."""
    try:
        speak_clear(text)
        # Clear any old voice error as soon as TTS works again.
        # This prevents a previous offline warning from staying visible
        # after the internet/voice service comes back.
        st.session_state["voice_error"] = ""
    except Exception as e:
        st.session_state["voice_error"] = str(e)


DEFAULTS = {
    "name": "",
    "subject": "",
    "interview_started": False,
    "interview_completed": False,
    "question_no": 0,
    "questions": [],
    "answers": [],
    "results": [],
    "scores": [],
    "answer_text": "",
    "welcome_spoken": False,
    "intro_spoken": False,
    "question_spoken": -1,
    "evaluation_spoken": -1,
    "completion_spoken": False,
    "last_mic_recording_id": 0,
    "voice_answer_error": "",
}
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Do not keep an old AI-voice warning pinned across reruns.
# A fresh rerun represents a new UI state; if TTS fails again, ai_say()
# will set the current error again during this run.
st.session_state["voice_error"] = ""

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 🎯 AI Interviewer")
    st.caption("Technical Interview Practice Platform")
    st.divider()
    st.markdown("**Developer**")
    st.write("Rahul Kumar & Gaurav Kumar")
    st.markdown("**Project**")
    st.write("Minor Project — AI Interviewer")
    st.divider()
    st.markdown("### Features")
    st.write("✓ Text & voice answers")
    st.write("✓ AI evaluation")
    st.write("✓ Score & feedback")
    st.write("✓ Final report")
    st.write("✓ PDF download")
    st.divider()
    st.caption("Stable submission build • Text & voice answers enabled")
    st.caption("Developed by Rahul Kumar & Gaurav Kumar")

# ---------------- HERO ----------------
st.markdown("""
<div class="hero">
    <h1>🎯 AI Technical Interviewer</h1>
    <p>Practice technical interviews with structured questions, AI-powered evaluation, scoring and a downloadable report.</p>
</div>
""", unsafe_allow_html=True)

if st.session_state.name:
    st.markdown(f"""
    <div class="profile-strip">
        <div>
            <div class="profile-title">👤 {st.session_state.name}</div>
            <div class="profile-sub">Candidate profile</div>
        </div>
        <div style="text-align:right">
            <div class="profile-title">{st.session_state.subject or "Not selected"}</div>
            <div class="profile-sub">Interview track</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- AI AUTO WELCOME ----------------
if (not st.session_state.interview_started and
    not st.session_state.interview_completed and
    not st.session_state.welcome_spoken):
    ai_say(
        "Hello! Welcome to AI Interviewer. I am your AI interviewer. "
        "Please enter your name and select an interview subject. "
        "When you are ready, click Start Interview."
    )
    st.session_state.welcome_spoken = True

# ---------------- HOME ----------------
if not st.session_state.interview_started and not st.session_state.interview_completed:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 👤 Candidate Setup")
    c1, c2 = st.columns([1.3, 1])
    with c1:
        name = st.text_input("Candidate Name", value=st.session_state.name, placeholder="Enter your full name")
    with c2:
        subject = st.selectbox("Interview Subject", (
            "Python", "SQL", "Data Analyst", "Data Science", "Software Engineering", "Cyber Security"
        ))
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">INTERVIEW SETUP</div><h3>🚀 Ready to Begin?</h3>', unsafe_allow_html=True)
    st.write("Answer each technical question clearly. The AI interviewer evaluates your response, assigns a score out of 10, and provides actionable feedback.")
    if st.button("🚀 Start Interview", use_container_width=True, type="primary"):
        if not name.strip():
            st.error("Please enter your name first.")
        else:
            st.session_state.name = name.strip()
            st.session_state.subject = subject
            st.session_state.question_no = 0
            st.session_state.interview_completed = False
            st.session_state.answers.clear()
            st.session_state.results.clear()
            st.session_state.scores.clear()
            st.session_state.answer_text = ""
            st.session_state.questions = manager.get_questions(subject)
            st.session_state.interview_started = True
            st.session_state.intro_spoken = False
            st.session_state.question_spoken = -1
            st.session_state.evaluation_spoken = -1
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# ---------------- INTERVIEW ----------------
if st.session_state.interview_started and not st.session_state.interview_completed:
    total_questions = len(st.session_state.questions)
    q_no = st.session_state.question_no
    question = st.session_state.questions[q_no]
    progress = (q_no + 1) / total_questions if total_questions else 0

    # Ask each question automatically exactly once.
    # For Question 1, intro + question are ONE TTS call,
    # so two voices cannot start at the same time.
    if st.session_state.question_spoken != q_no:

        if q_no == 0 and not st.session_state.intro_spoken:
            ai_say(
                f"Great, {st.session_state.name}. "
                f"Welcome to your {st.session_state.subject} technical interview. "
                "I will ask you technical questions and evaluate your answers. "
                f"Let's begin. Question 1. {question}"
            )
            st.session_state.intro_spoken = True

        else:
            ai_say(f"Question {q_no + 1}. {question}")

        st.session_state.question_spoken = q_no

    st.markdown(
        """
        <div class="ai-voice-panel">
            <div class="ai-avatar speaking">🤖</div>
            <div>
                <div class="ai-voice-title">AI Interviewer</div>
                <div class="ai-voice-status">● AI Voice Active • Deep Male Neural Voice</div>
            </div>
            <div class="ai-wave">
                <span></span><span></span><span></span><span></span><span></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(progress, text=f"Question {q_no + 1} of {total_questions}")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric"><div class="value">{q_no + 1}</div><div class="label">Current Question</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric"><div class="value">{len(st.session_state.results)}</div><div class="label">Evaluated</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric"><div class="value">{st.session_state.subject}</div><div class="label">Subject</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">LIVE INTERVIEW</div><span class="badge">TECHNICAL QUESTION</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="question">{question}</div>', unsafe_allow_html=True)
    if st.button("🔊 Repeat Question", use_container_width=False):
        ai_say(f"Question {q_no + 1}. {question}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="section-label">YOUR RESPONSE</div>
        <div class="voice-answer-box">
            <div class="voice-answer-title">🎤 Answer by Voice or Text</div>
            <div class="voice-answer-sub">
                Speak your answer, or type it below. Your spoken answer will automatically
                appear in the answer box and can be edited before submission.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Browser microphone recorder.
    # This does NOT render an audio player/progress bar.
    if mic_recorder is None or sr is None:
        st.error(
            "Voice answer is not installed yet. Run: "
            "pip install streamlit-mic-recorder SpeechRecognition"
        )
    else:
        # A new recording attempt starts from a clean voice-error state.
        st.session_state.voice_answer_error = ""

        # Small icon-only microphone control.
        # The component switches to the stop icon while recording.
        st.markdown(
            """
            <div class="voice-listening">
                <div class="voice-mic-icon">🎙️</div>
                <div>Voice input</div>
                <div class="voice-wave">
                    <span></span><span></span><span></span>
                    <span></span><span></span><span></span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        audio = mic_recorder(
            start_prompt="🎙️",
            stop_prompt="⏹️",
            just_once=True,
            use_container_width=False,
            format="wav",
            key=f"voice_answer_{q_no}"
        )

        if audio is not None:
            recording_id = audio.get("id", 0)

            if recording_id > st.session_state.last_mic_recording_id:
                st.session_state.last_mic_recording_id = recording_id

                try:
                    recognizer = sr.Recognizer()

                    recorded_audio = sr.AudioData(
                        audio["bytes"],
                        audio["sample_rate"],
                        audio["sample_width"],
                    )

                    # Google recognition needs a reasonably valid WAV stream.
                    # Convert the browser recording to mono/16-bit/16 kHz first.
                    try:
                        import io
                        import wave

                        raw = io.BytesIO(audio["bytes"])

                        with wave.open(raw, "rb") as wf:
                            frames = wf.readframes(wf.getnframes())
                            channels = wf.getnchannels()
                            sample_width = wf.getsampwidth()
                            sample_rate = wf.getframerate()

                        if channels != 1:
                            raise ValueError(
                                "Microphone recording is not mono."
                            )

                        normalized = sr.AudioData(
                            frames,
                            sample_rate,
                            sample_width,
                        )

                    except Exception:
                        # Fall back to the original component metadata.
                        normalized = recorded_audio

                    with st.spinner("🎤 Converting your voice to text..."):
                        spoken_text = recognizer.recognize_google(
                            normalized,
                            language="en-IN",
                        )

                    if spoken_text and spoken_text.strip():
                        spoken_text = spoken_text.strip()
                        st.session_state.answer_text = spoken_text
                        # Update the actual text-area widget state before rerun.
                        st.session_state[f"answer_box_{q_no}"] = spoken_text
                        st.session_state.voice_answer_error = ""
                        st.rerun()
                    else:
                        st.session_state.voice_answer_error = (
                            "No speech was detected. Please record again."
                        )

                except sr.UnknownValueError:
                    st.session_state.voice_answer_error = (
                        "I could not understand the recording. "
                        "Please speak clearly and try again."
                    )

                except sr.RequestError as e:
                    st.session_state.voice_answer_error = (
                        "Google Speech Recognition could not be reached. "
                        "Check your internet connection and try again. "
                        f"Details: {e}"
                    )

                except Exception as e:
                    st.session_state.voice_answer_error = (
                        "Voice conversion failed: " + str(e)
                    )

        if st.session_state.voice_answer_error:
            st.warning(
                "🎤 " + st.session_state.voice_answer_error
            )

    answer = st.text_area(
        "✍️ Your Answer",
        value=st.session_state.answer_text,
        height=180,
        key=f"answer_box_{q_no}",
        placeholder="Write your technical answer here or use the microphone above..."
    )
    st.session_state.answer_text = answer

    c1, c2 = st.columns(2)
    with c1:
        submit = st.button(
            "✅ Submit Answer",
            use_container_width=True,
            type="primary"
        )
    with c2:
        next_q = st.button(
            "➡ Next Question",
            use_container_width=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

    if submit:
        clean_answer = st.session_state.answer_text.strip()
        if not clean_answer:
            st.warning("Please enter your answer before submitting.")
        else:
            with st.spinner("🤖 AI is evaluating your answer..."):
                result = ask_gemini(st.session_state.subject, question, clean_answer)
            if len(st.session_state.results) <= q_no:
                st.session_state.results.append(result)
                match = re.search(r"Score:\s*(\d+)", result)
                st.session_state.scores.append(int(match.group(1)) if match else 0)
            st.success("Answer evaluated successfully")

            if st.session_state.evaluation_spoken != q_no:
                score_match = re.search(r"Score:\s*(\d+)", result)
                score_text = score_match.group(1) if score_match else "not available"
                ai_say(
                    f"Thank you. I have evaluated your answer. "
                    f"Your score for this question is {score_text} out of 10. "
                    "Please review the feedback on screen."
                )
                st.session_state.evaluation_spoken = q_no

            # ---------------- AI EVALUATION DISPLAY ----------------

            with st.container(border=True):

                st.markdown(
                    """
                    <h3 style="
                        color:#0f172a !important;
                        margin-top:0;
                        margin-bottom:18px;
                    ">
                        🤖 AI Evaluation
                    </h3>
                    """,
                    unsafe_allow_html=True
                )

                # Render AI response as Markdown
                st.markdown(result)

    if next_q:
        if len(st.session_state.results) <= q_no:
            st.warning("Please submit your answer first.")
        else:
            if len(st.session_state.answers) <= q_no:
                st.session_state.answers.append(st.session_state.answer_text)

            if q_no < total_questions - 1:
                st.session_state.question_no += 1
                st.session_state.answer_text = ""
                st.session_state.evaluation_spoken = -1
                st.rerun()
            else:
                st.session_state.interview_completed = True
                st.session_state.interview_started = False
                st.rerun()

# ---------------- AI COMPLETION VOICE ----------------
if st.session_state.interview_completed and not st.session_state.completion_spoken:
    ai_say(
        f"Congratulations, {st.session_state.name}. You have completed the interview. "
        "Your final score and report are ready."
    )
    st.session_state.completion_spoken = True

# ---------------- FINAL RESULT ----------------
if st.session_state.interview_completed:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.success("🎉 Interview Completed Successfully")
    total_score = sum(st.session_state.scores)
    max_score = len(st.session_state.questions) * 10
    percentage = (total_score / max_score) * 100 if max_score else 0

    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    else:
        grade = "Fail"

    a, b, c = st.columns(3)
    with a:
        st.markdown(f'<div class="metric"><div class="value">{total_score}/{max_score}</div><div class="label">Total Score</div></div>', unsafe_allow_html=True)
    with b:
        st.markdown(f'<div class="metric"><div class="value">{percentage:.1f}%</div><div class="label">Percentage</div></div>', unsafe_allow_html=True)
    with c:
        st.markdown(f'<div class="metric"><div class="value">{grade}</div><div class="label">Grade</div></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    pdf_file = generate_pdf(
        st.session_state.name,
        st.session_state.subject,
        st.session_state.answers,
        st.session_state.results,
        total_score,
        percentage,
        grade,
    )
    with open(pdf_file, "rb") as file:
        st.download_button("📥 Download Professional PDF Report", file, file_name=pdf_file, mime="application/pdf", use_container_width=True)

    st.markdown("### 📋 Interview Summary")
    for i, (ans, result) in enumerate(zip(st.session_state.answers, st.session_state.results)):
        with st.expander(f"Question {i + 1}"):
            st.markdown("**Your Answer**")
            st.write(ans)
            st.markdown("**AI Evaluation**")
            st.markdown(result)

    if st.button("🔄 Start New Interview", use_container_width=True):
        for key in ["interview_started", "interview_completed", "question_no", "questions", "answers", "results", "scores", "answer_text", "welcome_spoken", "intro_spoken", "question_spoken", "evaluation_spoken", "completion_spoken",
                         "last_mic_recording_id", "voice_answer_error"]:
            st.session_state[key] = DEFAULTS[key].copy() if isinstance(DEFAULTS[key], list) else DEFAULTS[key]
        st.rerun()

if st.session_state.get("voice_error"):
    st.warning("🔇 AI voice could not start. Check that edge-tts is installed and your ai/clear_voice.py is present.")

st.markdown('<div class="footer">AI Technical Interviewer • Minor Project • Developed by Rahul Kumar & Gaurav Kumar</div>', unsafe_allow_html=True)
