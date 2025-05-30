"""
API routes module.
"""

from fastapi import APIRouter, HTTPException, Depends, Body
from typing import Dict, Any

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat import chat_with_simple_chain, chat_with_graph
from app.enum.model import ModelProvider

# Create API router
router = APIRouter(prefix="/api")

def validate_model_provider(provider):
    """
    Validate and convert the model provider to the correct enum value.
    
    Args:
        provider: The provider value from the request
        
    Returns:
        ModelProvider: The validated ModelProvider enum
    """
    # If it's already an enum instance, return it
    if isinstance(provider, ModelProvider):
        return provider
    
    # If it's a string value, try to convert it
    if isinstance(provider, str):
        try:
            # Try to match by value
            for enum_provider in ModelProvider:
                if provider.lower() == enum_provider.value.lower():
                    return enum_provider
            
            # If no match found, raise error
            raise ValueError(f"Invalid model provider: {provider}")
        except Exception as e:
            raise ValueError(f"Invalid model provider: {provider}. Valid values are: {[p.value for p in ModelProvider]}")
    
    # If we got here, the type is not supported
    raise ValueError(f"Unsupported model provider type: {type(provider)}")

@router.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to the HSK Chatbot API. Use /chat endpoint to interact with the chatbot."
    }

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest = Body(...)):
    """
    Chat endpoint.
    
    Args:
        request (ChatRequest): The chat request
    
    Returns:
        ChatResponse: The chat response
    """
    try:
        # Validate the model provider
        validated_provider = validate_model_provider(request.model_provider)
        
        if request.use_graph:
            response, session_id = chat_with_graph(
                request.user_input, 
                request.session_id, 
                model_provider=validated_provider
            )
        else:
            response, session_id = chat_with_simple_chain(
                request.user_input, 
                request.session_id, 
                model_provider=validated_provider
            )
        
        return ChatResponse(response=response, session_id=session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"} 