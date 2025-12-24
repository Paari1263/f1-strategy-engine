"""
Redis Configuration Module

Provides Redis connection settings and configuration management.
"""

from pydantic_settings import BaseSettings
from pydantic import Field


class RedisSettings(BaseSettings):
    """Redis connection and configuration settings."""
    
    # Connection settings
    host: str = Field(default="localhost", description="Redis host")
    port: int = Field(default=6379, description="Redis port")
    password: str = Field(default="f1-redis-secret", description="Redis password")
    db: int = Field(default=0, description="Redis database number")
    
    # Connection pool settings
    max_connections: int = Field(default=50, description="Maximum pool connections")
    socket_timeout: int = Field(default=5, description="Socket timeout in seconds")
    socket_connect_timeout: int = Field(default=5, description="Socket connect timeout")
    socket_keepalive: bool = Field(default=True, description="Enable socket keepalive")
    retry_on_timeout: bool = Field(default=True, description="Retry on timeout")
    
    # Cache behavior settings
    default_ttl: int = Field(default=3600, description="Default TTL in seconds (1 hour)")
    max_ttl: int = Field(default=604800, description="Maximum TTL in seconds (7 days)")
    enable_cache: bool = Field(default=True, description="Enable/disable caching globally")
    
    # Cache key settings
    key_prefix: str = Field(default="f1:cache", description="Cache key prefix")
    
    class Config:
        env_file = ".env"
        env_prefix = "REDIS_"
        case_sensitive = False


# Global settings instance
redis_settings = RedisSettings()
