import json
import google.generativeai as genai
from app.config import LLM_MODEL, TEMPERATURE, LEAD_PROMPT_PATH

class LeadAgent:
    def __init__(self):
        self.model = genai.GenerativeModel(
            model_name=LLM_MODEL,
            generation_config={"temperature": TEMPERATURE}
        )
        with open(LEAD_PROMPT_PATH, "r") as f:
            self.prompt_template = f.read()


    def extract_info(self, user_input: str, current_state: dict) -> dict:
        """
        Uses the LLM to extract lead info from user input.
        """
        extraction_prompt = f"""
        Extract the following fields from the user input if they are present:
        - name
        - email
        - platform

        Current State:
        {json.dumps(current_state, indent=2)}

        User Input: {user_input}

        Respond ONLY with a JSON object containing the fields. Use null for missing fields.
        """
        
        try:
            response = self.model.generate_content(extraction_prompt)
            # Handle potential markdown formatting in LLM response
            content = response.text.strip()
            if content.startswith("```json"):
                content = content[7:-3].strip()
            extracted = json.loads(content)
            return extracted
        except Exception:
            return {}

    def get_response(self, user_input: str, state: dict) -> str:
        """
        Formulates the next question or acknowledgment.
        """
        prompt = self.prompt_template.format(
            name=state.get("name") or "Missing",
            email=state.get("email") or "Missing",
            platform=state.get("platform") or "Missing",
            input=user_input
        )
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception:
            return "I'm having a bit of trouble collecting your details. Could you please re-state that?"
