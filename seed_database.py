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
        }

def calculate_kpi_score(kpi_data):
    weights = {
        "internships": 10,
        "certifications": 5,
        "hackathons": 7,
        "publications": 12,
        "workshops": 3,
        "projects": 8,
        "club_activities": 4,
        "industrial_visits": 3,
    }
    max_vals = {
        "internships": 5, "certifications": 12, "hackathons": 8,
        "publications": 4, "workshops": 15, "projects": 10,
        "club_activities": 8, "industrial_visits": 10,
    }
    score = 0
    for key, weight in weights.items():
        val = min(kpi_data[key], max_vals[key])
        score += (val / max_vals[key]) * weight
    return round(min(score, 100), 2)

def get_career_readiness(score):
    if score >= 80:
        return "High Readiness"
    elif score >= 60:
        return "Moderate Readiness"
    elif score >= 40:
        return "Developing"
    else:
        return "Low Readiness"

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
            faculty = User(
                email="faculty@kpi.edu",
                password_hash=hash_pw("faculty123"),
                name="Dr. Ramesh Kumar",
                role="faculty",
                department="Computer Science & Engineering",
                is_active=True,
                created_at=datetime.utcnow()
            )
            coord = User(
                email="coordinator@kpi.edu",
                password_hash=hash_pw("coord123"),
                name="Prof. Sunita Sharma",
                role="coordinator",
                department="AI & Data Science",
                is_active=True,
                created_at=datetime.utcnow()
            )
            db.add_all([admin, faculty, coord])
            db.commit()
            print("Seeded users.")

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
                career_readiness_score=get_career_readiness(kpi_score),
                last_updated=datetime.utcnow() - timedelta(days=random.randint(0, 7))
            )
            db.add(score)

        db.commit()
        print(f"Successfully seeded {len(STUDENTS_DATA)} students with KPI and Score data!")
        print("\nSample login credentials:")
        print("  Admin:       admin@kpi.edu / admin123")
        print("  Faculty:     faculty@kpi.edu / faculty123")
        print("  Coordinator: coordinator@kpi.edu / coord123")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed()
