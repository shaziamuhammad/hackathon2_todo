#!/bin/bash
# AI Todo App - Stop Script
# This script stops both backend and frontend servers

echo "Stopping AI Todo App services..."

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$SCRIPT_DIR/phase-2-web/backend"
FRONTEND_DIR="$SCRIPT_DIR/phase-2-web/frontend"

# Stop backend
if [ -f "$BACKEND_DIR/backend.pid" ]; then
    BACKEND_PID=$(cat "$BACKEND_DIR/backend.pid")
    if kill -0 $BACKEND_PID 2>/dev/null; then
        echo "Stopping backend server (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
        rm "$BACKEND_DIR/backend.pid"
    else
        echo "Backend server is not running"
        rm "$BACKEND_DIR/backend.pid"
    fi
else
    echo "Backend PID file not found"
fi

# Stop frontend
if [ -f "$FRONTEND_DIR/frontend.pid" ]; then
    FRONTEND_PID=$(cat "$FRONTEND_DIR/frontend.pid")
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        echo "Stopping frontend server (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
        rm "$FRONTEND_DIR/frontend.pid"
    else
        echo "Frontend server is not running"
        rm "$FRONTEND_DIR/frontend.pid"
    fi
else
    echo "Frontend PID file not found"
fi

echo "All services stopped"
