"""
Application configuration module.
"""

import os
from typing import List, Union, Optional
from pydantic import BaseModel, Field

class Settings(BaseModel):
    """Application settings."""
    
    # App settings
    APP_NAME: str = "HSK Chatbot API"
    APP_DESCRIPTION: str = "A chatbot API built with LangChain, LangGraph, and FastAPI"
    APP_VERSION: str = "0.1.0"
    
    # API settings
    API_PREFIX: str = "/api"
    CORS_ORIGINS: List[str] = ["*"]  # In production, replace with specific origins
    
    # Database settings
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "hsk_chatbot")
    
    # LLM API settings
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
    DEFAULT_MODEL_PROVIDER: str = os.getenv("DEFAULT_MODEL_PROVIDER", "gemini")
    
    # LangSmith settings
    LANGSMITH_API_KEY: Optional[str] = os.getenv("LANGSMITH_API_KEY")
    LANGSMITH_PROJECT: str = os.getenv("LANGSMITH_PROJECT", "hsk-chatbot")
    LANGSMITH_TRACING: bool = os.getenv("LANGSMITH_TRACING", "false").lower() == "true"
    LANGSMITH_ENDPOINT: str = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "forbid"
    }

# Create global settings instance
settings = Settings() 