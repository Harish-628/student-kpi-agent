# Student KPI Management System

A complete, enterprise-grade student performance tracking and KPI management system with role-based authentication, analytics, and reporting capabilities.

## 📋 Table of Contents

- [System Features](#system-features)
- [Project Architecture](#project-architecture)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [User Roles & Permissions](#user-roles--permissions)
- [Technologies Used](#technologies-used)
- [Demo Credentials](#demo-credentials)

## ✨ System Features

### Core Features
- ✅ **User Authentication** - JWT-based login/register with role-based access control
- ✅ **Student Management** - Add, update, list, and delete student records
- ✅ **KPI Tracking** - Track 10+ key performance indicators per student
- ✅ **Score Calculation** - AI-powered KPI scoring and career readiness prediction
- ✅ **Milestone Tracking** - Track student achievements and milestones
- ✅ **Performance Analytics** - Comprehensive analytics and reporting
- ✅ **Peer Comparison** - Compare student performance with department peers
- ✅ **Trend Analysis** - Historical performance trends and improvements
- ✅ **Bulk Upload** - Import KPI data via CSV

### Advanced Features
- 📊 Dashboard analytics with department-wise statistics
- 🎯 Percentile ranking and peer benchmarking
- 📈 Performance trend visualization
- 🔐 Role-based access control (Admin, Coordinator, Faculty, Student)
- 🎨 Professional responsive frontend with 4 role-based dashboards
- 📱 Mobile-friendly design
- 🔄 Real-time score calculation

## 🏗️ Project Architecture

```
student-kpi-project/
├── backend/
│   ├── main.py                    # FastAPI application entry point
│   ├── kpi_engine.py              # KPI calculation algorithms
│   ├── auth.py                    # Authentication utilities (JWT, bcrypt)
│   ├── schemas.py                 # Pydantic validation schemas
│   └── api/
│       └── routes.py              # Comprehensive API endpoints
├── database/
│   ├── database.py                # SQLAlchemy configuration
│   └── models.py                  # Database models (7 tables)
│       ├── User                   # Authentication & user management
│       ├── Student                # Student information
│       ├── KPI                    # Key performance indicators
│       ├── Score                  # Calculated scores
│       ├── Milestone              # Student achievements
│       └── PerformanceHistory     # Historical tracking
├── frontend/                      # HTML5/CSS3/Vanilla JS
│   ├── index.html                 # Login page
│   ├── dashboard.html             # Main dashboard
│   ├── styles.css                 # Global styling
│   ├── auth.css                   # Authentication styling
│   ├── dashboard.css              # Dashboard styling
│   ├── auth.js                    # Login logic
│   ├── dashboard.js               # Main dashboard logic
│   └── charts.js                  # Chart.js configurations
├── agent/                         # LangChain agents (optional)
├── chatbot/                       # Chatbot interface (optional)
├── vector_db/                     # Vector database (optional)
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🚀 Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- pip package manager
- Node.js (optional, for frontend tooling)
- Git

### 2. Installation

#### Step 1: Clone Repository & Navigate

```bash
cd student-kpi-project
```

#### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 4: Initialize Database

```bash
# Database tables are auto-created on first run
# No manual setup needed!
```

## ▶️ Running the Application

### Option 1: Using Python Terminal

#### Terminal 1 - Start Backend API Server

```bash
cd student-kpi-project
uvicorn backend.main:app --reload --port 8000
```

Output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

#### Terminal 2 - Start Frontend Server (Python SimpleHTTP)

```bash
cd student-kpi-project/frontend
python -m http.server 8080
```

Output:
```
Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/)
```

### Option 2: One-Command Setup (Windows)

Create a `run.bat` file in project root:

```batch
@echo off
start cmd /k "cd student-kpi-project && uvicorn backend.main:app --reload --port 8000"
start cmd /k "cd student-kpi-project/frontend && python -m http.server 8080"
echo.
echo ✅ Backend API: http://localhost:8000
echo ✅ Frontend: http://localhost:8080
echo ✅ API Docs: http://localhost:8000/docs
```

Run: `run.bat`

### Access the Application

- 🌐 **Frontend**: http://localhost:8080
- 🔗 **API Base**: http://localhost:8000
- 📚 **API Docs (Swagger)**: http://localhost:8000/docs
- 📋 **API Redoc**: http://localhost:8000/redoc

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|----------------|
| POST | `/api/auth/login` | Login and get JWT token | No |
| POST | `/api/auth/register` | Register new user | No |
| GET | `/api/auth/me` | Get current user info | Yes |

### Student Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|----------------|
| POST | `/api/student/add` | Add new student | Yes (Admin/Coordinator/Faculty) |
| GET | `/api/student/{student_id}` | Get student details | Yes |
| PUT | `/api/student/{student_id}` | Update student info | Yes (Admin/Coordinator) |
| GET | `/api/students` | List all students | Yes |
| DELETE | `/api/student/{student_id}` | Delete student | Yes (Admin) |

### KPI Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/kpi/add` | Add KPI data for student |
| PUT | `/api/kpi/{student_id}` | Update KPI data |
| GET | `/api/student/{student_id}/kpi` | Get KPI data |
| POST | `/api/kpi/upload` | Bulk upload KPI via CSV |

### Scores & Performance

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/student/{student_id}/score` | Get calculated score |
| POST | `/api/student/{student_id}/calculate-score` | Calculate and store score |

### Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/analytics/dashboard` | Dashboard analytics |
| GET | `/api/analytics/comparison/{student_id}` | Peer comparison |
| GET | `/api/analytics/trends/{student_id}` | Performance trends |

### Example API Call

```bash
# Login (No auth required)
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "password": "student123"
  }'

# Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "student@example.com",
    "name": "John Student",
    "role": "student",
    "department": "CSE"
  }
}

# Get student info (With auth)
curl -X GET http://localhost:8000/api/student/STU001 \
  -H "Authorization: Bearer <access_token>"
```

## 👥 User Roles & Permissions

### 1. **Student**
- ✅ View own profile and KPI data
- ✅ View own score and milestones
- ✅ View performance trends
- ✅ Compare with peer group

### 2. **Faculty**
- ✅ All Student permissions
- ✅ Add/Update students
- ✅ Add/Update KPI data
- ✅ Calculate scores
- ❌ Cannot delete students

### 3. **Coordinator**
- ✅ All Faculty permissions
- ✅ Bulk upload KPI data (CSV)
- ✅ Delete student data
- ✅ View analytics dashboard
- ✅ Generate reports

### 4. **Admin**
- ✅ All permissions
- ✅ User management
- ✅ System configuration
- ✅ Full access to all data

## 🛠️ Technologies Used

### Backend
| Technology | Purpose |
|-----------|---------|
| **FastAPI** | High-performance API framework |
| **SQLAlchemy** | ORM for database operations |
| **SQLite** | Lightweight database |
| **Pydantic** | Data validation |
| **PyJWT** | JWT token generation/validation |
| **bcrypt** | Password hashing |

### Frontend
| Technology | Purpose |
|-----------|---------|
| **HTML5** | Structure |
| **CSS3** | Styling & responsive design |
| **Vanilla JavaScript** | Interactivity |
| **Chart.js** | Data visualization |
| **Fetch API** | Backend communication |

### Additional
| Technology | Purpose |
|-----------|---------|
| **Python 3.8+** | Backend language |
| **Uvicorn** | ASGI server |

## 🔐 Demo Credentials

The system comes with 4 demo users for testing:

### Admin Account
```
Email: admin@example.com
Password: admin123
Role: admin
Department: Administration
```

### Coordinator Account
```
Email: coordinator@example.com
Password: coordinator123
Role: coordinator
Department: Academic Affairs
```

### Faculty Account
```
Email: faculty@example.com
Password: faculty123
Role: faculty
Department: CSE
```

### Student Account
```
Email: student@example.com
Password: student123
Role: student
Department: CSE
```

## 📊 KPI Metrics Tracked

1. **Internships** - Number of internships completed
2. **Certifications** - Professional certifications obtained
3. **Hackathons** - Hackathon participation
4. **Publications** - Research papers published
5. **Workshops** - Workshops attended/conducted
6. **Projects** - Projects completed
7. **Club Activities** - Leadership in clubs
8. **Industrial Visits** - Industry exposure
9. **Research Papers** - Research contribution
10. **Patents** - Patent applications/grants

## 📈 Dashboard Views (Role-Based)

### Student Dashboard
- Personal KPI overview
- Performance score and career readiness
- Peer comparison (percentile ranking)
- Milestone achievements
- Performance trends

### Faculty Dashboard
- Department statistics
- Student KPI management
- Score calculation
- Performance analytics
- Bulk data upload

### Coordinator Dashboard
- Complete department overview
- Student management
- Data quality monitoring
- Report generation
- System analytics

### Admin Dashboard
- System-wide analytics
- User management
- Department comparison
- Performance metrics
- Configuration settings

## 🐛 Troubleshooting

### Q: Port already in use
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (Windows)
taskkill /PID <PID> /F
```

### Q: Database locked error
```bash
# Delete the database and restart (it will recreate)
rm student_kpi.db
```

### Q: CORS errors
- Backend already has CORS enabled
- Frontend running on port 8080 is whitelisted

### Q: Login not working
- Check demo credentials above
- Verify backend is running on port 8000
- Check browser console for network errors

## 📝 Example Workflow

1. **Admin** logs in → Adds new students and faculty
2. **Faculty** logs in → Enters student KPI data
3. **Coordinator** logs in → Verifies data, generates reports
4. **Student** logs in → Views personal performance and comparison
5. **System** → Calculates scores, generates analytics

## 🔄 Development Roadmap

- [ ] Email notifications for milestones
- [ ] Advanced AI recommendations using LangChain
- [ ] Export reports to PDF
- [ ] Mobile app (React Native)
- [ ] Webhooks for external integrations
- [ ] Multi-tenancy support

---

**Last Updated**: 2024
**Version**: 1.0.0
**Status**: Production Ready ✅
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
