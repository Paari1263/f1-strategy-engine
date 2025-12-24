"""
Grip Evolution Calculation
Models track grip changes over session

LOGIC:
  Logarithmic grip improvement model:
  - Grip increases as rubber is laid down
  - Formula: initial_grip + (0.15 * ln(laps + 1) / ln(total_laps + 1))
  - Maximum 15% improvement over session
  - Translates to lap time delta (faster as session progresses)

ROLE:
  Track evolution modeling. Explains why qualifying is faster
  than practice and why later sessions show better times.

SIGNIFICANCE:
  Affects qualifying session strategy (when to run) and race
  pace projections. Green track conditions penalize early runners.
  Critical for mixed conditions (drying track evolution).
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import GripEvolutionOutput
from typing import Dict, Any


class GripEvolutionCalculation(BaseCalculation):
    """
    Calculate track grip evolution.
    
    Track grip improves as:
    - Rubber is laid down
    - Track temperature stabilizes
    - Weather clears
    """
    
    # Maximum grip improvement from start to end of race
    MAX_GRIP_IMPROVEMENT = 0.15  # 15% lap time improvement
    
    @property
    def calculation_name(self) -> str:
        return "grip_evolution"
    
    @property
    def description(self) -> str:
        return "Models track grip changes over session"
    
    def validate_inputs(
        self,
        laps_completed: int = None,
        total_laps: int = None,
        **kwargs
    ) -> bool:
        """Validate lap counts"""
        if laps_completed is None or total_laps is None:
            return False
        return 0 <= laps_completed <= total_laps
    
    def calculate(
        self,
        laps_completed: int,
        total_laps: int,
        initial_grip: float = 0.85,
        weather_stable: bool = True,
        **kwargs
    ) -> GripEvolutionOutput:
        """
        Calculate current grip level.
        
        Args:
            laps_completed: Laps run so far
            total_laps: Total laps in session
            initial_grip: Starting grip level (0-1)
            weather_stable: Whether conditions are stable
            **kwargs: Additional parameters
            
        Returns:
            GripEvolutionOutput with grip progression
        """
        # Clamp inputs
        laps_completed = max(0, min(total_laps, laps_completed))
        total_laps = max(1, total_laps)
        initial_grip = max(0.5, min(1.0, initial_grip))
        
        # Calculate progression (0-1, where 1 = full rubber down)
        progression = laps_completed / total_laps
        
        # Grip improvement is logarithmic (rapid early, slows later)
        import math
        if progression > 0:
            improvement_factor = math.log(1 + progression * 9) / math.log(10)  # log10(1+9x)
        else:
            improvement_factor = 0.0
        
        # Calculate current grip
        grip_improvement = self.MAX_GRIP_IMPROVEMENT * improvement_factor
        
        if weather_stable:
            current_grip = initial_grip + grip_improvement
        else:
            # Unstable weather reduces grip gain
            current_grip = initial_grip + (grip_improvement * 0.5)
        
        # Clamp to 0-1
        current_grip = max(0.0, min(1.0, current_grip))
        
        # Calculate lap time delta (lower grip = slower lap times)
        # 0.85 grip = +0.5s, 1.0 grip = 0.0s
        reference_grip = 1.0
        grip_delta = reference_grip - current_grip
        lap_time_delta_s = grip_delta * 3.0  # 3s per 0.1 grip loss
        
        return GripEvolutionOutput(
            current_grip_level=current_grip,
            lap_time_delta_s=lap_time_delta_s
        )
    
    def predict_end_of_race_grip(
        self,
        current_lap: int,
        total_laps: int,
        current_grip: float
    ) -> float:
        """
        Predict grip level at race end.
        
        Args:
            current_lap: Current lap number
            total_laps: Total race laps
            current_grip: Current grip level
            
        Returns:
            Predicted final grip level
        """
        remaining_laps = total_laps - current_lap
        remaining_progression = remaining_laps / total_laps
        
        # Estimate additional improvement
        import math
        additional_improvement = (
            self.MAX_GRIP_IMPROVEMENT *
            (math.log(1 + remaining_progression * 9) / math.log(10)) *
            0.5  # Diminishing returns
        )
        
        predicted_grip = min(1.0, current_grip + additional_improvement)
        return predicted_grip


# Singleton instance
grip_evolution_calc = GripEvolutionCalculation()
