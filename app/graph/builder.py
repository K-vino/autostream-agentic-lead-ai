from langgraph.graph import StateGraph, END
from app.memory.state import AgentState
from app.graph.nodes import intent_node, rag_node, lead_node, tool_node, greeting_node
from app.graph.edges import route_intent, route_lead_capture

def create_graph():
    # Initialize the graph with our state schema
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("intent", intent_node)
    workflow.add_node("rag", rag_node)
    workflow.add_node("lead", lead_node)
    workflow.add_node("tool", tool_node)
    workflow.add_node("greeting", greeting_node)

    # Set entry point
    workflow.set_entry_point("intent")

    # Add conditional edges from intent node
    workflow.add_conditional_edges(
        "intent",
        route_intent,
        {
            "greeting": "greeting",
            "rag": "rag",
            "lead": "lead"
        }
    )

    # After RAG or Greeting, the conversation turn ends
    workflow.add_edge("rag", END)
    workflow.add_edge("greeting", END)

    # Conditional edge from lead node (trigger tool if complete)
    workflow.add_conditional_edges(
        "lead",
        route_lead_capture,
        {
            "tool": "tool",
            "__end__": END
        }
    )

    # After tool execution, the turn ends
    workflow.add_edge("tool", END)

    # Compile the graph
    return workflow.compile()
