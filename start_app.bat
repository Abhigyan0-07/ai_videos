@echo off
echo Starting AI Video Generator...

:: Start Backend
start "AI Video Backend" cmd /k "cd backend && venv\Scripts\activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

:: Start Frontend
start "AI Video Frontend" cmd /k "cd frontend && npm run dev"

echo Services started! 
echo Frontend: http://localhost:5173
echo Backend: http://localhost:8000/docs
pause
