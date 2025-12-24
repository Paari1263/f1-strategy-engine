"""
Driver Consistency Calculation
Measures lap-to-lap variation in driver performance

LOGIC:
  Statistical analysis using coefficient of variation (CV):
  - CV = standard_deviation / mean
  - Lower CV = more consistent
  - Score normalized: 0.002 CV = score 1.0 (perfect consistency)
  - Higher variation = lower score

ROLE:
  Reliability metric for driver performance. Identifies drivers
  who can maintain pace vs those with erratic performance.

SIGNIFICANCE:
  Consistent drivers are lower risk for strategy execution. High
  consistency enables predictable stint planning. Inconsistency
  increases uncertainty in gap projections and undercut timing.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import ConsistencyOutput
from typing import List, Dict, Any
import statistics


class DriverConsistencyCalculation(BaseCalculation):
    """
    Calculate driver consistency score.
    
    Consistent drivers maintain similar lap times throughout stint.
    Inconsistent drivers have high variation (errors, concentration lapses).
    """
    
    @property
    def calculation_name(self) -> str:
        return "driver_consistency"
    
    @property
    def description(self) -> str:
        return "Measures lap-to-lap variation in driver performance"
    
    def validate_inputs(self, lap_times: List[float] = None, **kwargs) -> bool:
        """Validate lap time data"""
        if not lap_times:
            return False
        return len(lap_times) >= 3  # Need at least 3 laps for meaningful consistency
    
    def calculate(
        self,
        lap_times: List[float],
        exclude_outliers: bool = True,
        **kwargs
    ) -> ConsistencyOutput:
        """
        Calculate consistency score.
        
        Args:
            lap_times: Driver's lap times (seconds)
            exclude_outliers: Whether to remove statistical outliers
            **kwargs: Additional parameters
            
        Returns:
            ConsistencyOutput with consistency metrics
        """
        if len(lap_times) < 3:
            return ConsistencyOutput(
                consistency_score=0.5,
                std_dev_s=0.0,
                coefficient_of_variation=0.0
            )
        
        # Optionally remove outliers (laps with errors, traffic, etc.)
        if exclude_outliers and len(lap_times) >= 5:
            times = self._remove_outliers(lap_times)
        else:
            times = lap_times
        
        # Calculate statistics
        mean_time = statistics.mean(times)
        std_dev = statistics.stdev(times) if len(times) > 1 else 0.0
        
        # Coefficient of variation (normalized std dev)
        cv = (std_dev / mean_time) if mean_time > 0 else 0.0
        
        # Consistency score (0-1, higher is better)
        # CV of 0.002 (0.2%) = very consistent = score 1.0
        # CV of 0.010 (1.0%) = inconsistent = score 0.0
        # Linear mapping
        if cv <= 0.002:
            score = 1.0
        elif cv >= 0.010:
            score = 0.0
        else:
            # Map 0.002 to 0.010 range to 1.0 to 0.0
            score = 1.0 - ((cv - 0.002) / 0.008)
        
        score = max(0.0, min(1.0, score))
        
        return ConsistencyOutput(
            consistency_score=score,
            std_dev_s=std_dev,
            coefficient_of_variation=cv
        )
    
    def _remove_outliers(self, lap_times: List[float]) -> List[float]:
        """
        Remove statistical outliers using IQR method.
        
        Args:
            lap_times: Raw lap times
            
        Returns:
            Filtered lap times
        """
        if len(lap_times) < 5:
            return lap_times
        
        sorted_times = sorted(lap_times)
        q1 = statistics.median(sorted_times[:len(sorted_times)//2])
        q3 = statistics.median(sorted_times[len(sorted_times)//2:])
        iqr = q3 - q1
        
        # Outliers are values outside [Q1 - 1.5*IQR, Q3 + 1.5*IQR]
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        filtered = [t for t in lap_times if lower_bound <= t <= upper_bound]
        
        # Always keep at least half the data
        if len(filtered) < len(lap_times) // 2:
            return lap_times
        
        return filtered if filtered else lap_times
    
    def classify_consistency(self, consistency_score: float) -> str:
        """
        Classify consistency level.
        
        Args:
            consistency_score: Consistency score (0-1)
            
        Returns:
            Classification string
        """
        if consistency_score >= 0.8:
            return "very_consistent"  # Robot-like (e.g., Prost, Rosberg)
        elif consistency_score >= 0.6:
            return "consistent"  # Solid and reliable
        elif consistency_score >= 0.4:
            return "moderate"  # Some variation
        elif consistency_score >= 0.2:
            return "inconsistent"  # Erratic performance
        else:
            return "very_inconsistent"  # High mistake rate


# Singleton instance
driver_consistency_calc = DriverConsistencyCalculation()
