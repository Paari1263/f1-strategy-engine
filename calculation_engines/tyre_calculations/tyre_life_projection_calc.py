"""
Tyre Life Projection Calculation
Predicts remaining tyre life and cliff point
LOGIC:
  Predicts when tyres will reach critical degradation:
  - Remaining laps = expected_life - laps_completed
  - Cliff point estimated at 90% of expected life
  - Confidence decreases as degradation accelerates
  - Considers current degradation rate trend

ROLE:
  Forward-looking tyre management. Provides early warning of
  approaching tyre cliff to optimize pit stop timing.

SIGNIFICANCE:
  Prevents being caught out by sudden tyre drop-off. Enables
  proactive pit strategy rather than reactive. Critical for
  races where tyre management determines outcome."""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import TyreLifeProjectionOutput
from typing import Dict, Any, Optional


class TyreLifeProjectionCalculation(BaseCalculation):
    """
    Project remaining usable tyre life based on current state and degradation.
    
    Considers:
    - Expected total life
    - Laps already completed
    - Current degradation rate
    - Cliff point prediction (rapid performance loss)
    """
    
    # Performance cliff typically occurs around 90% of expected life
    CLIFF_THRESHOLD = 0.90
    
    @property
    def calculation_name(self) -> str:
        return "tyre_life_projection"
    
    @property
    def description(self) -> str:
        return "Projects remaining tyre life and predicts performance cliff"
    
    def validate_inputs(
        self,
        total_expected_life: int = None,
        laps_completed: int = None,
        **kwargs
    ) -> bool:
        """Validate life parameters are reasonable"""
        if total_expected_life is None or laps_completed is None:
            return False
        return total_expected_life > 0 and laps_completed >= 0
    
    def calculate(
        self,
        total_expected_life: int,
        laps_completed: int,
        current_degradation_rate: float = 0.05,
        cliff_threshold: float = None,
        **kwargs
    ) -> TyreLifeProjectionOutput:
        """
        Calculate remaining tyre life.
        
        Args:
            total_expected_life: Expected tyre life in laps
            laps_completed: Laps already done on this tyre
            current_degradation_rate: Current deg rate (s/lap)
            cliff_threshold: When cliff occurs (0.0-1.0, default 0.90)
            **kwargs: Additional parameters
            
        Returns:
            TyreLifeProjectionOutput with remaining life prediction
        """
        if cliff_threshold is None:
            cliff_threshold = self.CLIFF_THRESHOLD
        
        # Clamp inputs
        cliff_threshold = max(0.5, min(1.0, cliff_threshold))
        laps_completed = max(0, laps_completed)
        
        # Calculate basic remaining life
        remaining_laps = max(0, total_expected_life - laps_completed)
        
        # Calculate life percentage used
        life_percentage_used = laps_completed / max(total_expected_life, 1)
        
        # Predict cliff lap (when rapid degradation begins)
        cliff_lap = int(total_expected_life * cliff_threshold)
        cliff_lap_estimate = cliff_lap if cliff_lap > laps_completed else None
        
        # Adjust confidence based on degradation rate
        # Higher deg rate = lower confidence in projection
        base_confidence = 0.8
        if current_degradation_rate > 0.1:
            # Rapid degradation reduces confidence
            confidence_penalty = min(0.3, (current_degradation_rate - 0.1) * 2)
            confidence = base_confidence - confidence_penalty
        else:
            confidence = base_confidence
        
        # If we're past expected life, confidence drops significantly
        if laps_completed > total_expected_life:
            confidence *= 0.5
        
        # Clamp confidence
        confidence = max(0.1, min(1.0, confidence))
        
        return TyreLifeProjectionOutput(
            remaining_laps=remaining_laps,
            cliff_lap_estimate=cliff_lap_estimate,
            confidence=confidence
        )
    
    def estimate_maximum_safe_stint(
        self,
        total_expected_life: int,
        safety_margin_laps: int = 3
    ) -> int:
        """
        Calculate maximum safe stint length with safety margin.
        
        Args:
            total_expected_life: Expected tyre life
            safety_margin_laps: Safety buffer before cliff
            
        Returns:
            Maximum recommended stint length
        """
        # Don't push to absolute limit - leave safety margin
        cliff_lap = int(total_expected_life * self.CLIFF_THRESHOLD)
        max_safe_stint = max(1, cliff_lap - safety_margin_laps)
        return max_safe_stint
    
    def calculate_stint_feasibility(
        self,
        remaining_race_laps: int,
        tyre_remaining_life: int,
        minimum_pace_requirement: bool = True
    ) -> tuple[bool, str]:
        """
        Determine if current tyres can finish race.
        
        Args:
            remaining_race_laps: Laps left in race
            tyre_remaining_life: Estimated tyre life remaining
            minimum_pace_requirement: Whether pace needs to be maintained
            
        Returns:
            (feasible: bool, reason: str)
        """
        if tyre_remaining_life >= remaining_race_laps + 2:
            return (True, "Tyres have comfortable margin")
        elif tyre_remaining_life >= remaining_race_laps:
            if minimum_pace_requirement:
                return (False, "Tyres will barely last but pace will drop")
            else:
                return (True, "Tyres will just last")
        else:
            laps_short = remaining_race_laps - tyre_remaining_life
            return (False, f"Tyres {laps_short} laps short")


# Singleton instance
tyre_life_projection_calc = TyreLifeProjectionCalculation()
