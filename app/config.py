import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model Settings
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
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
