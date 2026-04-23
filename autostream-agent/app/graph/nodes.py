from app.agents.intent_agent import IntentAgent
from app.agents.rag_agent import RAGAgent
from app.agents.lead_agent import LeadAgent
from app.tools.lead_capture import mock_lead_capture
from app.memory.state import AgentState
from langchain_core.messages import AIMessage, HumanMessage

# Initialize agents
intent_agent = IntentAgent()
rag_agent = RAGAgent()
lead_agent = LeadAgent()

def intent_node(state: AgentState):
    """
    Classifies the user's intent.
    """
    print("--- [NODE] Intent Classification ---")
    user_input = state["input"]
    intent = intent_agent.classify(user_input)
    
    return {
        "intent": intent,
        "history": state["history"] + [HumanMessage(content=user_input)]
    }

def rag_node(state: AgentState):
    """
    Handles product inquiries using RAG.
    """
    print("--- [NODE] RAG (Knowledge Retrieval) ---")
    response = rag_agent.answer(state["input"])
    
    return {
        "response": response,
        "history": state["history"] + [AIMessage(content=response)]
    }

def lead_node(state: AgentState):
    """
    Manages the lead collection flow.
    """
    print("--- [NODE] Lead Collection ---")
    
    # 1. Extract info from current input
    extracted = lead_agent.extract_info(state["input"], {
        "name": state.get("name"),
        "email": state.get("email"),
        "platform": state.get("platform")
    })
    
    # 2. Update state with extracted info
    new_state = {
        "name": extracted.get("name") or state.get("name"),
        "email": extracted.get("email") or state.get("email"),
        "platform": extracted.get("platform") or state.get("platform")
    }
    
    # 3. Check if we have everything
    if new_state["name"] and new_state["email"] and new_state["platform"]:
        new_state["lead_complete"] = True
        response = "Thank you! I've collected all the details. I'm setting up your account now..."
    else:
        new_state["lead_complete"] = False
        response = lead_agent.get_response(state["input"], new_state)
    
    new_state["response"] = response
    new_state["history"] = state["history"] + [AIMessage(content=response)]
    
    return new_state

def tool_node(state: AgentState):
    """
    Executes the mock lead capture tool.
    """
    print("--- [NODE] Tool Execution ---")
    result = mock_lead_capture(state["name"], state["email"], state["platform"])
    
    final_response = f"{state['response']}\n\n[System Notification: {result}]"
    
    return {
        "response": final_response,
        "history": state["history"] + [AIMessage(content="Lead captured successfully.")]
    }

def greeting_node(state: AgentState):
    """
    Handles simple greetings.
    """
    print("--- [NODE] Greeting ---")
    response = "Hello! Welcome to AutoStream. How can I help you today? I can answer questions about our pricing and features, or help you get started with a plan."
    
    return {
        "response": response,
        "history": state["history"] + [AIMessage(content=response)]
    }
