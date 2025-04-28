import os
from pydantic_settings import BaseSettings
from typing import Dict, List, Optional, Any

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "Healthcare Compliance RAG System"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # API settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # LLM settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    LLM_MODEL: str = "gpt-4o"
    
    # Vector database settings
    VECTOR_DB_PATH: str = "app/data/vector_db"
    
    # Compliance document settings
    COMPLIANCE_DOCS_PATH: str = "app/data/compliance_docs"
    
    # Logging settings
    LOG_LEVEL: str = "INFO"
    
    # Validation
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create settings instance
settings = Settings()

def get_settings() -> Settings:
    return settings 