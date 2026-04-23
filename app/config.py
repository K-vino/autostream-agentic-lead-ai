import os
import google.generativeai as genai
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

# Model Settings
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-1.5-flash")
TEMPERATURE = float(os.getenv("TEMPERATURE", 0))


# File Paths
DATA_DIR = BASE_DIR / "app" / "data"
PROMPTS_DIR = BASE_DIR / "app" / "prompts"

KNOWLEDGE_BASE_PATH = DATA_DIR / "knowledge.json"

# Prompt Paths
INTENT_PROMPT_PATH = PROMPTS_DIR / "intent_prompt.txt"
RAG_PROMPT_PATH = PROMPTS_DIR / "rag_prompt.txt"
LEAD_PROMPT_PATH = PROMPTS_DIR / "lead_prompt.txt"

# State Settings
MAX_HISTORY = 6
