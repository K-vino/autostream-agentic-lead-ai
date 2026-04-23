from langchain_openai import ChatOpenAI
from app.config import LLM_MODEL, TEMPERATURE, OPENAI_API_KEY, INTENT_PROMPT_PATH

class IntentAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=LLM_MODEL,
            temperature=TEMPERATURE,
            openai_api_key=OPENAI_API_KEY
        )
        with open(INTENT_PROMPT_PATH, "r") as f:
            self.prompt_template = f.read()

    def classify(self, user_input: str) -> str:
        prompt = self.prompt_template.format(input=user_input)
        response = self.llm.invoke(prompt)
        intent = response.content.strip().lower()
        
        # Validation to ensure we only get valid intents
        valid_intents = ["greeting", "inquiry", "high_intent"]
        if intent not in valid_intents:
            # Fallback
            return "inquiry"
        
        return intent
