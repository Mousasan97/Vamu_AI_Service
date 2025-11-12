"""
Configuration management using Pydantic Settings.
Environment variables are loaded from .env file.
"""
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "VAMU AI Service"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    PORT: int = 8001

    # Google Places API
    GOOGLE_PLACES_API_KEY: str
    GOOGLE_PLACES_BASE_URL: str = "https://places.googleapis.com/v1"

    # Groq API (for LLM features like wishlist)
    GROQ_API_KEY: str

    # NestJS Backend Integration
    BACKEND_API_URL: str = "http://localhost:3000"

    # CORS Settings (comma-separated string in .env)
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8001"

    # Optional: Redis for caching (future)
    REDIS_URL: str = "redis://localhost:6379"

    # Logging
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS_ORIGINS string to list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


# Global settings instance
settings = Settings()
