"""
HSK Chatbot Package.

This module initializes the application and provides the application factory.
"""

__version__ = "0.1.0"

from app.core.config import settings
from app.core.init import init_application

def create_app():
    """
    Application factory function.
    
    Returns:
        FastAPI: The configured FastAPI application
    """
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from app.api.routes import router as api_router
    
    # Initialize the application before creating the FastAPI instance
    init_application()
    
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API router
    app.include_router(api_router)
    
    return app 