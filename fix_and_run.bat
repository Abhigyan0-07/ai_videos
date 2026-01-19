@echo off
echo ===================================================
echo fixing and Starting AI Video Backend...
echo ===================================================

cd backend

:: Create venv if it doesn't exist (just in case)
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate venv
call venv\Scripts\activate

:: Install dependencies explicitly
echo Installing dependencies...
pip install fastapi uvicorn python-dotenv google-generativeai edge-tts ffmpeg-python requests aiofiles httpx

:: Start Server
echo Starting Server...
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
