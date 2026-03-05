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
REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Install from https://www.python.org
    pause
    exit /b 1
)
echo [OK] Python found

REM Install dependencies if fastapi is missing
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies ^(first run only^)...
    pip install -r requirements.txt
)
echo [OK] Dependencies ready

echo.
echo Running OD database migration...
python migrate_od.py
echo.

REM Kill anything on port 8000 or 8080
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000 "') do (
    taskkill /F /PID %%a >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8080 "') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo Starting Backend API  ^(port 8000^)...
start "NeuralKPI - Backend" cmd /k "cd /d %ROOT% && python -m uvicorn backend.main:app --reload --port 8000"

echo Waiting for backend to start...
timeout /t 4 /nobreak >nul

echo Starting Frontend Server ^(port 8080^)...
start "NeuralKPI - Frontend" cmd /k "cd /d %ROOT%\frontend && python -m http.server 8080"

timeout /t 2 /nobreak >nul

echo Opening browser...
start http://localhost:8080/dashboard.html

echo.
echo ========================================
echo   All servers started!
echo ========================================
echo.
echo   Dashboard:   http://localhost:8080/dashboard.html
echo   API Docs:    http://localhost:8000/docs
echo   API Health:  http://localhost:8000/
echo.
echo   Close the "Backend" and "Frontend" windows to stop servers.
echo.
pause
