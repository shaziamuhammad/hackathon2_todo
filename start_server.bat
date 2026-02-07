@echo off
echo Starting FastAPI Server with corrected CORS configuration...
cd /d "D:\hackathon2_todo\phase-2-web\backend"
echo Current directory: %cd%
echo.
echo Starting server on http://0.0.0.0:8000...
python -c "from app.main import app; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=8000, reload=False)"
pause