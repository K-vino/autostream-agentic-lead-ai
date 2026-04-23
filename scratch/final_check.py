import sys
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.graph.builder import create_graph
from langchain_core.messages import AIMessage, HumanMessage

def run_validation():
    print("\n" + "="*60)
    print("   AutoStream FINAL Project Validation   ")
    print("="*60)

    # 1. Initialize graph
    try:
        app = create_graph()
        print("[PASS] 1. Code Structure & Initialization")
    except Exception as e:
        print(f"[FAIL] 1. Initialization failed: {e}")
        return

    # Initial state
    state = {
        "input": "",
        "intent": None,
        "name": None,
        "email": None,
        "platform": None,
        "response": None,
        "history": [],
        "lead_complete": False
    }

    print("\n[TESTING] 2. End-to-End Conversation Flow")
    
    test_steps = [
        {
            "user": "Hi, tell me about your pricing",
            "expect_node": "rag",
            "check": lambda s: "$29" in s["response"] and "$79" in s["response"],
            "desc": "RAG Accuracy (Pricing)"
        },
        {
            "user": "Does Pro plan include support?",
            "expect_node": "rag",
            "check": lambda s: "24/7" in s["response"] and "Pro" in s["response"],
            "desc": "RAG Accuracy (Policies)"
        },
        {
            "user": "I want to try the Pro plan for my YouTube channel",
            "expect_node": "lead",
            "check": lambda s: s["intent"] == "high_intent" and s["platform"] == "YouTube",
            "desc": "Intent Detection & Info Extraction"
        },
        {
            "user": "My name is John Doe",
            "expect_node": "lead",
            "check": lambda s: s["name"] == "John Doe",
            "desc": "State Persistence (Name)"
        },
        {
            "user": "john@example.com",
            "expect_node": "tool",
            "check": lambda s: s["lead_complete"] is True and "successfully captured" in s["response"],
            "desc": "Tool Triggering & Output"
        }
    ]

    for i, step in enumerate(test_steps):
        print(f"  - Step {i+1} ({step['desc']}): {step['user']}")
        state["input"] = step["user"]
        
        try:
            state = app.invoke(state)
            if step["check"](state):
                print(f"    [PASS]")
            else:
                print(f"    [FAIL] Validation logic failed for: {step['desc']}")
                print(f"    DEBUG Response: {state.get('response')[:100]}...")
        except Exception as e:
            print(f"    [FAIL] Error: {e}")

    # 3. Verify Error Handling (Manual Check)
    print("\n[CHECK] 3. Error Handling (Static Analysis)")
    from app.agents.intent_agent import IntentAgent
    from app.agents.rag_agent import RAGAgent
    
    intent_code = open("app/agents/intent_agent.py").read()
    rag_code = open("app/agents/rag_agent.py").read()
    
    if "try:" in intent_code and "except Exception" in intent_code:
        print("  - IntentAgent Error Handling: [PASS]")
    else:
        print("  - IntentAgent Error Handling: [FAIL]")
        
    if "try:" in rag_code and "except Exception" in rag_code:
        print("  - RAGAgent Error Handling: [PASS]")
    else:
        print("  - RAGAgent Error Handling: [FAIL]")

    print("\n" + "="*60)
    print("   Final Validation Complete   ")
    print("="*60)

if __name__ == "__main__":
    run_validation()
