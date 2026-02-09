# phase-2-web\backend\app\core\config.py
from pydantic_settings import BaseSettings
from typing import List, Optional
import os
import json
from pydantic import Field


class Settings(BaseSettings):
    PROJECT_NAME: str = "Todo API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # From .env file
    APP_NAME: str = "Secure Todo API"
    API_VERSION: str = "v1"

    # Database
    DATABASE_URL: str

    # JWT
    BETTER_AUTH_SECRET: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Phase 3: AI Services (at least one required)
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    OPENROUTER_API_KEY: Optional[str] = None

    # Phase 3: MCP Server
    MCP_SERVER_URL: str = "http://localhost:8001"

    # Phase 3: OAuth Providers (optional)
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    FACEBOOK_CLIENT_ID: Optional[str] = None
    FACEBOOK_CLIENT_SECRET: Optional[str] = None

    # CORS Origins - support both ALLOWED_ORIGINS and CORS_ORIGINS
    ALLOWED_ORIGINS: Optional[str] = None
    CORS_ORIGINS: Optional[str] = None

    # CORS - This will be processed from ALLOWED_ORIGINS or CORS_ORIGINS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Process CORS origins - prefer CORS_ORIGINS, fallback to ALLOWED_ORIGINS
        origins_str = self.CORS_ORIGINS or self.ALLOWED_ORIGINS

        if origins_str:
            try:
                # Try parsing as JSON first
                parsed_origins = json.loads(origins_str)
                if isinstance(parsed_origins, list):
                    self.BACKEND_CORS_ORIGINS = parsed_origins
            except (json.JSONDecodeError, TypeError):
                # If not JSON, split by comma
                self.BACKEND_CORS_ORIGINS = [
                    origin.strip() for origin in origins_str.split(',')
                ]


settings = Settings()