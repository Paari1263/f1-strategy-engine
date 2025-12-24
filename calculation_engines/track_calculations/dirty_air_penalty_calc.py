"""
Dirty Air Penalty Calculation
Calculates lap time loss when following another car

LOGIC:
  Exponential decay model based on gap:
  - Max penalty at close range (~0.8s at 0.5s gap)
  - Formula: max_penalty * e^(-gap / 1.2)
  - Decay constant 1.2s represents effective aero wake
  - Car-specific aero sensitivity factor

ROLE:
  Traffic impact quantification. Determines cost of being stuck
  in dirty air vs clean air pace.

SIGNIFICANCE:
  Explains why faster car struggles to pass slower car. Critical
  for evaluating cost of traffic after pit stop. Influences
  optimal pit stop timing to avoid dirty air.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import DirtyAirPenaltyOutput
from typing import Dict, Any


class DirtyAirPenaltyCalculation(BaseCalculation):
    """
    Calculate dirty air effect on following car.
    
    Dirty air reduces downforce and increases lap time.
    Effect varies by:
    - Distance to car ahead
    - Track aero sensitivity
    - Speed of corners
    """
    
    # Maximum penalty when directly behind (seconds per lap)
    MAX_DIRTY_AIR_PENALTY = 0.8
    
    @property
    def calculation_name(self) -> str:
        return "dirty_air_penalty"
    
    @property
    def description(self) -> str:
        return "Calculates lap time loss from following another car"
    
    def validate_inputs(
        self,
        gap_s: float = None,
        **kwargs
    ) -> bool:
        """Validate gap parameter"""
        if gap_s is None:
            return False
        return gap_s >= 0.0
    
    def calculate(
        self,
        gap_s: float,
        aero_sensitivity: float = 0.5,
        **kwargs
    ) -> DirtyAirPenaltyOutput:
        """
        Calculate dirty air penalty.
        
        Args:
            gap_s: Time gap to car ahead (seconds)
            aero_sensitivity: Track's aero dependency (0=low, 1=high)
            **kwargs: Additional parameters
            
        Returns:
            DirtyAirPenaltyOutput with penalty calculation
        """
        # Clamp inputs
        gap_s = max(0.0, gap_s)
        aero_sensitivity = max(0.0, min(1.0, aero_sensitivity))
        
        # Dirty air effect diminishes with distance
        # 0s gap = maximum penalty
        # 1s gap = ~70% penalty
        # 2s gap = ~30% penalty
        # 3s+ gap = minimal penalty
        
        import math
        
        if gap_s >= 3.0:
            distance_factor = 0.0  # No effect
        else:
            # Exponential decay: e^(-gap/1.2)
            distance_factor = math.exp(-gap_s / 1.2)
        
        # Calculate penalty
        penalty_s = (
            self.MAX_DIRTY_AIR_PENALTY *
            distance_factor *
            aero_sensitivity
        )
        
        return DirtyAirPenaltyOutput(
            penalty_s_per_lap=penalty_s,
            gap_s=gap_s
        )
    
    def calculate_stint_impact(
        self,
        avg_gap_s: float,
        stint_length: int,
        aero_sensitivity: float = 0.5
    ) -> Dict[str, Any]:
        """
        Calculate total time lost to dirty air over stint.
        
        Args:
            avg_gap_s: Average gap to car ahead
            stint_length: Number of laps in stint
            aero_sensitivity: Track aero dependency
            
        Returns:
            Dict with stint impact analysis
        """
        result = self.calculate(gap_s=avg_gap_s, aero_sensitivity=aero_sensitivity)
        
        total_loss_s = result.penalty_s_per_lap * stint_length
        
        return {
            'penalty_per_lap_s': result.penalty_s_per_lap,
            'total_stint_loss_s': total_loss_s,
            'avg_gap_s': avg_gap_s,
            'laps_affected': stint_length
        }


# Singleton instance
dirty_air_penalty_calc = DirtyAirPenaltyCalculation()
