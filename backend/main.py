from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database.database import engine, Base
from backend.api import routes
import os
from datetime import datetime

# This automatically creates your database tables!
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student KPI Management System API",
    description="Comprehensive API for managing student KPIs, authentication, analytics, and reporting",
    version="1.0.0"
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connects the API routes
app.include_router(routes.router)

@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "Student KPI Management API is running!",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@app.get("/docs-custom")
def get_api_info():
    """Get API documentation and available endpoints."""
    return {
        "api_name": "Student KPI Management System",
        "version": "1.0.0",
        "description": "Full-featured API for student KPI tracking with authentication and analytics",
        "endpoints": {
            "authentication": [
                {"method": "POST", "path": "/api/auth/login", "description": "Login with email/password"},
                {"method": "POST", "path": "/api/auth/register", "description": "Register new user"},
                {"method": "GET", "path": "/api/auth/me", "description": "Get current user info"}
            ],
            "student_management": [
                {"method": "POST", "path": "/api/student/add", "description": "Add new student"},
                {"method": "GET", "path": "/api/student/{student_id}", "description": "Get student info"},
                {"method": "PUT", "path": "/api/student/{student_id}", "description": "Update student"},
                {"method": "GET", "path": "/api/students", "description": "List students with filters"},
                {"method": "DELETE", "path": "/api/student/{student_id}", "description": "Delete student"}
            ],
            "kpi_management": [
                {"method": "POST", "path": "/api/kpi/add", "description": "Add KPI data"},
                {"method": "PUT", "path": "/api/kpi/{student_id}", "description": "Update KPI"},
                {"method": "GET", "path": "/api/student/{student_id}/kpi", "description": "Get KPI data"},
                {"method": "POST", "path": "/api/kpi/upload", "description": "Bulk upload KPI CSV"}
            ],
            "scores_performance": [
                {"method": "GET", "path": "/api/student/{student_id}/score", "description": "Get student score"},
                {"method": "POST", "path": "/api/student/{student_id}/calculate-score", "description": "Calculate score"}
            ],
            "milestones": [
                {"method": "POST", "path": "/api/student/{student_id}/milestone", "description": "Add milestone"},
                {"method": "GET", "path": "/api/student/{student_id}/milestones", "description": "Get milestones"}
            ],
            "analytics": [
                {"method": "GET", "path": "/api/analytics/dashboard", "description": "Get dashboard analytics"},
                {"method": "GET", "path": "/api/analytics/comparison/{student_id}", "description": "Get peer comparison"},
                {"method": "GET", "path": "/api/analytics/trends/{student_id}", "description": "Get performance trends"}
            ]
        },
        "authentication": {
            "type": "JWT Bearer Token",
            "header": "Authorization: Bearer {token}",
            "expiry": "30 minutes"
        },
        "roles": ["student", "faculty", "coordinator", "admin"],
        "base_url": "http://localhost:8000"
    }