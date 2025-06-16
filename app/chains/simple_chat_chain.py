from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from app.models.llm_models import get_model
from app.models.memory import get_conversation_memory
from app.utils.langsmith import get_langchain_tracer
from app.config.config import LANGSMITH_TRACING
from app.enum.model import ModelProvider, ModelGeminiName, ModelOpenAiName

def create_simple_chat_chain(session_id, model_provider: ModelProvider = ModelProvider.GEMINI, model_name: ModelGeminiName = ModelGeminiName.GEMINI_2_0_FLASH.value, temperature=0.7, max_tokens=200):
    """
    Create a simple conversational chain with memory.
    
    Args:
        session_id (str): A unique identifier for the conversation
        model_provider (str): The LLM provider to use ('openai' or 'gemini')
        model_name (str, optional): The specific model name to use
        temperature (float): Controls randomness in responses
        max_tokens (int): Maximum number of tokens in the response (default: 150)
        
    Returns:
        Runnable: A runnable chain for chatting
    """
    # Configure model parameters
    model_kwargs = {
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    if model_provider == ModelProvider.OPENAI:
        model_name = ModelOpenAiName.OPENAI_GPT_4_1_NANO
    # Convert enum to string value if it's an enum
    model_name_value = model_name.value if hasattr(model_name, 'value') else model_name
    
    if model_name_value:
        model_kwargs["model_name"] = model_name_value
    
    # Run name for tracing
    run_name = f"{model_provider}-simple-chat-{session_id}"
    
    # Get the language model
    llm = get_model(provider=model_provider, run_name=run_name, **model_kwargs)
    
    # Get conversation memory
    message_history = get_conversation_memory(session_id)
    
    # Create the prompt template - handle differently based on model provider
    system_instruction = """You are a friendly and helpful HSK chatbot assistant. Your name is "mIA"
    Please respond in the same language as the user's input.
    You specialize in teaching Chinese (HSK) and can help with vocabulary, grammar, and language learning."""
    
    if model_provider == ModelProvider.GEMINI:
        # For Gemini, we include the system instruction in the first human message
        prompt = ChatPromptTemplate.from_messages([
            MessagesPlaceholder(variable_name="history"),
            ("human", f"{system_instruction}\n\n{{input}}"),
        ])
    elif model_provider == ModelProvider.OPENAI:
        # For other models like OpenAI, we use a separate system message
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_instruction),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ])
    
    # Chain together the components
    chain = prompt | llm | StrOutputParser()
    
    # Create the chain with memory handled manually
    def chain_with_memory(input_dict):
        # Get the chat history
        history = message_history.messages
        
        # Invoke the chain
        output = chain.invoke({
            "input": input_dict["input"],
            "history": history
        })
        
        # Add to history
        message_history.add_user_message(input_dict["input"])
        message_history.add_ai_message(output)
        
        # Return a dictionary with output key instead of just the string
        return {"output": output}
    
    # Return the chain function
    return chain_with_memory 