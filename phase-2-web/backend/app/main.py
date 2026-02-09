# phase-2-web\backend\app\main.py
from fastapi import FastAPI, Request
from app.api.api_v1.api import api_router
from app.core.config import settings
from contextlib import asynccontextmanager
from app.db.session import engine
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database on startup
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    yield
    # Shutdown logic can go here if needed


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware with explicit configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3002",
        "http://localhost:8000",  # For direct API testing
        "http://127.0.0.1:8000", # For direct API testing
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Explicitly allow all methods
    allow_headers=["*"],  # Explicitly allow all headers
    # Additional CORS settings for debugging
    # expose_headers=["Access-Control-Allow-Origin"]
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"message": "FastAPI server for Todo App is running!"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "api_version": settings.VERSION}