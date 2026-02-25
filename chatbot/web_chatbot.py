from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage
from agent.tools import get_top_students, upload_certificate_kpi, add_mock_faculty
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

        self.system_instructions = """You are the Neural KPI Agent, an advanced academic AI assistant with database interaction privileges.
You are chatting with a user who is logged in as: {user_role} (Email: {user_email}).

Role and Tone:
- Be concise, friendly, and professional.
- If the user is just saying hello, greet them warmly.
- You have been equipped with autonomous Tools. YOU CAN ACTUALLY INVOKE THEM.
- When you use a tool, explain what you did or what data you fetched clearly.
- If the user asks you to do something outside your Tool list capabilities (or their role permissions), politely inform them your current access level cannot perform that request.

Here is relevant general context retrieved from the KPI system's database (if any):
{context}

Now, answer the User's Query.
"""

    def generate_chat_response(self, query: str, user_role: str, user_email: str, context: str = "", image: str = None) -> str:
        """
        Generates an autonomous agentic chat response utilizing dynamic role-based tools.
        """
        
        # 1. Determine Role-Based Tools Access
        active_tools = []
        if user_role == "admin":
            active_tools = [get_top_students, upload_certificate_kpi, add_mock_faculty]
        elif user_role == "hod":
            active_tools = [get_top_students, upload_certificate_kpi]
        elif user_role == "faculty":
            active_tools = [get_top_students, upload_certificate_kpi]
        elif user_role == "student":
            active_tools = [upload_certificate_kpi]
            
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
