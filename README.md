<<<<<<< HEAD
# OrchestrAI Enterprise System 🚀

![OrchestrAI Banner](https://img.shields.io/badge/OrchestrAI-Enterprise%20System-blue?style=for-the-badge&logo=google-gemini)

**OrchestrAI** is an advanced, AI-powered enterprise workflow management system designed around a modular multi-agent architecture. It seamlessly bridges task management, team collaboration, live video conferencing, and automated performance tracking. 

Built with React, FastAPI, Python, and integrating major APIs like Google Gemini, Hugging Face, and Jitsi, OrchestrAI effectively automates the entire lifecycle of enterprise operations—from processing meeting transcripts into actionable tasks to analyzing employee sentiment.

---

## ✨ Key Features

- **Multi-Agent AI Architecture:** 14 Specialized AI agents governed by a centralized Orchestrator. Evaluates delays, balances workloads, detects team conflicts, and generates meeting summaries.
- **Real-Time Synchronization:** WebSocket integration ensuring Task Dashboards, Manager Views, and Notifications are updated globally in real-time.
- **Integrated Video Conferencing:** Built-in Jitsi Meet SDK for smooth, in-app video calls and meetings.
- **Automated AI Meeting Minutes (MOM):** Analyzes video conferencing transcripts using AI to summarize discussions and natively execute assignments.
- **Deep Sentiment Analysis:** Leverages Hugging Face Inference API along with Gemini to measure team sentiment, predict risks, and prevent employee burnout.
- **Automated Email Triggers:** Asynchronous email assignments, performance warnings, and delay alerts handled entirely without user interaction.
- **Instant Reporting:** Generates downloadable insights and visually rich analytical PDF reports using Chart.js and ReportLab.

---

## 🛠️ Technology Stack

| Component | Technology Used |
|-----------|------------------|
| **Frontend** | React.js, Vite, TailwindCSS (for Design) |
| **Backend** | Python, FastAPI, WebSockets |
| **Database** | Supabase (PostgreSQL), SQLite (Demo Fallback) |
| **Generative AI**| Google Gemini API |
| **NLP AI** | Hugging Face API |
| **Video Calls** | Jitsi Meet SDK |
| **Emailing** | SMTP (Gmail App Passwords) |
| **Reporting / UI**| ReportLab (PDF), Chart.js (Data Visualization) |

---

## 🧩 The 14 AI Agents

OrchestrAI thrives on its highly modular 14-agent system. Below are active agents operating continuously in the background:

1. **Meeting Agent:** Summarizes meeting transcripts.
2. **Task Extraction Agent:** Reads meetings and pulls directly actionable tasks.
3. **Assignment Agent:** Intelligently assigns those tasks based on employee load and skills.
4. **Deadline Agent:** Computes realistic smart deadlines.
5. **Feedback Agent:** Analyzes daily logs and updates.
6. **Sentiment Agent:** Grounded by Hugging Face NLP to measure frustration or satisfaction.
7. **Delay Prediction Agent:** Predicts which tasks will miss deadlines.
8. **Conflict Detection Agent:** Identifies clashing work or team drama.
9. **Performance Agent:** Calculates rolling KPIs and performance scores.
10. **Report Agent:** Synthesizes periodic reports.
11. **Notification Agent:** Handles standard, push, and WebSocket triggers.
12. **Workload Balancer Agent:** Distributes work evenly preventing burnout.
13. **Risk Prediction Agent:** Detects overall systemic project risks.
14. **Productivity Agent:** Tracks hours mapped strictly to deliverables.

---

## 🚀 Quick Setup Guide

### 1. Backend Setup
```bash
cd backend
python -m venv venv
# Activate virtual environment
# Windows: venv\Scripts\activate | MacOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```
> Configure `.env` in the `backend/` directory with `GEMINI_API_KEY`, `HF_API_KEY`, and `SMTP` details.

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 3. Run the App
Launch `python main.py` on the backend, ensuring it runs on port `8000`. Launch the frontend on port `5173`. Access the web portal at: `http://localhost:5173`.

---

## 👨‍💻 Project Authors
**Developed with ❤️ by SACHIN SHARMA**
"# OrchestrAI-Autonomous-Enterprise-Workflow-Management-System" 
=======
# OrchestrAI-Autonomous-Enterprise-Workflow-Management-System
OrchestrAI is a Multi-Agent AI powered enterprise workflow automation system that acts as an AI Manager. It automates meeting analysis, task assignment, deadline tracking, employee feedback analysis, performance monitoring, and report generation using a multi-agent architecture built with React, FastAPI, Supabase, and Gemini AI.
