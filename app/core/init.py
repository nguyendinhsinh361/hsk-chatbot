"""
Application initialization module.
"""

import os
import logging
from app.core.config import settings
from app.repositories.mongodb import get_mongodb_client
from app.core.langsmith import get_langsmith_client

# Set up logging
logger = logging.getLogger(__name__)

def init_application():
    """
    Initialize the application, setting up database connections and LangSmith tracing.
    
    Returns:
        bool: True if initialization was successful
    """
    # Connect to MongoDB to verify the connection
    client = get_mongodb_client()
    
    # Clear LangChain environment variables to prevent automatic tracing
    # We'll handle tracing directly through our own code
    os.environ.pop("LANGCHAIN_TRACING_V2", None)
    os.environ.pop("LANGCHAIN_TRACING", None)
    os.environ.pop("LANGCHAIN_API_KEY", None)
    
    # Enable LangSmith tracing if configured
    if settings.LANGSMITH_TRACING:
        if not settings.LANGSMITH_API_KEY:
            logger.warning("LangSmith tracing is enabled but LANGSMITH_API_KEY is not set.")
        else:
            try:
                # Initialize LangSmith client to verify connection
                langsmith_client = get_langsmith_client()
                if langsmith_client:
                    logger.info(f"LangSmith tracing is enabled for project: {settings.LANGSMITH_PROJECT}")
                    
                    # Set environment variables for LangChain
                    os.environ["LANGCHAIN_PROJECT"] = settings.LANGSMITH_PROJECT
            except Exception as e:
                logger.error(f"Failed to initialize LangSmith client: {e}")
    else:
        logger.info("LangSmith tracing is disabled.")
    
    logger.info("Application initialized successfully.")
    return True 