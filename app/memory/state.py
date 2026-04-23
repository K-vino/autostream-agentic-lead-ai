from typing import Annotated, List, TypedDict, Optional
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """
    Represents the state of our agent workflow.
    """
    # User input
    input: str
    
    # Classification result
    intent: Optional[str]
    
    # Lead collection fields
    name: Optional[str]
    email: Optional[str]
    platform: Optional[str]
    
    # The agent's response to the user
    response: Optional[str]
    
    # Full conversation history
    history: List[BaseMessage]
    
    # Flag to indicate if lead capture is complete
    lead_complete: bool
