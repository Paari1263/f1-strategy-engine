"""
FastF1 API Client
Handles all F1 data requests using FastF1 library with caching and error handling
"""
import fastf1
import logging
from typing import Any, Dict, Optional
from pathlib import Path
import pandas as pd
from datetime import datetime

from cache import get_cache_manager, CacheKeys, calculate_dynamic_ttl

logger = logging.getLogger(__name__)


class FastF1Client:
    """Client for accessing Formula 1 data via FastF1 library"""
    
    def __init__(self, cache_dir: str = "cache/fastf1"):
        """
        Initialize FastF1 client with caching
        
        Args:
            cache_dir: Directory for FastF1 cache storage
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Enable FastF1 caching for faster subsequent loads
        fastf1.Cache.enable_cache(str(self.cache_dir))
        logger.info(f"FastF1 cache enabled at: {self.cache_dir}")
        
        # Initialize Redis cache manager
        self.cache_manager = get_cache_manager()
        self.cache_keys = CacheKeys()
        logger.info("Redis cache manager initialized for FastF1 client")
    
    def get_session(self, year: int, gp: str, session_type: str, use_cache: bool = False):
        """
        Load a FastF1 session with Redis caching
        
        Args:
            year: Season year (e.g., 2024)
            gp: Grand Prix name or round number (e.g., 'Bahrain' or 1)
            session_type: Session identifier ('FP1', 'FP2', 'FP3', 'Q', 'SQ', 'R', 'S')
            use_cache: Whether to use Redis cache (default: False - session objects don't serialize well)
        
        Returns:
            FastF1 Session object with loaded data
            
        Raises:
            ValueError: If session parameters are invalid
            Exception: If session data cannot be loaded
        """
        # Generate cache key
        cache_key = self.cache_keys.session_data(year, str(gp), session_type)
        
        # NOTE: Session object caching is disabled by default because FastF1 session
        # objects are complex and don't serialize well to JSON. Individual data
        # (laps, telemetry) can still be cached separately.
        if use_cache:
            # Try to get from cache first
            cached_session = self.cache_manager.get_session_data(year, str(gp), session_type)
            if cached_session is not None:
                logger.info(f"Cache hit for session: {year} {gp} {session_type}")
                return cached_session
        
        try:
            logger.info(f"Loading FastF1 session from source: {year} {gp} {session_type}")
            
            session = fastf1.get_session(year, gp, session_type)
            session.load()
            
            logger.info(
                f"Session loaded successfully",
                extra={
                    "event": session.event['EventName'],
                    "session": session_type,
                    "laps_count": len(session.laps) if hasattr(session, 'laps') else 0
                }
            )
            
            # NOTE: Don't cache full session object - it doesn't serialize well.
            # Individual data like laps, telemetry can be cached separately
            # if use_cache:
            #     session_start = session.session_info.get('SessionStartDate')
            #     if isinstance(session_start, str):
            #         try:
            #             session_start = datetime.fromisoformat(session_start)
            #         except:
            #             session_start = None
            #     
            #     self.cache_manager.cache_session_data(
            #         year=year,
            #         event=str(gp),
            #         session_type=session_type,
            #         data=session,
            #         session_start=session_start
            #     )
            
            return session
            
        except Exception as e:
            logger.error(f"Failed to load FastF1 session: {e}")
            raise
    
    def get_schedule(self, year: int, use_cache: bool = True) -> pd.DataFrame:
        """
        Get F1 calendar for a specific year with Redis caching
        
        Args:
            year: Season year
            use_cache: Whether to use Redis cache (default: True)
            
        Returns:
            DataFrame with event schedule
        """
        cache_key = self.cache_keys.season_schedule(year)
        
        if use_cache:
            cached_schedule = self.cache_manager.get_reference_data("schedule", str(year))
            if cached_schedule is not None:
                logger.info(f"Cache hit for schedule: {year}")
                return pd.DataFrame(cached_schedule)
        
        try:
            logger.info(f"Fetching F1 schedule from source: {year}")
            schedule = fastf1.get_event_schedule(year)
            
            # Cache the schedule (reference data - 7 days TTL)
            if use_cache:
                self.cache_manager.cache_reference_data(
                    data_type="schedule",
                    data=schedule.to_dict('records'),
                    identifier=str(year)
                )
            
            return schedule
        except Exception as e:
            logger.error(f"Failed to fetch schedule: {e}")
            raise
    
    def get_event(self, year: int, gp: str) -> Dict[str, Any]:
        """
        Get event information for a specific Grand Prix
        
        Args:
            year: Season year
            gp: Grand Prix name or round number
            
        Returns:
            Dictionary with event details
        """
        try:
            event = fastf1.get_event(year, gp)
            return event.to_dict()
        except Exception as e:
            logger.error(f"Failed to fetch event: {e}")
            raise
    
    def get_driver_laps(self, year: int, gp: str, session_type: str, driver: str, use_cache: bool = True) -> pd.DataFrame:
        """
        Get lap data for a specific driver with Redis caching
        
        Args:
            year: Season year
            gp: Grand Prix name or round number
            session_type: Session identifier ('FP1', 'FP2', 'FP3', 'Q', 'SQ', 'R', 'S')
            driver: Driver abbreviation (e.g., 'VER', 'HAM')
            use_cache: Whether to use Redis cache (default: True)
            
        Returns:
            DataFrame with lap data for the specified driver
        """
        if use_cache:
            cached_laps = self.cache_manager.get_session_laps(year, str(gp), session_type, driver)
            if cached_laps is not None:
                logger.info(f"Cache hit for driver laps: {year} {gp} {session_type} {driver}")
                return pd.DataFrame(cached_laps)
        
        try:
            session = self.get_session(year, gp, session_type, use_cache=use_cache)
            driver_laps = session.laps[session.laps['Driver'] == driver]
            
            # Cache the driver laps
            if use_cache:
                session_start = session.session_info.get('SessionStartDate')
                if isinstance(session_start, str):
                    try:
                        session_start = datetime.fromisoformat(session_start)
                    except:
                        session_start = None
                
                self.cache_manager.cache_session_laps(
                    year=year,
                    event=str(gp),
                    session_type=session_type,
                    laps_data=driver_laps.to_dict('records'),
                    driver=driver,
                    session_start=session_start
                )
            
            return driver_laps
        except Exception as e:
            logger.error(f"Failed to get driver laps: {e}")
            raise


# Global client instance
_client: Optional[FastF1Client] = None


def get_client() -> FastF1Client:
    """Get or create the global FastF1 client instance"""
    global _client
    if _client is None:
        _client = FastF1Client()
    return _client


def get_session(year: int, gp: str, session_type: str):
    """
    Convenience function to get a session
    
    Args:
        year: Season year
        gp: Grand Prix name or round
        session_type: Session type ('FP1', 'FP2', 'FP3', 'Q', 'SQ', 'R', 'S')
    
    Returns:
        Loaded FastF1 session
    """
    client = get_client()
    return client.get_session(year, gp, session_type)


def get_schedule(year: int) -> pd.DataFrame:
    """
    Convenience function to get F1 schedule
    
    Args:
        year: Season year
        
    Returns:
        Schedule DataFrame
    """
    client = get_client()
    return client.get_schedule(year)
