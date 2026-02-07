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

    # Internal field to capture the raw ALLOWED_ORIGINS environment variable
    RAW_ALLOWED_ORIGINS: str = Field(default='["*"]', alias='ALLOWED_ORIGINS')

    # CORS - This will be processed from the raw ALLOWED_ORIGINS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Process the raw allowed origins after initialization
        try:
            parsed_origins = json.loads(self.RAW_ALLOWED_ORIGINS)
            if isinstance(parsed_origins, list):
                self.BACKEND_CORS_ORIGINS = parsed_origins
        except (json.JSONDecodeError, TypeError):
            # If parsing fails, keep the default
            pass


settings = Settings()