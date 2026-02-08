"""
Configuration settings for the Fantasy Copilot API
Uses environment variables with sensible defaults
"""
import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    FDE Interview Talking Point:
    - Centralized configuration makes the app easily customizable for different customers
    - Environment-based settings allow different configs per deployment (dev/staging/prod)
    """
    
    # Redis Configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    
    # Cache Configuration
    CACHE_ENABLED: bool = True
    CACHE_TTL_SECONDS: int = 3600  # 1 hour default
    
    # Perplexity API
    PERPLEXITY_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignore extra env vars


# Singleton instance
settings = Settings()
