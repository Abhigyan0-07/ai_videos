import httpx
import json
from app.schemas import VideoScript
from app.config import settings

class OllamaService:
    def __init__(self):
        self.base_url = settings.OLLAMA_URL
        self.model = "llama3" # Ensure user has run 'ollama run llama3'

    async def generate_script(self, topic: str, style: str, duration: int) -> VideoScript:
        num_scenes = max(3, duration // 5)
        
        prompt = f"""
        You are a professional video content creator for YouTube Shorts.
        Create a JSON video script about: "{topic}"
        Style: {style}
        Scenes: {num_scenes}
        
        Format strictly as JSON format with this structure:
        {{
          "title": "Video Title",
          "scenes": [
            {{
              "id": 1,
              "narration": "Spoken text...",
              "visual_description": "Image prompt...",
              "duration": 5.0
            }}
          ]
        }}
        """

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json" 
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(f"{self.base_url}/api/generate", json=payload, timeout=120.0)
                if response.status_code == 200:
                    data = response.json()
                    script_data = json.loads(data["response"])
                    return VideoScript(**script_data)
                else:
                    raise Exception(f"Ollama Error: {response.text}")
            except Exception as e:
                print(f"Error generating script with Ollama: {e}")
                raise e

ollama_service = OllamaService()
