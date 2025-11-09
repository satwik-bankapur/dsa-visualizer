@echo off
echo Starting DSA Visualizer - All Services
echo =====================================

echo.
echo 1. Starting ML Services (Port 8001)...
start "ML Services" cmd /k "cd ml_services && python main.py"

timeout /t 3 /nobreak >nul

echo.
echo 2. Starting Backend (Port 5000)...
start "Backend" cmd /k "cd backend && node server_simple.js"

timeout /t 3 /nobreak >nul

echo.
echo 3. Starting Frontend (Port 3000)...
start "Frontend" cmd /k "cd frontend && npm start"

echo.
echo All services are starting...
echo.
echo Services:
echo - ML Services: http://localhost:8001
echo - Backend: http://localhost:5000  
echo - Frontend: http://localhost:3000
echo.
echo Press any key to exit...
pause >nul