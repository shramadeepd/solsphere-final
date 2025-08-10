Write-Host "Starting SolSphere Application..." -ForegroundColor Green
Write-Host ""

# Start FastAPI Backend Server
Write-Host "Starting FastAPI Backend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\server'; .venv\Scripts\Activate.ps1; python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload" -WindowStyle Normal

# Wait for backend to start
Write-Host "Waiting 3 seconds for backend to start..." -ForegroundColor Cyan
Start-Sleep -Seconds 3

# Start React Frontend
Write-Host "Starting React Frontend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\dashboard'; npm start" -WindowStyle Normal

Write-Host ""
Write-Host "Both services are starting..." -ForegroundColor Green
Write-Host "Backend: http://localhost:8001" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to close this window..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 