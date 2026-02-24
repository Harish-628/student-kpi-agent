"""
Comprehensive API routes for Student KPI Management System.
Includes authentication, student management, KPI tracking, analytics, and reporting.
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, Header
from sqlalchemy import func, desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from typing import List, Optional
import csv
import io
import json

from database.database import get_db
from database.models import Student, KPI, Score, User, Milestone, PerformanceHistory
from backend.schemas import (
    StudentCreate, StudentUpdate, StudentResponse,
    KPIAdd, KPIUpdate, KPIResponse,
    ScoreResponse, MilestoneCreate, MilestoneResponse,
    UserLoginRequest, UserLoginResponse, UserRegister, UserResponse,
    DepartmentStats, YearStats, AnalyticsResponse, ComparisonMetrics
)
from backend.auth import (
    hash_password, verify_password, create_access_token,
    decode_access_token, create_demo_users
)
from backend.kpi_engine import calculate_kpi_score, predict_career_readiness
from agent.langgraph_workflow import agent_workflow
from agent.recommendation_engine import recommendation_engine
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["api"])

class ChatQueryRequest(BaseModel):
    query: str
    user_id: str
    role: str

# ============ Mock User Database (Replace with real DB after setup) ============
MOCK_USERS = {}
for user in create_demo_users():
    MOCK_USERS[user['email']] = user


def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """Extract and validate current user from JWT token."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_data = payload.get("user")
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid token structure")
    
    # Return user info from payload
    return {
        "id": user_data.get("id"),
        "email": user_data.get("email"),
        "role": user_data.get("role"),
        "name": user_data.get("name"),
        "department": user_data.get("department")
    }


def check_role(required_role: str):
    """Dependency to check user role."""
    async def role_checker(current_user = Depends(get_current_user)):
        if current_user["role"] != required_role and current_user["role"] != "admin":
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return role_checker


# ============ Authentication Endpoints ============

@router.post("/auth/login", response_model=UserLoginResponse)
def login(request: UserLoginRequest, db: Session = Depends(get_db)):
    """
    Login with email and password.
    Returns JWT access token.
    """
    # Check mock users first
    user = MOCK_USERS.get(request.email)
    if not user or not verify_password(request.password, user['password_hash']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create JWT token
    token_data = {
        "sub": str(user['id']),
        "user": {
            "id": user['id'],
            "email": user['email'],
            "role": user['role'],
            "name": user['name'],
            "department": user.get('department')
        }
    }
    access_token = create_access_token(token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user['id'],
            "email": user['email'],
            "name": user['name'],
            "role": user['role'],
            "department": user.get('department')
        }
    }


@router.post("/auth/register", response_model=UserResponse)
def register(request: UserRegister, db: Session = Depends(get_db)):
    """Register a new user."""
    if request.email in MOCK_USERS:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_id = max([u['id'] for u in MOCK_USERS.values()]) + 1 if MOCK_USERS else 1
    new_user = {
        "id": user_id,
        "email": request.email,
        "password_hash": hash_password(request.password),
        "name": request.name,
        "role": request.role,
        "department": request.department,
        "is_active": True,
        "created_at": datetime.utcnow(),
        "last_login": None
    }
    
    MOCK_USERS[request.email] = new_user
    
    return {
        "id": new_user['id'],
        "email": new_user['email'],
        "name": new_user['name'],
        "role": new_user['role'],
        "department": new_user['department'],
        "is_active": new_user['is_active'],
        "created_at": new_user['created_at'],
        "last_login": new_user['last_login']
    }


@router.get("/auth/me", response_model=UserResponse)
def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current authenticated user information."""
    return current_user


# ============ Student Management Endpoints ============

@router.post("/student/add", response_model=StudentResponse)
def add_student(student: StudentCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Add a new student. Admin, HOD, Faculty only."""
    if current_user["role"] not in ["admin", "hod", "faculty"]:
        raise HTTPException(status_code=403, detail="Only admin/hod/faculty can add students")
    
    db_student = Student(**student.dict())
    db.add(db_student)
    try:
        db.commit()
        db.refresh(db_student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Student with this ID already exists")
    
    return db_student


@router.post("/student/upload")
async def upload_student_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Bulk upload students via CSV file."""
    if current_user["role"] not in ["admin", "hod"]:
        raise HTTPException(status_code=403, detail="Only admin/hod can bulk upload students")
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    contents = await file.read()
    csv_reader = csv.DictReader(io.StringIO(contents.decode('utf-8')))
    
    imported = 0
    failed = 0
    errors = []
    
    for row in csv_reader:
        try:
            student_id = row.get('student_id', '').strip()
            name = row.get('name', '').strip()
            if not student_id or not name:
                failed += 1
                errors.append(f"Row {row}: Missing required student_id or name")
                continue
                
            student_data = {
                'student_id': student_id,
                'name': name,
                'email': row.get('email', f"{student_id.lower()}@college.edu").strip(),
                'department': row.get('department', 'Computer Science & Engineering').strip(),
                'section': row.get('section', 'A').strip(),
                'year': int(row.get('year', 1) or 1),
                'gpa': float(row.get('gpa', 0.0) or 0.0),
                'enrollment_date': datetime.utcnow()
            }
            
            db_student = Student(**student_data)
            db.add(db_student)
            db.commit()
            imported += 1
        except IntegrityError:
            db.rollback()
            failed += 1
            errors.append(f"Student {student_id}: Already exists")
        except Exception as e:
            db.rollback()
            failed += 1
            errors.append(f"Student {student_id}: {str(e)}")
            
    return {
        "message": "Student CSV upload completed",
        "imported": imported,
        "failed": failed,
        "errors": errors if errors else []
    }



@router.get("/student/{student_id}", response_model=StudentResponse)
def get_student(student_id: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Retrieve student information."""
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Students can only view their own data
    # if current_user["role"] == "student":  # Will be enhanced with student_id mapping
    #     pass  # Implement student ID check
    
    return student


@router.put("/student/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: str,
    update_data: StudentUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update student information."""
    if current_user["role"] not in ["admin", "hod"]:
        raise HTTPException(status_code=403, detail="Only admin/hod can update students")
    
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    update_dict = update_data.dict(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(student, field, value)
    
    db.commit()
    db.refresh(student)
    return student


@router.get("/students", response_model=List[StudentResponse])
def list_students(
    department: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    skip: int = Query(0),
    limit: int = Query(100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """List students with optional filtering. Faculty and HODs only see their own department."""
    
    # Enforce department isolation for Faculty and HOD
    if current_user["role"] in ["faculty", "hod"]:
        department = current_user.get("department")
        
    query = db.query(Student)
    
    if department:
        query = query.filter(Student.department == department)
        
    if year:
        query = query.filter(Student.year == year)
    
    students = query.offset(skip).limit(limit).all()
    return students


@router.delete("/student/{student_id}")
def delete_student(
    student_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete a student and related data."""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete students")
    
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(student)
    db.commit()
    
    return {"message": f"Student {student_id} deleted successfully"}


# ============ KPI Management Endpoints ============

@router.post("/kpi/add", response_model=KPIResponse)
def add_kpi(
    kpi: KPIAdd,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Add KPI data for a student."""
    if current_user["role"] not in ["admin", "hod", "faculty"]:
        raise HTTPException(status_code=403, detail="Only admin/hod/faculty can add KPI")
    
    # Verify student exists
    student = db.query(Student).filter(Student.student_id == kpi.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if KPI already exists
    existing_kpi = db.query(KPI).filter(KPI.student_id == kpi.student_id).first()
    if existing_kpi:
        raise HTTPException(status_code=400, detail="KPI data for this student already exists. Use update instead.")
    
    db_kpi = KPI(**kpi.dict())
    db.add(db_kpi)
    db.commit()
    db.refresh(db_kpi)
    
    return db_kpi


@router.put("/kpi/{student_id}", response_model=KPIResponse)
def update_kpi(
    student_id: str,
    kpi_update: KPIUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update existing KPI data."""
    if current_user["role"] not in ["admin", "hod", "faculty"]:
        raise HTTPException(status_code=403, detail="Only admin/hod/faculty can update KPI")
    
    db_kpi = db.query(KPI).filter(KPI.student_id == student_id).first()
    if not db_kpi:
        raise HTTPException(status_code=404, detail="KPI data not found for this student")
    
    update_dict = kpi_update.dict(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(db_kpi, field, value)
    
    db_kpi.last_updated = datetime.utcnow()
    db.commit()
    db.refresh(db_kpi)
    
    return db_kpi


@router.get("/student/{student_id}/kpi", response_model=KPIResponse)
def get_student_kpi(student_id: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Retrieve KPI data for a student."""
    kpi = db.query(KPI).filter(KPI.student_id == student_id).first()
    if not kpi:
        raise HTTPException(status_code=404, detail="KPI data not found for this student")
    return kpi


@router.post("/kpi/upload")
async def upload_kpi_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Bulk upload KPI data via CSV file."""
    if current_user["role"] not in ["admin", "hod"]:
        raise HTTPException(status_code=403, detail="Only admin/hod can bulk upload")
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    contents = await file.read()
    csv_reader = csv.DictReader(io.StringIO(contents.decode('utf-8')))
    
    imported = 0
    failed = 0
    errors = []
    
    for row in csv_reader:
        try:
            kpi_data = {
                'student_id': row['student_id'],
                'internships': int(row.get('internships', 0)),
                'certifications': int(row.get('certifications', 0)),
                'hackathons': int(row.get('hackathons', 0)),
                'publications': int(row.get('publications', 0)),
                'workshops': int(row.get('workshops', 0)),
                'projects': int(row.get('projects', 0)),
                'club_activities': int(row.get('club_activities', 0)),
                'industrial_visits': int(row.get('industrial_visits', 0)),
            }
            
            db_kpi = KPI(**kpi_data)
            db.add(db_kpi)
            db.commit()
            imported += 1
        except IntegrityError:
            db.rollback()
            failed += 1
            errors.append(f"KPI for {row['student_id']}: Already exists")
        except Exception as e:
            db.rollback()
            failed += 1
            errors.append(f"Row {row.get('student_id', 'unknown')}: {str(e)}")
    
    return {
        "message": "CSV upload completed",
        "imported": imported,
        "failed": failed,
        "errors": errors if errors else []
    }


# ============ Score & Performance Endpoints ============

@router.get("/student/{student_id}/score", response_model=ScoreResponse)
def get_student_score(student_id: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Get calculated score for a student."""
    score = db.query(Score).filter(Score.student_id == student_id).first()
    if not score:
        raise HTTPException(status_code=404, detail="Score not found for this student")
    return score


@router.post("/student/{student_id}/calculate-score")
def calculate_and_store_score(
    student_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Calculate KPI score and store in database."""
    if current_user["role"] not in ["admin", "hod", "faculty"]:
        raise HTTPException(status_code=403, detail="Only admin/hod/faculty can calculate scores")
    
    kpi = db.query(KPI).filter(KPI.student_id == student_id).first()
    if not kpi:
        raise HTTPException(status_code=404, detail="KPI data not found for this student")
    
    # Convert KPI to dict
    kpi_dict = {
        'internships': kpi.internships,
        'certifications': kpi.certifications,
        'hackathons': kpi.hackathons,
        'publications': kpi.publications,
        'workshops': kpi.workshops,
        'projects': kpi.projects,
        'club_activities': kpi.club_activities,
        'industrial_visits': kpi.industrial_visits,
        'research_papers': kpi.research_papers,
        'patents': kpi.patents,
    }
    
    # Calculate scores
    kpi_score = calculate_kpi_score(kpi_dict)
    career_readiness = predict_career_readiness(kpi_score)
    
    # Store in Score table
    existing_score = db.query(Score).filter(Score.student_id == student_id).first()
    if existing_score:
        existing_score.kpi_score = kpi_score
        existing_score.career_readiness_score = career_readiness
        existing_score.overall_performance = kpi_score
    else:
        new_score = Score(
            student_id=student_id,
            kpi_score=kpi_score,
            career_readiness_score=career_readiness,
            overall_performance=kpi_score
        )
        db.add(new_score)
    
    db.commit()
    
    return {
        "student_id": student_id,
        "kpi_score": kpi_score,
        "career_readiness": career_readiness
    }


# ============ Milestone Endpoints ============

@router.post("/student/{student_id}/milestone", response_model=MilestoneResponse)
def add_milestone(
    student_id: str,
    milestone: MilestoneCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Add a milestone for a student."""
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db_milestone = Milestone(student_id=student_id, **milestone.dict())
    db.add(db_milestone)
    db.commit()
    db.refresh(db_milestone)
    return db_milestone


@router.get("/student/{student_id}/milestones", response_model=List[MilestoneResponse])
def get_milestones(
    student_id: str,
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get milestones for a student."""
    query = db.query(Milestone).filter(Milestone.student_id == student_id)
    if status:
        query = query.filter(Milestone.status == status)
    return query.all()


# ============ Analytics & Reporting Endpoints ============

@router.get("/analytics/dashboard")
def get_dashboard_analytics(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get analytics data for dashboard. Enforces department isolation for Faculty/HODs."""
    
    is_restricted = current_user["role"] in ["faculty", "hod"]
    user_dept = current_user.get("department")

    # Base query filter for isolation
    student_query = db.query(Student)
    if is_restricted:
        student_query = student_query.filter(Student.department == user_dept)
        
    total_students = student_query.count()
    
    # KPI Average
    kpi_query = db.query(func.avg(Score.kpi_score)).select_from(Student).join(Score, Student.student_id == Score.student_id)
    if is_restricted:
        kpi_query = kpi_query.filter(Student.department == user_dept)
    average_kpi = kpi_query.scalar() or 0
    
    # GPA Average
    gpa_query = db.query(func.avg(Student.gpa))
    if is_restricted:
        gpa_query = gpa_query.filter(Student.department == user_dept)
    average_gpa = gpa_query.scalar() or 0
    
    # Department stats
    dept_stats_query = db.query(
        Student.department,
        func.count(Student.student_id).label('count'),
        func.avg(Score.kpi_score).label('avg_kpi')
    ).outerjoin(Score)
    
    if is_restricted:
        dept_stats_query = dept_stats_query.filter(Student.department == user_dept)
        
    dept_stats = dept_stats_query.group_by(Student.department).all()
    
    # Get top performers
    top_performers_query = db.query(Student).join(Score, Student.student_id == Score.student_id)
    if is_restricted:
        top_performers_query = top_performers_query.filter(Student.department == user_dept)
        
    top_performers = top_performers_query.order_by(desc(Score.kpi_score)).limit(5).all()
    
    return {
        "total_students": total_students,
        "average_kpi": round(average_kpi, 2),
        "average_gpa": round(average_gpa, 2),
        "department_stats": [
            {
                "department": dept,
                "student_count": count,
                "average_kpi": round(avg_kpi or 0, 2)
            }
            for dept, count, avg_kpi in dept_stats
        ],
        "top_performers": [{
            "student_id": s.student_id,
            "name": s.name,
            "kpi_score": db.query(Score).filter(Score.student_id == s.student_id).first().kpi_score
        } for s in top_performers]
    }


@router.get("/analytics/comparison/{student_id}")
def get_peer_comparison(
    student_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Compare student performance with peers."""
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Get student's score
    student_score = db.query(Score).filter(Score.student_id == student_id).first()
    if not student_score:
        raise HTTPException(status_code=404, detail="Score not found for this student")
    
    # Get department peers
    dept_peers = db.query(Student).filter(Student.department == student.department).all()
    dept_total = len(dept_peers)
    
    # Calculate percentile
    better_performing = db.query(func.count(Score.student_id)).filter(
        Score.student_id.in_([p.student_id for p in dept_peers]),
        Score.kpi_score > student_score.kpi_score
    ).scalar()
    
    percentile = ((dept_total - better_performing) / dept_total * 100) if dept_total > 0 else 0
    
    return {
        "student_id": student_id,
        "student_name": student.name,
        "kpi_score": student_score.kpi_score,
        "department": student.department,
        "department_percentile": round(percentile, 2),
        "department_rank": dept_total - better_performing,
        "total_in_department": dept_total,
        "average_department_kpi": db.query(func.avg(Score.kpi_score)).filter(
            Score.student_id.in_([p.student_id for p in dept_peers])
        ).scalar() or 0
    }


@router.get("/analytics/trends/{student_id}")
def get_performance_trends(
    student_id: str,
    days: int = Query(90),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get performance trends for a student over time."""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    history = db.query(PerformanceHistory).filter(
        PerformanceHistory.student_id == student_id,
        PerformanceHistory.timestamp >= cutoff_date
    ).order_by(PerformanceHistory.timestamp).all()
    
    if not history:
        raise HTTPException(status_code=404, detail="No performance history found")
    
    scores = [h.kpi_score for h in history]
    dates = [h.timestamp.isoformat() for h in history]
    
    trend_direction = "up" if scores[-1] > scores[0] else "down" if scores[-1] < scores[0] else "stable"
    improvement_rate = ((scores[-1] - scores[0]) / scores[0] * 100) if scores[0] != 0 else 0
    
    return {
        "student_id": student_id,
        "dates": dates,
        "scores": scores,
        "trend_direction": trend_direction,
        "improvement_rate": round(improvement_rate, 2),
        "current_score": scores[-1],
        "starting_score": scores[0]
    }


# ============ AI Intelligence Endpoints ============

@router.post("/chatbot/query")
def process_chatbot_query(
    request: ChatQueryRequest,
    db: Session = Depends(get_db)
):
    """Processes queries via LangGraph and Gemini for intelligent KPI responses."""
    
    # In this app architecture, request.user_id from the frontend JWT is often the email or student ID.
    user_email = request.user_id 
    
    # If the student email is just an ID like 'cse001', format it into the generated college email
    if "@" not in user_email and request.role == "student":
        user_email = f"{user_email.lower()}@college.edu"

    # Prepare inputs for LangGraph
    initial_state = {
        "query": request.query,
        "user_role": request.role,
        "user_email": user_email,
        "context": "",
        "response": ""
    }
    
    # Run the agent workflow
    final_state = agent_workflow.invoke(initial_state)
    
    return {
        "response": final_state.get("response", "The Neural Agent failed to generate a response.")
    }

@router.get("/notifications")
def get_user_notifications(user_id: str, role: str):
    """
    Returns AI-generated notifications specifically tailored to the user's KPI performance.
    Admins get a static welcome message since they don't have KPIs.
    """
    if role == "admin":
        return [{
            "title": "System Online",
            "message": "Welcome Admin! Your NeuralKPI platform is operating normally."
        }]
    
    # Generate insights for Faculty/HOD/Students
    try:
        notifications = recommendation_engine.generate_kpi_notifications(user_id, role)
        return notifications
    except Exception as e:
        return [{
            "title": "Notification Engine Offline",
            "message": f"Could not generate insights: {str(e)}"
        }]

# ============ Health Check ============

@router.get("/")
def health_check():
    """API health check endpoint."""
    return {
        "status": "ok",
        "message": "Student KPI API is running!",
        "timestamp": datetime.utcnow().isoformat()
    }
