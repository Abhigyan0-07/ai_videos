from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from app.routers import generate
from app.config import settings

load_dotenv()

# Ensure output directory exists
os.makedirs(settings.OUTPUT_DIR, exist_ok=True)

app = FastAPI(title="AI Video Generator API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directory to serve generated videos
app.mount("/static", StaticFiles(directory=settings.OUTPUT_DIR), name="static")

app.include_router(generate.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "AI Video Generator API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
