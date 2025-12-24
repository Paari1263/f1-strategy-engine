"""
Cache Decorators Module

Provides decorators for automatic function result caching.
"""

import functools
import inspect
import logging
from typing import Any, Callable, Optional, Union
from datetime import datetime, timedelta

from .cache_manager import get_cache_manager
from .cache_keys import CacheKeys
from .ttl_strategy import calculate_dynamic_ttl

logger = logging.getLogger(__name__)


def cached(
    key_prefix: Optional[str] = None,
    ttl: Optional[Union[int, timedelta]] = None,
    layer: str = CacheKeys.LAYER_API,
    key_generator: Optional[Callable] = None,
    enabled: bool = True
):
    """
    Decorator to cache function results.
    
    Automatically caches function return values based on arguments.
    Supports both sync and async functions.
    
    Args:
        key_prefix: Prefix for cache key (default: function name)
        ttl: Time-to-live in seconds or timedelta (default: dynamic based on layer)
        layer: Cache layer ('session', 'computed', 'api', 'reference')
        key_generator: Custom function to generate cache key from args/kwargs
        enabled: Enable/disable caching (useful for testing)
        
    Example:
        >>> @cached(key_prefix="driver_stats", ttl=3600, layer="computed")
        ... def get_driver_statistics(year: int, driver: str):
        ...     # Expensive calculation
        ...     return calculate_stats(year, driver)
        
        >>> @cached(key_generator=lambda year, event: f"schedule:{year}:{event}")
        ... async def get_event_schedule(year: int, event: str):
        ...     return await fetch_schedule(year, event)
    """
    def decorator(func: Callable) -> Callable:
        # Determine if function is async
        is_async = inspect.iscoroutinefunction(func)
        
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            if not enabled:
                return await func(*args, **kwargs)
            
            # Generate cache key
            cache_key = _generate_cache_key(
                func, args, kwargs, key_prefix, layer, key_generator
            )
            
            # Calculate TTL
            cache_ttl = _calculate_ttl(ttl, layer)
            
            # Get cache manager
            manager = get_cache_manager()
            
            # Try to get from cache
            cached_result = manager.client.get(cache_key)
            
            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__}: {cache_key}")
                return cached_result
            
            # Cache miss - execute function
            logger.debug(f"Cache miss for {func.__name__}: {cache_key}")
            result = await func(*args, **kwargs)
            
            # Cache result
            if result is not None:
                manager.client.set(cache_key, result, cache_ttl)
                logger.debug(f"Cached result for {func.__name__} (TTL: {cache_ttl}s)")
            
            return result
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            if not enabled:
                return func(*args, **kwargs)
            
            # Generate cache key
            cache_key = _generate_cache_key(
                func, args, kwargs, key_prefix, layer, key_generator
            )
            
            # Calculate TTL
            cache_ttl = _calculate_ttl(ttl, layer)
            
            # Get cache manager
            manager = get_cache_manager()
            
            # Try to get from cache
            cached_result = manager.client.get(cache_key)
            
            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__}: {cache_key}")
                return cached_result
            
            # Cache miss - execute function
            logger.debug(f"Cache miss for {func.__name__}: {cache_key}")
            result = func(*args, **kwargs)
            
            # Cache result
            if result is not None:
                manager.client.set(cache_key, result, cache_ttl)
                logger.debug(f"Cached result for {func.__name__} (TTL: {cache_ttl}s)")
            
            return result
        
        return async_wrapper if is_async else sync_wrapper
    
    return decorator


def invalidate_cache(
    key_pattern: Optional[str] = None,
    layer: Optional[str] = None,
    condition: Optional[Callable] = None
):
    """
    Decorator to invalidate cache after function execution.
    
    Useful for functions that modify data and should clear related cache entries.
    
    Args:
        key_pattern: Redis key pattern to invalidate (e.g., "f1:cache:session:2024:*")
        layer: Cache layer to invalidate entirely
        condition: Optional function that receives the result and returns bool
                  (only invalidate if condition returns True)
        
    Example:
        >>> @invalidate_cache(key_pattern="f1:cache:session:2024:monaco:*")
        ... def update_session_data(year: int, event: str):
        ...     # Update data
        ...     return updated_data
        
        >>> @invalidate_cache(layer="computed", condition=lambda r: r.get('success'))
        ... async def recalculate_metrics():
        ...     result = await perform_calculation()
        ...     return result
    """
    def decorator(func: Callable) -> Callable:
        is_async = inspect.iscoroutinefunction(func)
        
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Execute function first
            result = await func(*args, **kwargs)
            
            # Check condition if provided
            if condition and not condition(result):
                logger.debug(f"Skipping cache invalidation for {func.__name__} (condition not met)")
                return result
            
            # Invalidate cache
            _perform_invalidation(key_pattern, layer, func.__name__)
            
            return result
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Execute function first
            result = func(*args, **kwargs)
            
            # Check condition if provided
            if condition and not condition(result):
                logger.debug(f"Skipping cache invalidation for {func.__name__} (condition not met)")
                return result
            
            # Invalidate cache
            _perform_invalidation(key_pattern, layer, func.__name__)
            
            return result
        
        return async_wrapper if is_async else sync_wrapper
    
    return decorator


def cache_aside(
    key_generator: Callable,
    ttl: Optional[Union[int, timedelta]] = None,
    layer: str = CacheKeys.LAYER_API
):
    """
    Decorator implementing cache-aside pattern with custom key generation.
    
    This is more flexible than @cached as it allows complete control over
    the cache key based on function arguments.
    
    Args:
        key_generator: Function that takes (*args, **kwargs) and returns cache key
        ttl: Time-to-live in seconds or timedelta
        layer: Cache layer
        
    Example:
        >>> def generate_lap_key(year, event, session_type, driver, lap):
        ...     return CacheKeys().session_telemetry(year, event, session_type, driver, lap)
        
        >>> @cache_aside(key_generator=generate_lap_key, ttl=86400)
        ... def get_lap_telemetry(year, event, session_type, driver, lap):
        ...     return fetch_telemetry(year, event, session_type, driver, lap)
    """
    def decorator(func: Callable) -> Callable:
        is_async = inspect.iscoroutinefunction(func)
        
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Generate cache key using custom generator
            cache_key = key_generator(*args, **kwargs)
            cache_ttl = _calculate_ttl(ttl, layer)
            
            manager = get_cache_manager()
            
            # Use get_or_fetch for cache-aside pattern
            result = await manager.get_or_fetch_async(
                key=cache_key,
                fetch_fn=lambda: func(*args, **kwargs),
                ttl=cache_ttl
            )
            
            return result
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Generate cache key using custom generator
            cache_key = key_generator(*args, **kwargs)
            cache_ttl = _calculate_ttl(ttl, layer)
            
            manager = get_cache_manager()
            
            # Use get_or_fetch for cache-aside pattern
            result = manager.get_or_fetch(
                key=cache_key,
                fetch_fn=lambda: func(*args, **kwargs),
                ttl=cache_ttl
            )
            
            return result
        
        return async_wrapper if is_async else sync_wrapper
    
    return decorator


def conditional_cache(
    condition: Callable[[Any], bool],
    key_prefix: Optional[str] = None,
    ttl: Optional[Union[int, timedelta]] = None,
    layer: str = CacheKeys.LAYER_API
):
    """
    Decorator to conditionally cache results based on return value.
    
    Only caches if the condition function returns True for the result.
    Useful for caching only successful responses or valid data.
    
    Args:
        condition: Function that receives the result and returns bool
        key_prefix: Prefix for cache key
        ttl: Time-to-live
        layer: Cache layer
        
    Example:
        >>> @conditional_cache(
        ...     condition=lambda r: r is not None and r.get('laps') > 0,
        ...     ttl=3600
        ... )
        ... def get_session_laps(year, event):
        ...     laps = fetch_laps(year, event)
        ...     return laps
    """
    def decorator(func: Callable) -> Callable:
        is_async = inspect.iscoroutinefunction(func)
        
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            cache_key = _generate_cache_key(func, args, kwargs, key_prefix, layer, None)
            cache_ttl = _calculate_ttl(ttl, layer)
            
            manager = get_cache_manager()
            
            # Check cache first
            cached_result = manager.client.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_result
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Only cache if condition is met
            if condition(result):
                manager.client.set(cache_key, result, cache_ttl)
                logger.debug(f"Conditionally cached result for {func.__name__}")
            else:
                logger.debug(f"Condition not met, skipping cache for {func.__name__}")
            
            return result
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            cache_key = _generate_cache_key(func, args, kwargs, key_prefix, layer, None)
            cache_ttl = _calculate_ttl(ttl, layer)
            
            manager = get_cache_manager()
            
            # Check cache first
            cached_result = manager.client.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_result
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Only cache if condition is met
            if condition(result):
                manager.client.set(cache_key, result, cache_ttl)
                logger.debug(f"Conditionally cached result for {func.__name__}")
            else:
                logger.debug(f"Condition not met, skipping cache for {func.__name__}")
            
            return result
        
        return async_wrapper if is_async else sync_wrapper
    
    return decorator


# ============================================================================
# Helper Functions
# ============================================================================

def _generate_cache_key(
    func: Callable,
    args: tuple,
    kwargs: dict,
    key_prefix: Optional[str],
    layer: str,
    key_generator: Optional[Callable]
) -> str:
    """Generate cache key from function and arguments."""
    if key_generator:
        # Use custom key generator
        return key_generator(*args, **kwargs)
    
    # Default key generation
    prefix = key_prefix or func.__name__
    
    # Build key from arguments
    keys = CacheKeys()
    
    # Convert args and kwargs to dict for hashing
    sig = inspect.signature(func)
    bound_args = sig.bind(*args, **kwargs)
    bound_args.apply_defaults()
    
    params = dict(bound_args.arguments)
    
    # Use cache key utilities
    return keys._build_key(layer, prefix, keys._hash_params(params))


def _calculate_ttl(
    ttl: Optional[Union[int, timedelta]],
    layer: str
) -> int:
    """Calculate TTL in seconds."""
    if ttl is None:
        # Use dynamic TTL based on layer
        return calculate_dynamic_ttl(layer)
    
    if isinstance(ttl, timedelta):
        return int(ttl.total_seconds())
    
    return ttl


def _perform_invalidation(
    key_pattern: Optional[str],
    layer: Optional[str],
    func_name: str
) -> None:
    """Perform cache invalidation."""
    manager = get_cache_manager()
    
    if key_pattern:
        count = manager.client.clear_pattern(key_pattern)
        logger.info(f"Invalidated {count} keys matching pattern '{key_pattern}' after {func_name}")
    
    elif layer:
        count = manager.invalidate_layer(layer)
        logger.info(f"Invalidated {count} keys in layer '{layer}' after {func_name}")
    
    else:
        logger.warning(f"No invalidation pattern or layer specified for {func_name}")
