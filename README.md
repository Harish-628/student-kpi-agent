# ⚡ NeuralKPI: Advanced AI Student-KPI Management System

**NeuralKPI** is a production-grade academic performance tracking platform. It integrates generative AI, multi-agent **LangGraph workflows**, and a high-fidelity **"Neural" UI** to revolutionize how students manage activities and how faculty oversee department achievements.

---

## 🧠 The Neural Architecture

The heart of the system is a **Dual-Model Hybrid Routing** engine. This architecture ensures peak performance while strictly managing API quotas and latency.

| Component | AI Model | Purpose |
| :--- | :--- | :--- |
| **Router Node** | `gemini-3.1-flash-lite` | Instant classification of user intent and role-based security checks. |
| **Utility Agent** | `gemini-3.1-flash-lite` | High-speed data formatting and simple "On Duty" (OD) status updates. |
| **Response Agent** | `gemini-3.1-flash-lite` | Deep analytical reasoning for career advice and performance summarization. |

---

## 🌟 Key Features

### 🎙️ Neural Live: The AI Assistant
*   **Voice-First Interface:** A neon-themed, pulsing AI orb that reacts in real-time to student and faculty speech.
*   **Resilience Layer:** Integrated `tenacity` retry logic with exponential backoff to handle `429 RESOURCE_EXHAUSTED` errors gracefully.
*   **Contextual Awareness:** Uses `python-dotenv` for secure environment management and consistent API connectivity.
*   **Network Fallback:** Includes an automatic text-input redundancy system if the Web Speech API encounter errors.

### 📋 Intelligent On-Duty (OD) Management
*   **Multi-Turn Student Flow:** A stateful LangGraph workflow that "remembers" conversation context. Students can apply for OD over multiple voice turns as the AI identifies and asks for missing fields (College, Event, Date, etc.).
*   **Faculty Monitoring Dashboard:**
    *   **Voice-Activated Reporting:** Faculty can ask "Who is out?" to get a real-time verbal summary.
    *   **Auto-Modal Verification:** When a faculty member asks to "see" a prize certificate, the AI sends a JSON trigger that automatically opens the corresponding detail modal on the screen.

### 🍱 Premium UI/UX Ecosystem
*   **Glassmorphism Design:** A modern dark-mode interface with vibrant neon accents and dynamic CSS animations.
*   **Custom Brand Loading:** A unique animated loading circle featuring the **Kongunadu College logo** centered in the spinning ring.
*   **Event Rollout:** A high-speed marquee on the login page showcasing department event photos.

---

## 📂 Project Structure

```bash
├── 🤖 agent/                   # LangGraph state machines & multi-turn OD logic
├── ⚙️ backend/                 # FastAPI server & Role-Based Access Control (RBAC)
├── 💬 chatbot/                 # Hybrid Model Engine (Routing & Resilience)
├── 📂 database/                # SQLAlchemy models for ODRequests & Achievements
├── 💻 frontend/                # Glassmorphism UI (index.html, neon-app.js)
│   └── 🖼️ pictures/             # Core assets & Kongunadu College branding
└── 🚀 RUN_START.bat            # One-click deployment script
```

---

## 🛠️ Setup & Installation

### 1. Clone & Configure
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_fresh_api_key_here
DATABASE_URL=sqlite:///./student_kpi.db
```

### 2. Initialize System
Run the startup script to boot both the FastAPI backend and the Neon Frontend:
```powershell
.\RUN_START.bat
```

---

## 🏗️ Technology Stack
*   **AI Orchestration:** LangGraph (Stateful Multi-Agent Workflows)
*   **LLMs:** Google Gemini 3.1 Flash & Flash-Lite (Hybrid Configuration)
*   **Backend:** FastAPI (Python 3.10+)
*   **Database:** SQLAlchemy (SQLite)
*   **Frontend:** Vanilla JS & CSS3 (Custom "Neural" Animation Library)

---

Developed for **Kongunadu College of Engineering and Technology**. Optimized for the 2026 Gemini API ecosystem.
