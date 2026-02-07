# phase-2-web\backend\app\main.py
from fastapi import FastAPI
from app.api.api_v1.api import api_router
from app.core.config import settings
from contextlib import asynccontextmanager
from app.db.session import engine
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Add CORS middleware with explicit configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
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