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
import requests
import os
from backend.security.ela import analyze_image_tampering

from database.database import get_db
from database.models import Student, KPI, Score, Milestone, PerformanceHistory, EventCache, CertificateUpload
from backend.schemas import (
    StudentCreate, StudentUpdate, StudentResponse,
    KPIAdd, KPIUpdate, KPIResponse, CertificateManualUpload,
    ScoreResponse, MilestoneCreate, MilestoneResponse,
    UserLoginRequest, UserLoginResponse, UserRegister, UserResponse
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
    image: Optional[str] = None

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
    
    # Record last_login timestamp
    user['last_login'] = datetime.utcnow()
    
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


class CertificateVerifyRequest(BaseModel):
    image: str

# ============ KPI Management Endpoints ============

@router.post("/kpi/verify-certificate")
def verify_certificate_upload(request: CertificateVerifyRequest):
    """
    Validates manual certificate uploads using ELA tamper detection.
    Called from the frontend before processing the KPI addition.
    """
    try:
        ela_result = analyze_image_tampering(request.image)
        return {
            "is_suspicious": ela_result["is_suspicious"],
            "score": ela_result["score"],
            "message": ela_result["message"]
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "is_suspicious": False, 
            "score": 0, 
            "message": f"System validation error: {str(e)}"
        }

@router.post("/kpi/upload-document")
def upload_manual_certificate(
    upload: CertificateManualUpload,
    db: Session = Depends(get_db)
):
    """
    Handles student manual certificate uploads.
    Saves the Base64 image to the CertificateUpload table and increments the respective KPI.
    """
    # Verify student exists
    student = db.query(Student).filter(Student.student_id == upload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # 1. Save certificate to DB
    doc = CertificateUpload(
        student_id=upload.student_id,
        category=upload.category,
        file_path=upload.image,  # Storing the base64 string directly in file_path
        upload_date=datetime.utcnow()
    )
    db.add(doc)

    # 2. Increment KPI count category
    kpi_row = db.query(KPI).filter(KPI.student_id == upload.student_id).first()
    if not kpi_row:
        # Create an empty KPI row if the student doesn't have one yet
        kpi_row = KPI(student_id=upload.student_id)
        db.add(kpi_row)
        db.flush()
    
    if hasattr(kpi_row, upload.category):
        current_val = getattr(kpi_row, upload.category) or 0
        setattr(kpi_row, upload.category, current_val + 1)
        kpi_row.last_updated = datetime.utcnow()
        
    db.commit()
    
    # 3. Recalculate and store the score inline (cannot call route handler directly)
    try:
        kpi_row_fresh = db.query(KPI).filter(KPI.student_id == upload.student_id).first()
        if kpi_row_fresh:
            kpi_dict = {
                'internships': kpi_row_fresh.internships or 0,
                'certifications': kpi_row_fresh.certifications or 0,
                'hackathons': kpi_row_fresh.hackathons or 0,
                'publications': kpi_row_fresh.publications or 0,
                'workshops': kpi_row_fresh.workshops or 0,
                'projects': kpi_row_fresh.projects or 0,
                'club_activities': kpi_row_fresh.club_activities or 0,
                'industrial_visits': kpi_row_fresh.industrial_visits or 0,
                'research_papers': kpi_row_fresh.research_papers or 0,
            }
            kpi_score = calculate_kpi_score(kpi_dict)
            career_readiness = predict_career_readiness(kpi_score)

            existing_score = db.query(Score).filter(Score.student_id == upload.student_id).first()
            if existing_score:
                existing_score.kpi_score = kpi_score
                existing_score.career_readiness_score = career_readiness
                existing_score.overall_performance = kpi_score
            else:
                db.add(Score(
                    student_id=upload.student_id,
                    kpi_score=kpi_score,
                    career_readiness_score=career_readiness,
                    overall_performance=kpi_score
                ))
            db.commit()
    except Exception:
        # Non-critical: don't fail the whole upload if score calc breaks
        pass

    return {"message": f"Successfully uploaded {upload.category} document", "status": "success"}


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


@router.get("/student/{student_id}/documents/{category}")
def list_student_documents(
    student_id: str,
    category: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """List all uploaded certificates for a student in a given KPI category."""
    docs = (
        db.query(CertificateUpload)
        .filter(
            CertificateUpload.student_id == student_id,
            CertificateUpload.category == category
        )
        .order_by(CertificateUpload.upload_date.desc())
        .all()
    )
    return [
        {
            "id": d.id,
            "student_id": d.student_id,
            "category": d.category,
            "file_path": d.file_path,
            "upload_date": d.upload_date.isoformat() if d.upload_date else None,
            "filename": d.file_path.split("/")[-1] if d.file_path else f"document_{d.id}"
        }
        for d in docs
    ]


@router.delete("/documents/{doc_id}")
def delete_student_document(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete a specific uploaded certificate by its ID. Faculty/HOD/Admin only."""
    if current_user["role"] not in ["admin", "hod", "faculty"]:
        raise HTTPException(status_code=403, detail="Only faculty/HOD/admin can delete certificates")

    doc = db.query(CertificateUpload).filter(CertificateUpload.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    student_id = doc.student_id
    category = doc.category

    # Remove the physical file if it exists on disk
    import os as _os
    if doc.file_path and _os.path.exists(doc.file_path):
        try:
            _os.remove(doc.file_path)
        except Exception:
            pass

    db.delete(doc)

    # Decrement the KPI count for this category
    kpi_row = db.query(KPI).filter(KPI.student_id == student_id).first()
    if kpi_row and hasattr(kpi_row, category):
        current_val = getattr(kpi_row, category, 0) or 0
        setattr(kpi_row, category, max(0, current_val - 1))
        kpi_row.last_updated = datetime.utcnow()

    db.commit()
    return {"message": f"Document {doc_id} deleted and KPI '{category}' decremented for {student_id}"}


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

class IdeaEnhancerRequest(BaseModel):
    idea: str
    user_id: str

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

    # ELA Tamper Detection Step
    ela_status_msg = ""
    if request.image:
        try:
            ela_result = analyze_image_tampering(request.image)
            
            # Immediate Rejection if highly tampered
            if ela_result["is_suspicious"]:
                return {
                    "response": f"🚨 **Security Alert: Image Rejected**\n\nThe uploaded document failed our Error Level Analysis (ELA) integrity check with a Tamper Score of {ela_result['score']}.\n\n{ela_result['message']}\n\nPlease upload an original, unmodified certificate."
                }
                
            ela_status_msg = f"[System Note: ELA Integrity Check Passed (Score: {ela_result['score']}). {ela_result['message']}]"
        except Exception:
            import traceback
            traceback.print_exc()
            raise

    # Prepare inputs for LangGraph
    initial_state = {
        "query": request.query,
        "user_role": request.role,
        "user_email": user_email,
        "context": ela_status_msg,
        "response": "",
        "image": request.image or ""
    }
    
    # Run the agent workflow
    final_state = agent_workflow.invoke(initial_state)
    
    return {
        "response": final_state.get("response", "The Neural Agent failed to generate a response.")
    }

@router.post("/idea-enhancer")
def enhance_student_idea(
    request: IdeaEnhancerRequest,
    db: Session = Depends(get_db)
):
    """
    Critiques a student's project idea or blog post draft based on the Idea Enhancer logic.
    """
    if not request.idea or len(request.idea.strip()) < 5:
        raise HTTPException(status_code=400, detail="Idea is too short to analyze.")
        
    critique = recommendation_engine.enhance_idea(request.idea)
    return {"critique": critique}

@router.post("/extract-pdf")
async def extract_pdf_text(file: UploadFile = File(...)):
    """
    Server-side PDF text extraction.
    Accepts a PDF file upload and returns the extracted text content.
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    try:
        import PyPDF2
        import io
        
        content = await file.read()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
        
        full_text = ""
        max_pages = min(len(pdf_reader.pages), 10)  # Limit to first 10 pages
        for i in range(max_pages):
            page = pdf_reader.pages[i]
            page_text = page.extract_text() or ""
            full_text += page_text + "\n"
        
        # Trim to reasonable length for AI context
        extracted = full_text.strip()[:8000]
        
        return {"text": extracted, "pages": max_pages, "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract PDF text: {str(e)}")

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

@router.get("/notifications/engagement")
def get_engagement_notifications(user_id: str, role: str):
    """
    Returns motivational notifications for students who have been inactive for 2+ days.
    Checks last_login from MOCK_USERS.
    """
    if role != "student":
        return []
    
    # Find the user's last_login
    user_email = user_id
    if "@" not in user_email:
        user_email = f"{user_email.lower()}@college.edu"
    
    user = MOCK_USERS.get(user_email)
    if not user:
        return []
    
    last_login = user.get('last_login')
    if not last_login:
        # Never logged in before (or first login) — treat as inactive
        return [{
            "title": "⚡ Welcome Back!",
            "message": "- You're just two steps away from your target! 🎯\n- Upload a certificate or complete a hackathon to boost your KPI.\n- Your peers are making progress — don't fall behind!",
            "type": "engagement"
        }]
    
    days_inactive = (datetime.utcnow() - last_login).days
    
    if days_inactive >= 2:
        # Generate a motivational notification using the recommendation engine
        try:
            engagement = recommendation_engine.generate_engagement_notification(user_id)
            return engagement
        except Exception:
            return [{
                "title": "⚡ We Miss You!",
                "message": f"- You've been away for {days_inactive} days!\n- You're just two steps away from the target! 🎯\n- Come back and upload a certificate to boost your KPI score!",
                "type": "engagement"
            }]
    
    return []

@router.get("/notifications/realtime")
def get_realtime_notifications(user_id: str, role: str, db: Session = Depends(get_db)):
    """
    Returns WhatsApp-style real-time notifications (OD Request updates + Inactivity).
    """
    notifications = []
    
    # Check Inactivity (Student only)
    if role == "student":
        user_email = user_id if "@" in user_id else f"{user_id.lower()}@college.edu"
        user = MOCK_USERS.get(user_email)
        if user and user.get("last_login"):
            from datetime import datetime
            days_inactive = (datetime.utcnow() - user.get("last_login")).days
            if days_inactive >= 2:
                notifications.append({
                    "title": "Inactivity Alert \u23f0",
                    "message": f"You haven't logged any new KPIs in {days_inactive} days. Keep your streak alive!",
                    "type": "alert",
                    "timestamp": "Just now"
                })

    # Fetch OD Requests Status
    from database.models import ODRequest
    from datetime import datetime
    
    if role == "student":
        safe_student_id = user_id.upper().split("@")[0]
        # Get active or recently processed OD requests (not just submitted yesterday)
        ods = db.query(ODRequest).filter(
            ODRequest.student_id == safe_student_id,
            ODRequest.result_status != "Pending Result"
        ).order_by(ODRequest.id.desc()).limit(10).all()
        
        for od in ods:
            icon = "✅" if od.result_status in ["Won", "Participated"] else "⏳"
            action_html = ""
            
            # If the cron job marked it as needing proof, give them quick links to verify or claim prize
            if od.result_status == "Awaiting Proof":
                action_html = f'''
                <div style="margin-top:8px; display:flex; gap:8px;">
                    <a href="?action=verify_participation&od_id={od.id}" class="btn btn-outline-cyan btn-sm" style="font-size:0.7rem; padding: 4px 8px;">✔️ Verify</a>
                    <a href="?action=claim_prize&od_id={od.id}" class="btn btn-solid-cyan btn-sm" style="font-size:0.7rem; padding: 4px 8px;">🏆 Claim Prize</a>
                </div>
                '''
            
            notifications.append({
                "title": f"OD Event Ended {icon}",
                "message": f"Your OD request for '{od.event_details}' has concluded. Status: {od.result_status}." + action_html,
                "type": "od",
                "timestamp": f"For {od.date}"
            })
            
    elif role in ["faculty", "hod"]:
        # Get pending OD requests for their department
        ods = db.query(ODRequest).filter(ODRequest.result_status == "Pending Result").order_by(ODRequest.id.desc()).all()
        for od in ods:
            notifications.append({
                "title": "New OD Request 📩",
                "message": f"{od.student_name} ({od.student_id}) requested OD for '{od.event_details}'.",
                "type": "od",
                "timestamp": f"For {od.date}"
            })
            
    return notifications

@router.get("/events")
def get_upcoming_events(user_id: str, db: Session = Depends(get_db)):
    """
    Fetches upcoming college events from SerpApi based on the student's weakest KPI area.
    Results are cached in the database for 24 hours to minimize API usage.
    """
    if user_id == "admin":
        return {"events": [], "source": "admin", "query": ""}
        
    student = db.query(Student).filter(Student.student_id == user_id).first()
    search_query = "upcoming college tech events"
    
    if student and student.kpis:
        dept_name = student.department
        kpi = student.kpis
        areas = {
            "hackathons": kpi.hackathons,
            "workshops": kpi.workshops,
            "certifications": kpi.certifications,
            "internships": kpi.internships
        }
        weakest = min(areas, key=areas.get)
        search_query = f"upcoming college {weakest} {dept_name}"
    
    # Check Cache
    cached = db.query(EventCache).filter(EventCache.query == search_query).first()
    if cached:
        # Check if cache is < 24 hours old
        if datetime.utcnow() - cached.last_fetched < timedelta(hours=24):
            return {"events": cached.event_data, "source": "cache", "query": search_query}
            
    # Fetch from SerpApi
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        if cached:
             return {"events": cached.event_data, "source": "stale_cache", "query": search_query}
        return {"events": [], "source": "error", "query": search_query, "error": "No SERPAPI_API_KEY"}
        
    try:
        params = {
            "engine": "google_events",
            "q": search_query,
            "api_key": api_key,
            "hl": "en",
            "gl": "us"
        }
        res = requests.get("https://serpapi.com/search.json", params=params)
        res.raise_for_status()
        data = res.json()
        
        events_list = data.get("events_results", [])
        
        # Fallback if SerpApi returns 0 events for the specific query/location
        if not events_list:
            events_list = [
                {
                    "title": "Global Tech Summit 2026",
                    "date": {"when": "Next Friday"},
                    "link": "https://example.com/tech-summit",
                    "thumbnail": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=300&q=80"
                },
                {
                    "title": "Regional AI Hackathon",
                    "date": {"when": "Next Month"},
                    "link": "https://example.com/ai-hack",
                    "thumbnail": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=300&q=80"
                },
                {
                    "title": "Innovators Career Fair",
                    "date": {"when": "In 2 Weeks"},
                    "link": "https://example.com/career-fair",
                    "thumbnail": "https://images.unsplash.com/photo-1556761175-5973dc0f32b7?w=300&q=80"
                }
            ]
        
        # Save to Cache
        if cached:
            cached.event_data = events_list
            cached.last_fetched = datetime.utcnow()
        else:
            new_cache = EventCache(query=search_query, event_data=events_list)
            db.add(new_cache)
        db.commit()
        
        return {"events": events_list, "source": "api", "query": search_query}
        
    except Exception as e:
        print(f"SerpApi Error: {e}")
        if cached:
             return {"events": cached.event_data, "source": "stale_cache", "query": search_query}
        return {"events": [], "source": "error", "query": search_query, "error": str(e)}

# ============ Health Check ============

@router.get("/")
def health_check():
    """API health check endpoint."""
    return {
        "status": "ok",
        "message": "Student KPI API is running!",
        "timestamp": datetime.utcnow().isoformat()
    }


# ============ Neural Live — Voice AI ============

class NeuralLiveRequest(BaseModel):
    query: str
    user_id: str = "user"
    role: str = "student"

@router.post("/neural-live")
async def neural_live(request: NeuralLiveRequest, db: Session = Depends(get_db)):
    """
    Voice-to-voice AI endpoint for Neural Live.
    Receives a transcribed voice query and returns a concise,
    spoken-language AI response.
    """
    print(f"[Neural Live] Received query from user_id='{request.user_id}' role='{request.role}': {request.query[:80]}")
    try:
        # Build a context-aware prompt depending on the user's role
        role_context = {
            "student":  "You are Neural, a personal AI academic coach speaking directly to a student. Be encouraging and concise.",
            "faculty":  "You are Neural, an AI assistant for faculty. Be professional and data-driven. Stay concise.",
            "hod":      "You are Neural, a strategic AI advisor for a Head of Department. Be analytical. Stay concise.",
            "admin":    "You are Neural, a system AI for an administrator. Be clear and factual. Stay concise.",
        }.get(request.role, "You are Neural, an AI assistant. Be concise.")

        full_query = f"{role_context}\n\nUser said: {request.query}\n\nReply in 2-3 short sentences suitable for text-to-speech."

        # FIXED: AgentState expects 'user_role' and 'user_email', NOT 'role'/'user_id'
        # Also supply 'context' and 'response' defaults so nodes never hit a KeyError
        invoke_input = {
            "query":      full_query,
            "user_role":  request.role,          # was incorrectly 'role'
            "user_email": request.user_id,        # was incorrectly 'user_id'
            "context":    "",                     # will be filled by retrieve_vector_context_node
            "response":   "",                     # will be filled by generate_response_node
            "image":      None
        }
        print(f"[Neural Live] Invoking agent_workflow with keys: {list(invoke_input.keys())}")

        # Route through the existing LangGraph agent workflow
        result = await agent_workflow.ainvoke(invoke_input)
        print(f"[Neural Live] agent_workflow returned keys: {list(result.keys()) if isinstance(result, dict) else type(result)}")

        response_text = (
            result.get("response") if isinstance(result, dict) else None
        ) or "I'm here to help. Could you rephrase your question?"

        # Strip markdown — TTS works better with plain sentences
        import re
        response_text = re.sub(r"\*\*?|__?|#+\s?|`", "", str(response_text))
        response_text = response_text.replace("\n", " ").strip()
        if len(response_text) > 600:
            response_text = response_text[:600].rsplit(" ", 1)[0] + "."

        print(f"[Neural Live] Sending response ({len(response_text)} chars)")
        return {"response": response_text, "user_id": request.user_id, "role": request.role}

    except Exception as e:
        import traceback
        error_msg = str(e)
        print(f"[Neural Live ERROR] Exception type: {type(e).__name__}")
        print(f"[Neural Live ERROR] Message: {error_msg}")
        print(f"[Neural Live ERROR] Traceback:\n{traceback.format_exc()}")
        
        # Role-aware fallback + raw error for debugging (as requested by user)
        fallbacks = {
            "student": "I'm analysing your KPI profile. Try asking me about your certifications or internships.",
            "faculty": "I can help you review student performance metrics. Try asking about top performers.",
            "hod":     "I can provide department-level insights. Ask me about department averages or trends.",
            "admin":   "System is operational. Ask me about overall KPI statistics or student counts.",
        }
        fallback_res = fallbacks.get(request.role, "Neural Live is ready. How can I assist you today?")
        
        # Appending actual error for explicit exposure
        final_res = f"{fallback_res}\n\n[DEBUG ERROR]: {error_msg}"
        
        return {"response": final_res, "user_id": request.user_id, "role": request.role}
