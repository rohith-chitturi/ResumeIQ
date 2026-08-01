from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    """
    Application configuration using Pydantic Settings.
    This guarantees that the environment variables are validated at startup.
    """
    
    # Project Settings
    PROJECT_NAME: str = "ResumeIQ"
    PROJECT_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    
    # Database Settings (For Phase 3 Postgres)
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "resumeiq"
    
    # LLM Settings
    GEMINI_API_KEY: str = ""
    DEFAULT_MODEL: str = "gemini-2.5-flash"
    
    # Embeddings
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore" # Ignore extra env vars
    )

    @property
    def async_database_url(self) -> str:
        """Returns the async database URL for SQLAlchemy asyncpg."""
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

# Global settings instance
settings = Settings()
