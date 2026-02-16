# Day 2: Database Design - Usage Guide

This document explains how to use the SQLAlchemy database setup for the Student KPI project.

## Database Setup

### Files Created

1. **`database/database.py`** - Database configuration
   - SQLAlchemy engine setup with SQLite
   - SessionLocal factory for creating database sessions
   - Declarative Base for model inheritance
   - `get_db()` dependency function for FastAPI

2. **`database/models.py`** - Database models
   - `Student` - Student information
   - `KPI` - Student performance metrics
   - `Score` - Computed KPI scores

3. **`database/__init__.py`** - Module exports for easy imports

## Database Models

### Student Table
```python
class Student(Base):
    student_id: str (PK)
    name: str
    department: str
    section: str
    year: int
    
    # Relationships
    kpis: One-to-One with KPI
    scores: One-to-One with Score
```

### KPI Table
```python
class KPI(Base):
    id: int (PK)
    student_id: str (FK → Student)
    internships: int (default: 0)
    certifications: int (default: 0)
    hackathons: int (default: 0)
    publications: int (default: 0)
    workshops: int (default: 0)
    projects: int (default: 0)
    club_activities: int (default: 0)
    industrial_visits: int (default: 0)
```

### Score Table
```python
class Score(Base):
    id: int (PK)
    student_id: str (FK → Student)
    kpi_score: float (default: 0.0)
    career_readiness_score: str (default: "Low readiness")
    last_updated: datetime (default: current time)
```

## Usage Examples

### 1. Initialize the Database

In your `backend/main.py`:

```python
from fastapi import FastAPI
from database import init_db

app = FastAPI()

# Initialize database on startup
@app.on_event("startup")
def startup():
    init_db()
```

### 2. Use in FastAPI Routes

```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db, Student, KPI, Score

@app.post("/students/")
def create_student(student_id: str, name: str, db: Session = Depends(get_db)):
    db_student = Student(
        student_id=student_id,
        name=name,
        department="CS",
        section="A",
        year=3
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students/{student_id}")
def get_student(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    return student
```

### 3. Access Related Data

```python
# Get a student with all their KPI data
student = db.query(Student).filter(Student.student_id == "S001").first()

# Access related KPI data (lazy-loaded automatically)
if student.kpis:
    print(f"Internships: {student.kpis.internships}")
    print(f"Certifications: {student.kpis.certifications}")

# Access related Score data
if student.scores:
    print(f"KPI Score: {student.scores.kpi_score}")
    print(f"Career Readiness: {student.scores.career_readiness_score}")
```

### 4. Create KPI Records

```python
from datetime import datetime

# Create KPI for a student
kpi = KPI(
    student_id="S001",
    internships=2,
    certifications=3,
    hackathons=1,
    publications=0,
    workshops=5,
    projects=4,
    club_activities=2,
    industrial_visits=1
)
db.add(kpi)
db.commit()
```

### 5. Update Scores

```python
# Update score for a student
score = db.query(Score).filter(Score.student_id == "S001").first()
if score:
    score.kpi_score = 85.5
    score.career_readiness_score = "High readiness"
    score.last_updated = datetime.utcnow()
    db.commit()
else:
    # Create new score if doesn't exist
    score = Score(
        student_id="S001",
        kpi_score=85.5,
        career_readiness_score="High readiness"
    )
    db.add(score)
    db.commit()
```

### 6. Query Operations

```python
# Get all students
all_students = db.query(Student).all()

# Get students from specific department
cs_students = db.query(Student).filter(Student.department == "CS").all()

# Get students with high KPI scores
high_performers = db.query(Student).join(Score).filter(Score.kpi_score >= 80).all()

# Get top performers by internships
top_interns = db.query(Student).join(KPI).order_by(KPI.internships.desc()).limit(10).all()

# Count total students
total_students = db.query(Student).count()
```

## Database File Location

The SQLite database file `student_kpi.db` will be created in the project root directory when `init_db()` is called.

## Key Features

- **Automatic Schema Creation**: Call `init_db()` once to create all tables
- **SQLite**: No server required, file-based database
- **Relationships**: Easy access to related student data
- **FastAPI Integration**: `get_db()` dependency for automatic session management
- **Cascading Deletes**: Deleting a student automatically deletes related KPI and Score records
- **Type Hints**: Full typing support for better IDE autocomplete

## Full Integration in FastAPI

```python
# bakend/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import init_db, get_db, Student, KPI, Score

app = FastAPI(title="Student KPI Agent")

@app.on_event("startup")
async def startup():
    init_db()

# Define your routes here using get_db dependency
```

## Next Steps

1. Create API schemas (Pydantic models) for request/response validation
2. Implement CRUD operations for each model
3. Add business logic for calculating KPI scores
4. Integrate with LangChain agents for AI-powered insights
