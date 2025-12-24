"""
Cache Manager Module

Provides high-level cache operations for managing FastF1 data and API responses.
"""

import logging
from typing import Any, Callable, Optional, Dict, List
from datetime import datetime

from .redis_client import get_redis_client, RedisClient
from .cache_keys import CacheKeys
from .ttl_strategy import calculate_dynamic_ttl

logger = logging.getLogger(__name__)


class CacheManager:
    """
    High-level cache manager for F1 data.
    
    Provides convenient methods for caching, retrieval, and invalidation
    with automatic key generation and TTL calculation.
    """
    
    def __init__(self):
        """Initialize cache manager with Redis client."""
        self.client: RedisClient = get_redis_client()
        self.keys = CacheKeys()
    
    # ========================================================================
    # Core Cache Operations
    # ========================================================================
    
    def get_or_fetch(
        self,
        key: str,
        fetch_fn: Callable[[], Any],
        ttl: Optional[int] = None,
        force_refresh: bool = False
    ) -> Any:
        """
        Get data from cache or fetch if not available.
        
        This is the primary method for cache-aside pattern implementation.
        
        Args:
            key: Cache key
            fetch_fn: Function to call if cache miss (should return the data)
            ttl: Time-to-live in seconds (optional)
            force_refresh: Force refresh even if cached (default: False)
            
        Returns:
            Cached or freshly fetched data
            
        Example:
            >>> def fetch_session():
            ...     return fastf1.get_session(2024, "Monaco", "Q")
            >>> 
            >>> session = manager.get_or_fetch(
            ...     key="f1:cache:session:2024:monaco:q",
            ...     fetch_fn=fetch_session,
            ...     ttl=3600
            ... )
        """
        # Force refresh bypasses cache
        if force_refresh:
            logger.info(f"Force refresh: fetching fresh data for key '{key}'")
            data = fetch_fn()
            self.client.set(key, data, ttl)
            return data
        
        # Try to get from cache
        cached_data = self.client.get(key)
        
        if cached_data is not None:
            logger.debug(f"Cache hit for key '{key}'")
            return cached_data
        
        # Cache miss - fetch fresh data
        logger.info(f"Cache miss for key '{key}' - fetching fresh data")
        
        try:
            data = fetch_fn()
            
            # Store in cache
            if data is not None:
                self.client.set(key, data, ttl)
                logger.debug(f"Cached data for key '{key}' with TTL {ttl}s")
            
            return data
            
        except Exception as e:
            logger.error(f"Error fetching data for key '{key}': {e}")
            raise
    
    async def get_or_fetch_async(
        self,
        key: str,
        fetch_fn: Callable,
        ttl: Optional[int] = None,
        force_refresh: bool = False
    ) -> Any:
        """
        Async version of get_or_fetch.
        
        Args:
            key: Cache key
            fetch_fn: Async function to call if cache miss
            ttl: Time-to-live in seconds (optional)
            force_refresh: Force refresh even if cached
            
        Returns:
            Cached or freshly fetched data
        """
        if force_refresh:
            logger.info(f"Force refresh: fetching fresh data for key '{key}'")
            data = await fetch_fn()
            self.client.set(key, data, ttl)
            return data
        
        cached_data = self.client.get(key)
        
        if cached_data is not None:
            logger.debug(f"Cache hit for key '{key}'")
            return cached_data
        
        logger.info(f"Cache miss for key '{key}' - fetching fresh data")
        
        try:
            data = await fetch_fn()
            
            if data is not None:
                self.client.set(key, data, ttl)
                logger.debug(f"Cached data for key '{key}' with TTL {ttl}s")
            
            return data
            
        except Exception as e:
            logger.error(f"Error fetching data for key '{key}': {e}")
            raise
    
    # ========================================================================
    # Session Data Caching
    # ========================================================================
    
    def cache_session_data(
        self,
        year: int,
        event: str,
        session_type: str,
        data: Any,
        session_start: Optional[datetime] = None
    ) -> bool:
        """
        Cache FastF1 session data with dynamic TTL.
        
        Args:
            year: Season year
            event: Event name
            session_type: Session type
            data: Session data to cache
            session_start: Session start time (for dynamic TTL)
            
        Returns:
            True if successful, False otherwise
        """
        key = self.keys.session_data(year, event, session_type)
        ttl = calculate_dynamic_ttl('session', session_start)
        
        success = self.client.set(key, data, ttl)
        
        if success:
            logger.info(
                f"Cached session data: {year} {event} {session_type} (TTL: {ttl}s)"
            )
        
        return success
    
    def get_session_data(
        self,
        year: int,
        event: str,
        session_type: str
    ) -> Optional[Any]:
        """
        Get cached session data.
        
        Args:
            year: Season year
            event: Event name
            session_type: Session type
            
        Returns:
            Cached session data or None
        """
        key = self.keys.session_data(year, event, session_type)
        return self.client.get(key)
    
    def cache_session_laps(
        self,
        year: int,
        event: str,
        session_type: str,
        laps_data: Any,
        driver: Optional[str] = None,
        session_start: Optional[datetime] = None
    ) -> bool:
        """
        Cache session laps data.
        
        Args:
            year: Season year
            event: Event name
            session_type: Session type
            laps_data: Laps data to cache
            driver: Driver code (optional)
            session_start: Session start time (for dynamic TTL)
            
        Returns:
            True if successful
        """
        key = self.keys.session_laps(year, event, session_type, driver)
        ttl = calculate_dynamic_ttl('session', session_start)
        
        return self.client.set(key, laps_data, ttl)
    
    def get_session_laps(
        self,
        year: int,
        event: str,
        session_type: str,
        driver: Optional[str] = None
    ) -> Optional[Any]:
        """Get cached session laps data."""
        key = self.keys.session_laps(year, event, session_type, driver)
        return self.client.get(key)
    
    # ========================================================================
    # Computed Metrics Caching
    # ========================================================================
    
    def cache_computed_metric(
        self,
        metric_type: str,
        year: int,
        event: str,
        data: Any,
        session_start: Optional[datetime] = None,
        **kwargs
    ) -> bool:
        """
        Cache computed metric data.
        
        Args:
            metric_type: Type of metric
            year: Season year
            event: Event name
            data: Computed data to cache
            session_start: Session start time (for dynamic TTL)
            **kwargs: Additional parameters for key generation
            
        Returns:
            True if successful
        """
        key = self.keys.computed_metric(metric_type, year, event, **kwargs)
        ttl = calculate_dynamic_ttl('computed', session_start)
        
        return self.client.set(key, data, ttl)
    
    def get_computed_metric(
        self,
        metric_type: str,
        year: int,
        event: str,
        **kwargs
    ) -> Optional[Any]:
        """Get cached computed metric."""
        key = self.keys.computed_metric(metric_type, year, event, **kwargs)
        return self.client.get(key)
    
    def cache_driver_comparison(
        self,
        year: int,
        event: str,
        session_type: str,
        drivers: List[str],
        comparison_data: Any,
        session_start: Optional[datetime] = None
    ) -> bool:
        """Cache driver comparison data."""
        key = self.keys.driver_comparison(year, event, session_type, drivers)
        ttl = calculate_dynamic_ttl('computed', session_start)
        
        return self.client.set(key, comparison_data, ttl)
    
    def get_driver_comparison(
        self,
        year: int,
        event: str,
        session_type: str,
        drivers: List[str]
    ) -> Optional[Any]:
        """Get cached driver comparison data."""
        key = self.keys.driver_comparison(year, event, session_type, drivers)
        return self.client.get(key)
    
    # ========================================================================
    # API Response Caching
    # ========================================================================
    
    def cache_api_response(
        self,
        endpoint: str,
        response_data: Any,
        ttl: Optional[int] = None,
        **params
    ) -> bool:
        """
        Cache API response.
        
        Args:
            endpoint: API endpoint path
            response_data: Response data to cache
            ttl: Custom TTL (optional)
            **params: Request parameters
            
        Returns:
            True if successful
        """
        key = self.keys.api_response(endpoint, **params)
        
        if ttl is None:
            ttl = calculate_dynamic_ttl('api')
        
        return self.client.set(key, response_data, ttl)
    
    def get_api_response(
        self,
        endpoint: str,
        **params
    ) -> Optional[Any]:
        """Get cached API response."""
        key = self.keys.api_response(endpoint, **params)
        return self.client.get(key)
    
    # ========================================================================
    # Reference Data Caching
    # ========================================================================
    
    def cache_reference_data(
        self,
        data_type: str,
        data: Any,
        identifier: Optional[str] = None
    ) -> bool:
        """
        Cache reference data (drivers, teams, circuits, schedule).
        
        Args:
            data_type: Type of reference data
            data: Data to cache
            identifier: Optional identifier
            
        Returns:
            True if successful
        """
        key = self.keys.reference_data(data_type, identifier)
        ttl = calculate_dynamic_ttl('reference')
        
        return self.client.set(key, data, ttl)
    
    def get_reference_data(
        self,
        data_type: str,
        identifier: Optional[str] = None
    ) -> Optional[Any]:
        """Get cached reference data."""
        key = self.keys.reference_data(data_type, identifier)
        return self.client.get(key)
    
    # ========================================================================
    # Cache Invalidation
    # ========================================================================
    
    def invalidate_session(
        self,
        year: int,
        event: str,
        session_type: Optional[str] = None
    ) -> int:
        """
        Invalidate all cache entries for a session.
        
        This clears session data, laps, telemetry, and any computed metrics
        for the specified session.
        
        Args:
            year: Season year
            event: Event name
            session_type: Session type (optional - clears all sessions if not specified)
            
        Returns:
            Number of keys deleted
        """
        # Build pattern based on parameters
        if session_type:
            pattern = f"{self.keys._build_key(CacheKeys.LAYER_SESSION, str(year), event.lower().replace(' ', '-'), session_type.lower())}*"
        else:
            pattern = f"{self.keys._build_key(CacheKeys.LAYER_SESSION, str(year), event.lower().replace(' ', '-'))}*"
        
        count = self.client.clear_pattern(pattern)
        logger.info(f"Invalidated {count} session cache entries for {year} {event}")
        
        return count
    
    def invalidate_computed(
        self,
        year: Optional[int] = None,
        event: Optional[str] = None,
        metric_type: Optional[str] = None
    ) -> int:
        """
        Invalidate computed metrics.
        
        Args:
            year: Season year (optional)
            event: Event name (optional)
            metric_type: Metric type (optional)
            
        Returns:
            Number of keys deleted
        """
        # Build pattern
        parts = [CacheKeys.LAYER_COMPUTED]
        
        if metric_type:
            parts.append(metric_type.lower())
        if year:
            parts.append(str(year))
        if event:
            parts.append(event.lower().replace(' ', '-'))
        
        parts.append("*")
        pattern = self.keys._build_key(*parts)
        
        count = self.client.clear_pattern(pattern)
        logger.info(f"Invalidated {count} computed metric cache entries")
        
        return count
    
    def invalidate_api_responses(self, endpoint: Optional[str] = None) -> int:
        """
        Invalidate API response cache.
        
        Args:
            endpoint: Specific endpoint to invalidate (optional - clears all if not specified)
            
        Returns:
            Number of keys deleted
        """
        if endpoint:
            clean_endpoint = endpoint.lstrip("/").replace("/", "-")
            pattern = f"{self.keys._build_key(CacheKeys.LAYER_API, clean_endpoint)}*"
        else:
            pattern = self.keys.pattern_for_layer(CacheKeys.LAYER_API)
        
        count = self.client.clear_pattern(pattern)
        logger.info(f"Invalidated {count} API response cache entries")
        
        return count
    
    def invalidate_layer(self, layer: str) -> int:
        """
        Invalidate entire cache layer.
        
        Args:
            layer: Cache layer ('session', 'computed', 'api', 'reference')
            
        Returns:
            Number of keys deleted
        """
        pattern = self.keys.pattern_for_layer(layer)
        count = self.client.clear_pattern(pattern)
        
        logger.warning(f"Invalidated entire {layer} layer: {count} keys deleted")
        
        return count
    
    def invalidate_all(self) -> bool:
        """
        Invalidate ALL cache entries.
        
        WARNING: This clears the entire cache.
        
        Returns:
            True if successful
        """
        success = self.client.flush_all()
        
        if success:
            logger.warning("All cache entries invalidated")
        
        return success
    
    # ========================================================================
    # Cache Warming
    # ========================================================================
    
    def warm_cache(
        self,
        warm_functions: List[Dict[str, Any]]
    ) -> Dict[str, int]:
        """
        Pre-populate cache with frequently accessed data.
        
        Args:
            warm_functions: List of dictionaries with:
                - 'name': Function name
                - 'function': Callable to execute
                - 'key': Cache key
                - 'ttl': TTL in seconds
                
        Returns:
            Dictionary with warming statistics
            
        Example:
            >>> warming_tasks = [
            ...     {
            ...         'name': 'season_schedule',
            ...         'function': lambda: get_schedule(2024),
            ...         'key': cache_keys.season_schedule(2024),
            ...         'ttl': 604800
            ...     }
            ... ]
            >>> stats = manager.warm_cache(warming_tasks)
        """
        stats = {
            'total': len(warm_functions),
            'success': 0,
            'failed': 0,
            'errors': []
        }
        
        for task in warm_functions:
            try:
                name = task.get('name', 'unknown')
                fn = task['function']
                key = task['key']
                ttl = task.get('ttl')
                
                logger.info(f"Warming cache: {name}")
                
                # Execute function and cache result
                data = fn()
                success = self.client.set(key, data, ttl)
                
                if success:
                    stats['success'] += 1
                    logger.info(f"Successfully warmed: {name}")
                else:
                    stats['failed'] += 1
                    stats['errors'].append(f"Failed to cache: {name}")
                    
            except Exception as e:
                stats['failed'] += 1
                error_msg = f"Error warming {task.get('name', 'unknown')}: {str(e)}"
                stats['errors'].append(error_msg)
                logger.error(error_msg)
        
        logger.info(
            f"Cache warming complete: {stats['success']}/{stats['total']} successful"
        )
        
        return stats
    
    # ========================================================================
    # Cache Statistics
    # ========================================================================
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        base_stats = self.client.get_stats()
        
        # Count keys per layer
        layer_counts = {}
        for layer in [
            CacheKeys.LAYER_SESSION,
            CacheKeys.LAYER_COMPUTED,
            CacheKeys.LAYER_API,
            CacheKeys.LAYER_REFERENCE
        ]:
            pattern = self.keys.pattern_for_layer(layer)
            # Note: This uses KEYS which is O(N) - consider using SCAN in production
            keys = self.client.client.keys(pattern)
            layer_counts[layer] = len(keys) if keys else 0
        
        base_stats['layer_counts'] = layer_counts
        
        return base_stats


# Global cache manager instance
_cache_manager: Optional[CacheManager] = None


def get_cache_manager() -> CacheManager:
    """
    Get the global cache manager instance.
    
    Returns:
        CacheManager singleton instance
    """
    global _cache_manager
    
    if _cache_manager is None:
        _cache_manager = CacheManager()
    
    return _cache_manager
