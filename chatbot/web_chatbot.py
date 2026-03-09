from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv
load_dotenv(override=True)
from agent.tools import (
    get_top_students, get_lowest_students, upload_certificate_kpi, add_mock_faculty,
    extract_od_details, apply_student_od, get_od_summary_by_status, get_student_od_history, verify_prize_details
)
from google import genai
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from google.api_core import exceptions
from typing import Optional
class WebChatbot:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        
        # 1. Initialize distinct model profiles
        # Utility LLM: Optimized for classification and speed
        self.utility_llm = ChatGoogleGenerativeAI(
            model="gemini-3.1-flash-lite-preview",
            temperature=0.1,  # Low temperature for classification
            api_key=self.api_key
        )
        
        # Response LLM: Optimized for reasoning and depth
        self.response_llm = ChatGoogleGenerativeAI(
            model="gemini-3.1-flash-lite-preview",
            temperature=0.7,
            api_key=self.api_key
        )
        
        # Native SDK Client for specific use cases (Hybrid Architecture)
        self.genai_client = genai.Client(api_key=self.api_key)

        self.system_instructions = """You are the Neural KPI Agent, an advanced academic AI assistant for the NeuralKPI platform.
You are chatting with: {user_role} (Email: {user_email}).

═══════════════════════════════════════════════════
 KPI SCORING RULES (Live System — always reference these)
═══════════════════════════════════════════════════
KPI scores are calculated out of 100 based on the following weighted categories:

| Category              | Max Points | Weight |
|-----------------------|------------|--------|
| Internships           | 10         | High   |
| Certifications        | 10         | High   |
| Hackathons            | 10         | High   |
| Publications          | 10         | High   |
| Workshops             | 5          | Medium |
| Projects              | 10         | High   |
| Club Activities       | 5          | Medium |
| Industrial Visits     | 5          | Medium |
| Research Papers       | 10         | High   |
| Patents               | 10         | High   |
| Value Added Courses   | 5          | Medium |

Career Readiness Tiers:
- 80–100 → ⭐ Industry Ready
- 60–79  → ✅ Approaching Ready
- 40–59  → 📈 Developing
- 0–39   → ⚠️ Needs Support

═══════════════════════════════════════════════════
 ROLE-BASED PERFORMANCE REPORTING (CRITICAL RULES)
═══════════════════════════════════════════════════
Follow these rules STRICTLY when reporting performers:

STUDENT role:
  ✅ ALWAYS share the overall top performer (use get_top_students with no filter).
  ❌ Do NOT share lowest performers to students.

FACULTY role:
  ✅ ALWAYS share the top performer in their department.
  ✅ ALWAYS share the lowest performer in their department (so they can help).
  🔒 Filter BOTH calls by the faculty's department extracted from their email/context.

HOD role:
  ✅ ALWAYS share the top performer in their department.
  ✅ ALWAYS share the lowest performer in their department.
  🔒 Filter BOTH calls by the HOD's department extracted from their email/context.

ADMIN role:
  ✅ ALWAYS share the overall top performer (all departments).
  ✅ ALWAYS share the lowest performer across all departments (no filter).

═══════════════════════════════════════════════════
 ON DUTY (OD) & EVENT PARTICIPATION RULES
═══════════════════════════════════════════════════
STUDENT role:
- When a student asks to apply for OD, you must collect these 6 fields: college_name, event_details, date, start_time, end_time, num_days.
- Use `extract_od_details` to extract any fields they provide.
- They have already provided some details. Current OD Form State:
{od_form}
- If any fields are null/None, politely ask for them one by one.
- Only when ALL 6 fields are filled and the student confirms, call `apply_student_od`.

FACULTY / HOD role:
- When asked "who is on leave", "who is out today", etc., call `get_od_summary_by_status` (try 'Pending Result' or 'Participated').
- When asked about a specific student's OD history, call `get_student_od_history`.
- When asked to verify or show prize details for a specific OD, call `verify_prize_details`.
- CRITICAL: If a tool returns a JSON string like `{{"action": "OPEN_MODAL", "target_id": "od_123"}}`, you MUST include this exact JSON text in your verbal response so the frontend UI can trigger the modal automatically. Do not modify the JSON.

═══════════════════════════════════════════════════
 GENERAL INSTRUCTIONS
═══════════════════════════════════════════════════
- Be concise, friendly, and professional.
- You have autonomous Tools. YOU CAN ACTUALLY INVOKE THEM.
- Always call the appropriate tool proactively when the user asks about performance, rankings, who is out on OD, etc.
- When you use a tool, explain clearly what data you fetched.
- If the user asks something outside your tool capabilities or role permissions, politely explain why.

Now, answer the User's Query.
"""

    @staticmethod
    def return_quota_limit_msg(retry_state):
        print("[WebChatbot] ALL RETRIES EXHAUSTED (429 Quota). Returning fallback.")
        return "I'm currently assisting many users. Please wait 60 seconds."

    @retry(
        retry=retry_if_exception_type(exceptions.ResourceExhausted),
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=10, min=10, max=40),
        retry_error_callback=return_quota_limit_msg,
        reraise=False
    )
    def generate_chat_response(self, query: str, user_role: str, user_email: str, context: str = "", image: Optional[str] = None, od_form: Optional[dict] = None) -> str:
        """
        Generates an autonomous agentic chat response utilizing dynamic role-based tools.
        Uses Hybrid Model Routing: defaults to response_llm for tools/depth.
        """
        try:
            # 1. Determine Role-Based Tools Access
            active_tools = []
            if user_role == "admin":
                active_tools = [get_top_students, get_lowest_students, upload_certificate_kpi, add_mock_faculty, extract_od_details, apply_student_od, get_od_summary_by_status, get_student_od_history, verify_prize_details]
            elif user_role == "hod" or user_role == "faculty":
                active_tools = [get_top_students, get_lowest_students, upload_certificate_kpi, get_od_summary_by_status, get_student_od_history, verify_prize_details]
            elif user_role == "student":
                active_tools = [get_top_students, upload_certificate_kpi, extract_od_details, apply_student_od]
                
            # 2. Compile the ReAct Agent Graph with the tools subset
            # Using RESPONSE_LLM for detailed tool-based analysis
            llm_with_tools = self.response_llm.bind_tools(active_tools)
            agent = create_react_agent(llm_with_tools, tools=active_tools)

            
            # 3. Format instructions
            od_form_str = str(od_form) if od_form else "No OD form started."
            sys_msg = SystemMessage(content=self.system_instructions.format(
                user_role=user_role,
                user_email=user_email,
                context=context,
                od_form=od_form_str
            ))
            
            # Message formatting
            if image:
                if "," in image: b64_data = image.split(",", 1)[1]
                else: b64_data = image
                human_msg = HumanMessage(content=[
                    {"type": "text", "text": query},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_data}"}}
                ])
            else:
                human_msg = HumanMessage(content=query)
            
            # 4. Invoke with Logging
            print(f"[WebChatbot] Routing to RESPONSE_LLM (gemini-3.1-flash-preview)")
            query_preview = str(query)[:50]
            print(f"[WebChatbot] Invoking agent for: {query_preview}...")
            
            response_state = agent.invoke({"messages": [sys_msg, human_msg]})
            last_message = response_state["messages"][-1]
            
            if hasattr(last_message, "tool_calls"):
                print(f"[WebChatbot] RAW Tool Calls: {last_message.tool_calls}")
            
            content = last_message.content
            final_answer = str(content) if not isinstance(content, list) else " ".join([b.get("text", "") for b in content if isinstance(b, dict) and "text" in b])
            
            print(f"[WebChatbot] Success. Length: {len(final_answer)}")
            return final_answer

        except exceptions.ResourceExhausted:
            # Tenacity will retry based on decorator. 
            # If all attempts fail, it will return the fallback via the decorator logic (or we catch here if reraise=True)
            raise 
        except Exception as e:
            print(f"[WebChatbot ERROR] {str(e)}")
            return f"I encountered an error processing your request: {str(e)}"



# Singleton instance for the router
web_chatbot = WebChatbot()
