import httpx
import base64
import os
from app.config import settings

class LocalImageGenerator:
    def __init__(self):
        self.base_url = settings.SD_WEBUI_URL

    async def generate_image(self, prompt: str, output_path: str) -> str | None:
        payload = {
            "prompt": prompt,
            "negative_prompt": "blurry, low quality, distorted, ugly",
            "steps": 20,
            "width": 1024,
            "height": 1792,  # 9:16 aspect ratio for Shorts
            "cfg_scale": 7
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(f"{self.base_url}/sdapi/v1/txt2img", json=payload, timeout=120.0)
                
                if response.status_code == 200:
                    r = response.json()
                    image_base64 = r['images'][0]
                    
                    # Save image
                    with open(output_path, "wb") as f:
                        f.write(base64.b64decode(image_base64))
                    return output_path
                else:
                    print(f"Local SD Error: {response.status_code}")
                    return None
            except Exception as e:
                print(f"Exception during local image generation: {e}")
                return None

local_image_generator = LocalImageGenerator()
