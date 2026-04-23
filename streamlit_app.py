import streamlit as st
import sys
import os

# Ensure the project root is in the path for backend imports
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    # Importing the graph builder from the existing backend
    from app.graph.builder import create_graph
except ImportError:
    st.error("Error: Could not connect to the backend system. Ensure the 'app' directory is present.")
    st.stop()

# ---------------------------------------------------------
# UI CONFIGURATION & STYLING
# ---------------------------------------------------------
st.set_page_config(
    page_title="AutoStream Social-to-Lead Bot",
    page_icon="💬",
    layout="centered"
)

# WhatsApp-style Custom CSS
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #e5ddd5 !important;
    }

    /* WhatsApp Header */
    .whatsapp-header {
        background-color: #075e54;
        color: white;
        padding: 15px 20px;
        border-radius: 10px 10px 0 0;
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    .online-indicator {
        width: 10px;
        height: 10px;
        background-color: #25d366;
        border-radius: 50%;
        display: inline-block;
        margin-right: 5px;
    }

    /* Chat Bubbles Container */
    .chat-row {
        display: flex;
        width: 100%;
        margin-bottom: 12px;
    }

    /* Bubble Styling */
    .bubble {
        padding: 10px 15px;
        border-radius: 15px;
        max-width: 80%;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 15px;
        line-height: 1.4;
        box-shadow: 0 1px 1px rgba(0,0,0,0.1);
        position: relative;
    }

    /* User Bubble (Right Side, Green) */
    .user-bubble {
        background-color: #dcf8c6;
        margin-left: auto;
        border-bottom-right-radius: 2px;
        color: #303030;
    }

    /* Agent Bubble (Left Side, White) */
    .agent-bubble {
        background-color: #ffffff;
        margin-right: auto;
        border-bottom-left-radius: 2px;
        color: #303030;
    }

    /* Clean spacing for text */
    .bubble p {
        margin: 0;
    }

    /* Hide Streamlit standard header/footer */
    [data-testid="stHeader"] {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Input area styling */
    .stChatInputContainer {
        border-radius: 25px !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# UI HEADER
# ---------------------------------------------------------
st.markdown("""
    <div class="whatsapp-header">
        <div style="font-size: 28px;">👤</div>
        <div>
            <div style="font-weight: 600; font-size: 18px;">AutoStream Agent</div>
            <div style="font-size: 12px; opacity: 0.9;">
                <span class="online-indicator"></span>Online
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# BACKEND INITIALIZATION
# ---------------------------------------------------------
@st.cache_resource
def load_backend():
    return create_graph()

agent_graph = load_backend()

# ---------------------------------------------------------
# STATE MANAGEMENT
# ---------------------------------------------------------
# Chat history for display (list of dicts as requested)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Backend state object for LangGraph
if "agent_state" not in st.session_state:
    st.session_state.agent_state = {
        "input": "",
        "intent": None,
        "name": None,
        "email": None,
        "platform": None,
        "response": None,
        "history": [],
        "lead_complete": False
    }

# ---------------------------------------------------------
# MESSAGE RENDERING
# ---------------------------------------------------------
# Use a container for the messages
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        role_class = "user-bubble" if message["role"] == "user" else "agent-bubble"
        st.markdown(f"""
            <div class="chat-row">
                <div class="bubble {role_class}">
                    <p>{message["content"]}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# INTERACTION LOGIC
# ---------------------------------------------------------
# Input box at the bottom
if user_query := st.chat_input("Type your message here..."):
    # 1. Update UI History immediately
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # 2. Update Backend State input
    st.session_state.agent_state["input"] = user_query
    
    # 3. Get Agent Response (No artificial delay)
    try:
        # Run the agent graph with the current state
        output = agent_graph.invoke(st.session_state.agent_state)
        
        # Sync the entire state back
        st.session_state.agent_state = output
        
        # Extract the agent's response
        bot_response = output.get("response", "I'm sorry, I'm having trouble processing that.")
        
        # 4. Update UI History with agent response
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        # 5. Refresh UI
        st.rerun()
        
    except Exception as e:
        # Graceful error handling
        fallback_msg = "⚠️ I encountered an unexpected error. Please try again."
        st.session_state.messages.append({"role": "assistant", "content": fallback_msg})
        st.error(f"System Error: {e}")
        st.rerun()
