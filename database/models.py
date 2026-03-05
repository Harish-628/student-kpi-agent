"""
SQLAlchemy database models for Student KPI tracking system.
Includes Student, KPI, Score, User, and analytics models.
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database.database import Base


class User(Base):
    """
    User model for authentication and role-based access.
    Supports multiple roles: student, faculty, hod, admin.
    
    Attributes:
        id (int): Unique identifier
        email (str): User email (unique)
        password_hash (str): Hashed password
        name (str): Full name
        role (str): User role (student, faculty, hod, admin)
        department (str): Department affiliation
        is_active (bool): Account active status
        created_at (datetime): Account creation timestamp
        last_login (datetime): Last login timestamp
    """
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, default="student", nullable=False)  # student, faculty, hod, admin
    department = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<User(email='{self.email}', role='{self.role}')>"


class Student(Base):
    """
    Student model representing individual students in the system.
    
    Attributes:
        student_id (str): Unique student identifier (Primary Key)
        name (str): Full name of the student
        email (str): Student email
        department (str): Department/Faculty name
        section (str): Class section/division
        year (int): Academic year
        gpa (float): Current GPA
        phone (str): Contact phone number
        date_of_birth (datetime): Student DOB
        enrollment_date (datetime): Enrollment date
        kpis (relationship): One-to-One relationship with KPI model
        scores (relationship): One-to-One relationship with Score model
        milestones (relationship): One-to-Many with Milestone model
    """
    
    __tablename__ = "students"
    
    student_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    department = Column(String, nullable=False, index=True)
    section = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    gpa = Column(Float, default=0.0)
    phone = Column(String, nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    enrollment_date = Column(DateTime, default=datetime.utcnow)
    fcm_token = Column(String, nullable=True)  # For push notifications
    
    # Relationships
    kpis = relationship("KPI", back_populates="student", uselist=False, cascade="all, delete-orphan")
    scores = relationship("Score", back_populates="student", uselist=False, cascade="all, delete-orphan")
    milestones = relationship("Milestone", back_populates="student", cascade="all, delete-orphan")
    performance_history = relationship("PerformanceHistory", back_populates="student", cascade="all, delete-orphan")
    
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
        research_papers (int): Number of research papers
        patents (int): Number of patents
        last_updated (datetime): Last update timestamp
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
    research_papers = Column(Integer, default=0, nullable=False)
    patents = Column(Integer, default=0, nullable=False)
    value_added_courses = Column(Integer, default=0, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    student = relationship("Student", back_populates="kpis")
    
    def __repr__(self):
        return f"<KPI(student_id='{self.student_id}', internships={self.internships}, certifications={self.certifications})>"


class CertificateUpload(Base):
    """
    CertificateUpload model for tracking uploaded files supporting KPI metrics.
    
    Attributes:
        id (int): Unique identifier
        student_id (str): Foreign Key to Student
        category (str): The KPI category this supports (e.g., 'certifications', 'value_added_courses')
        file_path (str): The server path or URI of the uploaded file
        upload_date (datetime): When the file was uploaded
    """
    
    __tablename__ = "certificate_uploads"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, ForeignKey("students.student_id"), nullable=False)
    category = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student")
    
    def __repr__(self):
        return f"<CertificateUpload(id={self.id}, student_id='{self.student_id}', category='{self.category}')>"


class Score(Base):
    """
    Score model storing computed scores for each student.
    Includes KPI score, career readiness, and multiple performance metrics.
    
    Attributes:
        id (int): Unique identifier (Primary Key)
        student_id (str): Foreign Key reference to Student
        kpi_score (float): Computed KPI score (0.0-100.0), default 0.0
        career_readiness_score (str): Career readiness level assessment
        percentile_rank (float): Percentile ranking among peers (0-100)
        overall_performance (float): Overall performance score (0-100)
        academic_strength (float): Academic performance score
        professional_development (float): Professional development score
        leadership_score (float): Leadership and soft skills score
        last_updated (datetime): Timestamp of last score update
        student (relationship): Back reference to Student model
    """
    
    __tablename__ = "scores"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, ForeignKey("students.student_id"), nullable=False, unique=True)
    
    # Score Metrics
    kpi_score = Column(Float, default=0.0, nullable=False)
    career_readiness_score = Column(String, default="Low readiness", nullable=False)
    percentile_rank = Column(Float, default=0.0)
    overall_performance = Column(Float, default=0.0)
    academic_strength = Column(Float, default=0.0)
    professional_development = Column(Float, default=0.0)
    leadership_score = Column(Float, default=0.0)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    student = relationship("Student", back_populates="scores")
    
    def __repr__(self):
        return f"<Score(student_id='{self.student_id}', kpi_score={self.kpi_score}, percentile={self.percentile_rank})>"


class Milestone(Base):
    """
    Milestone model for tracking student achievements and goals.
    
    Attributes:
        id (int): Unique identifier
        student_id (str): Foreign Key to Student
        title (str): Milestone title
        description (str): Detailed description
        category (str): Milestone category (academic, professional, personal)
        achievement_date (datetime): When milestone was achieved
        target_date (datetime): Target date for completion
        status (str): Current status (completed, in_progress, planned)
        impact_score (float): Impact on overall score (0-10)
    """
    
    __tablename__ = "milestones"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, ForeignKey("students.student_id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=False)  # academic, professional, personal
    achievement_date = Column(DateTime, nullable=True)
    target_date = Column(DateTime, nullable=True)
    status = Column(String, default="planned")  # planned, in_progress, completed
    impact_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="milestones")
    
    def __repr__(self):
        return f"<Milestone(id={self.id}, title='{self.title}', status='{self.status}')>"


class PerformanceHistory(Base):
    """
    Track historical performance changes for analytics and trends.
    
    Attributes:
        id (int): Unique identifier
        student_id (str): Foreign Key to Student
        kpi_score (float): KPI score at this point in time
        timestamp (datetime): When this record was created
        notes (str): Additional notes about this performance record
    """
    
    __tablename__ = "performance_history"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, ForeignKey("students.student_id"), nullable=False)
    kpi_score = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)
    
    student = relationship("Student", back_populates="performance_history")
    
    def __repr__(self):
        return f"<PerformanceHistory(student_id='{self.student_id}', score={self.kpi_score}, date={self.timestamp})>"


class EventCache(Base):
    """
    Cache for SerpApi Google Events results to minimize API calls and respect Free Tier limits.
    
    Attributes:
        id (int): Unique identifier
        query (str): The search query used for SerpApi
        event_data (JSON): The JSON serialized list of events returned
        last_fetched (datetime): Timestamp of the API call
    """
    
    __tablename__ = "event_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, unique=True, index=True, nullable=False)
    event_data = Column(JSON, nullable=False)
    last_fetched = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<EventCache(query='{self.query}', updated='{self.last_fetched}')>"


class ODRequest(Base):
    """
    On Duty (OD) Request model for tracking student event participation.
    """
    
    __tablename__ = "od_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, ForeignKey("students.student_id"), nullable=False, index=True)
    student_name = Column(String, nullable=False)
    college_name = Column(String, nullable=False)
    date = Column(String, nullable=False)        # "YYYY-MM-DD"
    start_time = Column(String, nullable=False)  # "HH:MM"
    end_time = Column(String, nullable=False)    # "HH:MM"
    event_details = Column(String, nullable=False)
    days = Column(Integer, default=1, nullable=False)
    result_status = Column(String, default="Pending Result", nullable=False)
    prize_details = Column(String, nullable=True)
    certificate_data = Column(String, nullable=True)
    verification_status = Column(String, nullable=True)
    fcm_token = Column(String, nullable=True)
    faculty_notified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    student = relationship("Student", backref="od_requests")
    
    def __repr__(self):
        return f"<ODRequest(id={self.id}, student='{self.student_id}', event='{self.event_details}')>"

