"""
Fuel Effect Calculation
Calculates lap time impact from fuel load

LOGIC:
  Linear fuel effect model:
  - 0.03s per kilogram of fuel load
  - Starting fuel ~100kg, ending ~10kg
  - Pace improves ~2.7s from start to end of race
  Calculates stint fuel progression and average penalties

ROLE:
  Models natural pace improvement as fuel burns off. Essential
  for understanding gap evolution and undercut opportunities.

SIGNIFICANCE:
  Explains why cars are faster in second stint vs first stint.
  Critical for undercut timing - lighter car = faster in-lap.
  Affects optimal pit stop lap calculation significantly.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import FuelEffectOutput
from typing import Dict, Any


class FuelEffectCalculation(BaseCalculation):
    """
    Calculate lap time penalty from fuel weight.
    
    Heavier fuel load = slower lap times due to:
    - Increased mass
    - Reduced acceleration
    - Increased tyre degradation
    - Harder on brakes
    """
    
    # Typical fuel effect: ~0.03s per kg of fuel
    FUEL_EFFECT_PER_KG = 0.03
    
    # Average fuel consumption per lap (kg)
    AVG_FUEL_PER_LAP = 1.8
    
    # Maximum fuel capacity (kg)
    MAX_FUEL_CAPACITY = 110.0
    
    @property
    def calculation_name(self) -> str:
        return "fuel_effect"
    
    @property
    def description(self) -> str:
        return "Calculates lap time impact from fuel load"
    
    def validate_inputs(self, fuel_load_kg: float = None, **kwargs) -> bool:
        """Validate fuel load is reasonable"""
        if fuel_load_kg is None:
            return False
        return 0.0 <= fuel_load_kg <= self.MAX_FUEL_CAPACITY
    
    def calculate(
        self,
        fuel_load_kg: float,
        fuel_effect_per_kg: float = None,
        **kwargs
    ) -> FuelEffectOutput:
        """
        Calculate fuel load penalty.
        
        Args:
            fuel_load_kg: Current fuel load in kilograms
            fuel_effect_per_kg: Override default fuel effect (s/kg)
            **kwargs: Additional parameters
            
        Returns:
            FuelEffectOutput with fuel penalty
        """
        # Use custom fuel effect or default
        if fuel_effect_per_kg is None:
            fuel_effect_per_kg = self.FUEL_EFFECT_PER_KG
        
        # Clamp fuel load
        fuel_load_kg = max(0.0, min(self.MAX_FUEL_CAPACITY, fuel_load_kg))
        
        # Calculate lap time penalty
        penalty_s = fuel_load_kg * fuel_effect_per_kg
        
        return FuelEffectOutput(
            fuel_penalty_s=penalty_s,
            fuel_load_kg=fuel_load_kg
        )
    
    def calculate_stint_fuel_effect(
        self,
        stint_length: int,
        initial_fuel_kg: float = None,
        fuel_per_lap: float = None
    ) -> Dict[str, Any]:
        """
        Calculate fuel effect evolution over a stint.
        
        Args:
            stint_length: Number of laps in stint
            initial_fuel_kg: Starting fuel load (if None, calculates from stint length)
            fuel_per_lap: Fuel consumption rate (kg/lap)
            
        Returns:
            Dict with fuel progression and average penalty
        """
        if fuel_per_lap is None:
            fuel_per_lap = self.AVG_FUEL_PER_LAP
        
        # Calculate initial fuel if not provided
        if initial_fuel_kg is None:
            initial_fuel_kg = min(stint_length * fuel_per_lap, self.MAX_FUEL_CAPACITY)
        
        fuel_penalties = []
        current_fuel = initial_fuel_kg
        
        for lap in range(stint_length):
            result = self.calculate(fuel_load_kg=current_fuel)
            fuel_penalties.append(result.fuel_penalty_s)
            
            # Consume fuel
            current_fuel = max(0.0, current_fuel - fuel_per_lap)
        
        # Calculate average penalty over stint
        avg_penalty = sum(fuel_penalties) / max(len(fuel_penalties), 1)
        
        # Calculate fuel saving (first lap vs last lap)
        fuel_saving = fuel_penalties[0] - fuel_penalties[-1] if fuel_penalties else 0.0
        
        return {
            'lap_penalties': fuel_penalties,
            'average_penalty_s': avg_penalty,
            'total_fuel_effect_reduction_s': fuel_saving,
            'initial_fuel_kg': initial_fuel_kg,
            'final_fuel_kg': current_fuel
        }
    
    def estimate_laps_remaining(
        self,
        current_fuel_kg: float,
        fuel_per_lap: float = None
    ) -> int:
        """
        Estimate how many laps can be completed with current fuel.
        
        Args:
            current_fuel_kg: Current fuel load
            fuel_per_lap: Fuel consumption rate
            
        Returns:
            Estimated laps remaining
        """
        if fuel_per_lap is None:
            fuel_per_lap = self.AVG_FUEL_PER_LAP
        
        if fuel_per_lap <= 0:
            return 0
        
        laps_remaining = int(current_fuel_kg / fuel_per_lap)
        return max(0, laps_remaining)


# Singleton instance
fuel_effect_calc = FuelEffectCalculation()
