@echo off
REM AI Todo App - Windows Startup Script
REM This script starts both backend and frontend servers

echo ========================================
echo AI Todo App - Starting Services
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo [OK] Prerequisites check passed
echo.

REM Navigate to backend directory
cd /d "%~dp0phase-2-web\backend"

REM Check if .env file exists
if not exist ".env" (
    echo [WARNING] .env file not found in backend directory
    echo Creating .env from .env.example...
    if exist ".env.example" (
        copy ".env.example" ".env"
        echo [INFO] Please edit backend\.env and add your API keys
        echo Press any key to open .env file...
        pause >nul
        notepad ".env"
    ) else (
        echo [ERROR] .env.example not found
        pause
        exit /b 1
    )
)

REM Check if virtual environment exists
if not exist ".venv" (
    echo [INFO] Creating Python virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install/update dependencies
echo [INFO] Installing backend dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

REM Run database migrations
echo [INFO] Running database migrations...
alembic upgrade head
if errorlevel 1 (
    echo [ERROR] Database migration failed
    echo Please check your DATABASE_URL in .env file
    pause
    exit /b 1
)

echo [OK] Backend setup complete
echo.

REM Start backend server in new window
echo [INFO] Starting backend server on http://localhost:8000...
start "AI Todo Backend" cmd /k "cd /d %~dp0phase-2-web\backend && .venv\Scripts\activate.bat && uvicorn app.main:app --reload --port 8000"

REM Wait for backend to start
timeout /t 5 /nobreak >nul

REM Navigate to frontend directory
cd /d "%~dp0phase-2-web\frontend"

REM Check if node_modules exists
if not exist "node_modules" (
    echo [INFO] Installing frontend dependencies...
    call npm install
    if errorlevel 1 (
        echo [ERROR] Failed to install frontend dependencies
        pause
        exit /b 1
    )
)

REM Check if .env.local exists
if not exist ".env.local" (
    echo [INFO] Creating .env.local for frontend...
    echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local
)

echo [OK] Frontend setup complete
echo.

REM Start frontend server in new window
echo [INFO] Starting frontend server on http://localhost:3000...
start "AI Todo Frontend" cmd /k "cd /d %~dp0phase-2-web\frontend && npm run dev"

echo.
echo ========================================
echo Services Started Successfully!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to open the application in your browser...
pause >nul

REM Open browser
start http://localhost:3000

echo.
echo To stop the servers, close the terminal windows.
echo.
pause
