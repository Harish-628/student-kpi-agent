# Complete Setup Guide - Student KPI Management System

This guide will walk you through setting up and running the entire Student KPI Management System with backend API, database, and frontend.

## 📋 Prerequisites

- **Python 3.8+** - Download from [python.org](https://www.python.org/downloads/)
- **Terminal/Command Prompt** - PowerShell (Windows) or bash (macOS/Linux)
- **2 GB RAM** minimum
- **Internet connection** for initial setup

## 🚀 Step 1: Environment Setup (5 minutes)

### 1.1 Navigate to Project Directory

```bash
cd d:\student-kpi-project
```

### 1.2 Create Python Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 1.3 Install Dependencies

```bash
pip install -r requirements.txt
```

This will take 2-3 minutes. Wait for completion.

**Expected output:**
```
Successfully installed fastapi-0.104.1 uvicorn-0.24.0 sqlalchemy-2.0.23 ...
```

## 🗄️ Step 2: Database Initialization (1 minute)

The database is automatically created when you first run the backend. No manual steps needed!

**What happens automatically:**
- SQLite database `student_kpi.db` is created
- 7 tables (User, Student, KPI, Score, Milestone, PerformanceHistory, etc.) are created
- Demo users are initialized

## 🔧 Step 3: Start Backend Server (Separate Terminal)

### 3.1 Open New Terminal/Command Prompt

Keep the previous terminal with virtual environment open, and open a new one.

### 3.2 Activate Virtual Environment in New Terminal

```bash
cd d:\student-kpi-project

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3.3 Start FastAPI Backend

```bash
uvicorn backend.main:app --reload --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete
```

**Keep this terminal open!** The backend is now running.

### 3.4 Verify Backend is Working

Open browser: http://localhost:8000/
You should see: `{"status":"ok","message":"Student KPI Management API is running!",...}`

## 🖥️ Step 4: Start Frontend Server (Third Terminal)

### 4.1 Open Another New Terminal

Keep previous terminals running.

### 4.2 Activate Virtual Environment

```bash
cd d:\student-kpi-project

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 4.3 Navigate to Frontend Folder

```bash
cd frontend
```

### 4.4 Start Python Simple HTTP Server

```bash
python -m http.server 8080
```

**Expected output:**
```
Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
```

**Keep this terminal open!** The frontend is now running.

## 🌐 Step 5: Access the Application

Open your web browser and navigate to:

### **Frontend (Main Application)**
```
http://localhost:8080
```

### **API Documentation (Swagger UI)**
```
http://localhost:8000/docs
```

### **Alternative API Docs (ReDoc)**
```
http://localhost:8000/redoc
```

### **API Health Check**
```
http://localhost:8000/
```

## 🔐 Step 6: Login with Demo Credentials

Use these credentials to log in:

### Option 1: Student Account
- **Email:** `student@example.com`
- **Password:** `student123`
- **Role:** Student
- **Department:** CSE

### Option 2: Admin Account
- **Email:** `admin@example.com`
- **Password:** `admin123`
- **Role:** Admin

### Option 3: Faculty Account
- **Email:** `faculty@example.com`
- **Password:** `faculty123`
- **Role:** Faculty

### Option 4: Coordinator Account
- **Email:** `coordinator@example.com`
- **Password:** `coordinator123`
- **Role:** Coordinator

## 📊 Step 7: Explore the System

### Student Dashboard (Login as Student)
1. Click "Login" on the frontend
2. Enter student@example.com / student123
3. View your KPI metrics
4. Check your performance score
5. Compare with peers
6. View milestones

### Admin/Coordinator Dashboard (Login as Admin)
1. Use admin@example.com / admin123
2. Add new students
3. Upload KPI data
4. View department statistics
5. Generate analytics reports

### Faculty Dashboard (Login as Faculty)
1. Use faculty@example.com / faculty123
2. Adding student KPI data
3. View class performance
4. Calculate scores

## 📝 Step 8: Testing the API

### Using Browser (Swagger UI)
1. Go to http://localhost:8000/docs
2. All endpoints are documented and testable
3. Click on any endpoint to expand
4. Click "Try it out"
5. Fill in parameters and click "Execute"

### Using Command Line (cURL)

```bash
# Login and get JWT token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"student@example.com","password":"student123"}'

# Response will include access_token
# Copy the token and use in next request

# Get current user (replace TOKEN with actual token)
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer TOKEN"

# Get dashboard analytics
curl -X GET http://localhost:8000/api/analytics/dashboard \
  -H "Authorization: Bearer TOKEN"
```

## 🛠️ Troubleshooting

### Port Already in Use

If you see "Address already in use" error:

**Windows:**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID 1234 /F
```

**macOS/Linux:**
```bash
# Find process
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Virtual Environment Issues

If `(venv)` doesn't appear in terminal:

```bash
# Windows - Try full path
d:\student-kpi-project\venv\Scripts\activate.bat

# Make sure you're in the right directory
cd d:\student-kpi-project
```

### Database Locked Error

If you see "database is locked":

```bash
# Stop all running instances
# Then delete the database (it will be recreated)
rm student_kpi.db

# Or Windows:
del student_kpi.db

# Restart backend
```

### Can't Connect to Backend

1. Verify terminal 2 is still running (backend process)
2. Check http://localhost:8000 shows a response
3. Make sure all dependencies installed: `pip install -r requirements.txt`
4. Restart the backend server

### Frontend Shows Blank Page

1. Try hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
2. Check browser console for errors: Press `F12`
3. Verify frontend server is running (terminal 3)
4. Check files exist in `friend/` folder

## ✅ Quick Verification Checklist

- [ ] Python virtual environment activated (see `(venv)` in prompt)
- [ ] Backend server running on http://localhost:8000
- [ ] Frontend server running on http://localhost:8080
- [ ] Can access http://localhost:8080 in browser
- [ ] Can login with demo credentials
- [ ] Database file exists: `student_kpi.db`
- [ ] API documentation accessible: http://localhost:8000/docs

## 🎯 Next Steps

### For Development
1. Modify frontend files in `frontend/` folder - changes auto-refresh in browser
2. Modify backend in `backend/` folder - `--reload` flag auto-restarts server
3. Check API docs at http://localhost:8000/docs

### For Data Import
1. Use CSV upload feature in coordinator dashboard
2. Or use `/api/kpi/upload` endpoint with CSV file

### For Advanced Features
- Edit `backend/kpi_engine.py` for custom KPI algorithms
- Edit `backend/auth.py` for additional authentication logic
- Extend database models in `database/models.py`

## 📚 File Structure Reference

```
d:\student-kpi-project/
├── venv/                      # Virtual environment (created)
├── student_kpi.db             # SQLite database (created on first run)
├── backend/
│   ├── main.py               # API entry point ← START HERE
│   ├── auth.py               # Authentication logic
│   ├── kpi_engine.py         # KPI calculations
│   ├── schemas.py            # Data schemas
│   ├── api/
│   │   └── routes.py         # All API endpoints
│   └── __pycache__/
├── database/
│   ├── database.py           # DB configuration
│   ├── models.py             # Database models
│   └── __pycache__/
├── frontend/                 # Web frontend
│   ├── index.html            # Login page
│   ├── dashboard.html        # Main dashboard
│   ├── auth.js               # Login logic
│   ├── dashboard.js          # Dashboard logic
│   └── styles.css            # Global styling
├── requirements.txt          # Python packages
├── README.md                 # Full documentation
└── SETUP_GUIDE.md           # This file
```

## 🔍 API Endpoints Overview

### Authentication
- `POST /api/auth/login` - Login
- `POST /api/auth/register` - Register
- `GET /api/auth/me` - Current user

### Students
- `POST /api/student/add` - Add student
- `GET /api/student/{id}` - Get student
- `GET /api/students` - List students

### KPI
- `POST /api/kpi/add` - Add KPI
- `GET /api/student/{id}/kpi` - Get KPI
- `PUT /api/kpi/{id}` - Update KPI

### Analytics
- `GET /api/analytics/dashboard` - Dashboard stats
- `GET /api/analytics/comparison/{id}` - Peer comparison
- `GET /api/analytics/trends/{id}` - Performance trends

For complete API documentation, visit: http://localhost:8000/docs

## 💡 Pro Tips

1. **Auto-reload Development**: Backend with `--reload` flag auto-restarts on code changes
2. **Clear Browser Cache**: If frontend acts weird, do Ctrl+Shift+Delete and clear cache
3. **Keep Terminals Open**: Don't close the terminal windows while running
4. **Copy Token for Testing**: In Swagger UI, you can get a token from `/auth/login` endpoint and use it for subsequent calls
5. **Monitor Logs**: Keep an eye on the backend terminal output for debugging

## 📞 Need Help?

If you encounter issues:

1. **Check the README.md** - More detailed documentation
2. **API Docs** - http://localhost:8000/docs - Interactive testing
3. **Check Database** - Verify `student_kpi.db` exists
4. **Terminal Output** - Look for error messages in the backend terminal
5. **Browser Console** - Press F12 in browser for JavaScript errors

---

**Congratulations! 🎉** 

Your Student KPI Management System is now up and running!

For more information, see [README.md](README.md)
