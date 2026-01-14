import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    HF_TOKEN = os.getenv("HF_TOKEN")
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "generated_videos")

settings = Settings()
