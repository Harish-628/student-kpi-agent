from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from database.models import Student, KPI, Score
from database.database import get_db
import os
import json

class RecommendationEngine:
    def __init__(self):
        # Configure Gemini model for recommendations
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7,
            api_key=os.environ.get("GEMINI_API_KEY")
        )

        self.student_prompt = PromptTemplate(
            input_variables=["student_name", "department", "kpi_score", "career_readiness", "kpi_breakdown"],
            template="""You are an expert AI academic and career advisor.
You are generating personalized notification alerts for {student_name}, a student in the {department} department.

Their current KPI Score is {kpi_score}/100.
Their Career Readiness assessment is: {career_readiness}.

Here is the breakdown of their current KPI achievements:
{kpi_breakdown}

Analyze the student's activity specifically focusing on:
1. Their underlying domain/interests based on where they score high (e.g., if they do many projects but few publications, they lean towards practical dev).
2. Their Hackathon metrics. If it's low or 0, explicitly tell them mistakes they made by skipping hackathons or how to start.
3. Their Publications/Blogs metrics. Point out how to improve or praise them.
4. General advice tailored closely to their specific high/low points.

You MUST respond strictly with a valid JSON array of exactly 3 or 4 notification objects. 
Each object must have a "title" string and a "message" string. DO NOT use markdown formatting outside the JSON array.

Example output format:
[
  {{"title": "Hackathon Strategy", "message": "You haven't participated in any hackathons yet! This is a missed opportunity to network and test your practical skills."}},
  {{"title": "Domain Insight: Practical Dev", "message": "Your high project count shows great practical capability. Try to write a blog post documenting your best project."}}
]
"""
        )

        self.faculty_prompt = PromptTemplate(
            input_variables=["role", "department", "student_count", "avg_kpi", "metrics_breakdown"],
            template="""You are an AI Academic Dean advising a {role} managing the {department} department.

Department Overview:
Active Students Analyzed: {student_count}
Average Department KPI Score: {avg_kpi}/100

Aggregated Department Metrics:
{metrics_breakdown}

Analyze these aggregate metrics and generate strategic insights for the {role}:
1. Identify areas where the department is excelling (e.g., high average projects or internships).
2. Identify critical gaps where students are underperforming (e.g., low hackathon participation or publications) and suggest how the {role} can encourage them.
3. Provide one actionable strategy to boost overall student career readiness.

You MUST respond strictly with a valid JSON array of exactly 3 or 4 notification objects. 
Each object must have a "title" string and a "message" string. DO NOT use markdown formatting outside the JSON array.
"""
        )

    def generate_kpi_notifications(self, user_id: str, role: str = "student"):
        """
        Generates contextual AI notification alerts tailored for a specific student's KPI footprint.
        Returns a list of dictionaries: [{"title": "...", "message": "..."}]
        """
        db = next(get_db())
        try:
            if role in ["faculty", "hod"]:
                # user_id is like "fac.cse" or "hod.cse". Extract department.
                parts = user_id.split('.')
                dept_code = parts[1].upper() if len(parts) > 1 else "CSE"
                
                # Map dept code to full name for DB matching if needed, but our student_id prefix is often the dept code (e.g. CSE001)
                students = db.query(Student).filter(Student.student_id.like(f"{dept_code}%")).all()
                if not students:
                    return [{"title": "Department Alert", "message": f"No students found in the {dept_code} department."}]
                
                student_ids = [s.student_id for s in students]
                scores = db.query(Score).filter(Score.student_id.in_(student_ids)).all()
                kpis = db.query(KPI).filter(KPI.student_id.in_(student_ids)).all()
                
                avg_kpi = round(sum([s.kpi_score for s in scores]) / len(scores), 1) if scores else 0
                
                avg_hackathons = round(sum([k.hackathons for k in kpis]) / len(kpis), 1) if kpis else 0
                avg_projects = round(sum([k.projects for k in kpis]) / len(kpis), 1) if kpis else 0
                avg_pubs = round(sum([k.publications for k in kpis]) / len(kpis), 1) if kpis else 0
                avg_intern = round(sum([k.internships for k in kpis]) / len(kpis), 1) if kpis else 0
                
                metrics_text = f"Avg Hackathons: {avg_hackathons}\nAvg Projects: {avg_projects}\nAvg Publications: {avg_pubs}\nAvg Internships: {avg_intern}"
                
                chain = self.faculty_prompt | self.llm
                response = chain.invoke({
                    "role": role.upper(),
                    "department": dept_code,
                    "student_count": len(students),
                    "avg_kpi": avg_kpi,
                    "metrics_breakdown": metrics_text
                })
                
            else:
                # Student Logic
                safe_student_id = user_id.upper()
                student = db.query(Student).filter(Student.student_id == safe_student_id).first()
                if not student:
                    return [{"title": "System Alert", "message": "Student profile not found. Unable to generate recommendations."}]

                kpi = db.query(KPI).filter(KPI.student_id == safe_student_id).first()
                if not kpi:
                    return [{"title": "System Alert", "message": "Student KPI metrics not found. Add data to unlock AI recommendations!"}]

                score = db.query(Score).filter(Score.student_id == safe_student_id).first()
                kpi_score_val = score.kpi_score if score else 0
                readiness_val = score.career_readiness_score if score else "Unknown"

                kpi_breakdown_text = f"""
                Internships: {kpi.internships}
                Certifications: {kpi.certifications}
                Hackathons: {kpi.hackathons}
                Publications/Blogs: {kpi.publications}
                Workshops: {kpi.workshops}
                Projects: {kpi.projects}
                Club Activities: {kpi.club_activities}
                Industrial Visits: {kpi.industrial_visits}
                """

                chain = self.student_prompt | self.llm
                response = chain.invoke({
                    "student_name": student.name,
                    "department": student.department,
                    "kpi_score": kpi_score_val,
                    "career_readiness": readiness_val,
                    "kpi_breakdown": kpi_breakdown_text
                })
            
            raw = response.content.strip()
            
            # Remove any markdown wrapping the LLM might mistakenly add
            if raw.startswith("```json"):
                raw = raw[7:]
            if raw.endswith("```"):
                raw = raw[:-3]
            
            try:
                notifications = json.loads(raw)
                return notifications
            except json.JSONDecodeError:
                # Fallback if the LLM output is malformed
                return [{"title": "AI Error", "message": "I generated insights but failed to format them correctly. Please try again later."}]

        finally:
            db.close()

recommendation_engine = RecommendationEngine()
