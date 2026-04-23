import streamlit as st
import sys
import os
from datetime import datetime

# Ensure the project root is in the path for backend imports
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    # Importing the graph builder from the existing backend
    from app.graph.builder import create_graph
    from app.config import MAX_HISTORY
except ImportError:
    st.error("⚠️ Error: Could not connect to the backend system. Ensure the 'app' directory is present.")
    MAX_HISTORY = 6 # Fallback
    st.stop()

# ---------------------------------------------------------
# UI CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="AutoStream Social-to-Lead",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# PREMIUM WHATSAPP-STYLE CSS
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Main Background & Reset */
    .stApp {
        background-color: #efeae2 !important;
        background-image: url("https://user-images.githubusercontent.com/15075759/28719144-86dc0f70-73b1-11e7-911d-60d70fcded21.png");
        background-repeat: repeat;
        background-blend-mode: multiply;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* Hide standard Streamlit header/footer to clean up the UI */
    [data-testid="stHeader"] {display: none;}
    footer {visibility: hidden;}
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 5rem !important;
        max-width: 800px;
    }

    /* Sticky WhatsApp Header */
    .whatsapp-header {
        background-color: #008069;
        color: white;
        padding: 12px 20px;
        display: flex;
        align-items: center;
        gap: 15px;
        position: sticky;
        top: 0;
        z-index: 999;
        border-radius: 0 0 12px 12px;
        box-shadow: 0 2px 4px -1px rgba(0,0,0,0.2);
        margin-bottom: 20px;
        margin-top: 0px;
    }

    .header-avatar {
        font-size: 32px;
        background: rgba(255,255,255,0.2);
        border-radius: 50%;
        width: 45px;
        height: 45px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .online-indicator {
        width: 8px;
        height: 8px;
        background-color: #25d366;
        border-radius: 50%;
        display: inline-block;
        margin-right: 5px;
        box-shadow: 0 0 5px #25d366;
    }

    /* Chat Bubbles Container */
    .chat-row {
        display: flex;
        width: 100%;
        margin-bottom: 15px;
        animation: fadeIn 0.3s ease-out forwards;
    }

    /* Common Bubble Styling */
    .bubble {
        padding: 8px 12px;
        border-radius: 12px;
        max-width: 85%;
        font-size: 15px;
        line-height: 1.5;
        box-shadow: 0 1px 2px rgba(0,0,0,0.15);
        position: relative;
        display: flex;
        flex-direction: column;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .bubble:hover {
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    /* User Bubble (Right Side, Green) */
    .user-bubble {
        background-color: #dcf8c6;
        margin-left: auto;
        border-top-right-radius: 4px;
        color: #111b21;
    }

    /* Agent Bubble (Left Side, White) */
    .agent-bubble {
        background-color: #ffffff;
        margin-right: auto;
        border-top-left-radius: 4px;
        color: #111b21;
    }

    /* Clean spacing for text */
    .bubble p {
        margin: 0;
        margin-bottom: 4px;
        white-space: pre-wrap;
    }

    /* Timestamp */
    .timestamp {
        font-size: 11px;
        color: rgba(17, 27, 33, 0.6);
        align-self: flex-end;
        margin-top: -2px;
    }

    /* Floating Input styling */
    .stChatInputContainer {
        border-radius: 24px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1) !important;
        background-color: #f0f2f5 !important;
        padding-bottom: 10px !important;
    }

    /* Typing Animation */
    .typing-indicator {
        display: flex;
        gap: 4px;
        padding: 8px 12px;
        background: #ffffff;
        border-radius: 12px;
        border-top-left-radius: 4px;
        width: fit-content;
        box-shadow: 0 1px 2px rgba(0,0,0,0.15);
        animation: fadeIn 0.3s ease-out forwards;
        margin-bottom: 15px;
    }
    .dot {
        width: 6px;
        height: 6px;
        background: #8696a0;
        border-radius: 50%;
        animation: bounce 1.4s infinite ease-in-out both;
    }
    .dot:nth-child(1) { animation-delay: -0.32s; }
    .dot:nth-child(2) { animation-delay: -0.16s; }

    @keyframes bounce {
        0%, 80%, 100% { transform: scale(0); }
        40% { transform: scale(1); }
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Error Box */
    .error-box {
        background-color: #ffe6e6;
        color: #d32f2f;
        padding: 10px 15px;
        border-radius: 8px;
        font-size: 14px;
        margin-bottom: 15px;
        border-left: 4px solid #d32f2f;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR / FUNCTIONAL CONTROLS
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Session Controls")
    
    # System Status Indicator
    st.markdown("---")
    st.markdown("**System Status:** <span style='color:#25d366;'>🟢 Connected</span>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Reset/Clear controls
    if st.button("🗑️ Clear Chat & Reset", use_container_width=True):
        st.session_state.messages = []
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
        st.rerun()

# ---------------------------------------------------------
# UI HEADER (Sticky)
# ---------------------------------------------------------
st.markdown("""
    <div class="whatsapp-header">
        <div class="header-avatar">🤖</div>
        <div style="display: flex; flex-direction: column;">
            <span style="font-weight: 600; font-size: 17px;">AutoStream Agent</span>
            <span style="font-size: 13px; opacity: 0.9; margin-top: 1px;">
                <span class="online-indicator"></span>Online
            </span>
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
if "messages" not in st.session_state:
    st.session_state.messages = []

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

if "fast_cache" not in st.session_state:
    st.session_state.fast_cache = {}

def get_fast_response(text):
    """Bypasses LLM for ultra-fast responses (<10ms)"""
    text = text.lower().strip()
    if text in st.session_state.fast_cache:
        return st.session_state.fast_cache[text]
    
    # Direct Keyword Matching (Fast Path)
    if any(x in text for x in ["hi", "hello", "hey", "greeting"]):
        return "Hello! Welcome to AutoStream. How can I help you today?"
    if any(x in text for x in ["price", "cost", "plan", "subscription"]):
        return "AutoStream offers two main plans: Basic ($29/mo) for 10 videos and Pro ($79/mo) for unlimited 4K videos. Which one interests you?"
    if "refund" in text:
        return "Our policy is: No refunds after 7 days of subscription."
    if any(x in text for x in ["who", "what is autostream", "about"]):
        return "AutoStream is an automated video editing tool designed for creators to streamline their workflow."
    
    return None

# ---------------------------------------------------------
# MESSAGE RENDERING
# ---------------------------------------------------------
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        role_class = "user-bubble" if message["role"] == "user" else "agent-bubble"
        timestamp = message.get("time", "")
        
        st.markdown(f"""
            <div class="chat-row">
                <div class="bubble {role_class}">
                    <p>{message["content"]}</p>
                    <span class="timestamp">{timestamp}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

# Element to anchor auto-scrolling
st.markdown("<div id='chat-end'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# INTERACTION LOGIC
# ---------------------------------------------------------
# Floating Input box
if user_query := st.chat_input("Message AutoStream Agent..."):
    
    current_time = datetime.now().strftime("%I:%M %p")
    
    # 1. Update UI History instantly
    st.session_state.messages.append({
        "role": "user", 
        "content": user_query,
        "time": current_time
    })
    
    # Render user message instantly
    with chat_container:
        st.markdown(f"""
            <div class="chat-row">
                <div class="bubble user-bubble">
                    <p>{user_query}</p>
                    <span class="timestamp">{current_time}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
        typing_placeholder = st.empty()
        typing_placeholder.markdown("""
            <div class="typing-indicator">
                <div class="dot"></div><div class="dot"></div><div class="dot"></div>
            </div>
        """, unsafe_allow_html=True)

    # 2. FAST-PATH LOOKUP (<50ms)
    bot_response = get_fast_response(user_query)
    
    if not bot_response:
        # 3. Backend State & Trim History
        st.session_state.agent_state["input"] = user_query
        if len(st.session_state.agent_state["history"]) > MAX_HISTORY:
            st.session_state.agent_state["history"] = st.session_state.agent_state["history"][-MAX_HISTORY:]
        
        # 4. Get Agent Response
        try:
            output = agent_graph.invoke(st.session_state.agent_state)
            st.session_state.agent_state = output
            bot_response = output.get("response", "I'm sorry, I couldn't process that.")
            st.session_state.fast_cache[user_query.lower().strip()] = bot_response
        except Exception as e:
            typing_placeholder.empty()
            st.error(f"Backend Error: {e}")
            st.stop()

    # Clear typing indicator
    typing_placeholder.empty()
    
    # 5. Update UI History & Render Response Directly
    bot_time = datetime.now().strftime("%I:%M %p")
    st.session_state.messages.append({
        "role": "assistant", 
        "content": bot_response,
        "time": bot_time
    })
    
    with chat_container:
        st.markdown(f"""
            <div class="chat-row">
                <div class="bubble agent-bubble">
                    <p>{bot_response}</p>
                    <span class="timestamp">{bot_time}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# AUTO-SCROLL JS ENFORCEMENT
# ---------------------------------------------------------
st.components.v1.html("""
    <script>
        // Smoothly scrolls the window to the bottom to track new messages
        window.parent.document.getElementById('chat-end').scrollIntoView({behavior: 'smooth'});
    </script>
""", height=0, width=0)