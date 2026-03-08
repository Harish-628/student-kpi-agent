from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage
from agent.tools import get_top_students, get_lowest_students, upload_certificate_kpi, add_mock_faculty
import os
from dotenv import load_dotenv

load_dotenv()

class WebChatbot:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7,
            api_key=os.environ.get("GEMINI_API_KEY")
        )

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
 LIVE CONTEXT (from database)
═══════════════════════════════════════════════════
{context}

═══════════════════════════════════════════════════
 GENERAL INSTRUCTIONS
═══════════════════════════════════════════════════
- Be concise, friendly, and professional.
- You have autonomous Tools. YOU CAN ACTUALLY INVOKE THEM.
- Always call the appropriate performer tool proactively when the user asks about performance,
  rankings, who is at the top, who needs help, etc. — do not just say "I can look that up."
- When you use a tool, explain clearly what data you fetched.
- For file uploads: visually inspect the attached image. If it looks like a valid certificate/document,
  call upload_certificate_kpi. If it is clearly irrelevant (e.g., a photo of a dog), politely refuse.
- If the user asks something outside your tool capabilities or role permissions, politely explain why.

Now, answer the User's Query.
"""

    def generate_chat_response(self, query: str, user_role: str, user_email: str, context: str = "", image: str = None) -> str:
        """
        Generates an autonomous agentic chat response utilizing dynamic role-based tools.
        """
        
        # 1. Determine Role-Based Tools Access
        active_tools = []
        if user_role == "admin":
            active_tools = [get_top_students, get_lowest_students, upload_certificate_kpi, add_mock_faculty]
        elif user_role == "hod":
            active_tools = [get_top_students, get_lowest_students, upload_certificate_kpi]
        elif user_role == "faculty":
            active_tools = [get_top_students, get_lowest_students, upload_certificate_kpi]
        elif user_role == "student":
            active_tools = [get_top_students, upload_certificate_kpi]
            
        # 2. Compile the ReAct Agent Graph with the tools subset
        agent = create_react_agent(self.llm, tools=active_tools)
        
        # 3. Format the specific instructions for this turn
        sys_msg = SystemMessage(content=self.system_instructions.format(
            user_role=user_role,
            user_email=user_email,
            context=context
        ))
        
        # Format HumanMessage to support image if provided
        if image:
            # Check if it has a data URL prefix and extract the base64 part
            content_blocks = [{"type": "text", "text": query}]
            
            # Extract just the base64 part if formatted as data:image/png;base64,...
            if "," in image:
                b64_data = image.split(",", 1)[1]
            else:
                b64_data = image
                
            content_blocks.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{b64_data}"}
            })
            human_msg = HumanMessage(content=content_blocks)
        else:
            human_msg = HumanMessage(content=query)
        
        # 4. Invoke the Graph
        response_state = agent.invoke({"messages": [sys_msg, human_msg]})
        
        # The agent's final answer is always the last AIMessage in the state
        content = response_state["messages"][-1].content
        if isinstance(content, list):
            # Sometimes LangChain returns a list of blocks like [{'type': 'text', 'text': '...'}]
            final_answer = " ".join([block.get("text", "") for block in content if isinstance(block, dict) and "text" in block])
            if not final_answer:
                final_answer = str(content)
        else:
            final_answer = str(content)
            
        return final_answer


# Singleton instance for the router
web_chatbot = WebChatbot()
