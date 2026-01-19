import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
print(f"Checking models for API key: {api_key[:5]}...")

if not api_key:
    print("API Key not found in .env")
    exit(1)

genai.configure(api_key=api_key)
try:
    with open("models_clean.txt", "w", encoding="utf-8") as f:
        f.write("Available GenerateContent models:\n")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                f.write(f" - {m.name}\n")
    print("Models written to models_clean.txt")
except Exception as e:
    print(f"Error listing models: {e}")
