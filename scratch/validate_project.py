import sys
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.graph.builder import create_graph
from langchain_core.messages import AIMessage, HumanMessage

def run_test():
    print("\n" + "="*50)
    print("   AutoStream Project Validation Script   ")
    print("="*50)

    # Initialize graph
    try:
        app = create_graph()
        print("[PASS] Graph Initialization")
    except Exception as e:
        print(f"[FAIL] Graph Initialization: {e}")
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

    test_steps = [
        {
            "user": "Hi, tell me about your pricing",
            "expect_node": "rag",
            "check": lambda s: "$29" in s["response"] and "$79" in s["response"]
        },
        {
            "user": "Does Pro plan include support?",
            "expect_node": "rag",
            "check": lambda s: "24/7" in s["response"] or "exclusive" in s["response"].lower()
        },
        {
            "user": "I want to try the Pro plan for my YouTube channel",
            "expect_node": "lead",
            "check": lambda s: s["intent"] == "high_intent" and s["platform"] == "YouTube"
        },
        {
            "user": "My name is John Doe",
            "expect_node": "lead",
            "check": lambda s: s["name"] == "John Doe"
        },
        {
            "user": "john@example.com",
            "expect_node": "tool",
            "check": lambda s: s["lead_complete"] is True and "Lead captured" in s["response"]
        }
    ]

    for i, step in enumerate(test_steps):
        print(f"\nStep {i+1}: User: {step['user']}")
        state["input"] = step["user"]
        
        try:
            state = app.invoke(state)
            print(f"  - Intent: {state.get('intent')}")
            print(f"  - Response: {state.get('response')[:100]}...")
            
            if step["check"](state):
                print(f"  [PASS] Step {i+1}")
            else:
                print(f"  [FAIL] Step {i+1} (Validation logic failed)")
                print(f"  DEBUG STATE: {state}")
        except Exception as e:
            print(f"  [FAIL] Step {i+1} Error: {e}")

    print("\n" + "="*50)
    print("   Validation Complete   ")
    print("="*50)

if __name__ == "__main__":
    run_test()
