# phase-2-web\backend\app\api\api_v1\api.py
from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, tasks
from app.api.v1.endpoints import chat, notifications, preferences, oauth, conversations, analytics


api_router = APIRouter()

# Include auth routes
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Include OAuth routes
api_router.include_router(oauth.router, tags=["auth"])

# Include tasks routes
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

# Include chat routes
api_router.include_router(chat.router, tags=["chat"])

# Include conversation routes
api_router.include_router(conversations.router, tags=["conversations"])

# Include analytics routes
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])

# Include notifications routes
api_router.include_router(notifications.router, tags=["notifications"])

# Include preferences routes
api_router.include_router(preferences.router, tags=["preferences"])