"""
Chat session repository module.
"""

import uuid
from typing import Dict, Any, Optional, List
from app.repositories.mongodb import MongoRepository
from app.enum.model import ModelProvider

class ChatSessionRepository(MongoRepository):
    """Repository for chat sessions."""
    
    def __init__(self):
        """Initialize the chat session repository."""
        super().__init__("chat_sessions")
    
    def create_session(self, model_provider: ModelProvider = ModelProvider.GEMINI) -> str:
        """
        Create a new chat session.
        
        Args:
            model_provider (ModelProvider): The LLM provider to use
            
        Returns:
            str: The session ID
        """
        session_id = str(uuid.uuid4())
        
        # Store the string value of the enum in MongoDB
        provider_value = model_provider.value if isinstance(model_provider, ModelProvider) else str(model_provider)
        
        self.collection.insert_one({
            "session_id": session_id,
            "model_provider": provider_value,
            "created_at": uuid.uuid1().time,
            "messages": []
        })
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a chat session by ID.
        
        Args:
            session_id (str): The session ID
            
        Returns:
            Optional[Dict[str, Any]]: The chat session document or None if not found
        """
        return self.collection.find_one({"session_id": session_id})
    
    def save_message(self, session_id: str, role: str, content: str) -> bool:
        """
        Save a message to a chat session.
        
        Args:
            session_id (str): The session ID
            role (str): The message role (user or assistant)
            content (str): The message content
            
        Returns:
            bool: True if successful, False otherwise
        """
        result = self.collection.update_one(
            {"session_id": session_id},
            {
                "$push": {
                    "messages": {
                        "role": role,
                        "content": content,
                        "timestamp": uuid.uuid1().time
                    }
                }
            }
        )
        
        return result.modified_count > 0
    
    def get_messages(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Get all messages for a chat session.
        
        Args:
            session_id (str): The session ID
            
        Returns:
            List[Dict[str, Any]]: The list of messages
        """
        session = self.get_session(session_id)
        if not session:
            return []
        
        return session.get("messages", []) 