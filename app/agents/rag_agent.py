import json
from langchain_openai import ChatOpenAI
from app.config import LLM_MODEL, TEMPERATURE, OPENAI_API_KEY, RAG_PROMPT_PATH, KNOWLEDGE_BASE_PATH

class RAGAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=LLM_MODEL,
            temperature=TEMPERATURE,
            openai_api_key=OPENAI_API_KEY
        )
        with open(RAG_PROMPT_PATH, "r") as f:
            self.prompt_template = f.read()
        
        with open(KNOWLEDGE_BASE_PATH, "r") as f:
            self.knowledge = json.load(f)

    def answer(self, user_input: str) -> str:
        # Convert knowledge dict to a readable string for the prompt
        knowledge_str = json.dumps(self.knowledge, indent=2)
        prompt = self.prompt_template.format(knowledge=knowledge_str, input=user_input)
        response = self.llm.invoke(prompt)
        return response.content.strip()
