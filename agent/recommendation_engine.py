from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from database.models import Student, KPI, Score
from database.database import get_db
import os
import json
import time

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
You are generating personalized notification alerts and recommendations for {student_name}, a student in the {department} department.

Their current KPI Score is {kpi_score}/100.
Their Career Readiness assessment is: {career_readiness}.

Here is the breakdown of their current KPI achievements:
{kpi_breakdown}

Analyze the student's activity specifically focusing on:
1. **Blog Topics & Content**: Suggest highly specific blog topics they should write about based on their highest-performing domains (e.g., if they have 3 publications and 0 projects, suggest writing about academic research methodologies).
2. **Hackathon Ideas & Mistakes**: Analyze their Hackathon metrics. If it's low or 0, explicitly tell them mistakes they made by skipping hackathons, and give them 1 specific beginner hackathon project idea to build.
3. **Upcoming Events**: Invent 1 realistic "upcoming college event" (e.g., "Annual AI Symposium 2026") that directly matches their weak points so they can improve.
4. **General Advice**: Advice tailored closely to their specific high/low points.

You MUST respond strictly with a valid JSON array of exactly 4 notification objects. 
Each object must have a "title" string and a "message" string. 
CRITICAL: The "message" string MUST be composed of 2-3 short, punchy bullet points formatted with the '-' character. Be highly concise. Do not write paragraphs.

Example output format:
[
  {{"title": "Hackathon Strategy", "message": "- You haven't participated in any hackathons!\n- Mistake: Skipping practical networking.\n- Idea: Build a simple CRUD app next weekend."}},
  {{"title": "Recommended Blog Topic", "message": "- Your 3 projects show practical capability.\n- Action: Write a blog post titled 'Building My First Robust Full-Stack Project'."}}
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

Analyze these aggregate metrics and generate strategic insights for the {role} specifically focusing on:
1. **Improving Performance**: Actionable recommendations for improving the department's weakest student performance areas.
2. **Strengths & Weaknesses**: Explicitly state the strong parts and weak parts of the students in this department.
3. **Active Participation**: Highlight where students are actively participating the most and how to leverage that momentum.

You MUST respond strictly with a valid JSON array of exactly 4 notification objects. 
Each object must have a "title" string and a "message" string. 
CRITICAL: The "message" string MUST be composed of 2-3 short, punchy bullet points formatted with the '-' character. Be highly concise. Do not write paragraphs.
"""
        )

        self.idea_enhancer_prompt = PromptTemplate(
            input_variables=["student_idea"],
            template="""You are an expert AI mentor and technical editor. Evaluate the following idea or blog content submitted by a student.

Student Submission:
"{student_idea}"

1. Critique the idea/content for clarity, impact, and technical feasibility.
2. Provide 3 specific, actionable recommendations on how to dramatically improve it.
3. Suggest an eye-catching alternative title.

Format your response as a deeply helpful, markdown-formatted critique. Use bolding, bullet points, and headers (##) to make it highly readable. Do not output JSON.
"""
        )

    def enhance_idea(self, idea_text: str) -> str:
        """
        Critiques a student's idea or blog content.
        """
        chain = self.idea_enhancer_prompt | self.llm
        
        # Add a retry loop for SSL EOF errors
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = chain.invoke({"student_idea": idea_text})
                return response.content.strip()
            except Exception as e:
                err_str = str(e)
                if "SSL" in err_str or "EOF" in err_str or "protocol" in err_str:
                    if attempt < max_retries - 1:
                        time.sleep(1)
                        continue
                return f"**Error generating critique:** {err_str}\n\nOur AI engine is currently experiencing connectivity issues. Please try again in a moment."

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
                
                # Add retry loop for student generation
                response = None
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        response = chain.invoke({
                            "student_name": student.name,
                            "department": student.department,
                            "kpi_score": kpi_score_val,
                            "career_readiness": readiness_val,
                            "kpi_breakdown": kpi_breakdown_text
                        })
                        break
                    except Exception as e:
                        err_str = str(e)
                        if "SSL" in err_str or "EOF" in err_str or "protocol" in err_str:
                            if attempt < max_retries - 1:
                                time.sleep(1)
                                continue
                        return [{"title": "Connection Interrupted", "message": f"Our AI engine experienced a temporary drop: {err_str}. Please refresh to try again."}]
            
            if not response:
                return [{"title": "AI Offline", "message": "Failed to generate recommendations after multiple attempts."}]
                
            raw = response.content.strip()
            
            import re
            
            # Robust JSON array extraction to handle unpredictable LLM markdown wrapping
            json_match = re.search(r'\[.*\]', raw, re.DOTALL)
            if json_match:
                raw = json_match.group(0)
            else:
                # If no array brackets are found, try fallback standard cleanup
                raw = raw.replace("```json", "").replace("```", "").strip()
            
            try:
                notifications = json.loads(raw)
                return notifications
            except json.JSONDecodeError:
                # Fallback if the LLM output is malformed
                return [{"title": "AI Error", "message": "I generated insights but failed to format them correctly. Please try again later."}]

        finally:
            db.close()

recommendation_engine = RecommendationEngine()
