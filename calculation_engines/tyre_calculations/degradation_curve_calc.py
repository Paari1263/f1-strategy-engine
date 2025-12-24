"""
Degradation Curve Calculation
Models tyre degradation rate over stint lifetime

LOGIC:
  Non-linear degradation using exponential curve:
  - Base rate from track abrasion and temperature
  - Wear multiplier = e^(1.5 * wear_level)
  - Accelerating degradation as tyres age (cliff effect)
  - Combines wear, temperature, abrasion, and push factors

ROLE:
  Most sophisticated tyre model - predicts realistic performance
  drop-off over stint. Accounts for the 'tyre cliff' phenomenon
  where performance suddenly collapses.

SIGNIFICANCE:
  Prevents unrealistic long stints. Models real F1 behavior where
  tyres perform well initially but deteriorate rapidly near end of
  life. Essential for accurate stint length optimization.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import DegradationCurveOutput
from typing import Dict, Any
import math


class DegradationCurveCalculation(BaseCalculation):
    """
    Calculate tyre degradation rate considering multiple factors.
    
    Degradation is non-linear and affected by:
    - Base wear level
    - Temperature (thermal window)
    - Track abrasiveness
    - Driving style (push level)
    """
    
    # Base degradation rates (seconds per lap per wear unit)
    BASE_DEGRADATION = 0.05
    
    @property
    def calculation_name(self) -> str:
        return "degradation_curve"
    
    @property
    def description(self) -> str:
        return "Models tyre degradation rate with multiple factors"
    
    def validate_inputs(
        self, 
        wear_level: float = None,
        temp_factor: float = None,
        **kwargs
    ) -> bool:
        """Validate wear level is in range"""
        if wear_level is None or temp_factor is None:
            return False
        return 0.0 <= wear_level <= 1.0 and temp_factor >= 0.0
    
    def calculate(
        self,
        wear_level: float,
        temp_factor: float = 1.0,
        track_abrasion: float = 0.5,
        push_multiplier: float = 1.0,
        **kwargs
    ) -> DegradationCurveOutput:
        """
        Calculate current degradation rate.
        
        Args:
            wear_level: Current tyre wear (0=new, 1=completely worn)
            temp_factor: Temperature multiplier (from thermal_window_calc)
            track_abrasion: Track surface severity (0=smooth, 1=very abrasive)
            push_multiplier: Push penalty multiplier (from push_penalty_calc)
            **kwargs: Additional parameters
            
        Returns:
            DegradationCurveOutput with degradation metrics
        """
        # Clamp inputs
        wear_level = max(0.0, min(1.0, wear_level))
        track_abrasion = max(0.0, min(1.0, track_abrasion))
        temp_factor = max(0.5, temp_factor)  # Min 0.5x, no upper limit
        push_multiplier = max(1.0, push_multiplier)
        
        # Non-linear wear curve (exponential increase as tyre wears)
        # Fresh tyres degrade slowly, worn tyres degrade rapidly
        wear_curve_factor = math.exp(wear_level * 1.5)  # e^(1.5*wear)
        
        # Track abrasion effect (linear)
        track_factor = 1.0 + (track_abrasion * 0.5)  # Up to 1.5x for very abrasive
        
        # Calculate base degradation rate
        base_rate = self.BASE_DEGRADATION * wear_curve_factor
        
        # Apply all multipliers
        total_degradation_rate = (
            base_rate * 
            track_factor * 
            temp_factor * 
            push_multiplier
        )
        
        # Calculate overall wear multiplier (for reporting)
        overall_multiplier = (
            wear_curve_factor * 
            track_factor * 
            temp_factor * 
            push_multiplier
        )
        
        # Thermal penalty component (for breakdown)
        thermal_penalty = base_rate * (temp_factor - 1.0) * track_factor
        
        return DegradationCurveOutput(
            degradation_rate_s_per_lap=total_degradation_rate,
            wear_multiplier=overall_multiplier,
            thermal_penalty_s=max(0.0, thermal_penalty)
        )
    
    def project_degradation_over_stint(
        self,
        initial_wear: float,
        stint_length: int,
        track_abrasion: float = 0.5,
        temp_factor: float = 1.0,
        push_multiplier: float = 1.0
    ) -> list[float]:
        """
        Project degradation rates for each lap in stint.
        
        Args:
            initial_wear: Starting wear level
            stint_length: Number of laps in stint
            track_abrasion: Track severity
            temp_factor: Temperature multiplier
            push_multiplier: Push penalty
            
        Returns:
            List of degradation rates per lap
        """
        wear_progression = []
        current_wear = initial_wear
        wear_increment = (1.0 - initial_wear) / max(stint_length, 1)
        
        for lap in range(stint_length):
            result = self.calculate(
                wear_level=current_wear,
                temp_factor=temp_factor,
                track_abrasion=track_abrasion,
                push_multiplier=push_multiplier
            )
            wear_progression.append(result.degradation_rate_s_per_lap)
            current_wear = min(1.0, current_wear + wear_increment)
        
        return wear_progression


# Singleton instance
degradation_curve_calc = DegradationCurveCalculation()
