def normalize(value: float, min_v: float, max_v: float) -> float:
    """
    Normalize a value to 0-1 range.
    
    Args:
        value: Value to normalize
        min_v: Minimum value in range
        max_v: Maximum value in range
    
    Returns:
        Normalized value (0-1)
    """
    # Avoid division by zero
    if max_v == min_v:
        return 0.0
    
    # Clamp result to 0-1 range
    normalized = (value - min_v) / (max_v - min_v)
    return max(0.0, min(1.0, normalized))
