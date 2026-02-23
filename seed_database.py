"""
Database seeding script for Student KPI Management System.
Creates 20+ students across multiple departments with realistic KPI data.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from database.database import engine, Base, SessionLocal
from database.models import Student, KPI, Score, User
from datetime import datetime, timedelta
import random
import hashlib
from backend.kpi_engine import calculate_kpi_score, predict_career_readiness

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# Create all tables
Base.metadata.create_all(bind=engine)

# Sample student data
STUDENTS_DATA = [
    # CSE Department
    {"student_id": "CSE001", "name": "Arjun Sharma", "department": "Computer Science & Engineering", "section": "A", "year": 3},
    {"student_id": "CSE002", "name": "Priya Patel", "department": "Computer Science & Engineering", "section": "A", "year": 3},
    {"student_id": "CSE003", "name": "Rahul Verma", "department": "Computer Science & Engineering", "section": "B", "year": 2},
    {"student_id": "CSE004", "name": "Sneha Iyer", "department": "Computer Science & Engineering", "section": "B", "year": 4},
    {"student_id": "CSE005", "name": "Vikram Nair", "department": "Computer Science & Engineering", "section": "C", "year": 1},
    # ECE Department
    {"student_id": "ECE001", "name": "Ananya Krishnan", "department": "Electronics & Communication", "section": "A", "year": 3},
    {"student_id": "ECE002", "name": "Karthik Reddy", "department": "Electronics & Communication", "section": "A", "year": 2},
    {"student_id": "ECE003", "name": "Divya Menon", "department": "Electronics & Communication", "section": "B", "year": 4},
    {"student_id": "ECE004", "name": "Sai Kumar", "department": "Electronics & Communication", "section": "C", "year": 1},
    # MECH Department
    {"student_id": "ME001", "name": "Rohit Singh", "department": "Mechanical Engineering", "section": "A", "year": 4},
    {"student_id": "ME002", "name": "Kavitha Suresh", "department": "Mechanical Engineering", "section": "B", "year": 2},
    {"student_id": "ME003", "name": "Arun Raj", "department": "Mechanical Engineering", "section": "A", "year": 3},
    # Civil Department
    {"student_id": "CE001", "name": "Deepa Thomas", "department": "Civil Engineering", "section": "A", "year": 3},
    {"student_id": "CE002", "name": "Harish Kumar", "department": "Civil Engineering", "section": "B", "year": 2},
    # IT Department
    {"student_id": "IT001", "name": "Meera Nambiar", "department": "Information Technology", "section": "A", "year": 4},
    {"student_id": "IT002", "name": "Ajay Chandran", "department": "Information Technology", "section": "A", "year": 3},
    {"student_id": "IT003", "name": "Lakshmi Pillai", "department": "Information Technology", "section": "B", "year": 2},
    # AIDS Department
    {"student_id": "AI001", "name": "Ravi Teja", "department": "AI & Data Science", "section": "A", "year": 3},
    {"student_id": "AI002", "name": "Pooja Gupta", "department": "AI & Data Science", "section": "A", "year": 2},
    {"student_id": "AI003", "name": "Nikhil Bose", "department": "AI & Data Science", "section": "B", "year": 4},
    {"student_id": "AI004", "name": "Sreya Nair", "department": "AI & Data Science", "section": "A", "year": 1},
]

# KPI data ranges per performance tier
def generate_kpi(tier="medium"):
    if tier == "high":
        return {
            "internships": random.randint(2, 5),
            "certifications": random.randint(5, 12),
            "hackathons": random.randint(3, 8),
            "publications": random.randint(1, 4),
            "workshops": random.randint(8, 15),
            "projects": random.randint(5, 10),
            "club_activities": random.randint(4, 8),
            "industrial_visits": random.randint(5, 10),
            "value_added_courses": random.randint(3, 6),
        }
    elif tier == "medium":
        return {
            "internships": random.randint(1, 3),
            "certifications": random.randint(2, 7),
            "hackathons": random.randint(1, 4),
            "publications": random.randint(0, 2),
            "workshops": random.randint(3, 9),
            "projects": random.randint(2, 6),
            "club_activities": random.randint(2, 5),
            "industrial_visits": random.randint(2, 6),
            "value_added_courses": random.randint(1, 3),
        }
    else:  # low
        return {
            "internships": random.randint(0, 1),
            "certifications": random.randint(0, 3),
            "hackathons": random.randint(0, 2),
            "publications": 0,
            "workshops": random.randint(1, 5),
            "projects": random.randint(1, 3),
            "club_activities": random.randint(0, 2),
            "industrial_visits": random.randint(1, 3),
            "value_added_courses": 0,
        }



# Assign tiers
TIERS = [
    "high", "high", "medium", "medium", "low",  # CSE
    "high", "medium", "medium", "low",           # ECE
    "medium", "low", "medium",                   # MECH
    "medium", "low",                             # CE
    "high", "high", "medium",                    # IT
    "high", "medium", "high", "low",             # AIDS
]

def seed():
    db: Session = SessionLocal()
    try:
        # Clear existing data
        db.query(Score).delete()
        db.query(KPI).delete()
        db.query(Student).delete()
        db.commit()
        print("Cleared existing student/KPI/score data.")

        # Seed users (admin + faculty)
        existing_admin = db.query(User).filter(User.email == "admin@kpi.edu").first()
        if not existing_admin:
            admin = User(
                email="admin@kpi.edu",
                password_hash=hash_pw("admin123"),
                name="System Administrator",
                role="admin",
                department="Administration",
                is_active=True,
                created_at=datetime.utcnow()
            )
            # CSE Faculty
            fac1 = User(email="fac01@kpi.edu", password_hash=hash_pw("faculty123"), name="Dr. Ramesh Kumar", role="faculty", department="Computer Science & Engineering", is_active=True, created_at=datetime.utcnow())
            fac2 = User(email="fac02@kpi.edu", password_hash=hash_pw("faculty123"), name="Prof. Anjali Desai", role="faculty", department="Computer Science & Engineering", is_active=True, created_at=datetime.utcnow())
            fac3 = User(email="fac03@kpi.edu", password_hash=hash_pw("faculty123"), name="Dr. Vivek Sharma", role="faculty", department="Computer Science & Engineering", is_active=True, created_at=datetime.utcnow())
            fac4 = User(email="fac04@kpi.edu", password_hash=hash_pw("faculty123"), name="Prof. Neha Singh", role="faculty", department="Computer Science & Engineering", is_active=True, created_at=datetime.utcnow())
            fac5 = User(email="fac05@kpi.edu", password_hash=hash_pw("faculty123"), name="Dr. Arjun Patel", role="faculty", department="Computer Science & Engineering", is_active=True, created_at=datetime.utcnow())
            # ECE Faculty
            fac6 = User(email="fac06@kpi.edu", password_hash=hash_pw("faculty123"), name="Dr. Vikram Seth", role="faculty", department="Electronics & Communication", is_active=True, created_at=datetime.utcnow())
            fac7 = User(email="fac07@kpi.edu", password_hash=hash_pw("faculty123"), name="Prof. Neha Gupta", role="faculty", department="Electronics & Communication", is_active=True, created_at=datetime.utcnow())
            fac8 = User(email="fac08@kpi.edu", password_hash=hash_pw("faculty123"), name="Dr. Rohan Mehra", role="faculty", department="Electronics & Communication", is_active=True, created_at=datetime.utcnow())
            fac9 = User(email="fac09@kpi.edu", password_hash=hash_pw("faculty123"), name="Prof. Anil Kapoor", role="faculty", department="Electronics & Communication", is_active=True, created_at=datetime.utcnow())
            fac10 = User(email="fac10@kpi.edu", password_hash=hash_pw("faculty123"), name="Dr. Priya Reddy", role="faculty", department="Electronics & Communication", is_active=True, created_at=datetime.utcnow())
            # MECH Faculty
            fac11 = User(email="fac11@kpi.edu", password_hash=hash_pw("faculty123"), name="Dr. Rajesh Pillai", role="faculty", department="Mechanical Engineering", is_active=True, created_at=datetime.utcnow())
            fac12 = User(email="fac12@kpi.edu", password_hash=hash_pw("faculty123"), name="Prof. Sanjay Dutt", role="faculty", department="Mechanical Engineering", is_active=True, created_at=datetime.utcnow())
            fac13 = User(email="fac13@kpi.edu", password_hash=hash_pw("faculty123"), name="Dr. Kiran Rao", role="faculty", department="Mechanical Engineering", is_active=True, created_at=datetime.utcnow())
            fac14 = User(email="fac14@kpi.edu", password_hash=hash_pw("faculty123"), name="Prof. Amit Shah", role="faculty", department="Mechanical Engineering", is_active=True, created_at=datetime.utcnow())
            fac15 = User(email="fac15@kpi.edu", password_hash=hash_pw("faculty123"), name="Dr. Sneha Verma", role="faculty", department="Mechanical Engineering", is_active=True, created_at=datetime.utcnow())
            # CE Faculty
            fac16 = User(email="fac16@kpi.edu", password_hash=hash_pw("faculty123"), name="Dr. Suresh Reddy", role="faculty", department="Civil Engineering", is_active=True, created_at=datetime.utcnow())
            fac17 = User(email="fac17@kpi.edu", password_hash=hash_pw("faculty123"), name="Prof. Manoj Tiwari", role="faculty", department="Civil Engineering", is_active=True, created_at=datetime.utcnow())
            fac18 = User(email="fac18@kpi.edu", password_hash=hash_pw("faculty123"), name="Dr. Deepa Nair", role="faculty", department="Civil Engineering", is_active=True, created_at=datetime.utcnow())
            fac19 = User(email="fac19@kpi.edu", password_hash=hash_pw("faculty123"), name="Prof. Rahul Bose", role="faculty", department="Civil Engineering", is_active=True, created_at=datetime.utcnow())
            fac20 = User(email="fac20@kpi.edu", password_hash=hash_pw("faculty123"), name="Dr. Karthik Raj", role="faculty", department="Civil Engineering", is_active=True, created_at=datetime.utcnow())
            # IT Faculty
            fac21 = User(email="fac21@kpi.edu", password_hash=hash_pw("faculty123"), name="Prof. Meera Iyer", role="faculty", department="Information Technology", is_active=True, created_at=datetime.utcnow())
            fac22 = User(email="fac22@kpi.edu", password_hash=hash_pw("faculty123"), name="Dr. Ajay Verma", role="faculty", department="Information Technology", is_active=True, created_at=datetime.utcnow())
            fac23 = User(email="fac23@kpi.edu", password_hash=hash_pw("faculty123"), name="Prof. Sunita Shenoy", role="faculty", department="Information Technology", is_active=True, created_at=datetime.utcnow())
            fac24 = User(email="fac24@kpi.edu", password_hash=hash_pw("faculty123"), name="Dr. Tarun Kumar", role="faculty", department="Information Technology", is_active=True, created_at=datetime.utcnow())
            fac25 = User(email="fac25@kpi.edu", password_hash=hash_pw("faculty123"), name="Prof. Pooja Hegde", role="faculty", department="Information Technology", is_active=True, created_at=datetime.utcnow())
            # AIDS Faculty
            fac26 = User(email="fac26@kpi.edu", password_hash=hash_pw("faculty123"), name="Prof. Amit Bose", role="faculty", department="AI & Data Science", is_active=True, created_at=datetime.utcnow())
            fac27 = User(email="fac27@kpi.edu", password_hash=hash_pw("faculty123"), name="Dr. Manish Pandey", role="faculty", department="AI & Data Science", is_active=True, created_at=datetime.utcnow())
            fac28 = User(email="fac28@kpi.edu", password_hash=hash_pw("faculty123"), name="Prof. Shreya Ghoshal", role="faculty", department="AI & Data Science", is_active=True, created_at=datetime.utcnow())
            fac29 = User(email="fac29@kpi.edu", password_hash=hash_pw("faculty123"), name="Dr. Rakesh Jhunjhunwala", role="faculty", department="AI & Data Science", is_active=True, created_at=datetime.utcnow())
            fac30 = User(email="fac30@kpi.edu", password_hash=hash_pw("faculty123"), name="Prof. Nidhi Awasthi", role="faculty", department="AI & Data Science", is_active=True, created_at=datetime.utcnow())

            hod_cse = User(
                email="hod.cse@kpi.edu",
                password_hash=hash_pw("hod123"),
                name="Prof. Sharma (CSE)",
                role="hod",
                department="Computer Science & Engineering",
                is_active=True,
                created_at=datetime.utcnow()
            )
            hod_ece = User(
                email="hod.ece@kpi.edu",
                password_hash=hash_pw("hod123"),
                name="Prof. Reddy (ECE)",
                role="hod",
                department="Electronics & Communication",
                is_active=True,
                created_at=datetime.utcnow()
            )
            hod_mech = User(
                email="hod.mech@kpi.edu",
                password_hash=hash_pw("hod123"),
                name="Prof. Singh (MECH)",
                role="hod",
                department="Mechanical Engineering",
                is_active=True,
                created_at=datetime.utcnow()
            )
            hod_ce = User(
                email="hod.ce@kpi.edu",
                password_hash=hash_pw("hod123"),
                name="Prof. Thomas (CE)",
                role="hod",
                department="Civil Engineering",
                is_active=True,
                created_at=datetime.utcnow()
            )
            hod_it = User(
                email="hod.it@kpi.edu",
                password_hash=hash_pw("hod123"),
                name="Prof. Nambiar (IT)",
                role="hod",
                department="Information Technology",
                is_active=True,
                created_at=datetime.utcnow()
            )
            hod_ai = User(
                email="hod.ai@kpi.edu",
                password_hash=hash_pw("hod123"),
                name="Prof. Bose (AIDS)",
                role="hod",
                department="AI & Data Science",
                is_active=True,
                created_at=datetime.utcnow()
            )
            all_fac = [fac1, fac2, fac3, fac4, fac5, fac6, fac7, fac8, fac9, fac10, fac11, fac12, fac13, fac14, fac15, fac16, fac17, fac18, fac19, fac20, fac21, fac22, fac23, fac24, fac25, fac26, fac27, fac28, fac29, fac30]
            db.add_all([admin, hod_cse, hod_ece, hod_mech, hod_ce, hod_it, hod_ai] + all_fac)
            db.commit()
            print("Seeded users (including 6 HODs and 30 Faculty).")

        # Seed students, KPIs, scores
        for i, student_data in enumerate(STUDENTS_DATA):
            tier = TIERS[i] if i < len(TIERS) else "medium"

            # Student
            student = Student(
                student_id=student_data["student_id"],
                name=student_data["name"],
                email=f"{student_data['student_id'].lower()}@college.edu",
                department=student_data["department"],
                section=student_data["section"],
                year=student_data["year"],
                gpa=round(random.uniform(6.5 if tier == "low" else 7.5, 9.8 if tier == "high" else 8.5), 2),
                enrollment_date=datetime.utcnow() - timedelta(days=365 * student_data["year"]),
            )
            db.add(student)
            db.flush()

            # KPI
            kpi_data = generate_kpi(tier)
            kpi = KPI(
                student_id=student_data["student_id"],
                **kpi_data,
                last_updated=datetime.utcnow() - timedelta(days=random.randint(0, 30))
            )
            db.add(kpi)
            db.flush()

            # Score
            kpi_score = calculate_kpi_score(kpi_data)
            score = Score(
                student_id=student_data["student_id"],
                kpi_score=kpi_score,
                career_readiness_score=predict_career_readiness(kpi_score),
                last_updated=datetime.utcnow() - timedelta(days=random.randint(0, 7))
            )
            db.add(score)

        db.commit()
        print(f"Successfully seeded {len(STUDENTS_DATA)} students with KPI and Score data!")
        print("\nSample login credentials:")
        print("  Admin:       admin@kpi.edu / admin123")
        print("  Faculty 1:   fac01@kpi.edu / faculty123")
        print("  Faculty X:   fac[01-30]@kpi.edu / faculty123")
        print("  HOD CSE:     hod.cse@kpi.edu / hod123")
        print("  HOD ECE:     hod.ece@kpi.edu / hod123")
        print("  (and so on for hod.mech, hod.ce, hod.it, hod.ai)")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed()
