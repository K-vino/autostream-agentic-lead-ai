import sys
from app.graph.builder import create_graph

def main():
    print("===============================================")
    print("   AutoStream Social-to-Lead Agentic Bot      ")
    print("===============================================")
    print("Type 'exit', 'quit', or 'bye' to end the session.")
    print("-----------------------------------------------")

    # Initialize graph
    app = create_graph()
    
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

    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Agent: Goodbye! Have a great day!")
                break
            
            if not user_input:
                continue

            # Update input in state
            state["input"] = user_input
            
            # Run the graph
            # Note: We pass the entire state dict and get the updated one back
            output = app.invoke(state)
            
            # Update state with output
            state = output
            
            # Print agent response
            print(f"Agent: {state['response']}")

        except KeyboardInterrupt:
            print("\nAgent: Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            break

if __name__ == "__main__":
    main()
