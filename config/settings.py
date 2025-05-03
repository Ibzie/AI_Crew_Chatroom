# config/settings.py
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Base directory
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    
    # API Keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    # LLM Configuration
    DEFAULT_MODEL: str = "llama3-8b-8192"  # Groq's Llama 3 8B model
    PREMIUM_MODEL: str = "mixtral-8x7b-32768"  # Mixtral model if needed for more complex tasks
    DEFAULT_TEMPERATURE: float = 0.7
    SYSTEM_TEMPERATURE: float = 0.2  # Lower temperature for more predictable system operations
    
    # Agent Configuration
    MAX_ITERATIONS: int = 10
    DEFAULT_VERBOSE: bool = True
    THINKING_DEPTH: int = 3  # How many levels of thinking before responding
    
    # Memory Configuration
    MAX_CONTEXT_MESSAGES: int = 10  # Maximum number of messages to include in context window
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Validate configuration
    def validate(self):
        if not self.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        return self

# Initialize settings
settings = Settings().validate()