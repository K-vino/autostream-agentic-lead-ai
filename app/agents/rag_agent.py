import json
import google.generativeai as genai
from app.config import LLM_MODEL, TEMPERATURE, RAG_PROMPT_PATH, KNOWLEDGE_BASE_PATH

class RAGAgent:
    def __init__(self):
        self.model = genai.GenerativeModel(
            model_name=LLM_MODEL,
            generation_config={"temperature": TEMPERATURE}
        )
        with open(RAG_PROMPT_PATH, "r") as f:
            self.prompt_template = f.read()
        
        with open(KNOWLEDGE_BASE_PATH, "r") as f:
            self.knowledge = json.load(f)

    def answer(self, user_input: str) -> str:
        try:
            # Convert knowledge dict to a readable string for the prompt
            knowledge_str = json.dumps(self.knowledge, indent=2)
            prompt = self.prompt_template.format(knowledge=knowledge_str, input=user_input)
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception:
            return "I'm having trouble accessing my knowledge base right now. Please try again in a moment!"


