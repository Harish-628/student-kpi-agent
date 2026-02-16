"""
SQLAlchemy database models for Student KPI tracking system.
Includes Student, KPI, and Score models with relationships.
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database.database import Base


class Student(Base):
    """
    Student model representing individual students in the system.
    
    Attributes:
        student_id (str): Unique student identifier (Primary Key)
        name (str): Full name of the student
        department (str): Department/Faculty name
        section (str): Class section/division
        year (int): Academic year
        kpis (relationship): One-to-One relationship with KPI model
        scores (relationship): One-to-One relationship with Score model
    """
    
    __tablename__ = "students"
    
    student_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    department = Column(String, nullable=False)
    section = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    
    # Relationships
    kpis = relationship("KPI", back_populates="student", uselist=False, cascade="all, delete-orphan")
    scores = relationship("Score", back_populates="student", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Student(student_id='{self.student_id}', name='{self.name}', department='{self.department}')>"


class KPI(Base):
    """
    KPI model storing Key Performance Indicator metrics for each student.
    All metrics are tracked as integer counts with default value of 0.
    
    Attributes:
        id (int): Unique identifier (Primary Key)
        student_id (str): Foreign Key reference to Student
        internships (int): Number of internships completed
        certifications (int): Number of certifications obtained
        hackathons (int): Number of hackathon participations
        publications (int): Number of publications
        workshops (int): Number of workshops attended
        projects (int): Number of projects completed
        club_activities (int): Number of club activities participated
        industrial_visits (int): Number of industrial visits attended
        student (relationship): Back reference to Student model
    """
    
    __tablename__ = "kpis"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, ForeignKey("students.student_id"), nullable=False, unique=True)
    
    # KPI Metrics - All integers with default value of 0
    internships = Column(Integer, default=0, nullable=False)
    certifications = Column(Integer, default=0, nullable=False)
    hackathons = Column(Integer, default=0, nullable=False)
    publications = Column(Integer, default=0, nullable=False)
    workshops = Column(Integer, default=0, nullable=False)
    projects = Column(Integer, default=0, nullable=False)
    club_activities = Column(Integer, default=0, nullable=False)
    industrial_visits = Column(Integer, default=0, nullable=False)
    
    # Relationship
    student = relationship("Student", back_populates="kpis")
    
    def __repr__(self):
        return f"<KPI(student_id='{self.student_id}', internships={self.internships}, certifications={self.certifications})>"


class Score(Base):
    """
    Score model storing computed scores for each student.
    Includes KPI score and career readiness assessment.
    
    Attributes:
        id (int): Unique identifier (Primary Key)
        student_id (str): Foreign Key reference to Student
        kpi_score (float): Computed KPI score (0.0-100.0), default 0.0
        career_readiness_score (str): Career readiness level assessment, default "Low readiness"
        last_updated (datetime): Timestamp of last score update, default current time
        student (relationship): Back reference to Student model
    """
    
    __tablename__ = "scores"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, ForeignKey("students.student_id"), nullable=False, unique=True)
    
    # Score Metrics
    kpi_score = Column(Float, default=0.0, nullable=False)
    career_readiness_score = Column(String, default="Low readiness", nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship
    student = relationship("Student", back_populates="scores")
    
    def __repr__(self):
        return f"<Score(student_id='{self.student_id}', kpi_score={self.kpi_score}, career_readiness='{self.career_readiness_score}')>"
