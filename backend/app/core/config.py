from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True

    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    BACKEND_URL: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:5173"

    # Security Configuration
    JWT_SECRET: str = "your-super-secret-jwt-signing-key-for-local-development"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Database Settings
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/autofiller"

    # Firebase Service Configuration
    FIREBASE_SERVICE_ACCOUNT_JSON: Optional[str] = "firebase/service-account.json"

    # AI Config
    GEMINI_API_KEY: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
def is_development() -> bool:
    return settings.ENV == "development"
