"""
Chat-related schemas.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from app.enum.model import ModelProvider

class ChatRequest(BaseModel):
    """Chat request schema."""
    
    user_input: str = Field(..., description="User's message")
    session_id: Optional[str] = Field(None, description="Session ID (optional)")
    model_provider: ModelProvider = Field(ModelProvider.GEMINI, description="LLM provider (openai or gemini)")
    use_graph: bool = Field(True, description="Use graph-based approach")
    
    model_config = {
        "protected_namespaces": (),
        "use_enum_values": True,
        "json_schema_extra": {
            "properties": {
                "model_provider": {
                    "type": "string",
                    "enum": [provider.value for provider in ModelProvider],
                    "default": ModelProvider.GEMINI.value
                },
                "use_graph": {
                    "type": "boolean",
                    "default": True
                },
                "session_id": {
                    "type": "string",
                    "default": None
                },
                "user_input": {
                    "type": "string",
                    "default": None
                }
            }
        }
    }

class Message(BaseModel):
    """Chat message schema."""
    
    role: str = Field(..., description="Message role (user or assistant)")
    content: str = Field(..., description="Message content")
    timestamp: Optional[int] = Field(None, description="Message timestamp")

class ChatSession(BaseModel):
    """Chat session schema."""
    
    session_id: str = Field(..., description="Session ID")
    model_provider: str = Field(..., description="LLM provider")
    created_at: Optional[int] = Field(None, description="Creation timestamp")
    messages: List[Message] = Field(default_factory=list, description="Session messages")
    
    model_config = {
        "protected_namespaces": ()
    }

class ChatResponse(BaseModel):
    """Chat response schema."""
    
    response: Dict[str, Any] = Field(..., description="Response data")
    session_id: str = Field(..., description="Session ID") 