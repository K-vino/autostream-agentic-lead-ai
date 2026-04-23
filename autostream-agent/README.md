# AutoStream Social-to-Lead Agentic Workflow
*Submission for ServiceHive - Inflx ML Intern Assignment*

## 🚀 Overview
This project implements a stateful conversational AI agent for **AutoStream**, a fictional SaaS platform for automated video editing. The system simulates a real-world “social-to-lead” workflow, converting social media inquiries into qualified business leads.

Built with **LangChain** and **LangGraph**, the agent handles:
1. **Intent Detection**: Classifying user input (Greeting, Inquiry, High Intent).
2. **RAG-based Retrieval**: Answering product/pricing questions using a local JSON knowledge base.
3. **Stateful Lead Capture**: Collecting user details (Name, Email, Platform) before triggering a mock tool.

---

## 🛠️ How to Run Locally

### 1. Prerequisites
- Python 3.9+
- OpenAI API Key

### 2. Setup
Clone the repository and navigate to the project folder:
```bash
cd autostream-agent
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file:
```bash
cp .env.example .env
```
Add your `OPENAI_API_KEY` to the `.env` file.

### 4. Run the Agent
```bash
python main.py
```

---

## 🏗️ Architecture Explanation

### Why LangGraph?
LangGraph was selected because it provides fine-grained control over the **agentic loop**. Unlike standard linear chains, LangGraph allows for:
- **Cyclic Logic**: Essential for multi-turn lead collection where the agent must repeatedly check for missing information and loop back until the "goal" (full lead capture) is met.
- **State Management**: It maintains a robust `AgentState` object that persists across turns, ensuring that the agent "remembers" the user's name and email even if they ask a pricing question in the middle of the flow.
- **Clean Routing**: Separates the "thinking" (Intent Detection) from the "acting" (RAG or Tool Execution) using conditional edges.

### How State is Handled
The state is managed using a `TypedDict` that tracks:
- `history`: Full conversation history for context.
- `intent`: The current user goal.
- `name`, `email`, `platform`: Specific lead data collected over time.
- `lead_complete`: A boolean flag that triggers the `tool_node` once all data is present.

Each node in the graph processes the state and returns only the fields that have changed, ensuring a clean and traceable state transition.

---

## 📲 WhatsApp Deployment (Webhooks)

To integrate this agent with WhatsApp using Webhooks:

1. **Host the Agent**: Deploy the agent code as a REST API using FastAPI.
2. **Set up a Webhook**: Configure a Meta for Developers account (WhatsApp Business API) or Twilio. Set your API's `/webhook` endpoint as the callback URL.
3. **Handle Incoming Messages**:
   - When a user sends a message, WhatsApp sends a POST request to your webhook.
   - Your API identifies the user by their phone number (`sender_id`).
4. **State Persistence**: 
   - Instead of in-memory storage, use a database (Redis/MongoDB) to store the `AgentState` keyed by the phone number.
   - Load the state, call `graph.invoke()`, and update the database with the new state.
5. **Send Response**: Use the WhatsApp API (e.g., `/messages` endpoint) to send the agent's response back to the user.

---

## 📂 Project Structure
- `app/agents/`: Core logic for Intent, RAG, and Lead extraction.
- `app/graph/`: LangGraph orchestration (nodes and edges).
- `app/memory/`: State schema definition.
- `app/tools/`: The `mock_lead_capture` implementation.
- `app/data/`: `knowledge.json` containing pricing and policies.
- `main.py`: Interactive CLI for the assignment demo.
