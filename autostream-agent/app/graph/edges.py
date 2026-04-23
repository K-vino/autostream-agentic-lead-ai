from app.memory.state import AgentState

def route_intent(state: AgentState):
    """
    Routes the workflow based on detected intent.
    """
    intent = state.get("intent")
    
    if intent == "greeting":
        return "greeting"
    elif intent == "inquiry":
        return "rag"
    elif intent == "high_intent":
        return "lead"
    else:
        return "rag" # Default

def route_lead_capture(state: AgentState):
    """
    Decides whether to trigger the tool or end the turn.
    """
    if state.get("lead_complete"):
        return "tool"
    else:
        return "__end__"
