from typing import Dict, TypedDict, List, Annotated, Literal
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.models.llm_models import get_model
from app.models.memory import get_mongodb_chat_history
from app.utils.langsmith import get_langchain_tracer
from app.config.config import LANGSMITH_TRACING
from app.enum.model import ModelProvider, ModelGeminiName, ModelOpenAiName

# Define state types
class AgentState(TypedDict):
    messages: List[BaseMessage]

def create_chat_graph(session_id, model_provider: ModelProvider = ModelProvider.GEMINI, model_name: ModelGeminiName = ModelGeminiName.GEMINI_2_0_FLASH, temperature=0.7):
    """
    Create a simplified version of a conversation agent.
    
    Args:
        session_id (str): A unique identifier for the conversation
        model_provider (str): The LLM provider to use ('openai' or 'gemini')
        model_name (str, optional): The specific model name to use
        temperature (float): Controls randomness in responses
        
    Returns:
        A function that processes messages
    """
    # Configure model parameters
    model_kwargs = {"temperature": temperature}
    
    # Convert enum to string value if it's an enum
    model_name_value = model_name.value if hasattr(model_name, 'value') else model_name
    
    if model_name_value:
        model_kwargs["model_name"] = model_name_value
    
    # Run name for tracing
    run_name = f"{model_provider}-graph-chat-{session_id}"
    
    # Get the language model
    llm = get_model(provider=model_provider, run_name=run_name, **model_kwargs)
    
    # Get conversation history
    message_history = get_mongodb_chat_history(session_id)
    
    # Create a system prompt for the chatbot
    system_prompt = """Bạn là một trợ lý trò chuyện thân thiện, hữu ích.
    Trả lời các câu hỏi của con người theo khả năng tốt nhất của bạn."""
    
    # Create the prompt template - handle differently based on model provider
    if model_provider == ModelProvider.GEMINI:
        # For Gemini, we'll handle the system prompt differently
        # First, check if there are any messages yet
        if message_history.messages:
            # If there are existing messages, we'll just use those
            prompt = ChatPromptTemplate.from_messages([
                MessagesPlaceholder(variable_name="messages"),
            ])
        else:
            # If this is a new conversation, add the system instruction to the first message
            # We'll add it dynamically in the process_messages function
            prompt = ChatPromptTemplate.from_messages([
                MessagesPlaceholder(variable_name="messages"),
            ])
    elif model_provider == ModelProvider.OPENAI:
        # For other models like OpenAI, we use a separate system message
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ])
    
    # Define the process function
    def process_messages(messages):
        # For Gemini model and empty conversation, add system instruction to first message
        if model_provider == ModelProvider.GEMINI and not message_history.messages:
            if messages and isinstance(messages[0], HumanMessage):
                # Prepend system instruction to the first human message
                messages[0] = HumanMessage(content=f"{system_prompt}\n\n{messages[0].content}")
        
        # Get the response from the LLM
        response = prompt.invoke({"messages": messages})
        # Don't pass callbacks here as they're already included in the model
        chain_response = llm.invoke(response)
        
        # Create a new AI message
        ai_message = AIMessage(content=chain_response.content)
        
        # Save the message to the chat history
        message_history.add_message(ai_message)
        
        # Return the updated messages
        return messages + [ai_message]
    
    return process_messages

def process_user_input(graph_function, user_input, session_id):
    """
    Process user input through the graph function.
    
    Args:
        graph_function: The function that processes messages
        user_input (str): The user's input message
        session_id (str): The session ID for retrieving history
        
    Returns:
        str: The assistant's response
    """
    # Get the message history
    message_history = get_mongodb_chat_history(session_id)
    messages = message_history.messages
    
    # Add the new user message
    human_message = HumanMessage(content=user_input)
    message_history.add_message(human_message)
    
    # Add the message to the messages list
    messages.append(human_message)
    
    # Process the messages
    updated_messages = graph_function(messages)
    
    # Get the last message (the assistant's response)
    last_message = updated_messages[-1] if updated_messages else None
    
    if last_message and hasattr(last_message, 'content'):
        return {"output": last_message.content}
    
    return {"output": "I'm sorry, I couldn't generate a response."} 