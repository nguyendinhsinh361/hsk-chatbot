"""
LLM models service.
"""

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models.chat_models import BaseChatModel
from app.core.config import settings
from app.core.langsmith import get_langsmith_tracer
from app.enum.model import ModelProvider, ModelGeminiName, ModelOpenAiName

def get_openai_model(model_name: ModelOpenAiName = ModelOpenAiName.OPENAI_GPT_4O_MINI, temperature=0.7, run_name=None) -> BaseChatModel:
    """
    Initialize and return an OpenAI chat model.
    
    Args:
        model_name (str): The name of the OpenAI model to use
        temperature (float): Controls randomness in responses
        run_name (str, optional): Name for tracing runs
        
    Returns:
        ChatOpenAI: An instance of ChatOpenAI
    """
    if not settings.OPENAI_API_KEY:
        raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
    
    callbacks = []
    if settings.LANGSMITH_TRACING:
        tracer = get_langsmith_tracer(run_name=run_name or f"openai-{model_name}")
        if tracer:
            callbacks.append(tracer)
    
    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        api_key=settings.OPENAI_API_KEY,
        callbacks=callbacks if callbacks else None
    )

def get_gemini_model(model_name="gemini-2.0-flash", temperature=0.7, run_name=None) -> BaseChatModel:
    """
    Initialize and return a Google Gemini chat model.
    
    Args:
        model_name (str): The name of the Gemini model to use
        temperature (float): Controls randomness in responses
        run_name (str, optional): Name for tracing runs
        
    Returns:
        ChatGoogleGenerativeAI: An instance of ChatGoogleGenerativeAI
    """
    if not settings.GOOGLE_API_KEY:
        raise ValueError("Google API key is not set. Please set the GOOGLE_API_KEY environment variable.")
    
    callbacks = []
    if settings.LANGSMITH_TRACING:
        tracer = get_langsmith_tracer(run_name=run_name or f"gemini-{model_name}")
        if tracer:
            callbacks.append(tracer)
    
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
        google_api_key=settings.GOOGLE_API_KEY,
        callbacks=callbacks if callbacks else None
    )

def get_model(provider: ModelProvider = ModelProvider.GEMINI, run_name=None, **kwargs) -> BaseChatModel:
    """
    Factory function to get the appropriate model based on provider.
    
    Args:
        provider (ModelProvider): The model provider to use (ModelProvider.OPENAI or ModelProvider.GEMINI)
        run_name (str, optional): Name for tracing runs
        **kwargs: Additional arguments to pass to the model initializer
        
    Returns:
        BaseChatModel: An instance of a chat model
    """
    if provider == ModelProvider.OPENAI or provider.value == ModelProvider.OPENAI.value:
        return get_openai_model(run_name=run_name, **kwargs)
    elif provider == ModelProvider.GEMINI or provider.value == ModelProvider.GEMINI.value:
        return get_gemini_model(run_name=run_name, **kwargs)
    else:
        raise ValueError(f"Unsupported model provider: {provider}. Use 'openai' or 'gemini'.") 