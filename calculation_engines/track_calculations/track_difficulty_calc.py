"""
Track Difficulty Calculation
Overall circuit challenge rating

LOGIC:
  Composite difficulty score from multiple factors:
  - Technical challenge: corner count, average corner speed
  - Physical demand: speed, elevation changes
  - Error margin: barrier proximity, run-off areas
  Weighted combination produces 0-10 difficulty rating

ROLE:
  Driver performance context. Difficult tracks increase error risk,
  fatigue effects, and performance variation.

SIGNIFICANCE:
  Influences error risk calculations and driver form adjustments.
  Monaco (high difficulty) amplifies driver skill differences.
  Affects realistic performance predictions and strategy risk.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import TrackDifficultyOutput
from typing import Dict, Any


class TrackDifficultyCalculation(BaseCalculation):
    """
    Calculate overall track difficulty.
    
    Combines:
    - Technical complexity (corners)
    - Physical demands
    - Error margin
    - Weather variability
    """
    
    @property
    def calculation_name(self) -> str:
        return "track_difficulty"
    
    @property
    def description(self) -> str:
        return "Calculates overall circuit challenge rating"
    
    def validate_inputs(
        self,
        corner_count: int = None,
        **kwargs
    ) -> bool:
        """Validate corner count"""
        if corner_count is None:
            return False
        return 5 <= corner_count <= 30
    
    def calculate(
        self,
        corner_count: int,
        avg_corner_speed_kph: float = 120.0,
        elevation_change_m: float = 20.0,
        barrier_proximity: float = 0.5,
        **kwargs
    ) -> TrackDifficultyOutput:
        """
        Calculate track difficulty.
        
        Args:
            corner_count: Number of corners
            avg_corner_speed_kph: Average cornering speed
            elevation_change_m: Total elevation change
            barrier_proximity: How close barriers are (0=far, 1=very close)
            **kwargs: Additional parameters
            
        Returns:
            TrackDifficultyOutput with difficulty rating
        """
        # Clamp inputs
        corner_count = max(5, min(30, corner_count))
        avg_corner_speed_kph = max(60.0, min(250.0, avg_corner_speed_kph))
        elevation_change_m = max(0.0, min(200.0, elevation_change_m))
        barrier_proximity = max(0.0, min(1.0, barrier_proximity))
        
        # Technical complexity (more corners = harder)
        # 10 corners = 3.0, 20 corners = 6.0, 25 corners = 7.5
        technical_score = min(10.0, corner_count / 3.3)
        
        # Speed difficulty (slower corners = more technical = harder)
        # 200+ kph corners = 2.0 (flowing, easy)
        # <100 kph corners = 8.0 (slow, technical, hard)
        if avg_corner_speed_kph > 180:
            speed_score = 2.0
        elif avg_corner_speed_kph < 100:
            speed_score = 8.0
        else:
            # Linear interpolation 100-180
            speed_score = 8.0 - ((avg_corner_speed_kph - 100) / 80 * 6.0)
        
        # Physical demand (elevation changes)
        # Flat = 2.0, 100m+ elevation = 8.0
        physical_score = 2.0 + min(6.0, elevation_change_m / 100 * 6.0)
        
        # Error margin (barrier proximity)
        # Barriers far = 2.0, Monaco-style = 10.0
        error_margin_score = 2.0 + (barrier_proximity * 8.0)
        
        # Calculate overall difficulty (weighted average)
        difficulty_rating = (
            technical_score * 0.30 +
            speed_score * 0.30 +
            physical_score * 0.20 +
            error_margin_score * 0.20
        )
        
        # Clamp to 0-10
        difficulty_rating = max(0.0, min(10.0, difficulty_rating))
        
        return TrackDifficultyOutput(
            difficulty_rating=difficulty_rating
        )
    
    def classify_track_type(
        self,
        difficulty_rating: float,
        corner_count: int,
        avg_corner_speed_kph: float
    ) -> str:
        """
        Classify track into category.
        
        Args:
            difficulty_rating: Overall difficulty
            corner_count: Number of corners
            avg_corner_speed_kph: Average corner speed
            
        Returns:
            Track type classification
        """
        if avg_corner_speed_kph > 180 and corner_count < 15:
            return "high_speed"  # Monza, Spa
        elif avg_corner_speed_kph < 100 and difficulty_rating > 7:
            return "street_circuit"  # Monaco, Singapore
        elif corner_count > 20:
            return "technical"  # Suzuka, Barcelona
        elif difficulty_rating < 4:
            return "flowing"  # Silverstone
        else:
            return "balanced"  # Most modern circuits


# Singleton instance
track_difficulty_calc = TrackDifficultyCalculation()
