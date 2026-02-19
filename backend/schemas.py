from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# ============ Authentication Schemas ============

class UserLoginRequest(BaseModel):
    email: str
    password: str

class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

class UserRegister(BaseModel):
    email: str
    password: str
    name: str
    role: str = "student"  # student, faculty, coordinator, admin
    department: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    role: str
    department: Optional[str]
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True

# ============ Student Schemas ============

class StudentCreate(BaseModel):
    student_id: str
    name: str
    email: Optional[str] = None
    department: str
    section: str
    year: int
    gpa: Optional[float] = 0.0
    phone: Optional[str] = None
    date_of_birth: Optional[datetime] = None

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    gpa: Optional[float] = None
    phone: Optional[str] = None
    section: Optional[str] = None
    year: Optional[int] = None

class StudentResponse(BaseModel):
    student_id: str
    name: str
    email: Optional[str]
    department: str
    section: str
    year: int
    gpa: float
    phone: Optional[str]
    date_of_birth: Optional[datetime]
    enrollment_date: datetime
    
    class Config:
        from_attributes = True

# ============ KPI Schemas ============

class KPIAdd(BaseModel):
    student_id: str
    internships: int = 0
    certifications: int = 0
    hackathons: int = 0
    publications: int = 0
    workshops: int = 0
    projects: int = 0
    club_activities: int = 0
    industrial_visits: int = 0
    research_papers: int = 0
    patents: int = 0

class KPIUpdate(BaseModel):
    internships: Optional[int] = None
    certifications: Optional[int] = None
    hackathons: Optional[int] = None
    publications: Optional[int] = None
    workshops: Optional[int] = None
    projects: Optional[int] = None
    club_activities: Optional[int] = None
    industrial_visits: Optional[int] = None
    research_papers: Optional[int] = None
    patents: Optional[int] = None

class KPIResponse(BaseModel):
    id: int
    student_id: str
    internships: int
    certifications: int
    hackathons: int
    publications: int
    workshops: int
    projects: int
    club_activities: int
    industrial_visits: int
    research_papers: int
    patents: int
    last_updated: datetime
    
    class Config:
        from_attributes = True

# ============ Score & Performance Schemas ============

class ScoreResponse(BaseModel):
    id: int
    student_id: str
    kpi_score: float
    career_readiness_score: str
    percentile_rank: float
    overall_performance: float
    academic_strength: float
    professional_development: float
    leadership_score: float
    last_updated: datetime
    
    class Config:
        from_attributes = True

class MilestoneCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: str  # academic, professional, personal
    target_date: Optional[datetime] = None

class MilestoneResponse(BaseModel):
    id: int
    student_id: str
    title: str
    description: Optional[str]
    category: str
    achievement_date: Optional[datetime]
    target_date: Optional[datetime]
    status: str
    impact_score: float
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============ Analytics & Dashboard Schemas ============

class StudentWithKPI(BaseModel):
    student: StudentResponse
    kpi: Optional[KPIResponse]
    score: Optional[ScoreResponse]
    
    class Config:
        from_attributes = True

class DepartmentStats(BaseModel):
    department: str
    total_students: int
    average_kpi: float
    average_gpa: float
    top_performers: int
    active_students: int

class YearStats(BaseModel):
    year: int
    total_students: int
    average_kpi: float
    average_gpa: float
    departmentwise_distribution: dict

class AnalyticsResponse(BaseModel):
    total_students: int
    average_kpi: float
    average_gpa: float
    department_stats: List[DepartmentStats]
    year_stats: List[YearStats]
    top_performers: List[StudentResponse]
    bottom_performers: List[StudentResponse]

class ComparisonMetrics(BaseModel):
    student_id: str
    student_name: str
    kpi_score: float
    percentile: float
    department_rank: int
    year_rank: int
    benchmark_score: float

class PerformanceTrendResponse(BaseModel):
    student_id: str
    historical_scores: List[tuple]  # [(timestamp, score)]
    trend_direction: str  # up, down, stable
    improvement_rate: float  # percentage change per month