from pydantic import BaseModel
from typing import List

class Scene(BaseModel):
    id: int
    narration: str
    visual_description: str
    duration: float

class VideoScript(BaseModel):
    title: str
    scenes: List[Scene]

class GenerateRequest(BaseModel):
    topic: str
    video_style: str = "documentary" # emotional, dramatic, upbeat
    duration: int = 30
