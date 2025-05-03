from langchain_groq import ChatGroq
from langchain.schema import SystemMessage
from typing import Optional, Dict, Any
from config.settings import settings
from config.logging_config import logger


# Cache 
_llm_cache: Dict[str, ChatGroq] = {}

def get_llm(model: Optional[str] = None, temperature: Optional[float] = None) -> ChatGroq:
    """
    Getting a groq llm

    ARGs:
    Model: Model name/id to use
    Temperature: Temperaturs setting

    Returns:
    Configured ChatGroq Instance

    All defaults are in config/settings.py
    """

    # Use the defaults
    model_name = model or settings.DEFAULT_MODEL
    temp = temperature if temperature is not None else settings.DEFAULT_TEMPERATURE

    cache_key = f"{model_name}_{temp}"
    print(cache_key)

    # Return cache if exists
    if cache_key in _llm_cache:
        return _llm_cache[cache_key]
    
    # Log LLM creation
    logger.info(f"Creating new LLM Instance via {cache_key}")

    # Create LLM Instance
    llm = ChatGroq(
        api_key = settings.GROQ_API_KEY,
        model_name = model_name,
        temperature= temp,
    )

    # Add instance to cache
    _llm_cache[cache_key] = llm
    
    # Voila, we got an LLM BOISSSS
    return llm
