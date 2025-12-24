from typing import List


def ema(values: List[float], alpha: float = 0.3) -> List[float]:
    """
    Apply Exponential Moving Average smoothing.
    
    Args:
        values: List of values to smooth
        alpha: Smoothing factor (0-1), higher = more responsive
    
    Returns:
        Smoothed values list
    """
    if not values:
        return []
    
    if len(values) == 1:
        return values.copy()
    
    # Clamp alpha to valid range
    alpha = max(0.0, min(1.0, alpha))
    
    smoothed = [values[0]]
    for v in values[1:]:
        smoothed.append(alpha * v + (1 - alpha) * smoothed[-1])
    return smoothed
