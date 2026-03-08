@echo off
set ROOT=%~dp0
if "%ROOT:~-1%"=="\" set ROOT=%ROOT:~0,-1%
cd /d "%ROOT%"

echo.
echo ========================================
echo   NeuralKPI - Starting All Servers
echo ========================================
echo.

REM 1. Cleanup existing processes
echo [1/4] Cleaning up existing processes...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000 "') do taskkill /F /PID %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8080 "') do taskkill /F /PID %%a >nul 2>&1

REM 2. Start Backend API
echo [2/4] Starting Backend API (port 8000)...
set PYTHONPATH=%ROOT%
start "NeuralKPI-Backend" cmd /k "set PYTHONPATH=%ROOT% && venv\Scripts\python.exe -m uvicorn backend.main:app --reload --port 8000"

REM 3. Start Frontend 
echo [3/4] Starting Frontend Server (port 8080)...
ping 127.0.0.1 -n 3 >nul
start "NeuralKPI-Frontend" cmd /k "cd /d frontend && ..\venv\Scripts\python.exe -m http.server 8080"

REM 4. Open Dashboard
echo [4/4] Opening browser...
ping 127.0.0.1 -n 2 >nul
start http://localhost:8080/dashboard.html

echo.
echo ========================================
echo   STATUS: ALL SYSTEMS GO
echo ========================================
echo.
echo   Keep the Backend and Frontend 
echo   command windows open to use the app.
echo.
pause
