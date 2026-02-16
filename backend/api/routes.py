from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Student, KPI
from backend.schemas import StudentCreate, KPIAdd

router = APIRouter()

@router.post("/student/add")
def add_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return {"message": "Student added successfully", "student": db_student}

@router.post("/kpi/add")
def add_kpi(kpi: KPIAdd, db: Session = Depends(get_db)):
    db_kpi = KPI(**kpi.dict())
    db.add(db_kpi)
    db.commit()
    db.refresh(db_kpi)
    return {"message": "KPI data added successfully"}