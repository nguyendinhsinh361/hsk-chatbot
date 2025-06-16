from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models.chat_models import BaseChatModel
from app.config.config import OPENAI_API_KEY, GOOGLE_API_KEY, LANGSMITH_TRACING
from app.utils.langsmith import get_langsmith_tracer
from app.enum.model import ModelProvider, ModelGeminiName, ModelOpenAiName

def get_openai_model(model_name: ModelOpenAiName = ModelOpenAiName.OPENAI_GPT_4_1_NANO, temperature=0.7, max_tokens=None, run_name=None) -> BaseChatModel:
    """
    Initialize and return an OpenAI chat model.
    
    Args:
        model_name (str): The name of the OpenAI model to use
        temperature (float): Controls randomness in responses
        max_tokens (int, optional): Maximum number of tokens to generate
        run_name (str, optional): Name for tracing runs
        
    Returns:
        ChatOpenAI: An instance of ChatOpenAI
    """
    if not OPENAI_API_KEY:
        raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
    
    # Convert enum to string value if it's an enum
    model_name_value = model_name.value if hasattr(model_name, 'value') else str(model_name)
    
    callbacks = []
    if LANGSMITH_TRACING:
        tracer = get_langsmith_tracer(run_name=run_name or f"openai-{model_name_value}")
        if tracer:
            callbacks.append(tracer)
    
    model_kwargs = {
        "model": model_name_value,
        "temperature": temperature,
        "api_key": OPENAI_API_KEY,
        "callbacks": callbacks if callbacks else None
    }
    
    # Add max_tokens if provided
    if max_tokens is not None:
        model_kwargs["max_tokens"] = max_tokens
    
    return ChatOpenAI(**model_kwargs)

def get_gemini_model(model_name: ModelGeminiName = ModelGeminiName.GEMINI_2_0_FLASH, temperature=0.7, max_tokens=None, run_name=None) -> BaseChatModel:
    """
    Initialize and return a Google Gemini chat model.
    
    Args:
        model_name (str): The name of the Gemini model to use
        temperature (float): Controls randomness in responses
        max_tokens (int, optional): Maximum number of tokens to generate
        run_name (str, optional): Name for tracing runs
        
    Returns:
        ChatGoogleGenerativeAI: An instance of ChatGoogleGenerativeAI
    """
    if not GOOGLE_API_KEY:
        raise ValueError("Google API key is not set. Please set the GOOGLE_API_KEY environment variable.")
    
    # Convert enum to string value if it's an enum
    model_name_value = model_name.value if hasattr(model_name, 'value') else str(model_name)
    
    callbacks = []
    if LANGSMITH_TRACING:
        tracer = get_langsmith_tracer(run_name=run_name or f"gemini-{model_name_value}")
        if tracer:
            callbacks.append(tracer)
    
    model_kwargs = {
        "model": model_name_value,
        "temperature": temperature,
        "google_api_key": GOOGLE_API_KEY,
        "callbacks": callbacks if callbacks else None
    }
    
    # Add max_tokens if provided
    if max_tokens is not None:
        model_kwargs["max_output_tokens"] = max_tokens  # Gemini uses max_output_tokens instead of max_tokens
    
    return ChatGoogleGenerativeAI(**model_kwargs)

def get_model(provider: ModelProvider = ModelProvider.GEMINI, run_name=None, **kwargs) -> BaseChatModel:
    """
    Factory function to get the appropriate model based on provider.
    
    Args:
        provider (str): The model provider to use ('openai' or 'gemini')
        run_name (str, optional): Name for tracing runs
        **kwargs: Additional arguments to pass to the model initializer
        
    Returns:
        BaseChatModel: An instance of a chat model
    """
    if provider == ModelProvider.OPENAI or (hasattr(provider, 'value') and provider.value == ModelProvider.OPENAI.value):
        return get_openai_model(run_name=run_name, **kwargs)
    elif provider == ModelProvider.GEMINI or (hasattr(provider, 'value') and provider.value == ModelProvider.GEMINI.value):
        return get_gemini_model(run_name=run_name, **kwargs)
    else:
        raise ValueError(f"Unsupported model provider: {provider}. Use 'openai' or 'gemini'.") 