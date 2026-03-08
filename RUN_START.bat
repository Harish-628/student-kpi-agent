@echo off
REM ============================================================
REM  NeuralKPI — One-Click Start Script
REM  Double-click this file to start everything
REM ============================================================

setlocal enabledelayedexpansion

REM Store project root immediately before anything changes it
set ROOT=%~dp0
if "%ROOT:~-1%"=="\" set ROOT=%ROOT:~0,-1%

cd /d "%ROOT%"

echo.
echo ========================================
echo   NeuralKPI — Starting All Servers
echo ========================================
echo.

REM 1. Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python from https://www.python.org
    pause
    exit /b 1
)
echo [OK] Python found.

REM 2. Check and Activate Virtual Environment
if exist "%ROOT%\venv\Scripts\activate.bat" (
    echo [OK] Found virtual environment. Activating...
    call "%ROOT%\venv\Scripts\activate.bat"
) else (
    echo [!] Virtual environment (venv) not found. Using system Python...
)

REM 3. Install/Check Dependencies
echo Checking dependencies...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo [!] Dependencies missing. Installing...
    pip install -r requirements.txt
)
echo [OK] Dependencies ready.

REM 4. Database Migration (Conditional)
echo.
if exist "migrate_od.py" (
    echo [OK] Running OD database migration...
    python migrate_od.py
) else (
    echo [i] Skipping OD migration (migrate_od.py not found).
)
echo.

REM 5. Cleanup existing processes on ports 8000 and 8080
echo Cleaning up existing processes...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000 "') do (
    taskkill /F /PID %%a >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8080 "') do (
    taskkill /F /PID %%a >nul 2>&1
)

REM 6. Start Servers
echo Starting Backend API (port 8000)...
set PYTHONPATH=%ROOT%
start "NeuralKPI - Backend" cmd /k "cd /d %ROOT% && set PYTHONPATH=%ROOT% && venv\Scripts\python.exe -m uvicorn backend.main:app --reload --port 8000"

echo Waiting for backend...
timeout /t 3 /nobreak >nul

echo Starting Frontend Server (port 8080)...
start "NeuralKPI - Frontend" cmd /k "cd /d %ROOT%\frontend && ..\venv\Scripts\python.exe -m http.server 8080"

timeout /t 2 /nobreak >nul

REM 7. Launch Dashboard
echo Opening browser...
start http://localhost:8080/dashboard.html

echo.
echo ========================================
echo   STATUS: ALL SYSTEMS GO
echo ========================================
echo.
echo   Dashboard:   http://localhost:8080/dashboard.html
echo   API Docs:    http://localhost:8000/docs
echo.
echo   NOTE: Please keep the Backend and Frontend 
echo   command windows open while using the app.
echo.
pause
