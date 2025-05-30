"""
Chat service module.
"""

from typing import Dict, Any, Tuple, Optional
import uuid

from app.services.llm import get_model
from app.services.memory import get_memory, save_message_to_memory
from app.repositories.chat_session import ChatSessionRepository
from app.enum.model import ModelProvider
from app.chains.simple_chat_chain import create_simple_chat_chain
from app.graph.chat_graph import create_chat_graph, process_user_input

def get_or_create_session(session_id: Optional[str] = None, model_provider: ModelProvider = ModelProvider.GEMINI) -> str:
    """
    Get an existing session or create a new one.
    
    Args:
        session_id (str, optional): An existing session ID
        model_provider (str): The LLM provider to use
        
    Returns:
        str: The session ID
    """
    repo = ChatSessionRepository()
    
    if session_id:
        # Check if the session exists
        session = repo.get_session(session_id)
        if session:
            return session_id
    
    # Create a new session
    return repo.create_session(model_provider=model_provider)

def chat_with_simple_chain(
    user_input: str, 
    session_id: Optional[str] = None, 
    model_provider: ModelProvider = ModelProvider.GEMINI
) -> Tuple[Dict[str, Any], str]:
    """
    Chat with the user using the simple chain approach.
    
    Args:
        user_input (str): The user's input message
        session_id (str, optional): An existing session ID
        model_provider (str): The LLM provider to use
        
    Returns:
        Tuple[Dict[str, Any], str]: (response, session_id)
    """
    # Get or create a session
    session_id = get_or_create_session(session_id, model_provider)
    
    # Save user message
    save_message_to_memory(session_id, "user", user_input)
    
    # Create the chain
    chain = create_simple_chat_chain(session_id, model_provider=model_provider)
    
    # Call the chain
    result = chain({"input": user_input})
    
    # Save assistant response
    save_message_to_memory(session_id, "assistant", result["output"])
    
    return result, session_id

def chat_with_graph(
    user_input: str, 
    session_id: Optional[str] = None, 
    model_provider: ModelProvider = ModelProvider.GEMINI
) -> Tuple[Dict[str, Any], str]:
    """
    Chat with the user using the graph-based approach.
    
    Args:
        user_input (str): The user's input message
        session_id (str, optional): An existing session ID
        model_provider (str): The LLM provider to use
        
    Returns:
        Tuple[Dict[str, Any], str]: (response, session_id)
    """
    # Get or create a session
    session_id = get_or_create_session(session_id, model_provider)
    
    # Save user message
    save_message_to_memory(session_id, "user", user_input)
    
    # Create the graph
    graph = create_chat_graph(session_id, model_provider=model_provider)
    
    # Process user input
    result = process_user_input(graph, user_input, session_id)
    
    # Save assistant response
    if "output" in result:
        save_message_to_memory(session_id, "assistant", result["output"])
    
    return result, session_id 