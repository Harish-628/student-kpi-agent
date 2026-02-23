from typing import Dict, Any
from langgraph.graph import StateGraph, END
from vector_db.chroma_helper import chroma_db
from chatbot.web_chatbot import web_chatbot

# Define state dictionary schema for the LangGraph
class AgentState(Dict[str, Any]):
    query: str
    user_role: str
    user_email: str
    context: str
    response: str

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

def generate_response_node(state: AgentState):
    """Final node passes context and query to Gemini via LangChain wrapper."""
    response = web_chatbot.generate_chat_response(
        query=state["query"],
        user_role=state["user_role"],
        user_email=state["user_email"],
        context=state["context"]
    )
    state["response"] = response
    print(f"[LangGraph] Generated response length: {len(response)}")
    return state

# Build LangGraph Workflow
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("parse_query", parse_query_node)
workflow.add_node("retrieve_vector_context", retrieve_vector_context_node)
workflow.add_node("generate_response", generate_response_node)

# Add edges connecting the nodes
workflow.add_edge("parse_query", "retrieve_vector_context")
workflow.add_edge("retrieve_vector_context", "generate_response")
workflow.add_edge("generate_response", END)

# Set entry point
workflow.set_entry_point("parse_query")

# Compile LangGraph application
agent_workflow = workflow.compile()
