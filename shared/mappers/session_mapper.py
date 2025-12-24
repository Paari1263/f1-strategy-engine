"""
Session Mapper
Maps between different session identifier formats (OpenF1 session_key vs FastF1 year/gp/session)
"""
from typing import Dict, Optional, Tuple


# Mapping of common OpenF1 session keys to FastF1 identifiers
# Format: session_key -> (year, gp, session_type)
SESSION_KEY_MAP: Dict[int, Tuple[int, str, str]] = {
    # 2024 Season
    9472: (2024, "Bahrain", "R"),  # Bahrain 2024 Race
    9471: (2024, "Bahrain", "Q"),  # Bahrain 2024 Qualifying
    9470: (2024, "Bahrain", "FP3"),
    9469: (2024, "Bahrain", "FP2"),
    9468: (2024, "Bahrain", "FP1"),
    
    # Add more mappings as needed
    # You can populate this dynamically by querying both APIs
}


def session_key_to_fastf1(session_key: int) -> Optional[Tuple[int, str, str]]:
    """
    Convert OpenF1 session_key to FastF1 format
    
    Args:
        session_key: OpenF1 session identifier
        
    Returns:
        Tuple of (year, gp, session_type) or None if not found
    """
    return SESSION_KEY_MAP.get(session_key)


def fastf1_to_session_key(year: int, gp: str, session_type: str) -> Optional[int]:
    """
    Convert FastF1 format to OpenF1 session_key (reverse lookup)
    
    Args:
        year: Season year
        gp: Grand Prix name
        session_type: Session type
        
    Returns:
        OpenF1 session_key or None if not found
    """
    lookup = (year, gp, session_type)
    for key, value in SESSION_KEY_MAP.items():
        if value == lookup:
            return key
    return None


def validate_fastf1_params(year: int, gp: str, session_type: str) -> bool:
    """
    Validate FastF1 session parameters
    
    Args:
        year: Season year (should be 2018-2025)
        gp: Grand Prix name or round number
        session_type: Session type
        
    Returns:
        True if valid, False otherwise
    """
    # Validate year range
    if not (2018 <= year <= 2025):
        return False
    
    # Validate session type
    valid_sessions = {'FP1', 'FP2', 'FP3', 'Q', 'SQ', 'R', 'S'}
    if session_type not in valid_sessions:
        return False
    
    return True
