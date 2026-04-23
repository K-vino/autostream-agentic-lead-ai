# Social-to-Lead Agentic Workflow: AutoStream
*Technical Submission for the ServiceHive - Inflx Machine Learning Intern Assignment*

## 📖 1. Project Background & Problem Statement
**ServiceHive** is developing **Inflx**, an AI-powered platform designed to convert social media conversations into qualified business leads. This project implements a core component of that vision: a high-reasoning conversational agent for **AutoStream**, a SaaS product providing automated video editing tools.

### The Challenge
The agent must go beyond simple chatbots by:
- **Understanding Intent**: Distinguishing between casual greetings, product inquiries, and high-purchase intent.
- **Strict Grounding (RAG)**: Answering questions using *only* a provided knowledge base to prevent hallucinations.
- **Stateful Lead Capture**: Conducting a multi-turn data collection process (Name, Email, Platform) without repetitive questioning.
- **Safe Tool Execution**: Triggering a lead capture function only when all required data is verified.

---

## 🏗️ 2. System Architecture & Core Logic

### Why LangGraph?
This project utilizes **LangGraph** (built on top of LangChain) to manage the agent's workflow. Unlike standard linear chains, LangGraph allows for:
- **Cyclic States**: The agent can loop through the lead collection node multiple times until all fields are filled.
- **Persistence**: The state is maintained across 5-6 conversation turns, allowing for "memory."
- **Conditional Routing**: Decisions (edges) are separated from processing (nodes), making the system robust and easy to debug.

### Workflow Logic
The agent follows a graph-based state machine:
1. **Intent Node**: Every input is analyzed by GPT-4o-mini to classify the intent.
2. **Conditional Edge**: Routes the user based on intent:
   - `greeting` → **Greeting Node** (Friendly small talk).
   - `inquiry` → **RAG Node** (Knowledge retrieval).
   - `high_intent` → **Lead Node** (Information collection).
3. **Lead Node Logic**:
   - The agent extracts potential info from the input.
   - It checks the `AgentState` for missing fields.
   - It asks for exactly **one** missing field at a time.
4. **Tool Node**: Once `name`, `email`, and `platform` are present, the graph routes to the Tool Node to execute `mock_lead_capture()`.

---

## 🛠️ 3. How to Run Locally

### Step 1: Clone and Navigate
```bash
cd autostream-agent
```

### Step 2: Install Dependencies
Ensure you have Python 3.9+ installed.
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment
Create a `.env` file from the example:
```bash
cp .env.example .env
```
Open `.env` and enter your `OPENAI_API_KEY`.

### Step 4: Start the Agent
```bash
python main.py
```

---

## 📂 4. Project Structure
```text
autostream-agent/
├── app/
│   ├── agents/          # Individual LLM logic (Intent, RAG, Lead)
│   ├── graph/           # LangGraph orchestration (Nodes, Edges, Builder)
│   ├── memory/          # TypedDict state schema
│   ├── tools/           # External actions (mock_lead_capture)
│   ├── data/            # Local knowledge base (knowledge.json)
│   ├── prompts/         # Cleanly separated prompt templates
│   └── config.py        # Centralized settings & file paths
├── main.py              # CLI Interactive Demo
├── requirements.txt     # Dependency list
└── README.md            # Project documentation
```

---

## 📑 5. Knowledge Base (RAG Data)
The agent answers strictly based on the following data:

| Plan | Price | Videos | Resolution | Support |
| :--- | :--- | :--- | :--- | :--- |
| **Basic** | $29/mo | 10/mo | 720p | Email |
| **Pro** | $79/mo | Unlimited | 4K | 24/7 |

**Policies**:
- **Refunds**: No refunds after 7 days.
- **Support**: 24/7 support is exclusive to Pro plan users.

---

## 📲 6. WhatsApp Deployment Strategy
To deploy this agent for WhatsApp using **Webhooks**:

1. **Infrastructure**:
   - Use **FastAPI** to host the agent as a REST API.
   - Use the **Meta for Developers** (WhatsApp Business API) or **Twilio** for messaging.
2. **Webhook Flow**:
   - User sends a message → WhatsApp sends a POST request to your `/webhook` endpoint.
   - Your API parses the `sender_id` (phone number).
3. **State Persistence**:
   - Instead of in-memory dictionaries, use **Redis** or **MongoDB** to store the `AgentState` keyed by the phone number.
   - Fetch state → `graph.invoke(input, state)` → Update state in DB.
4. **Response**:
   - Send the resulting `response` string back to the user via the WhatsApp API.

---

## 🎯 7. Evaluation Highlights
- **No Hallucination**: RAG prompt enforces strict grounding.
- **Intelligent Flow**: Lead capture recognizes if you provide information out of order.
- **Production Quality**: Modular code with clear separation of concerns, suitable for real-world scaling.
