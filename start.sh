#!/bin/bash
# AI Todo App - Linux/Mac Startup Script
# This script starts both backend and frontend servers

set -e  # Exit on error

echo "========================================"
echo "AI Todo App - Starting Services"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Python 3 is not installed"
    echo "Please install Python 3.9+ from https://www.python.org/"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Node.js is not installed"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

echo -e "${GREEN}[OK]${NC} Prerequisites check passed"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$SCRIPT_DIR/phase-2-web/backend"
FRONTEND_DIR="$SCRIPT_DIR/phase-2-web/frontend"

# Navigate to backend directory
cd "$BACKEND_DIR"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}[WARNING]${NC} .env file not found in backend directory"
    if [ -f ".env.example" ]; then
        echo "Creating .env from .env.example..."
        cp ".env.example" ".env"
        echo -e "${YELLOW}[INFO]${NC} Please edit backend/.env and add your API keys"
        echo "Opening .env file..."
        ${EDITOR:-nano} ".env"
    else
        echo -e "${RED}[ERROR]${NC} .env.example not found"
        exit 1
    fi
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}[INFO]${NC} Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo -e "${YELLOW}[INFO]${NC} Activating virtual environment..."
source .venv/bin/activate

# Install/update dependencies
echo -e "${YELLOW}[INFO]${NC} Installing backend dependencies..."
pip install -r requirements.txt --quiet

# Run database migrations
echo -e "${YELLOW}[INFO]${NC} Running database migrations..."
alembic upgrade head || {
    echo -e "${RED}[ERROR]${NC} Database migration failed"
    echo "Please check your DATABASE_URL in .env file"
    exit 1
}

echo -e "${GREEN}[OK]${NC} Backend setup complete"
echo ""

# Start backend server in background
echo -e "${YELLOW}[INFO]${NC} Starting backend server on http://localhost:8000..."
uvicorn app.main:app --reload --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > backend.pid

# Wait for backend to start
sleep 5

# Check if backend is running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${RED}[ERROR]${NC} Backend failed to start. Check backend.log for details."
    exit 1
fi

# Navigate to frontend directory
cd "$FRONTEND_DIR"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}[INFO]${NC} Installing frontend dependencies..."
    npm install
fi

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo -e "${YELLOW}[INFO]${NC} Creating .env.local for frontend..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
fi

echo -e "${GREEN}[OK]${NC} Frontend setup complete"
echo ""

# Start frontend server in background
echo -e "${YELLOW}[INFO]${NC} Starting frontend server on http://localhost:3000..."
npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > frontend.pid

# Wait for frontend to start
sleep 5

# Check if frontend is running
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo -e "${RED}[ERROR]${NC} Frontend failed to start. Check frontend.log for details."
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo ""
echo "========================================"
echo "Services Started Successfully!"
echo "========================================"
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Logs:"
echo "  Backend:  $BACKEND_DIR/backend.log"
echo "  Frontend: $FRONTEND_DIR/frontend.log"
echo ""
echo "To stop the servers, run: ./stop.sh"
echo ""

# Open browser (works on most systems)
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:3000
elif command -v open &> /dev/null; then
    open http://localhost:3000
fi

# Keep script running and handle Ctrl+C
trap "echo ''; echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT TERM

echo "Press Ctrl+C to stop all servers"
wait
