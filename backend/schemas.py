from pydantic import BaseModel

class StudentCreate(BaseModel):
    student_id: str
    name: str
    department: str
    section: str
    year: int

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