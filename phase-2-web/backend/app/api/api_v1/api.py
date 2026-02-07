# phase-2-web\backend\app\api\api_v1\api.py
from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, tasks


api_router = APIRouter()

# Include auth routes
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Include tasks routes
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])