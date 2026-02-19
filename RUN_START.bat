@echo off
REM ============================================================
REM Student KPI Management System - Quick Start Script
REM Windows Batch File for Easy Startup
REM ============================================================

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Student KPI Management System
echo Quick Start Script v1.0
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✓ Python detected
echo.

REM Check if in correct directory
if not exist "backend\main.py" (
    echo ERROR: This batch file must be run from the project root directory
    echo Current directory: %CD%
    echo Expected files not found
    pause
    exit /b 1
)

echo ✓ Project directory verified
echo.

REM Create venv if it doesn't exist
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

echo.

REM Activate venv
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo ✓ Virtual environment activated
echo.

REM Check if requirements are installed
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies (this may take a few minutes)...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo ✓ Dependencies installed
) else (
    echo ✓ Dependencies already installed
)

echo.
echo ========================================
echo Startup Complete!
echo ========================================
echo.
echo Opening servers in new windows...
echo.

REM Start Backend API Server
echo Starting Backend API Server (Port 8000)...
start cmd /k "cd /d %CD% && venv\Scripts\activate.bat && uvicorn backend.main:app --reload --port 8000"

REM Wait a moment for backend to start
timeout /t 2 /nobreak

REM Start Frontend Server
echo Starting Frontend Server (Port 8080)...
start cmd /k "cd /d %CD%\frontend && venv\Scripts\activate.bat && python -m http.server 8080"

echo.
echo ========================================
echo ✓ All Servers Started!
echo ========================================
echo.
echo Please close these windows when done:
echo   - Backend API window (Python/Uvicorn)
echo   - Frontend Server window (HTTP Server)
echo.
echo Access the application:
echo   Frontend:    http://localhost:8080
echo   API Docs:    http://localhost:8000/docs
echo   API Health:  http://localhost:8000/
echo.
echo Demo Credentials:
echo   Email:    student@example.com (or admin@example.com)
echo   Password: student123 (or admin123)
echo.
echo ========================================
echo.

pause
