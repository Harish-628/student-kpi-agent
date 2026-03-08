from typing import Dict, Any
from langgraph.graph import StateGraph, END
from vector_db.chroma_helper import chroma_db
from chatbot.web_chatbot import web_chatbot
from agent.tools import get_top_students, get_lowest_students
from database.database import SessionLocal
from database.models import User

# Define state dictionary schema for the LangGraph
class AgentState(Dict[str, Any]):
    query: str
    user_role: str
    user_email: str
    context: str
    response: str
    image: str

def parse_query_node(state: AgentState):
    """Initial node just normalizes the input state."""
    print(f"[LangGraph] Received query: {state['query']} from {state['user_email']}")
    return state

def retrieve_vector_context_node(state: AgentState):
    """Second node reaches out to ChromaDB to fetch RAG context."""
    # Bypass heavy RAG query for simple greetings
    if len(state["query"]) < 15 and any(word in state["query"].lower() for word in ["hi", "hello", "hey", "hai", "how are you"]):
        state["context"] = "User is just saying hello. Be friendly."
        print("[LangGraph] Bypassed ChromaDB for greeting.")
        return state

    context = chroma_db.retrieve_context(state["query"], n_results=2)
    state["context"] = context
    print(f"[LangGraph] Retrieved context length: {len(context)}")
    return state

def inject_live_kpi_context_node(state: AgentState):
    """
    Third node automatically injects live KPI data (top/lowest performers)
    based on the user's role and department, empowering the chatbot with
    up-to-the-second data before it even calls a tool.
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == state["user_email"]).first()
        if not user:
            print(f"[LangGraph WARNING] User not found for email: '{state['user_email']}'. Data injection may be incomplete.")
            dept = None
        else:
            dept = user.department
            print(f"[LangGraph] User found: {user.name} ({user.role}) in {dept or 'No Dept'}")

        role = state.get("user_role", "student")
        live_data = "\n\n--- AUTO-INJECTED LIVE KPI DATA ---\n"

        if role == "admin":
            live_data += get_top_students.invoke({"department": None}) + "\n\n" + get_lowest_students.invoke({"department": None})
        elif role in ["faculty", "hod"]:
            live_data += get_top_students.invoke({"department": dept}) + "\n\n" + get_lowest_students.invoke({"department": dept})
        elif role == "student":
            live_data += get_top_students.invoke({"department": None})

        state["context"] = str(state.get("context", "")) + live_data
        print(f"[LangGraph] Injected live KPI context for role {role}")

    except Exception as e:
        print(f"[LangGraph Error] Failed to inject live context: {e}")
    finally:
        db.close()

    return state

def generate_response_node(state: AgentState):
    """Final node passes context and query to Gemini via LangChain wrapper."""
    response = web_chatbot.generate_chat_response(
        query=state["query"],
        user_role=state["user_role"],
        user_email=state["user_email"],
        context=state["context"],
        image=state.get("image")
    )
    state["response"] = response
    print(f"[LangGraph] Generated response length: {len(response)}")
    return state

# Build LangGraph Workflow
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("parse_query", parse_query_node)
workflow.add_node("retrieve_vector_context", retrieve_vector_context_node)
workflow.add_node("inject_live_kpi_context", inject_live_kpi_context_node)
workflow.add_node("generate_response", generate_response_node)

# Add edges connecting the nodes
workflow.add_edge("parse_query", "retrieve_vector_context")
workflow.add_edge("retrieve_vector_context", "inject_live_kpi_context")
workflow.add_edge("inject_live_kpi_context", "generate_response")
workflow.add_edge("generate_response", END)

# Set entry point
workflow.set_entry_point("parse_query")

# Compile LangGraph application
agent_workflow = workflow.compile()
