"""
Driver-Car Fusion Calculation
Combines driver and car performance into unified rating

LOGIC:
  Weighted combination of driver and car performance:
  - Car rating: 60% weight (F1 is constructor championship)
  - Driver rating: 40% weight (driver makes difference)
  - Synergy adjustment (+/- 10% for driver-car fit)
  - Output: combined performance index (0-10)

ROLE:
  Holistic performance assessment. Separates car vs driver
  contribution. Enables realistic performance predictions.

SIGNIFICANCE:
  Core metric for race simulation. Elite driver in weak car
  has ceiling. Average driver in strong car has floor. Explains
  real F1 performance variation. Essential for multi-driver/team
  race simulations.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import DriverCarFusionOutput
from typing import Dict, Any


class DriverCarFusionCalculation(BaseCalculation):
    """
    Fuse driver and car performance metrics.
    
    Creates composite performance rating accounting for:
    - Driver skill
    - Car performance
    - Driver-car synergy
    """
    
    @property
    def calculation_name(self) -> str:
        return "driver_car_fusion"
    
    @property
    def description(self) -> str:
        return "Combines driver and car performance into unified rating"
    
    def validate_inputs(
        self,
        driver_rating: float = None,
        car_rating: float = None,
        **kwargs
    ) -> bool:
        """Validate rating inputs"""
        if driver_rating is None or car_rating is None:
            return False
        return 0.0 <= driver_rating <= 10.0 and 0.0 <= car_rating <= 10.0
    
    def calculate(
        self,
        driver_rating: float,
        car_rating: float,
        synergy_factor: float = 0.0,
        **kwargs
    ) -> DriverCarFusionOutput:
        """
        Calculate fused performance.
        
        Args:
            driver_rating: Driver performance (0-10)
            car_rating: Car performance (0-10)
            synergy_factor: Driver-car synergy (-1 to 1, 0=neutral)
            **kwargs: Additional parameters
            
        Returns:
            DriverCarFusionOutput with combined rating
        """
        # Clamp inputs
        driver_rating = max(0.0, min(10.0, driver_rating))
        car_rating = max(0.0, min(10.0, car_rating))
        synergy_factor = max(-1.0, min(1.0, synergy_factor))
        
        # Base combined performance (weighted average)
        # Car matters more (60%) than driver (40%) for raw pace
        base_performance = (car_rating * 0.60 + driver_rating * 0.40)
        
        # Synergy adjustment
        # Positive synergy: driver extracts more from car
        # Negative synergy: driver struggles with car characteristics
        synergy_adjustment = synergy_factor * 1.0  # Up to ±1.0 points
        
        # Calculate final performance
        combined_performance = base_performance + synergy_adjustment
        
        # Clamp to 0-10
        combined_performance = max(0.0, min(10.0, combined_performance))
        
        return DriverCarFusionOutput(
            combined_performance=combined_performance
        )
    
    def estimate_race_pace(
        self,
        combined_performance: float,
        baseline_lap_time_s: float = 90.0
    ) -> Dict[str, Any]:
        """
        Estimate race pace from combined performance.
        
        Args:
            combined_performance: Fused performance rating (0-10)
            baseline_lap_time_s: Reference lap time
            
        Returns:
            Dict with pace estimation
        """
        # Performance 5.0 = baseline pace
        # Performance 10.0 = 1.5s faster
        # Performance 0.0 = 1.5s slower
        
        performance_delta = (combined_performance - 5.0) / 5.0  # -1 to +1
        pace_adjustment_s = performance_delta * -1.5  # Negative = faster
        
        estimated_pace_s = baseline_lap_time_s + pace_adjustment_s
        
        # Classify performance level
        if combined_performance >= 8.5:
            performance_tier = "elite"
        elif combined_performance >= 7.0:
            performance_tier = "strong"
        elif combined_performance >= 5.0:
            performance_tier = "midfield"
        elif combined_performance >= 3.0:
            performance_tier = "struggling"
        else:
            performance_tier = "backmarker"
        
        return {
            'estimated_lap_time_s': estimated_pace_s,
            'pace_delta_to_baseline_s': pace_adjustment_s,
            'performance_tier': performance_tier,
            'combined_performance': combined_performance
        }


# Singleton instance
driver_car_fusion_calc = DriverCarFusionCalculation()
