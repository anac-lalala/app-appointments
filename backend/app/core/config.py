"""
Application configuration.

Reads from environment variables defined in .env file.
Non-negotiable control values per docs/implementacion.md section 4.
"""
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


_CORE_DIR = Path(__file__).resolve().parent
_APP_DIR = _CORE_DIR.parent
_BACKEND_DIR = _APP_DIR.parent
_REPO_ROOT_DIR = _BACKEND_DIR.parent


class Settings(BaseSettings):
    """Application settings with validation."""

    model_config = SettingsConfigDict(
        env_file=(
            str(_BACKEND_DIR / ".env"),
            str(_REPO_ROOT_DIR / ".env"),
            ".env",
        ),
        case_sensitive=True,
    )
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://citas:devpass@localhost:5432/citas"
    
    # JWT (non-negotiable)
    JWT_SECRET_KEY: str = "change-this-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRES_MINUTES: int = 30
    
    # OTP (non-negotiable control values)
    OTP_TTL_SECONDS: int = 300  # 5 minutes
    OTP_MAX_ATTEMPTS: int = 5
    OTP_REQUEST_RATE_LIMIT_PER_IP: str = "10/15m"
    OTP_REQUEST_RATE_LIMIT_PER_EMAIL: str = "5/h"
    OTP_COOLDOWN_SECONDS: int = 60
    OTP_DEV_LOG_CODE: bool = False
    
    # SMTP (for OTP delivery)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = ""
    
    # CORS (allow frontend by default)
    CORS_ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Environment
    ENVIRONMENT: str = "development"
    
# Global settings instance
settings = Settings()
