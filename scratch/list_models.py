import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print("Listing available models:")
try:
    found = False
    for m in genai.list_models():
        if "gemini-1.5-flash" in m.name:
            print(f"- {m.name} (supports: {m.supported_generation_methods})")
            found = True
    if not found:
        print("gemini-1.5-flash NOT found. Listing all available gemini models:")
        for m in genai.list_models():
            if "gemini" in m.name:
                print(f"- {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")

