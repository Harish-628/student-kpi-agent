![Version](https://img.shields.io/badge/version-1.0.0-blue?style=flat-square)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688)
![License](https://img.shields.io/badge/license-MIT-green)
![Gemini](https://img.shields.io/badge/AI-Gemini%203.1-orange)

# ⚡ NeuralKPI: Advanced AI Student-KPI Management System

**NeuralKPI** is a production-grade academic performance tracking platform. It integrates generative AI, stateful multi-agent workflows, and a high-fidelity "Neural" UI to revolutionize how students manage activities and how faculty oversee department achievements.

---

## 🧠 Hybrid Model Architecture

The heart of the system is a **Dual-Model Hybrid Routing** engine. This architecture ensures peak performance while strictly managing API quotas and reducing latency for real-time voice interaction.

| Component | AI Model | Purpose |
|---|---|---|
| **Router Node** | `gemini-3.1-flash-lite` | Instant classification of user intent and role-based security checks. |
| **Utility Agent** | `gemini-1.5-flash` | High-speed data formatting and simple "On Duty" (OD) status updates. |
| **Response Agent** | `gemini-1.5-pro` | Deep analytical reasoning for career advice and performance summarization. |

---

## 🌟 Key Features

### 🎙️ Neural Live: The AI Assistant
*   **Voice-First Interface:** A neon-themed, pulsing AI orb that reacts in real-time to speech using the `google-genai` SDK.
*   **Resilience Layer:** Integrated `tenacity` retry logic with exponential backoff (10s → 20s → 40s) to handle `429 RESOURCE_EXHAUSTED` errors gracefully.
*   **Environment Injection Bypass:** Optimized `python-dotenv` implementation using `load_dotenv(override=True)` to ensure consistent API connectivity across different terminal environments.

### 📋 Intelligent On-Duty (OD) Management
*   **Multi-Turn Student Flow:** A stateful **LangGraph** workflow that "remembers" conversation context. Students can apply for OD over multiple voice turns as the AI identifies and asks for missing fields (*College, Event, Date, Duration, Start/End Time*).
*   **Faculty Monitoring Dashboard:**
    *   **Voice-Activated Reporting:** Faculty can ask "Who is out?" to get a real-time verbal summary of pending requests.
    *   **Auto-Modal Verification:** When a faculty member asks to "see" a prize certificate, the AI sends a JSON trigger (`{"action": "OPEN_MODAL"}`) that automatically invokes the UI modal.

---

### 🎨 Premium UI/UX Ecosystem
*   **Glassmorphism Design:** A stunning dark-mode interface with multi-layered orb animations and vibrant neon accents.
*   **Kongunadu Branding:** Custom-integrated Global Neon Loading Overlay featuring the Kongunadu College logo centered in a pulsing animation ring.
*   **Performance Rollout:** A dynamic event photo marquee on the login page showcasing department achievements.

---

## 📂 Project Structure

```bash
├── 🤖 agent/                   # LangGraph state machines & multi-turn OD logic
├── ⚙️ backend/                 # FastAPI server & Role-Based Access Control (RBAC)
├── 💬 chatbot/                 # Hybrid Model Engine (Routing & Resilience)
├── 📂 database/                # SQLAlchemy models for ODRequests & Achievements
├── 💻 frontend/                # Glassmorphism UI (index.html, neon-app.js)
│   └── 🖼️ pictures/             # Core assets & Kongunadu College branding
├── 🚀 RUN_START.bat            # One-click deployment script (Backend + Frontend)
└── 📋 requirements.txt         # Project dependencies
```

---

## 🛠️ Setup & Installation

### 1. Environment Configuration
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=sqlite:///./student_kpi.db
```

### 2. Quick Start
Run the startup batch script to boot the FastAPI backend and the Neon Frontend simultaneously:
```powershell
.\RUN_START.bat
```

*   **Backend API:** `http://localhost:8000`
*   **Frontend UI:** `http://localhost:8080`

---

## 🏗️ Technology Stack
*   **AI Orchestration:** LangGraph (Stateful Multi-Agent Workflows)
*   **LLMs:** Google Gemini 3.1 Flash-Lite (Optimized for Speed/Quota)
*   **Backend:** FastAPI (Python 3.10+)
*   **Frontend:** Vanilla JS & CSS3 (Custom Design System)
*   **Database:** SQLAlchemy (SQLite)

---

Developed for **Kongunadu College of Engineering and Technology**. All Rights Reserved.
