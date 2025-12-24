"""
Car Performance Index Calculation
Calculates overall car performance rating from component metrics

LOGIC:
  Weighted composite score (0-10 scale) from four key areas:
  - Power unit: 30% (acceleration, top speed)
  - Aerodynamic efficiency: 35% (downforce generation)
  - Drag coefficient: 15% (straight-line speed, inverted score)
  - Mechanical grip: 20% (low-speed corners, traction)
  All inputs normalized to 0-10 scale.

ROLE:
  Single metric representing overall car competitiveness. Enables
  comparison across teams and seasons. Foundation for driver-car
  fusion calculations.

SIGNIFICANCE:
  Determines baseline pace expectations. Critical for understanding
  performance gaps in field and setting realistic strategy goals.
  Essential for multi-team race simulations.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_input_models import CarPerformanceInput
from calculation_engines.interfaces.calculation_output_models import CarPerformanceIndexOutput
from typing import Dict, Any


class CarPerformanceIndexCalculation(BaseCalculation):
    """
    Calculate composite car performance index (0-10 scale).
    
    Combines multiple car characteristics into single performance rating:
    - Power unit performance
    - Aerodynamic efficiency
    - Drag coefficient
    - Mechanical grip
    """
    
    # Weighting factors for each component
    POWER_WEIGHT = 0.30      # 30% power unit
    AERO_WEIGHT = 0.35       # 35% aero efficiency
    DRAG_WEIGHT = 0.15       # 15% drag (inverse - lower is better)
    GRIP_WEIGHT = 0.20       # 20% mechanical grip
    
    @property
    def calculation_name(self) -> str:
        return "car_performance_index"
    
    @property
    def description(self) -> str:
        return "Calculates composite car performance rating from component metrics"
    
    def validate_inputs(
        self,
        power: float = None,
        aero_efficiency: float = None,
        **kwargs
    ) -> bool:
        """Validate component metrics are in valid range"""
        if power is None or aero_efficiency is None:
            return False
        return 0.0 <= power <= 10.0 and 0.0 <= aero_efficiency <= 10.0
    
    def calculate(
        self,
        power: float,
        aero_efficiency: float,
        drag_coefficient: float,
        mechanical_grip: float,
        **kwargs
    ) -> CarPerformanceIndexOutput:
        """
        Calculate car performance index.
        
        Args:
            power: Power unit rating (0-10, higher is better)
            aero_efficiency: Aero efficiency rating (0-10, higher is better)
            drag_coefficient: Drag rating (0-10, LOWER is better - inverted)
            mechanical_grip: Mechanical grip rating (0-10, higher is better)
            **kwargs: Additional parameters
            
        Returns:
            CarPerformanceIndexOutput with composite index
        """
        # Clamp all inputs to 0-10 range
        power = max(0.0, min(10.0, power))
        aero_efficiency = max(0.0, min(10.0, aero_efficiency))
        drag_coefficient = max(0.0, min(10.0, drag_coefficient))
        mechanical_grip = max(0.0, min(10.0, mechanical_grip))
        
        # Invert drag (lower drag is better, so 10 - drag)
        inverted_drag = 10.0 - drag_coefficient
        
        # Calculate weighted contributions
        power_contrib = power * self.POWER_WEIGHT
        aero_contrib = aero_efficiency * self.AERO_WEIGHT
        drag_contrib = inverted_drag * self.DRAG_WEIGHT
        grip_contrib = mechanical_grip * self.GRIP_WEIGHT
        
        # Calculate composite index
        performance_index = (
            power_contrib +
            aero_contrib +
            drag_contrib +
            grip_contrib
        )
        
        # Clamp final result to 0-10
        performance_index = max(0.0, min(10.0, performance_index))
        
        return CarPerformanceIndexOutput(
            performance_index=performance_index,
            power_contribution=power_contrib,
            aero_contribution=aero_contrib,
            drag_penalty=drag_contrib,
            grip_contribution=grip_contrib
        )
    
    def calculate_with_custom_weights(
        self,
        power: float,
        aero_efficiency: float,
        drag_coefficient: float,
        mechanical_grip: float,
        weights: Dict[str, float]
    ) -> CarPerformanceIndexOutput:
        """
        Calculate index with custom component weights.
        
        Args:
            power, aero_efficiency, drag_coefficient, mechanical_grip: Component ratings
            weights: Dict with keys: power_weight, aero_weight, drag_weight, grip_weight
            
        Returns:
            CarPerformanceIndexOutput with custom weighting
        """
        # Normalize weights to sum to 1.0
        total_weight = sum(weights.values())
        if total_weight == 0:
            total_weight = 1.0
        
        normalized_weights = {k: v / total_weight for k, v in weights.items()}
        
        # Temporarily override weights
        original_weights = {
            'power': self.POWER_WEIGHT,
            'aero': self.AERO_WEIGHT,
            'drag': self.DRAG_WEIGHT,
            'grip': self.GRIP_WEIGHT
        }
        
        self.POWER_WEIGHT = normalized_weights.get('power_weight', self.POWER_WEIGHT)
        self.AERO_WEIGHT = normalized_weights.get('aero_weight', self.AERO_WEIGHT)
        self.DRAG_WEIGHT = normalized_weights.get('drag_weight', self.DRAG_WEIGHT)
        self.GRIP_WEIGHT = normalized_weights.get('grip_weight', self.GRIP_WEIGHT)
        
        # Calculate with custom weights
        result = self.calculate(power, aero_efficiency, drag_coefficient, mechanical_grip)
        
        # Restore original weights
        self.POWER_WEIGHT = original_weights['power']
        self.AERO_WEIGHT = original_weights['aero']
        self.DRAG_WEIGHT = original_weights['drag']
        self.GRIP_WEIGHT = original_weights['grip']
        
        return result


# Singleton instance
car_performance_index_calc = CarPerformanceIndexCalculation()
