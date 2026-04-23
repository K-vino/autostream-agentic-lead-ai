import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from app.config import LLM_MODEL, TEMPERATURE, OPENAI_API_KEY, LEAD_PROMPT_PATH

class LeadAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=LLM_MODEL,
            temperature=TEMPERATURE,
            openai_api_key=OPENAI_API_KEY
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
        
        response = self.llm.invoke(extraction_prompt)
        try:
            # Handle potential markdown formatting in LLM response
            content = response.content.strip()
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
        response = self.llm.invoke(prompt)
        return response.content.strip()
