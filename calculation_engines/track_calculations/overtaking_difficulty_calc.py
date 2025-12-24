"""
Overtaking Difficulty Calculation
Rates how hard it is to overtake at a circuit

LOGIC:
  Multi-factor difficulty score (0-10):
  - DRS zones: more zones = easier overtaking
  - Longest straight length: longer = more opportunity
  - Track width: wider = more racing lines
  Combined into single difficulty rating

ROLE:
  Track position value assessment. High difficulty = track position
  premium. Low difficulty = pace more important than position.

SIGNIFICANCE:
  Critical for strategic priorities. Monaco (diff 9/10) = protect
  track position at all costs. Bahrain (diff 3/10) = pace matters
  more. Influences undercut vs overcut decisions.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import OvertakingDifficultyOutput
from typing import Dict, Any


class OvertakingDifficultyCalculation(BaseCalculation):
    """
    Calculate track overtaking difficulty.
    
    Factors:
    - DRS zones (number and effectiveness)
    - Straight length
    - Corner characteristics
    - Track width
    """
    
    @property
    def calculation_name(self) -> str:
        return "overtaking_difficulty"
    
    @property
    def description(self) -> str:
        return "Rates how difficult overtaking is at a circuit"
    
    def validate_inputs(
        self,
        drs_zones: int = None,
        **kwargs
    ) -> bool:
        """Validate DRS zones count"""
        if drs_zones is None:
            return False
        return 0 <= drs_zones <= 5
    
    def calculate(
        self,
        drs_zones: int,
        longest_straight_m: float = 500.0,
        avg_corner_speed_kph: float = 120.0,
        track_width_m: float = 12.0,
        **kwargs
    ) -> OvertakingDifficultyOutput:
        """
        Calculate overtaking difficulty.
        
        Args:
            drs_zones: Number of DRS zones
            longest_straight_m: Length of longest straight (meters)
            avg_corner_speed_kph: Average corner speed (km/h)
            track_width_m: Average track width (meters)
            **kwargs: Additional parameters
            
        Returns:
            OvertakingDifficultyOutput with difficulty rating
        """
        # Clamp inputs
        drs_zones = max(0, min(5, drs_zones))
        longest_straight_m = max(100.0, min(2000.0, longest_straight_m))
        avg_corner_speed_kph = max(60.0, min(250.0, avg_corner_speed_kph))
        track_width_m = max(8.0, min(20.0, track_width_m))
        
        # DRS factor (more DRS = easier overtaking)
        # 0 zones = 1.5x difficulty, 3 zones = 1.0x, 5 zones = 0.7x
        drs_multiplier = 1.5 - (drs_zones * 0.16)
        
        # Straight length factor
        # Short straight (300m) = 1.3x difficulty
        # Long straight (1000m+) = 0.7x difficulty
        if longest_straight_m < 500:
            straight_multiplier = 1.3
        elif longest_straight_m > 1000:
            straight_multiplier = 0.7
        else:
            # Linear interpolation 500-1000m
            straight_multiplier = 1.3 - ((longest_straight_m - 500) / 500 * 0.6)
        
        # Track width factor
        # Narrow (8m) = 1.2x difficulty
        # Wide (15m+) = 0.8x difficulty
        if track_width_m < 10:
            width_multiplier = 1.2
        elif track_width_m > 15:
            width_multiplier = 0.8
        else:
            width_multiplier = 1.2 - ((track_width_m - 10) / 5 * 0.4)
        
        # Base difficulty (5.0 on 0-10 scale, 10 = impossible)
        base_difficulty = 5.0
        
        # Calculate overall difficulty
        difficulty_rating = (
            base_difficulty *
            drs_multiplier *
            straight_multiplier *
            width_multiplier
        )
        
        # Clamp to 0-10
        difficulty_rating = max(0.0, min(10.0, difficulty_rating))
        
        # Classify
        if difficulty_rating < 3.0:
            difficulty_class = "easy"  # Bahrain, Monza
        elif difficulty_rating < 5.0:
            difficulty_class = "moderate"
        elif difficulty_rating < 7.0:
            difficulty_class = "hard"  # Most circuits
        else:
            difficulty_class = "very_hard"  # Monaco, Hungary
        
        return OvertakingDifficultyOutput(
            difficulty_rating=difficulty_rating,
            difficulty_class=difficulty_class
        )
    
    def estimate_overtakes_per_race(
        self,
        difficulty_rating: float,
        field_size: int = 20
    ) -> int:
        """
        Estimate number of overtakes in race.
        
        Args:
            difficulty_rating: Overtaking difficulty (0-10)
            field_size: Number of cars
            
        Returns:
            Expected number of overtakes
        """
        # Easy tracks (difficulty 2): ~40 overtakes
        # Hard tracks (difficulty 8): ~5 overtakes
        base_overtakes = max(5, int(50 - (difficulty_rating * 5)))
        
        # Scale by field size
        scaled_overtakes = int(base_overtakes * (field_size / 20))
        
        return max(1, scaled_overtakes)


# Singleton instance
overtaking_difficulty_calc = OvertakingDifficultyCalculation()
