from typing import Any, Dict, List, Optional, Union
import secrets
from pydantic import AnyHttpUrl, EmailStr, field_validator, ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings.
    
    These settings are loaded from environment variables and/or .env file.
    """
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)
    
    # API Settings
    PROJECT_NAME: str = "Teacherly AI Backend"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ENCRYPTION_KEY: str = secrets.token_urlsafe(32)
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database Settings
    DATABASE_URL: str
    TEST_DATABASE_URL: Optional[str] = None
    
    # Vector Database Settings
    # These are optional as different vector DBs might be used
    PINECONE_API_KEY: Optional[str] = None
    PINECONE_ENVIRONMENT: Optional[str] = None
    PINECONE_INDEX_NAME: Optional[str] = None
    
    QDRANT_URL: Optional[str] = None
    QDRANT_COLLECTION_NAME: Optional[str] = None
    
    WEAVIATE_URL: Optional[str] = None
    WEAVIATE_API_KEY: Optional[str] = None
    
    PGVECTOR_CONNECTION_STRING: Optional[str] = None
    
    # AI API Keys
    GEMINI_API_KEY: Optional[str] = None
    OCR_API_KEY: Optional[str] = None
    
    # Email Settings
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None


# Create a global settings object
settings = Settings()
