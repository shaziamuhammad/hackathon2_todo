from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Secure Todo API"
    API_VERSION: str = "v1"
    ALLOWED_ORIGINS: list[str] = ["*"]
    DATABASE_URL: str = "sqlite:///./todo_app.db"
    BETTER_AUTH_SECRET: str = "your-super-secret-jwt-token-with-at-least-32-characters-long"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()