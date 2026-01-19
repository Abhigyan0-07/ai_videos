import edge_tts
import os
from app.config import settings

class VoiceGenerator:
    def __init__(self):
        # Good default voices: "en-US-ChristopherNeural", "en-US-AriaNeural", "en-US-GuyNeural"
        self.voice = "en-US-ChristopherNeural"
    
    async def generate_audio(self, text: str, output_path: str) -> str:
        """
        Generates TTS audio and saves to output_path.
        Returns the path.
        """
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(output_path)
        return output_path

voice_generator = VoiceGenerator()
