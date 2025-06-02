import os
from typing import Dict, Any
from pydantic_settings import BaseSettings

class Config:
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_WORKERS: int = int(os.getenv("API_WORKERS", "1"))
    
    # Model Configuration
    MODEL_NAME: str = os.getenv("MODEL_NAME", "google/flan-t5-base")
    MAX_NEW_TOKENS: int = int(os.getenv("MAX_NEW_TOKENS", "100"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    TOP_P: float = float(os.getenv("TOP_P", "0.9"))
    NUM_BEAMS: int = int(os.getenv("NUM_BEAMS", "4"))
    
    # Cache Configuration
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))  # 1 hour
    CACHE_MAX_SIZE: int = int(os.getenv("CACHE_MAX_SIZE", "1000"))
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "DEBUG")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: str = os.getenv("LOG_FILE", "agent.log")
    
    # Security Configuration
    API_KEY_HEADER: str = "X-API-Key"
    RATE_LIMIT: int = int(os.getenv("RATE_LIMIT", "100"))  # requests per minute
    
    @classmethod
    def get_all(cls) -> Dict[str, Any]:
        """Get all configuration values as a dictionary."""
        return {
            key: value for key, value in cls.__dict__.items()
            if not key.startswith('_') and isinstance(value, (str, int, float, bool))
        }
    
    @classmethod
    def validate(cls) -> None:
        """Validate configuration values."""
        if cls.API_PORT < 1 or cls.API_PORT > 65535:
            raise ValueError("Invalid API_PORT value")
        if cls.CACHE_TTL < 0:
            raise ValueError("CACHE_TTL must be positive")
        if cls.CACHE_MAX_SIZE < 0:
            raise ValueError("CACHE_MAX_SIZE must be positive")
        if cls.RATE_LIMIT < 0:
            raise ValueError("RATE_LIMIT must be positive")
        if cls.TEMPERATURE < 0 or cls.TEMPERATURE > 1:
            raise ValueError("TEMPERATURE must be between 0 and 1")
        if cls.TOP_P < 0 or cls.TOP_P > 1:
            raise ValueError("TOP_P must be between 0 and 1")
        if cls.NUM_BEAMS < 1:
            raise ValueError("NUM_BEAMS must be positive")

class Settings(BaseSettings):
    # API Configuration
    API_KEY: str = "your-secret-key-here"
    CACHE_TTL: int = 3600  # Cache time-to-live in seconds

    class Config:
        env_file = ".env"

# Create settings instance
settings = Settings() 