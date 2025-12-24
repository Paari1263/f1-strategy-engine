"""
Cache Key Generator Module

Provides utilities for generating hierarchical cache keys with consistent patterns.
"""

import hashlib
import json
from typing import Any, Dict, Optional

from config.redis_config import redis_settings


class CacheKeys:
    """
    Cache key generator with hierarchical patterns.
    
    Key Format: {prefix}:{layer}:{resource}:{parameters_hash}
    Example: f1:cache:session:2024:monaco:qualifying:abc123
    """
    
    # Cache layers
    LAYER_SESSION = "session"      # L1: FastF1 session data
    LAYER_COMPUTED = "computed"    # L2: Computed metrics
    LAYER_API = "api"              # L3: API responses
    LAYER_REFERENCE = "reference"  # L4: Reference data
    
    @staticmethod
    def _hash_params(params: Dict[str, Any]) -> str:
        """
        Create a consistent hash from parameters.
        
        Args:
            params: Dictionary of parameters
            
        Returns:
            MD5 hash of sorted parameters
        """
        # Sort keys for consistency
        sorted_params = json.dumps(params, sort_keys=True, default=str)
        return hashlib.md5(sorted_params.encode()).hexdigest()[:12]
    
    @staticmethod
    def _build_key(*parts: str) -> str:
        """
        Build a cache key from parts.
        
        Args:
            parts: Key components
            
        Returns:
            Formatted cache key
        """
        # Filter out None/empty parts
        valid_parts = [str(p) for p in parts if p]
        return ":".join([redis_settings.key_prefix] + valid_parts)
    
    # ========================================================================
    # L1: Session Data Keys
    # ========================================================================
    
    @classmethod
    def session_data(
        cls,
        year: int,
        event: str,
        session_type: str
    ) -> str:
        """
        Generate key for FastF1 session data.
        
        Args:
            year: Season year
            event: Event name (e.g., "Monaco")
            session_type: Session type (e.g., "Qualifying")
            
        Returns:
            Cache key for session data
        """
        return cls._build_key(
            cls.LAYER_SESSION,
            str(year),
            event.lower().replace(" ", "-"),
            session_type.lower()
        )
    
    @classmethod
    def session_laps(
        cls,
        year: int,
        event: str,
        session_type: str,
        driver: Optional[str] = None
    ) -> str:
        """
        Generate key for session laps data.
        
        Args:
            year: Season year
            event: Event name
            session_type: Session type
            driver: Driver code (optional)
            
        Returns:
            Cache key for laps data
        """
        parts = [
            cls.LAYER_SESSION,
            str(year),
            event.lower().replace(" ", "-"),
            session_type.lower(),
            "laps"
        ]
        
        if driver:
            parts.append(driver.upper())
        
        return cls._build_key(*parts)
    
    @classmethod
    def session_telemetry(
        cls,
        year: int,
        event: str,
        session_type: str,
        driver: str,
        lap: int
    ) -> str:
        """
        Generate key for lap telemetry data.
        
        Args:
            year: Season year
            event: Event name
            session_type: Session type
            driver: Driver code
            lap: Lap number
            
        Returns:
            Cache key for telemetry data
        """
        return cls._build_key(
            cls.LAYER_SESSION,
            str(year),
            event.lower().replace(" ", "-"),
            session_type.lower(),
            "telemetry",
            driver.upper(),
            f"lap-{lap}"
        )
    
    # ========================================================================
    # L2: Computed Metrics Keys
    # ========================================================================
    
    @classmethod
    def computed_metric(
        cls,
        metric_type: str,
        year: int,
        event: str,
        **kwargs
    ) -> str:
        """
        Generate key for computed metrics.
        
        Args:
            metric_type: Type of metric (e.g., "lap-comparison", "sector-analysis")
            year: Season year
            event: Event name
            **kwargs: Additional parameters
            
        Returns:
            Cache key for computed metric
        """
        param_hash = cls._hash_params(kwargs) if kwargs else "all"
        
        return cls._build_key(
            cls.LAYER_COMPUTED,
            metric_type.lower(),
            str(year),
            event.lower().replace(" ", "-"),
            param_hash
        )
    
    @classmethod
    def driver_comparison(
        cls,
        year: int,
        event: str,
        session_type: str,
        drivers: list[str]
    ) -> str:
        """
        Generate key for driver comparison data.
        
        Args:
            year: Season year
            event: Event name
            session_type: Session type
            drivers: List of driver codes
            
        Returns:
            Cache key for driver comparison
        """
        # Sort drivers for consistency
        sorted_drivers = "-".join(sorted([d.upper() for d in drivers]))
        
        return cls._build_key(
            cls.LAYER_COMPUTED,
            "driver-comparison",
            str(year),
            event.lower().replace(" ", "-"),
            session_type.lower(),
            sorted_drivers
        )
    
    @classmethod
    def strategy_analysis(
        cls,
        year: int,
        event: str,
        driver: Optional[str] = None
    ) -> str:
        """
        Generate key for strategy analysis data.
        
        Args:
            year: Season year
            event: Event name
            driver: Driver code (optional)
            
        Returns:
            Cache key for strategy analysis
        """
        parts = [
            cls.LAYER_COMPUTED,
            "strategy",
            str(year),
            event.lower().replace(" ", "-")
        ]
        
        if driver:
            parts.append(driver.upper())
        
        return cls._build_key(*parts)
    
    # ========================================================================
    # L3: API Response Keys
    # ========================================================================
    
    @classmethod
    def api_response(
        cls,
        endpoint: str,
        **params
    ) -> str:
        """
        Generate key for API response.
        
        Args:
            endpoint: API endpoint path
            **params: Request parameters
            
        Returns:
            Cache key for API response
        """
        # Clean endpoint (remove leading slash, replace slashes with dashes)
        clean_endpoint = endpoint.lstrip("/").replace("/", "-")
        param_hash = cls._hash_params(params) if params else "no-params"
        
        return cls._build_key(
            cls.LAYER_API,
            clean_endpoint,
            param_hash
        )
    
    # ========================================================================
    # L4: Reference Data Keys
    # ========================================================================
    
    @classmethod
    def reference_data(
        cls,
        data_type: str,
        identifier: Optional[str] = None
    ) -> str:
        """
        Generate key for reference data.
        
        Args:
            data_type: Type of reference data (e.g., "schedule", "drivers", "teams")
            identifier: Optional identifier (e.g., year for schedule)
            
        Returns:
            Cache key for reference data
        """
        parts = [cls.LAYER_REFERENCE, data_type.lower()]
        
        if identifier:
            parts.append(str(identifier))
        
        return cls._build_key(*parts)
    
    @classmethod
    def season_schedule(cls, year: int) -> str:
        """Generate key for season schedule."""
        return cls.reference_data("schedule", str(year))
    
    @classmethod
    def driver_info(cls, driver: Optional[str] = None) -> str:
        """Generate key for driver information."""
        return cls.reference_data("drivers", driver.upper() if driver else None)
    
    @classmethod
    def team_info(cls, team: Optional[str] = None) -> str:
        """Generate key for team information."""
        return cls.reference_data("teams", team.upper() if team else None)
    
    @classmethod
    def circuit_info(cls, circuit: Optional[str] = None) -> str:
        """Generate key for circuit information."""
        return cls.reference_data("circuits", circuit.lower() if circuit else None)
    
    # ========================================================================
    # Utility Methods
    # ========================================================================
    
    @classmethod
    def pattern_for_session(
        cls,
        year: Optional[int] = None,
        event: Optional[str] = None
    ) -> str:
        """
        Generate a pattern to match session keys.
        
        Args:
            year: Season year (optional)
            event: Event name (optional)
            
        Returns:
            Redis key pattern
        """
        parts = [redis_settings.key_prefix, cls.LAYER_SESSION]
        
        if year:
            parts.append(str(year))
            if event:
                parts.append(event.lower().replace(" ", "-"))
                parts.append("*")
            else:
                parts.append("*")
        else:
            parts.append("*")
        
        return ":".join(parts)
    
    @classmethod
    def pattern_for_layer(cls, layer: str) -> str:
        """
        Generate a pattern to match all keys in a layer.
        
        Args:
            layer: Cache layer (session, computed, api, reference)
            
        Returns:
            Redis key pattern
        """
        return f"{redis_settings.key_prefix}:{layer}:*"
    
    @classmethod
    def pattern_all(cls) -> str:
        """Generate a pattern to match all cache keys."""
        return f"{redis_settings.key_prefix}:*"
