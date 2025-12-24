"""
Driver Pace Delta Calculation
Calculates driver performance relative to field average

LOGIC:
  Statistical analysis of lap times:
  - Calculates average of driver's clean laps
  - Compares to field average pace
  - Percentile ranking (faster = higher percentile)
  - Negative delta = faster than field average

ROLE:
  Driver performance benchmarking. Quantifies driver skill level
  relative to competition. Foundation for driver ratings.

SIGNIFICANCE:
  Identifies elite vs struggling drivers. Critical for understanding
  if poor results are driver or car limited. Essential for
  driver-car fusion calculations and performance predictions.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_input_models import DriverPaceInput
from calculation_engines.interfaces.calculation_output_models import PaceDeltaOutput
from typing import List, Dict, Any
import statistics


class DriverPaceCalculation(BaseCalculation):
    """
    Calculate driver pace relative to field.
    
    Analyzes lap times to determine:
    - Average pace delta vs field
    - Percentile ranking
    - Raw performance metrics
    """
    
    @property
    def calculation_name(self) -> str:
        return "driver_pace_delta"
    
    @property
    def description(self) -> str:
        return "Calculates driver performance relative to field average"
    
    def validate_inputs(
        self,
        lap_times: List[float] = None,
        field_average: float = None,
        **kwargs
    ) -> bool:
        """Validate lap time data"""
        if not lap_times or field_average is None:
            return False
        return len(lap_times) > 0 and field_average > 0
    
    def calculate(
        self,
        lap_times: List[float],
        field_average: float,
        **kwargs
    ) -> PaceDeltaOutput:
        """
        Calculate driver pace delta.
        
        Args:
            lap_times: Driver's lap times (seconds)
            field_average: Field average lap time (seconds)
            **kwargs: Additional parameters
            
        Returns:
            PaceDeltaOutput with pace analysis
        """
        if not lap_times:
            return PaceDeltaOutput(
                pace_delta_s=0.0,
                percentile_rank=50.0
            )
        
        # Calculate driver's average
        driver_average = statistics.mean(lap_times)
        
        # Calculate delta (negative = faster than field)
        pace_delta = driver_average - field_average
        
        # Estimate percentile (simplified model)
        # Top drivers: ~0.5s faster than average (99th percentile)
        # Bottom drivers: ~1.5s slower than average (1st percentile)
        # Linear interpolation
        if pace_delta <= -0.5:
            percentile = 99.0  # Top tier
        elif pace_delta >= 1.5:
            percentile = 1.0  # Bottom tier
        else:
            # Map -0.5 to +1.5 range to 99 to 1 percentile
            normalized = (pace_delta + 0.5) / 2.0  # 0 to 1
            percentile = 99.0 - (normalized * 98.0)  # 99 to 1
        
        percentile = max(1.0, min(99.0, percentile))
        
        return PaceDeltaOutput(
            pace_delta_s=pace_delta,
            percentile_rank=percentile
        )
    
    def classify_driver_tier(self, pace_delta: float) -> str:
        """
        Classify driver into performance tier.
        
        Args:
            pace_delta: Pace delta vs field (seconds)
            
        Returns:
            Tier classification
        """
        if pace_delta <= -0.5:
            return "elite"  # Top 3-4 drivers
        elif pace_delta <= -0.2:
            return "strong"  # Solid midfield leaders
        elif pace_delta <= 0.2:
            return "average"  # Typical F1 driver
        elif pace_delta <= 0.8:
            return "below_average"  # Struggling
        else:
            return "weak"  # Backmarker


# Singleton instance
driver_pace_calc = DriverPaceCalculation()
