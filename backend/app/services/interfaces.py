from typing import Protocol, List
from app.schemas import VideoScript

class ScriptGenerator(Protocol):
    async def generate_script(self, topic: str, style: str, duration: int) -> VideoScript:
        ...

class ImageGenerator(Protocol):
    async def generate_image(self, prompt: str, output_path: str) -> str | None:
        ...
