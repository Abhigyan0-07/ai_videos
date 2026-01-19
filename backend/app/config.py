import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    HF_TOKEN = os.getenv("HF_TOKEN")
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "generated_videos")
    
    # Local AI Config
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
    SD_WEBUI_URL = os.getenv("SD_WEBUI_URL", "http://127.0.0.1:7860")

settings = Settings()
