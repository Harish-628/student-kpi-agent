from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.database import get_db
from database.models import Student, KPI, Score
from backend.schemas import StudentCreate, KPIAdd
from backend.kpi_engine import calculate_kpi_score, predict_career_readiness
import csv
import io

router = APIRouter()

@router.post("/student/add")
def add_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(**student.dict())
    db.add(db_student)
    try:
        db.commit()
        db.refresh(db_student)
    except IntegrityError:
        db.rollback()
        # student_id must be unique
        raise HTTPException(status_code=400, detail="Student with this ID already exists")
    return {"message": "Student added successfully", "student": db_student}

@router.post("/kpi/add")
def add_kpi(kpi: KPIAdd, db: Session = Depends(get_db)):
    db_kpi = KPI(**kpi.dict())
    db.add(db_kpi)
    try:
        db.commit()
        db.refresh(db_kpi)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="KPI data for this student already exists")
    return {"message": "KPI data added successfully"}

@router.post("/kpi/upload")
async def upload_kpi_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload KPI data via CSV file.
    Expected CSV columns: student_id, internships, certifications, hackathons, publications, 
    workshops, projects, club_activities, industrial_visits
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    contents = await file.read()
    csv_reader = csv.DictReader(io.StringIO(contents.decode('utf-8')))
    
    imported = 0
    failed = 0
    errors = []
    
    for row in csv_reader:
        try:
            # Convert string values to integers
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
            errors.append(f"Row {row['student_id']}: KPI data already exists")
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

@router.get("/student/{student_id}")
def get_student(student_id: str, db: Session = Depends(get_db)):
    """Retrieve student information"""
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.get("/student/{student_id}/kpi")
def get_student_kpi(student_id: str, db: Session = Depends(get_db)):
    """Retrieve KPI data for a student"""
    kpi = db.query(KPI).filter(KPI.student_id == student_id).first()
    if not kpi:
        raise HTTPException(status_code=404, detail="KPI data not found for this student")
    return kpi

@router.get("/student/{student_id}/kpi_score")
def get_kpi_score(student_id: str, db: Session = Depends(get_db)):
    """Calculate and return KPI score for a student"""
    kpi = db.query(KPI).filter(KPI.student_id == student_id).first()
    if not kpi:
        raise HTTPException(status_code=404, detail="KPI data not found for this student")
    
    kpi_dict = {
        'internships': kpi.internships,
        'certifications': kpi.certifications,
        'hackathons': kpi.hackathons,
        'publications': kpi.publications,
        'workshops': kpi.workshops,
        'projects': kpi.projects,
        'club_activities': kpi.club_activities,
        'industrial_visits': kpi.industrial_visits,
    }
    
    score = calculate_kpi_score(kpi_dict)
    readiness = predict_career_readiness(score)
    
    # Store in database
    existing_score = db.query(Score).filter(Score.student_id == student_id).first()
    if existing_score:
        existing_score.kpi_score = score
        existing_score.career_readiness_score = readiness
        db.commit()
    else:
        new_score = Score(student_id=student_id, kpi_score=score, career_readiness_score=readiness)
        db.add(new_score)
        db.commit()
    
    return {
        "student_id": student_id,
        "kpi_score": score,
        "career_readiness": readiness
    }
