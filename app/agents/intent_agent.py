import google.generativeai as genai
from app.config import LLM_MODEL, TEMPERATURE, INTENT_PROMPT_PATH

class IntentAgent:
    def __init__(self):
        self.model = genai.GenerativeModel(
            model_name=LLM_MODEL,
            generation_config={"temperature": TEMPERATURE}
        )
        with open(INTENT_PROMPT_PATH, "r") as f:
            self.prompt_template = f.read()

    def classify(self, user_input: str) -> str:
        prompt = self.prompt_template.format(input=user_input)
        response = self.model.generate_content(prompt)
        intent = response.text.strip().lower()

        
        # Validation to ensure we only get valid intents
        valid_intents = ["greeting", "inquiry", "high_intent"]
        if intent not in valid_intents:
            # Fallback
            return "inquiry"
        
        return intent
