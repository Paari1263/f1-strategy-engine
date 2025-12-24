"""
TTL Strategy Module

Provides dynamic TTL (Time-To-Live) calculation based on session timing and data type.
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

from config.redis_config import redis_settings


class SessionStatus(str, Enum):
    """Session status enumeration."""
    FUTURE = "future"          # Session hasn't started yet
    LIVE = "live"              # Session is currently happening
    RECENTLY_COMPLETED = "recently_completed"  # Completed < 2 hours ago
    COMPLETED = "completed"    # Completed 2-48 hours ago
    HISTORICAL = "historical"  # Completed > 48 hours ago


class TTLStrategy:
    """
    Dynamic TTL calculation based on session timing.
    
    TTL Ranges:
    - Future sessions: 1 hour (subject to schedule changes)
    - Live sessions: 5 minutes (frequently updating)
    - Recently completed: 6 hours (may have corrections)
    - Completed sessions: 24 hours (stable data)
    - Historical data: 7 days (permanent reference)
    """
    
    # TTL constants (in seconds)
    TTL_FUTURE = 3600              # 1 hour
    TTL_LIVE = 300                 # 5 minutes
    TTL_RECENT = 21600             # 6 hours
    TTL_COMPLETED = 86400          # 24 hours
    TTL_HISTORICAL = 604800        # 7 days
    TTL_REFERENCE = 604800         # 7 days (same as historical)
    TTL_API_RESPONSE = 3600        # 1 hour (default for API responses)
    
    @staticmethod
    def determine_session_status(
        session_start: datetime,
        session_end: Optional[datetime] = None
    ) -> SessionStatus:
        """
        Determine session status based on timing.
        
        Args:
            session_start: Session start datetime
            session_end: Session end datetime (optional, estimated if not provided)
            
        Returns:
            SessionStatus enum value
        """
        now = datetime.now(session_start.tzinfo or None)
        
        # Estimate session end if not provided (assume 2-hour session)
        if session_end is None:
            session_end = session_start + timedelta(hours=2)
        
        # Future session
        if now < session_start:
            return SessionStatus.FUTURE
        
        # Live session
        if session_start <= now <= session_end:
            return SessionStatus.LIVE
        
        # Calculate time since session end
        time_since_end = now - session_end
        
        # Recently completed (< 2 hours)
        if time_since_end < timedelta(hours=2):
            return SessionStatus.RECENTLY_COMPLETED
        
        # Completed (2-48 hours)
        if time_since_end < timedelta(hours=48):
            return SessionStatus.COMPLETED
        
        # Historical (> 48 hours)
        return SessionStatus.HISTORICAL
    
    @classmethod
    def get_ttl_for_session(
        cls,
        session_start: datetime,
        session_end: Optional[datetime] = None
    ) -> int:
        """
        Get TTL for session data based on timing.
        
        Args:
            session_start: Session start datetime
            session_end: Session end datetime (optional)
            
        Returns:
            TTL in seconds
        """
        status = cls.determine_session_status(session_start, session_end)
        
        ttl_map = {
            SessionStatus.FUTURE: cls.TTL_FUTURE,
            SessionStatus.LIVE: cls.TTL_LIVE,
            SessionStatus.RECENTLY_COMPLETED: cls.TTL_RECENT,
            SessionStatus.COMPLETED: cls.TTL_COMPLETED,
            SessionStatus.HISTORICAL: cls.TTL_HISTORICAL,
        }
        
        return ttl_map[status]
    
    @classmethod
    def get_ttl_for_computed(
        cls,
        session_start: datetime,
        session_end: Optional[datetime] = None
    ) -> int:
        """
        Get TTL for computed metrics.
        
        Computed metrics use slightly shorter TTL than raw session data
        since they may need recalculation if data is corrected.
        
        Args:
            session_start: Session start datetime
            session_end: Session end datetime (optional)
            
        Returns:
            TTL in seconds
        """
        status = cls.determine_session_status(session_start, session_end)
        
        # Computed data has 50% of session data TTL for recent/completed
        ttl_map = {
            SessionStatus.FUTURE: cls.TTL_FUTURE // 2,
            SessionStatus.LIVE: cls.TTL_LIVE,
            SessionStatus.RECENTLY_COMPLETED: cls.TTL_RECENT // 2,
            SessionStatus.COMPLETED: cls.TTL_COMPLETED // 2,
            SessionStatus.HISTORICAL: cls.TTL_HISTORICAL,
        }
        
        return ttl_map[status]
    
    @classmethod
    def get_ttl_for_api_response(
        cls,
        session_start: Optional[datetime] = None,
        session_end: Optional[datetime] = None
    ) -> int:
        """
        Get TTL for API responses.
        
        Args:
            session_start: Session start datetime (optional)
            session_end: Session end datetime (optional)
            
        Returns:
            TTL in seconds
        """
        if session_start is None:
            # Default API response TTL
            return cls.TTL_API_RESPONSE
        
        # Use computed TTL if session timing is available
        return cls.get_ttl_for_computed(session_start, session_end)
    
    @classmethod
    def get_ttl_for_reference(cls) -> int:
        """
        Get TTL for reference data (drivers, teams, circuits, etc.).
        
        Returns:
            TTL in seconds (7 days)
        """
        return cls.TTL_REFERENCE


def calculate_dynamic_ttl(
    data_type: str,
    session_start: Optional[datetime] = None,
    session_end: Optional[datetime] = None
) -> int:
    """
    Calculate dynamic TTL based on data type and session timing.
    
    Args:
        data_type: Type of data ('session', 'computed', 'api', 'reference')
        session_start: Session start datetime (optional)
        session_end: Session end datetime (optional)
        
    Returns:
        TTL in seconds
        
    Examples:
        >>> # Live session data
        >>> ttl = calculate_dynamic_ttl('session', datetime.now())
        >>> # Result: 300 seconds (5 minutes)
        
        >>> # Historical session data
        >>> old_session = datetime.now() - timedelta(days=10)
        >>> ttl = calculate_dynamic_ttl('session', old_session)
        >>> # Result: 604800 seconds (7 days)
        
        >>> # Reference data
        >>> ttl = calculate_dynamic_ttl('reference')
        >>> # Result: 604800 seconds (7 days)
    """
    data_type = data_type.lower()
    
    if data_type == 'session':
        if session_start is None:
            return redis_settings.default_ttl
        return TTLStrategy.get_ttl_for_session(session_start, session_end)
    
    elif data_type == 'computed':
        if session_start is None:
            return redis_settings.default_ttl
        return TTLStrategy.get_ttl_for_computed(session_start, session_end)
    
    elif data_type == 'api':
        return TTLStrategy.get_ttl_for_api_response(session_start, session_end)
    
    elif data_type == 'reference':
        return TTLStrategy.get_ttl_for_reference()
    
    else:
        # Default TTL for unknown types
        return redis_settings.default_ttl
