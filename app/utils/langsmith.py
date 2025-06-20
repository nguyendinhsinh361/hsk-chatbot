from langsmith import Client
from langchain_core.tracers import LangChainTracer
import logging
from app.config.config import (
    LANGSMITH_API_KEY, 
    LANGSMITH_PROJECT, 
    LANGSMITH_TRACING,
    LANGSMITH_ENDPOINT
)

# Set up logging
logger = logging.getLogger(__name__)

def get_langsmith_client():
    """
    Returns a configured LangSmith client or None if not configured
    """
    if not LANGSMITH_API_KEY:
        logger.warning("LangSmith API key not set. Tracing disabled.")
        return None
    
    try:
        return Client(
            api_key=LANGSMITH_API_KEY,
            api_url=LANGSMITH_ENDPOINT
        )
    except Exception as e:
        logger.warning(f"Failed to initialize LangSmith client: {str(e)}")
        return None

def get_langchain_tracer(run_name=None):
    """
    Returns a configured LangChain tracer for LangSmith
    
    Args:
        run_name (str, optional): Name for the trace run
        
    Returns:
        LangChainTracer or None: Configured tracer
    """
    if not LANGSMITH_TRACING or not LANGSMITH_API_KEY:
        return None
    
    try:
        # In newer versions, run_name is not supported
        client = get_langsmith_client()
        
        if not client:
            return None
            
        # Use tags to include the run name
        tags = [run_name] if run_name else None
        
        return LangChainTracer(
            project_name=LANGSMITH_PROJECT,
            client=client,
            tags=tags
        )
    except Exception as e:
        logger.warning(f"Failed to initialize LangChain tracer: {str(e)}")
        return None

def get_langsmith_tracer(run_name=None):
    """
    Returns a configured LangSmith tracer
    
    Args:
        run_name (str, optional): Name for the trace run
        
    Returns:
        LangChainTracer or None: Configured tracer
    """
    # In newer versions, LangSmithTracer doesn't exist separately
    # We'll use LangChainTracer for both cases
    return get_langchain_tracer(run_name) 