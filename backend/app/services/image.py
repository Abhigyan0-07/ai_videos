import httpx
import os
import asyncio
from typing import Optional
from .config import settings

# Using SDXL Base 1.0 for better quality free inference
# Alternatively use "stabilityai/stable-diffusion-2-1" or "runwayml/stable-diffusion-v1-5"
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

class ImageGenerator:
    def __init__(self):
        self.headers = {"Authorization": f"Bearer {settings.HF_TOKEN}"}
        if not settings.HF_TOKEN:
             print("Warning: HF_TOKEN is not set. Image generation might fail or be rate-limited.")
    
    async def generate_image(self, prompt: str, output_path: str) -> Optional[str]:
        """
        Generates an image from prompt and saves it to output_path.
        Returns the path if successful, None otherwise.
        """
        payload = {
            "inputs": prompt,
            "parameters": {
                "negative_prompt": "blurry, low quality, distorted, ugly, bad anatomy",
                # SDXL specific parameters could go here if supported by the inference endpoint
            }
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(API_URL, headers=self.headers, json=payload, timeout=60.0)
                
                if response.status_code == 200:
                    with open(output_path, "wb") as f:
                        f.write(response.content)
                    return output_path
                else:
                    print(f"Error generating image: {response.status_code} - {response.text}")
                    # Fallback logic could be added here (e.g., try a different model)
                    return None
            except Exception as e:
                print(f"Exception during image generation: {e}")
                return None

image_generator = ImageGenerator()
