"""
Thermal Window Calculation
Calculates performance penalty for operating outside optimal tyre temperature

LOGIC:
  Each compound has optimal temperature window (90-100°C default).
  Temperature outside range causes performance penalty:
  - 0.02s per lap for each degree Celsius outside optimal range
  - Linear penalty model
  - Compound-specific temperature ranges

ROLE:
  Environmental adaptation - determines if track/weather conditions
  suit chosen compound. Prevents unrealistic strategies ignoring
  thermal constraints.

SIGNIFICANCE:
  Explains why certain compounds underperform in specific conditions
  (e.g., HARD in cold weather). Essential for weather-dependent
  strategy adjustments.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import ThermalWindowOutput
from typing import Dict, Any


class ThermalWindowCalculation(BaseCalculation):
    """
    Calculate tyre performance penalty based on temperature.
    
    Tyres perform optimally within a specific temperature window.
    Operating outside this window incurs lap time penalties.
    """
    
    # Default optimal temperature ranges by compound (°C)
    OPTIMAL_TEMPS = {
        "SOFT": (85, 95),
        "MEDIUM": (90, 100),
        "HARD": (95, 105),
        "INTERMEDIATE": (70, 90),
        "WET": (50, 80)
    }
    
    # Penalty factor: seconds per degree Celsius outside window
    TEMP_PENALTY_FACTOR = 0.02
    
    @property
    def calculation_name(self) -> str:
        return "thermal_window"
    
    @property
    def description(self) -> str:
        return "Calculates performance penalty from operating outside optimal tyre temperature"
    
    def validate_inputs(
        self, 
        track_temp_c: float = None,
        compound: str = None,
        **kwargs
    ) -> bool:
        """Validate temperature is reasonable"""
        if track_temp_c is None:
            return False
        return -10 <= track_temp_c <= 80  # Reasonable track temp range
    
    def calculate(
        self,
        track_temp_c: float,
        compound: str = "MEDIUM",
        optimal_temp_override: tuple = None,
        **kwargs
    ) -> ThermalWindowOutput:
        """
        Calculate thermal penalty.
        
        Args:
            track_temp_c: Current track temperature in Celsius
            compound: Tyre compound (for default optimal range)
            optimal_temp_override: Override optimal temp range (min, max)
            **kwargs: Additional parameters
            
        Returns:
            ThermalWindowOutput with penalty calculation
        """
        # Get optimal temperature range
        if optimal_temp_override:
            optimal_min, optimal_max = optimal_temp_override
        else:
            optimal_min, optimal_max = self.OPTIMAL_TEMPS.get(
                compound.upper(), 
                (90, 100)
            )
        
        # Calculate temperature delta from optimal window
        if track_temp_c < optimal_min:
            temp_delta = optimal_min - track_temp_c
            is_in_window = False
        elif track_temp_c > optimal_max:
            temp_delta = track_temp_c - optimal_max
            is_in_window = False
        else:
            temp_delta = 0.0
            is_in_window = True
        
        # Calculate lap time penalty
        penalty_s = abs(temp_delta) * self.TEMP_PENALTY_FACTOR
        
        return ThermalWindowOutput(
            temp_penalty_s_per_lap=penalty_s,
            is_in_window=is_in_window,
            temp_delta_c=temp_delta if not is_in_window else 0.0
        )


# Singleton instance
thermal_window_calc = ThermalWindowCalculation()
