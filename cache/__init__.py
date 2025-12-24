"""
F1 Strategy Engine - Caching Module

Multi-tier Redis caching for FastF1 data and API responses.
Provides connection pooling, cache key generation, and TTL strategies.
"""

from .redis_client import RedisClient, get_redis_client
from .cache_keys import CacheKeys
from .ttl_strategy import TTLStrategy, calculate_dynamic_ttl
from .cache_manager import CacheManager, get_cache_manager
from .cache_decorators import (
    cached,
    invalidate_cache,
    cache_aside,
    conditional_cache,
)

__all__ = [
    # Redis client
    "RedisClient",
    "get_redis_client",
    
    # Cache keys
    "CacheKeys",
    
    # TTL strategy
    "TTLStrategy",
    "calculate_dynamic_ttl",
    
    # Cache manager
    "CacheManager",
    "get_cache_manager",
    
    # Decorators
    "cached",
    "invalidate_cache",
    "cache_aside",
    "conditional_cache",
]
