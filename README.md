# ATS Resume Coach — AI Resume Screening & Career Coaching Bot

**ATS Resume Coach** is an intelligent AI-powered resume evaluation and career coaching service built with **Python**, **FastAPI**, **python-telegram-bot**, **Matplotlib**, and **Google Gemini API**. It allows job seekers and recruiters to analyze candidate resumes against Applicant Tracking Systems (ATS) and target Job Descriptions across messaging platforms (**Telegram**, **WhatsApp**, **Discord**, and **Web**).

The bot automatically parses documents (PDF, DOCX, TXT), evaluates ATS machine readability, generates server-side dark-theme visual competency charts, calculates explainable merit-based compatibility scores, and recommends curated accredited online courses (Coursera, edX, Udemy) tailored specifically to the target job role.

---

## Key Features

- **Multi-Platform Adapter Layer**: Platform-agnostic architecture supporting Telegram Bot long-polling, WhatsApp Cloud API (Twilio TwiML), Discord Bot, and a live Web Dashboard.
- **Zero Experience Bias ATS Scoring**: Pure merit-driven weighted formula excluding tenure penalties:
  - **Technical & Domain Skill Alignment**: **70%**
  - **ATS Machine Formatting & Parseability**: **15%**
  - **Action Verbs & Quantifiable Impact Density**: **15%**
- **Role-Adaptive Course Recommendation Engine**: Dynamically identifies the target job role across 15+ specialized career tracks (*Frontend, Java/Spring Boot, Data Analytics, Mobile/Flutter, Cybersecurity, UI/UX, Full Stack, DevOps/Cloud, QA Automation, Salesforce, Blockchain*) and delivers direct clickable course links to Coursera, edX, and Udemy.
- **Server-Side High-DPI Visual Chart Generation**: Built-in Matplotlib engine generating sleek dark-theme chart photos delivered natively into chat:
  - **Skills Competency Profile Bar Chart**: Sent immediately upon resume upload.
  - **4-Axis Role Compatibility Matrix (Radar Chart)**: Sent upon Job Description evaluation.
  - **Candidate Comparison Leaderboard Chart**: Sent during multi-resume evaluations.
- **Multi-Resume Single-JD Leaderboard**: Allows uploading multiple resumes against one target Job Description to rank candidates side-by-side with match scores and skill deltas.
- **Multi-Format Document Parser**: Extracts clean text, contact details, skills, metrics, and detects formatting issues (tables, columns, special characters) from PDF and DOCX files.
- **Session State Management**: In-memory session store tracking candidate resumes, target job descriptions, chat history, and evaluation versions.

---

## Directory Structure

```text
ats-resume-coach/
├── app/
│   ├── main.py                     # FastAPI application & webhook entrypoint
│   ├── api.py                      # REST API endpoints & evaluation routes
│   ├── config.py                   # Pydantic Settings & environment variables
│   ├── ats_engine.py               # Scoring engine, role detector & course catalog
│   ├── chart_generator.py          # Matplotlib server-side dark-theme charts
│   ├── parser.py                   # Multi-format PDF/DOCX parser & skills extractor
│   ├── session_store.py            # In-memory candidate session & version store
│   ├── llm_service.py              # Google Gemini LLM integration service
│   └── adapters/                   # Platform Adapter Layer
│       ├── base_adapter.py         # Unified messaging & report formatting logic
│       ├── telegram_bot.py         # Async Telegram bot service (polling & charts)
│       ├── whatsapp_adapter.py     # Twilio WhatsApp webhook adapter
│       └── discord_bot.py          # Discord Bot integration
├── static/                         # Web UI frontend dashboard
├── requirements.txt                # Project dependencies
├── test_ats_bot.py                 # Automated 10-step test suite
├── run_telegram.py                 # Interactive Telegram runner & token validator
├── start_telegram_bot.bat          # Windows 1-click Telegram bot launcher
├── start_server.bat                # Windows 1-click FastAPI server launcher
├── start_whatsapp_bot.bat          # Windows 1-click WhatsApp tunnel launcher
└── .env                            # Environment variables & API tokens
```

---

## Quick Start

### 1. Installation

Clone the repository and install dependencies:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate      # On Windows
source venv/bin/activate  # On macOS / Linux

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

Create or edit your `.env` file in the project root:

```env
# Telegram Bot Token (from @BotFather)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Google Gemini API Key (optional for LLM enhancements)
GEMINI_API_KEY=your_gemini_api_key_here

# Server Settings
HOST=0.0.0.0
PORT=8000
```

### 3. Run Application

#### Option A: Run Telegram Bot Directly
```bash
python run_telegram.py
```
*(Or double-click `start_telegram_bot.bat` on Windows)*

#### Option B: Run Full FastAPI Web Server
```bash
python main.py
```
Access the web dashboard at: [http://localhost:8000](http://localhost:8000)

### 4. Running Tests

Run the automated test suite to verify scoring, parsing, charts, and course recommendations:

```bash
python test_ats_bot.py
```

Expected Output:
```text
==========================================
RUNNING ATS CHATBOT AUTOMATED TEST SUITE
==========================================
[PASSED] 1/10 Resume Parser Test
[PASSED] 2/10 ATS Engine Test (Score excludes experience)
[PASSED] 3/10 Live What-If Test
[PASSED] 4/10 Multi-JD Matrix Test
[PASSED] 5/10 JD-Based Course Recommendations Test
[PASSED] 6/10 Multi-Resume Single-JD Comparison Test
[PASSED] 7/10 Session Store Multi-Resume State Test
[PASSED] 8/10 Server-Side Chart PNG Generator Test
[PASSED] 9/10 Base Messaging Adapter Flow Test
[PASSED] 10/10 WhatsApp TwiML Webhook Test
==========================================
ALL 10 AUTOMATED TESTS PASSED SUCCESSFULLY!
==========================================
```

---

## Bot Interaction Flow

1. Send `/start` to begin an analysis session.
2. **Step 1 — Send Resume**: Upload your resume file (PDF or DOCX).
   - The bot parses the document, extracts technical skills, calculates formatting parseability, and **immediately replies with a visual Skills Competency Profile Chart (PNG photo)**.
3. **Step 2 — Send Job Description**: Paste or type the target job requirements or role title (e.g. *"Frontend Developer with React and TypeScript"*).
   - The bot detects the role, calculates the **Overall ATS Match Score (0–100)**, displays the score breakdown, lists matched/missing skills, and delivers **curated course recommendations with clickable links**.
   - The bot **immediately sends the 4-Axis Role Compatibility Matrix (Radar Chart PNG photo)**.
4. **Compare Multiple Resumes**: Upload additional resumes to automatically generate a **Candidate Leaderboard** ranking candidates against the active Job Description.
5. Send `/reset` at any time to clear the session and start fresh.


