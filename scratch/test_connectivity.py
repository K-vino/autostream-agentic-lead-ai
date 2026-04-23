import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"API Key present: {bool(api_key)}")

try:
    genai.configure(api_key=api_key)
    print("Configured genai")
    model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")
    print("Initialized model")
    response = model.generate_content("Hi")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
