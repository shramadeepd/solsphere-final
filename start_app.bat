@echo off
echo Starting SolSphere Application...
echo.

echo Starting FastAPI Backend Server...
start "Backend Server" cmd /k "cd server && .venv\Scripts\activate && python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload"

echo Waiting 3 seconds for backend to start...
timeout /t 3 /nobreak > nul

echo Starting React Frontend...
start "Frontend" cmd /k "cd dashboard && npm start"

echo.
echo Both services are starting...
echo Backend: http://localhost:8001
echo Frontend: http://localhost:3000
echo.
echo Press any key to close this window...
pause > nul 