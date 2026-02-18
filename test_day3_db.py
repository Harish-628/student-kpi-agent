"""
Day 3: Direct Database Testing
Tests KPI ingestion functionality directly without HTTP server
"""

from database.database import engine, Base, SessionLocal
from database.models import Student, KPI, Score
from backend.kpi_engine import calculate_kpi_score, predict_career_readiness
from backend.schemas import StudentCreate, KPIAdd
import csv
import io

# Create all tables
Base.metadata.create_all(bind=engine)

print("\n" + "=" * 60)
print("DAY 3: KPI DATA INGESTION MODULE - DATABASE TESTS")
print("=" * 60)

# Test 1: Add Students via Database
print("\n=== Test 1: Add Students ===")
db = SessionLocal()
try:
    students = [
        Student(student_id="STU001", name="Alice Johnson", department="CSE", section="A", year=3),
        Student(student_id="STU002", name="Bob Smith", department="CSE", section="A", year=3),
        Student(student_id="STU003", name="Charlie Brown", department="CSE", section="B", year=3),
        Student(student_id="STU004", name="Diana Prince", department="ECE", section="A", year=3),
        Student(student_id="STU005", name="Eve Wilson", department="ECE", section="B", year=3),
    ]
    
    for student in students:
        existing = db.query(Student).filter(Student.student_id == student.student_id).first()
        if not existing:
            db.add(student)
            print(f"✓ Added student: {student.student_id} - {student.name}")
        else:
            print(f"→ Student {student.student_id} already exists")
    
    db.commit()
except Exception as e:
    print(f"✗ Error: {str(e)}")
    db.rollback()

# Test 2: Add individual KPI record
print("\n=== Test 2: Add Individual KPI Records ===")
try:
    kpi_records = [
        KPI(student_id="STU001", internships=2, certifications=3, hackathons=1, publications=0, 
            workshops=2, projects=4, club_activities=5, industrial_visits=1),
        KPI(student_id="STU002", internships=1, certifications=2, hackathons=2, publications=1,
            workshops=1, projects=3, club_activities=2, industrial_visits=1),
    ]
    
    for kpi in kpi_records:
        existing = db.query(KPI).filter(KPI.student_id == kpi.student_id).first()
        if not existing:
            db.add(kpi)
            print(f"✓ Added KPI for student: {kpi.student_id}")
        else:
            print(f"→ KPI for {kpi.student_id} already exists")
    
    db.commit()
except Exception as e:
    print(f"✗ Error: {str(e)}")
    db.rollback()

# Test 3: Bulk CSV-style migration simulation
print("\n=== Test 3: CSV-style Bulk Import ===")
csv_data = """student_id,internships,certifications,hackathons,publications,workshops,projects,club_activities,industrial_visits
STU003,3,4,2,2,3,5,4,2
STU004,1,1,0,0,1,2,1,0
STU005,2,2,1,1,2,3,3,1"""

try:
    csv_reader = csv.DictReader(io.StringIO(csv_data))
    imported = 0
    failed = 0
    
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
            
            existing = db.query(KPI).filter(KPI.student_id == row['student_id']).first()
            if existing:
                failed += 1
                print(f"  → {row['student_id']}: Already exists (skipped)")
            else:
                db_kpi = KPI(**kpi_data)
                db.add(db_kpi)
                db.commit()
                imported += 1
                print(f"  ✓ Imported {row['student_id']}")
        except Exception as e:
            failed += 1
            print(f"  ✗ {row['student_id']}: {str(e)}")
            db.rollback()
    
    print(f"\nCSV Import Summary: {imported} imported, {failed} failed")
except Exception as e:
    print(f"✗ CSV processing error: {str(e)}")

# Test 4: KPI Score Calculation & Storage
print("\n=== Test 4: KPI Score Calculation ===")
try:
    students_to_score = ["STU001", "STU002", "STU003", "STU004", "STU005"]
    
    for student_id in students_to_score:
        kpi = db.query(KPI).filter(KPI.student_id == student_id).first()
        if kpi:
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
            
            # Store in Score table
            existing_score = db.query(Score).filter(Score.student_id == student_id).first()
            if existing_score:
                existing_score.kpi_score = score
                existing_score.career_readiness_score = readiness
            else:
                new_score = Score(student_id=student_id, kpi_score=score, career_readiness_score=readiness)
                db.add(new_score)
            
            db.commit()
            print(f"✓ {student_id}: Score={score}, Readiness={readiness}")
except Exception as e:
    print(f"✗ Error: {str(e)}")
    db.rollback()

# Test 5: Verify stored data
print("\n=== Test 5: Verify Stored Data ===")
try:
    print("\nStudent KPI Data:")
    kpis = db.query(KPI).all()
    for kpi in kpis:
        print(f"  {kpi.student_id}: Internships={kpi.internships}, Certifications={kpi.certifications}, "
              f"Hackathons={kpi.hackathons}, Projects={kpi.projects}")
    
    print("\nStudent KPI Scores:")
    scores = db.query(Score).all()
    for score in scores:
        print(f"  {score.student_id}: Score={score.kpi_score}, Readiness={score.career_readiness_score}")
except Exception as e:
    print(f"✗ Error: {str(e)}")

db.close()

print("\n" + "=" * 60)
print("✓ DAY 3 DATABASE TESTS COMPLETE!")
print("=" * 60)
