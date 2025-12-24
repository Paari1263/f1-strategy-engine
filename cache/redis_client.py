"""
Redis Client Module

Provides a singleton Redis client with connection pooling and error handling.
"""

import json
import logging
from typing import Any, Optional, Union
from datetime import timedelta

import redis
from redis.connection import ConnectionPool

from config.redis_config import redis_settings

logger = logging.getLogger(__name__)


class RedisClient:
    """
    Singleton Redis client with connection pooling.
    
    Provides thread-safe Redis operations with automatic serialization,
    connection pooling, and error handling.
    """
    
    _instance: Optional['RedisClient'] = None
    _pool: Optional[ConnectionPool] = None
    _client: Optional[redis.Redis] = None
    
    def __new__(cls) -> 'RedisClient':
        """Ensure singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize Redis client with connection pool."""
        if self._client is None:
            self._initialize_connection()
    
    def _initialize_connection(self) -> None:
        """Create Redis connection pool and client."""
        try:
            self._pool = ConnectionPool(
                host=redis_settings.host,
                port=redis_settings.port,
                password=redis_settings.password,
                db=redis_settings.db,
                max_connections=redis_settings.max_connections,
                socket_timeout=redis_settings.socket_timeout,
                socket_connect_timeout=redis_settings.socket_connect_timeout,
                socket_keepalive=redis_settings.socket_keepalive,
                retry_on_timeout=redis_settings.retry_on_timeout,
                decode_responses=False,  # We'll handle encoding/decoding
            )
            
            self._client = redis.Redis(connection_pool=self._pool)
            
            # Test connection
            self._client.ping()
            logger.info(
                f"Redis client initialized: {redis_settings.host}:{redis_settings.port}"
            )
            
        except redis.ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
        except Exception as e:
            logger.error(f"Error initializing Redis client: {e}")
            raise
    
    @property
    def client(self) -> redis.Redis:
        """Get Redis client instance."""
        if self._client is None:
            self._initialize_connection()
        return self._client
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value (deserialized) or None if not found
        """
        if not redis_settings.enable_cache:
            return None
        
        try:
            value = self.client.get(key)
            if value is None:
                return None
            
            # Deserialize JSON
            return json.loads(value.decode('utf-8'))
            
        except redis.RedisError as e:
            logger.error(f"Redis GET error for key '{key}': {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error for key '{key}': {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting key '{key}': {e}")
            return None
    
    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[Union[int, timedelta]] = None
    ) -> bool:
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache (will be JSON serialized)
            ttl: Time-to-live in seconds or timedelta
            
        Returns:
            True if successful, False otherwise
        """
        if not redis_settings.enable_cache:
            return False
        
        try:
            # Serialize to JSON
            serialized_value = json.dumps(value, default=str)
            
            # Convert timedelta to seconds
            if isinstance(ttl, timedelta):
                ttl = int(ttl.total_seconds())
            
            # Use default TTL if not specified
            if ttl is None:
                ttl = redis_settings.default_ttl
            
            # Cap at max TTL
            ttl = min(ttl, redis_settings.max_ttl)
            
            # Set with expiration
            result = self.client.setex(
                name=key,
                time=ttl,
                value=serialized_value
            )
            
            return bool(result)
            
        except redis.RedisError as e:
            logger.error(f"Redis SET error for key '{key}': {e}")
            return False
        except (TypeError, ValueError) as e:
            logger.error(f"Serialization error for key '{key}': {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error setting key '{key}': {e}")
            return False
    
    def delete(self, *keys: str) -> int:
        """
        Delete one or more keys.
        
        Args:
            keys: One or more cache keys to delete
            
        Returns:
            Number of keys deleted
        """
        if not redis_settings.enable_cache or not keys:
            return 0
        
        try:
            return self.client.delete(*keys)
        except redis.RedisError as e:
            logger.error(f"Redis DELETE error: {e}")
            return 0
        except Exception as e:
            logger.error(f"Unexpected error deleting keys: {e}")
            return 0
    
    def exists(self, *keys: str) -> int:
        """
        Check if one or more keys exist.
        
        Args:
            keys: One or more cache keys to check
            
        Returns:
            Number of existing keys
        """
        if not redis_settings.enable_cache or not keys:
            return 0
        
        try:
            return self.client.exists(*keys)
        except redis.RedisError as e:
            logger.error(f"Redis EXISTS error: {e}")
            return 0
        except Exception as e:
            logger.error(f"Unexpected error checking keys: {e}")
            return 0
    
    def clear_pattern(self, pattern: str) -> int:
        """
        Clear all keys matching a pattern.
        
        Args:
            pattern: Redis key pattern (e.g., "f1:cache:session:*")
            
        Returns:
            Number of keys deleted
        """
        if not redis_settings.enable_cache:
            return 0
        
        try:
            keys = self.client.keys(pattern)
            if keys:
                return self.client.delete(*keys)
            return 0
        except redis.RedisError as e:
            logger.error(f"Redis CLEAR pattern error: {e}")
            return 0
        except Exception as e:
            logger.error(f"Unexpected error clearing pattern '{pattern}': {e}")
            return 0
    
    def flush_all(self) -> bool:
        """
        Flush all keys from the database.
        
        WARNING: This deletes ALL cached data.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            result = self.client.flushdb()
            logger.warning("All cache keys flushed")
            return bool(result)
        except redis.RedisError as e:
            logger.error(f"Redis FLUSH error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error flushing cache: {e}")
            return False
    
    def get_info(self) -> dict:
        """
        Get Redis server information.
        
        Returns:
            Dictionary with server info
        """
        try:
            return self.client.info()
        except redis.RedisError as e:
            logger.error(f"Redis INFO error: {e}")
            return {}
        except Exception as e:
            logger.error(f"Unexpected error getting info: {e}")
            return {}
    
    def get_stats(self) -> dict:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache stats
        """
        try:
            info = self.get_info()
            return {
                "connected": info.get("redis_version") is not None,
                "version": info.get("redis_version", "unknown"),
                "uptime_seconds": info.get("uptime_in_seconds", 0),
                "total_keys": self.client.dbsize(),
                "used_memory": info.get("used_memory_human", "0"),
                "hit_rate": self._calculate_hit_rate(info),
                "pool_size": redis_settings.max_connections,
            }
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {
                "connected": False,
                "error": str(e)
            }
    
    def _calculate_hit_rate(self, info: dict) -> float:
        """Calculate cache hit rate percentage."""
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total = hits + misses
        
        if total == 0:
            return 0.0
        
        return round((hits / total) * 100, 2)
    
    def close(self) -> None:
        """Close Redis connection pool."""
        if self._pool:
            self._pool.disconnect()
            logger.info("Redis connection pool closed")


# Global singleton instance
_redis_client: Optional[RedisClient] = None


def get_redis_client() -> RedisClient:
    """
    Get the global Redis client instance.
    
    Returns:
        RedisClient singleton instance
    """
    global _redis_client
    
    if _redis_client is None:
        _redis_client = RedisClient()
    
    return _redis_client
