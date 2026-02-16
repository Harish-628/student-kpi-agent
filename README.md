# Student Performance AI Agent

An intelligent AI-powered system for analyzing and predicting student performance using LangChain, LangGraph, and ChromaDB.

## 📋 Table of Contents

- [Project Architecture](#project-architecture)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [Technologies Used](#technologies-used)
- [Project Status](#project-status)

## 🏗️ Project Architecture

```
student-kpi-agent/
├── backend/                  # FastAPI backend services
│   ├── main.py               # API application entry point
│   └── api/                  # API route definitions
├── agent/                    # LangChain & LangGraph agents
│   ├── langgraph_workflow.py # Graph-based agent workflows
│   └── recommendation_engine.py # AI recommendation generation
├── database/                 # Relational database schemas
│   └── models.py             # Database models
├── dashboard/                # Streamlit UI
│   └── streamlit_app.py      # Web dashboard implementation
├── chatbot/                  # Chatbot interface and logic
│   └── web_chatbot.py        # Integrated AI Chatbot
├── vector_db/                # ChromaDB storage and embedding logic
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## 🚀 Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

### 2. Installation

Create and activate a virtual environment:

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Unix/macOS
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file in the project root with the necessary API keys and configuration:

```
API_KEY=your_api_key_here
DATABASE_URL=your_database_url_here
CHROMADB_PATH=./vector_db
```

A template `.env.example` file is provided for reference.

## ▶️ Running the Application

### Backend API

```bash
uvicorn backend.main:app --reload
```

The API will be available at `http://localhost:8000`

### Dashboard UI

```bash
streamlit run dashboard/streamlit_app.py
```

The dashboard will open at `http://localhost:8501`

## 🛠️ Technologies Used

| Technology | Purpose |
|-----------|---------|
| **FastAPI** | High-performance API framework |
| **Streamlit** | Interactive web interface & dashboard |
| **LangChain** | LLM orchestration and chains |
| **LangGraph** | Graph-based agent workflows |
| **ChromaDB** | Vector database for embeddings |
| **Gemini / Grok API** | Core LLM intelligence |
| **PostgreSQL / SQLite** | Relational data storage |

## 📊 Project Status

### ✅ Day 1: Project Setup & Architecture Initialization

- [x] GitHub repo initialized
- [x] Python environment configured
- [x] Required packages installed
- [x] Project structure created

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For support, please open an issue in the GitHub repository.
