# PowerShell script to start all services
Write-Host "Starting DSA Visualizer - All Services" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

Write-Host "`n1. Starting ML Services (Port 8001)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd ml_services; python main_simple.py"

Start-Sleep -Seconds 3

Write-Host "`n2. Starting Backend (Port 5000)..." -ForegroundColor Yellow  
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; node server_simple.js"

Start-Sleep -Seconds 3

Write-Host "`n3. Starting Frontend (Port 3000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm start"

Write-Host "`nAll services are starting..." -ForegroundColor Green
Write-Host "`nServices:" -ForegroundColor Cyan
Write-Host "- ML Services: http://localhost:8001" -ForegroundColor White
Write-Host "- Backend: http://localhost:5000" -ForegroundColor White  
Write-Host "- Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "`nPress any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")