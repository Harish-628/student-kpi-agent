from langchain_core.tools import tool
from typing import Optional, List, Dict, Any
from database.database import SessionLocal
from database.models import Student, Score, KPI, CertificateUpload, User, ODRequest
from passlib.context import CryptContext
from tenacity import retry, wait_exponential, stop_after_attempt
import json
from datetime import datetime


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

@tool
def get_top_students(department: Optional[str] = None) -> str:
    """
    Get the top 5 students with the highest KPI scores from the database.
    Optionally filter by department. Use this when asked about top performers,
    best students, highest scorers, or who is doing well.
    """
    db = SessionLocal()
    try:
        query = db.query(Student, Score).join(Score, Student.student_id == Score.student_id)
        
        if department and department.strip():
            query = query.filter(Student.department.ilike(f"%{department}%"))
            
        results = query.order_by(Score.kpi_score.desc()).limit(5).all()
        
        if not results:
            return f"No students found in the database for department: {department or 'All'}."
            
        response_lines = [f"🏆 Top Students ({department or 'All Departments'}):"]
        for idx, (student, score) in enumerate(results, 1):
            response_lines.append(
                f"{idx}. {student.name} ({student.student_id}) - {student.department} | "
                f"Score: {score.kpi_score:.1f}/100 | Readiness: {score.career_readiness_score}"
            )
            
        return "\n".join(response_lines)
    except Exception as e:
        return f"Error retrieving students from database: {str(e)}"
    finally:
        db.close()


@tool
def get_lowest_students(department: Optional[str] = None) -> str:
    """
    Get the bottom 5 students with the LOWEST KPI scores from the database.
    Optionally filter by department. Use this when asked about lowest performers,
    students who need help, students at risk, who is struggling, or worst scores.
    Faculty and HOD should always pass their department here.
    """
    db = SessionLocal()
    try:
        query = db.query(Student, Score).join(Score, Student.student_id == Score.student_id)

        if department and department.strip():
            query = query.filter(Student.department.ilike(f"%{department}%"))

        results = query.order_by(Score.kpi_score.asc()).limit(5).all()

        if not results:
            return f"No students found in the database for department: {department or 'All'}."

        scope = department or 'All Departments'
        response_lines = [f"⚠️ Students Needing Support ({scope}):"]
        for idx, (student, score) in enumerate(results, 1):
            response_lines.append(
                f"{idx}. {student.name} ({student.student_id}) - {student.department} | "
                f"Score: {score.kpi_score:.1f}/100 | Readiness: {score.career_readiness_score}"
            )

        return "\n".join(response_lines)
    except Exception as e:
        return f"Error retrieving students from database: {str(e)}"
    finally:
        db.close()


@tool
def upload_certificate_kpi(student_email: str, category: str, file_name: str) -> str:
    """
    Simulates a user uploading a certificate document for a specific KPI category.
    This tool increments their integer KPI value and creates a database record under CertificateUpload.
    Valid categories: internships, certifications, hackathons, publications, workshops, projects, club_activities, industrial_visits, research_papers, patents, value_added_courses.
    """
    valid_categories = [
        "internships", "certifications", "hackathons", "publications", 
        "workshops", "projects", "club_activities", "industrial_visits", 
        "research_papers", "patents", "value_added_courses"
    ]
    
    cat = category.lower().replace(" ", "_")
    if cat not in valid_categories:
        return f"Error: Category '{cat}' is not a valid KPI field. Must be one of: {', '.join(valid_categories)}"
        
    db = SessionLocal()
    try:
        # 1. Find the student ID from email
        student = db.query(Student).filter(Student.email == student_email).first()
        if not student:
            return f"Error: Cannot upload certificate. No student found with email {student_email}."
            
        student_id = student.student_id
        
        # 2. Add Certificate Upload Record
        cert = CertificateUpload(
            student_id=student_id,
            category=cat,
            file_path=f"/uploads/simulated/{file_name}"
        )
        db.add(cert)
        
        # 3. Read & Increment the KPI Table
        kpi = db.query(KPI).filter(KPI.student_id == student_id).first()
        if not kpi:
            return f"Error: No KPI record initialized for student {student_id}."
            
        current_val = getattr(kpi, cat)
        setattr(kpi, cat, current_val + 1)
        
        import backend.kpi_engine as kpi_engine
        
        # Build KPI Data Dict
        kpi_data = {
            "internships": kpi.internships,
            "certifications": kpi.certifications,
            "hackathons": kpi.hackathons, 
            "publications": kpi.publications,
            "workshops": kpi.workshops,
            "projects": kpi.projects,
            "club_activities": kpi.club_activities,
            "industrial_visits": kpi.industrial_visits,
            "research_papers": kpi.research_papers,
            "patents": kpi.patents,
            "value_added_courses": kpi.value_added_courses
        }
        
        # 4. Re-calculate KPI Score
        new_score = kpi_engine.calculate_kpi_score(kpi_data)
        new_readiness = kpi_engine.predict_career_readiness(new_score)
        
        # 5. Update Score Record
        score_record = db.query(Score).filter(Score.student_id == student_id).first()
        if score_record:
            score_record.kpi_score = new_score
            score_record.career_readiness_score = new_readiness
            
        db.commit()
        new_val = getattr(kpi, cat)
        
        return f"✅ Auto-Upload Successful! 1 {cat} certificate ('{file_name}') has been added to {student.name}'s profile. Their total {cat} count is now {new_val} and their overall KPI Score has been recalculated automatically."
    except Exception as e:
        db.rollback()
        return f"Database Error during transaction: {str(e)}"
    finally:
        db.close()



@tool
def add_mock_faculty(email: str, name: str, department: str) -> str:
    """
    Provisions a new User account with the 'faculty' role. 
    Only the Admin can run this function. Use it when the user asks to add or create a new faculty/teacher.
    """
    db = SessionLocal()
    try:
        # Check if exists
        user = db.query(User).filter(User.email == email).first()
        if user:
            return f"Error: A user with the email {email} already exists."
            
        new_faculty = User(
            email=email,
            name=name,
            role="faculty",
            department=department,
            password_hash=get_password_hash("faculty123")  # default demo password
        )
        db.add(new_faculty)
        db.commit()
        return f"🎉 Faculty member successfully added to the system! {name} can now login using {email} and the default password 'faculty123'."
    except Exception as e:
        db.rollback()
        return f"Database Error provisioning user: {str(e)}"
# Global in-memory session store for OD forms
OD_SESSIONS: Dict[str, Dict[str, Any]] = {}

# OD Management Tools

@tool
@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
def extract_od_details(
    student_email: str,
    college_name: Optional[str] = None,
    event_details: Optional[str] = None,
    date: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    num_days: Optional[int] = None
) -> str:
    """
    Extracts On Duty (OD) application fields from a student's conversational input.
    Use this tool whenever a student provides any details relating to an OD request.
    Always pass the user's email as student_email.
    """
    if student_email not in OD_SESSIONS:
        OD_SESSIONS[student_email] = {
            "college_name": None,
            "event_details": None,
            "date": None,
            "start_time": None,
            "end_time": None,
            "num_days": None
        }
        
    session = OD_SESSIONS[student_email]
    if college_name: session["college_name"] = college_name
    if event_details: session["event_details"] = event_details
    if date: session["date"] = date
    if start_time: session["start_time"] = start_time
    if end_time: session["end_time"] = end_time
    if num_days is not None: session["num_days"] = num_days
    
    missing = [k for k, v in session.items() if v is None]
    
    return f"Extracted details saved. Current form state: {json.dumps(session)}. Missing fields: {missing}. Ask the user for the next missing field."

@tool
@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
def apply_student_od(
    student_email: str
) -> str:
    """
    Formally submits a completed On Duty (OD) application to the database.
    Only call this tool when ALL fields in the form state have been confirmed by the student.
    Always pass the user's email as student_email.
    """
    db = SessionLocal()
    try:
        session = OD_SESSIONS.get(student_email)
        if not session:
            return "Error: No active OD form session found."
            
        missing = [k for k, v in session.items() if v is None]
        if missing:
            return f"Error: Cannot submit. Missing fields: {missing}"
            
        student = db.query(Student).filter(Student.email == student_email).first()
        if not student:
            return f"Error: Student not found with email {student_email}."
            
        od = ODRequest(
            student_id=student.student_id,
            student_name=student.name,
            college_name=session["college_name"],
            event_details=session["event_details"],
            date=session["date"],
            start_time=session["start_time"],
            end_time=session["end_time"],
            days=session["num_days"],
            result_status="Pending Result"
        )
        db.add(od)
        db.commit()
        db.refresh(od)
        
        # Clear session after successful submission
        OD_SESSIONS.pop(student_email, None)
        
        return f"✅ OD Request submitted successfully! OD ID: {od.id}. Faculty have been notified."
    except Exception as e:
        db.rollback()
        return f"Database Error submitting OD request: {str(e)}"
    finally:
        db.close()

@tool
@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
def get_od_summary_by_status(status: str) -> str:
    """
    Fetches a summary of student OD requests based on their status. 
    Use this for Faculty/HOD monitoring.
    Valid statuses: 'Pending Result', 'Awaiting Proof', 'Participated', 'Won'
    """
    db = SessionLocal()
    try:
        ods = db.query(ODRequest).filter(ODRequest.result_status == status).order_by(ODRequest.created_at.desc()).limit(10).all()
        if not ods:
            return f"No OD requests found with status: '{status}'."
            
        summary = [f"📊 OD Requests ({status}):"]
        for od in ods:
            summary.append(f"- ID {od.id}: {od.student_name} ({od.student_id}) at {od.college_name} for '{od.event_details}' on {od.date}.")
        return "\\n".join(summary)
    except Exception as e:
        return f"Database error fetching ODs: {str(e)}"
    finally:
        db.close()

@tool
@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
def get_student_od_history(student_id: str) -> str:
    """
    Fetches the entire On Duty (OD) participation history for a specific student_id.
    Use this when Faculty asks about a particular student's OD track record.
    """
    db = SessionLocal()
    try:
        student_id = student_id.strip().upper()
        ods = db.query(ODRequest).filter(ODRequest.student_id == student_id).order_by(ODRequest.created_at.desc()).all()
        if not ods:
            return f"No OD history found for student {student_id}."
            
        summary = [f"📜 OD History for {ods[0].student_name} ({student_id}):"]
        for od in ods:
            prize = f" | Prize: {od.prize_details}" if od.prize_details else ""
            summary.append(f"- [OD {od.id}] {od.date}: {od.event_details} at {od.college_name} | Status: {od.result_status}{prize}")
        return "\\n".join(summary)
    except Exception as e:
        return f"Database error fetching OD history: {str(e)}"
    finally:
        db.close()

@tool
@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
def verify_prize_details(od_id: int) -> str:
    """
    Fetches the specific prize details and verification status for an OD request.
    Use this when Faculty wants to verify or detailed info about a specific OD/prize.
    CRITICAL: This tool automatically triggers the UI Modal, so simply recount the text details.
    """
    db = SessionLocal()
    try:
        od = db.query(ODRequest).filter(ODRequest.id == od_id).first()
        if not od:
            return f"OD request #{od_id} not found."
            
        details = (
            f"🔍 Verification Details for OD #{od_id} ({od.student_name}):\\n"
            f"- Event: {od.event_details} at {od.college_name}\\n"
            f"- Status: {od.result_status}\\n"
            f"- Prize: {od.prize_details or 'None'}\\n"
            f"- AI Verification: {od.verification_status or 'Pending'}\\n"
            f'\\n{json.dumps({"action": "OPEN_MODAL", "target_id": f"od_{od_id}"})}'
        )
        return details
    except Exception as e:
        return f"Database error verifying prize: {str(e)}"
    finally:
        db.close()
