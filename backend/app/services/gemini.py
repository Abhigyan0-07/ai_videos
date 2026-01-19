import google.generativeai as genai
import json
from app.schemas import VideoScript
from app.config import settings

class GeminiService:
    def __init__(self):
        if not settings.GEMINI_API_KEY:
            print("Warning: GEMINI_API_KEY is not set.")
        else:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.0-flash-lite')

    async def generate_script(self, topic: str, style: str, duration: int) -> VideoScript:
        # Estimate scene count: approx 5 seconds per scene
        num_scenes = max(3, duration // 5)
        
        prompt = f"""
        You are a professional video content creator for YouTube Shorts and Instagram Reels.
        Create a compelling video script about: "{topic}"
        Style: {style}
        Target Total Duration: {duration} seconds.
        
        Break this down into exactly {num_scenes} scenes.
        
        For each scene provide:
        1. Narration: The exact spoken words (keep it punchy and engaging).
        2. Visual Description: A detailed prompt for an image generator (Stable Diffusion). Include keywords like 'cinematic', '4k', 'detailed'.
        3. Duration: Estimated seconds for this scene.
        
        Output stricly in valid JSON format matching this structure:
        {{
          "title": "Video Title",
          "scenes": [
            {{
              "id": 1,
              "narration": "Script text here...",
              "visual_description": "Detailed image prompt...",
              "duration": 5.0
            }}
          ]
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Cleanup JSON if needed (sometimes LLMs add markdown code blocks)
            text_response = response.text.replace("```json", "").replace("```", "").strip()
            data = json.loads(text_response)
            return VideoScript(**data)
        except Exception as e:
            print(f"Error generating script: {e}")
            raise e

gemini_service = GeminiService()
