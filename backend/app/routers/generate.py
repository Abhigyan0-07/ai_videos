from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
import uuid
import os
import asyncio
import logging

from ..schemas import GenerateRequest, VideoScript
from ..services.gemini import gemini_service
from ..services.image import image_generator
from ..services.tts import voice_generator
from ..services.video import video_composer
from ..config import settings

router = APIRouter()

# Simple in-memory job store for demo purposes (use DB for production)
jobs = {}

class JobStatus(BaseModel):
    id: str
    status: str # pending, processing, completed, failed
    progress: int = 0
    video_url: Optional[str] = None
    error: Optional[str] = None

async def process_video_generation(job_id: str, request: GenerateRequest):
    try:
        jobs[job_id]["status"] = "processing"
        jobs[job_id]["progress"] = 5
        
        # 1. Generate Script
        print(f"[{job_id}] Generating script...")
        script = await gemini_service.generate_script(request.topic, request.video_style, request.duration)
        jobs[job_id]["progress"] = 15
        
        # Working directory for this job
        job_dir = os.path.join(settings.OUTPUT_DIR, job_id)
        os.makedirs(job_dir, exist_ok=True)
        
        # 2. Process Scenes (Parallel Image & Audio)
        print(f"[{job_id}] Processing {len(script.scenes)} scenes...")
        
        scene_clips = []
        
        # Semaphore to limit concurrency if needed (free tier safety)
        sem = asyncio.Semaphore(3) 

        async def process_scene(scene):
            async with sem:
                scene_idx = scene.id
                print(f"[{job_id}] Processing scene {scene_idx}...")
                
                # Paths
                audio_path = os.path.join(job_dir, f"audio_{scene_idx}.mp3")
                image_path = os.path.join(job_dir, f"image_{scene_idx}.png")
                clip_path = os.path.join(job_dir, f"clip_{scene_idx}.mp4")
                
                # Generate Assets
                # Run Image and Audio in parallel
                results = await asyncio.gather(
                    voice_generator.generate_audio(scene.narration, audio_path),
                    image_generator.generate_image(scene.visual_description, image_path),
                    return_exceptions=True
                )
                
                audio_res, image_res = results
                
                if isinstance(audio_res, Exception) or isinstance(image_res, Exception):
                    raise Exception(f"Failed to generate assets for scene {scene_idx}")
                
                if not image_res:
                     raise Exception(f"Failed to generate image for scene {scene_idx}")

                # Create Video Clip
                print(f"[{job_id}] Creating clip for scene {scene_idx}...")
                await video_composer.create_clip(image_path, audio_path, clip_path, scene.duration)
                return clip_path

        # Run all scenes
        clip_paths = []
        # We want to maintain order, so we await gather
        tasks = [process_scene(scene) for scene in script.scenes]
        clip_paths = await asyncio.gather(*tasks)
        
        jobs[job_id]["progress"] = 80
        
        # 3. Stitch Video
        print(f"[{job_id}] Stitching video...")
        final_filename = f"{job_id}.mp4"
        final_path = os.path.join(settings.OUTPUT_DIR, final_filename)
        await video_composer.stitch_videos(list(clip_paths), final_path)
        
        jobs[job_id]["progress"] = 100
        jobs[job_id]["status"] = "completed"
        # In a real app, upload to S3 or serve static file
        jobs[job_id]["video_url"] = f"/static/{final_filename}"
        print(f"[{job_id}] Video completed: {final_path}")

    except Exception as e:
        print(f"[{job_id}] Job failed: {e}")
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)

@router.post("/generate", response_model=JobStatus)
async def generate_video(request: GenerateRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "id": job_id,
        "status": "pending",
        "progress": 0,
        "video_url": None,
        "error": None
    }
    
    background_tasks.add_task(process_video_generation, job_id, request)
    return JobStatus(**jobs[job_id])

@router.get("/status/{job_id}", response_model=JobStatus)
async def get_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobStatus(**jobs[job_id])

@router.get("/videos", response_model=List[JobStatus])
async def list_videos():
    # Return completed videos
    return [JobStatus(**job) for job in jobs.values() if job["status"] == "completed"]
