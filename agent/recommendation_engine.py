from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from backend.kpi_engine import calculate_kpi_score, predict_career_readiness
from database.models import Student, KPI, Score
from database.database import get_db
import os

class RecommendationEngine:
    def __init__(self):
        # Configure Gemini model for recommendations
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7,
            api_key=os.environ.get("GEMINI_API_KEY")
        )

        self.recommendation_prompt = PromptTemplate(
            input_variables=["student_name", "department", "kpi_score", "career_readiness", "kpi_breakdown", "context"],
            template="""You are an expert AI academic and career advisor.
You are advising {student_name}, a student in the {department} department.

Their current KPI Score is {kpi_score}/100.
Their Career Readiness assessment is: {career_readiness}.

Here is the breakdown of their current KPI achievements:
{kpi_breakdown}

General Knowledge base context to guide your advice:
{context}

Based on this specific student's profile and the general knowledge context, provide a concise, personalized, and actionable 3-point recommendation plan. 
Focus heavily on the areas in their KPI breakdown where they score a 0 or very low. 
Highlight why improving those specific areas will help their career readiness. Be encouraging but direct.
"""
        )

    def generate_recommendation(self, student_id: str, context: str = "") -> str:
        """
        Generates a personalized recommendation snippet for the student dashboard.
        Requires a database session to fetch student stats.
        """
        db = next(get_db())
        try:
            student = db.query(Student).filter(Student.student_id == student_id).first()
            if not student:
                return "Student profile not found. Unable to generate recommendations at this time."

            kpi = db.query(KPI).filter(KPI.student_id == student_id).first()
            if not kpi:
                return "Student KPI metrics not found. Add some KPI data to get personalized recommendations!"

            score = db.query(Score).filter(Score.student_id == student_id).first()
            
            kpi_score_val = score.kpi_score if score else 0
            readiness_val = score.career_readiness_score if score else "Unknown"

            kpi_breakdown_text = f"""
            Internships: {kpi.internships}
            Certifications: {kpi.certifications}
            Hackathons: {kpi.hackathons}
            Publications: {kpi.publications}
            Workshops: {kpi.workshops}
            Projects: {kpi.projects}
            Club Activities: {kpi.club_activities}
            Industrial Visits: {kpi.industrial_visits}
            """

            chain = self.recommendation_prompt | self.llm
            response = chain.invoke({
                "student_name": student.name,
                "department": student.department,
                "kpi_score": kpi_score_val,
                "career_readiness": readiness_val,
                "kpi_breakdown": kpi_breakdown_text,
                "context": context
            })
            
            return response.content

        finally:
            db.close()

recommendation_engine = RecommendationEngine()
