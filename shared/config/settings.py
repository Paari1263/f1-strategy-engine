"""
Configuration settings for F1 Race Strategy Simulator
Uses pydantic-settings for environment variable management
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # API Configuration
    app_name: str = "F1 Race Strategy Simulator"
    app_version: str = "1.0.0"
    api_prefix: str = ""
    debug: bool = False
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8001
    reload: bool = False
    
    # FastF1 Configuration
    fastf1_cache_dir: str = "cache/fastf1"
    fastf1_cache_enabled: bool = True
    fastf1_ergast_support: bool = True
    
    # CORS Configuration
    cors_origins: list[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]
    
    # Logging Configuration
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Cache Configuration (for future use)
    cache_enabled: bool = False
    cache_ttl: int = 300  # seconds
    
    # Rate Limiting (for future use)
    rate_limit_enabled: bool = False
    rate_limit_requests: int = 100
    rate_limit_window: int = 60  # seconds
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
