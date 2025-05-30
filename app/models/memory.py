from langchain_mongodb import MongoDBChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from app.config.config import MONGODB_URI, MONGODB_DB_NAME

def get_mongodb_chat_history(session_id):
    """
    Create a MongoDB-backed chat message history.
    
    Args:
        session_id (str): A unique identifier for the conversation
        
    Returns:
        MongoDBChatMessageHistory: A chat history stored in MongoDB
    """
    return MongoDBChatMessageHistory(
        connection_string=MONGODB_URI,
        database_name=MONGODB_DB_NAME,
        collection_name="chat_history",
        session_id=session_id,
    )

def get_conversation_memory(session_id, memory_key="chat_history", return_messages=True):
    """
    Create a conversation memory with MongoDB backend.
    
    Args:
        session_id (str): A unique identifier for the conversation
        memory_key (str): The key to use for the memory in the chain
        return_messages (bool): Whether to return the history as messages
        
    Returns:
        BaseChatMessageHistory: A history object to use in chains
    """
    # In newer versions of LangChain, we use ChatMessageHistory directly
    # instead of ConversationBufferMemory
    return get_mongodb_chat_history(session_id) 