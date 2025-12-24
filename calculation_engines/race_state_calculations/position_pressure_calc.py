"""
Position Pressure Calculation
Evaluates strategic pressure from track position

LOGIC:
  Dual pressure assessment (0-10 scale):
  - Pressure from ahead: gap_ahead / reference_gap (attack opportunity)
  - Pressure from behind: reference_gap / gap_behind (defense urgency)
  - Position multiplier: higher positions = more pressure
  - Combined into single pressure rating

ROLE:
  Strategic urgency quantification. Determines how aggressively
  to pursue position or defend current placement.

SIGNIFICANCE:
  High pressure from behind may force early pit stop to protect
  position. Low pressure enables patient strategy execution.
  P3-P5 often highest pressure zone (podium battle).
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import PositionPressureOutput
from typing import Dict, Any


class PositionPressureCalculation(BaseCalculation):
    """
    Calculate positional pressure.
    
    Pressure from:
    - Car behind (defending)
    - Car ahead (attacking)
    - Championship implications
    """
    
    @property
    def calculation_name(self) -> str:
        return "position_pressure"
    
    @property
    def description(self) -> str:
        return "Evaluates strategic pressure from track position"
    
    def validate_inputs(
        self,
        gap_to_car_ahead_s: float = None,
        gap_to_car_behind_s: float = None,
        **kwargs
    ) -> bool:
        """Validate gap inputs"""
        return gap_to_car_ahead_s is not None or gap_to_car_behind_s is not None
    
    def calculate(
        self,
        gap_to_car_ahead_s: float = 99.0,
        gap_to_car_behind_s: float = 99.0,
        position: int = 10,
        **kwargs
    ) -> PositionPressureOutput:
        """
        Calculate position pressure.
        
        Args:
            gap_to_car_ahead_s: Gap to car ahead (99 = no car)
            gap_to_car_behind_s: Gap to car behind (99 = no car)
            position: Current position (1-20)
            **kwargs: Additional parameters
            
        Returns:
            PositionPressureOutput with pressure rating
        """
        # Attack pressure (wanting to overtake car ahead)
        if gap_to_car_ahead_s < 1.0:
            attack_pressure = 1.0  # Very close, high pressure
        elif gap_to_car_ahead_s < 3.0:
            attack_pressure = 0.7  # Close, moderate pressure
        elif gap_to_car_ahead_s < 5.0:
            attack_pressure = 0.3  # Within reach, some pressure
        else:
            attack_pressure = 0.0  # Too far, no pressure
        
        # Defense pressure (car behind threatening)
        if gap_to_car_behind_s < 1.0:
            defense_pressure = 1.0  # Under immediate threat
        elif gap_to_car_behind_s < 3.0:
            defense_pressure = 0.7  # Close, moderate threat
        elif gap_to_car_behind_s < 5.0:
            defense_pressure = 0.3  # Some threat
        else:
            defense_pressure = 0.0  # Safe
        
        # Position importance (podium/points positions matter more)
        if position <= 3:
            position_importance = 1.0  # Podium
        elif position <= 10:
            position_importance = 0.7  # Points
        else:
            position_importance = 0.3  # Outside points
        
        # Overall pressure (0-10 scale)
        # Max of attack/defense, weighted by position importance
        max_situational_pressure = max(attack_pressure, defense_pressure)
        overall_pressure = max_situational_pressure * position_importance * 10.0
        
        overall_pressure = max(0.0, min(10.0, overall_pressure))
        
        return PositionPressureOutput(
            pressure_rating=overall_pressure
        )
    
    def determine_strategic_mode(
        self,
        pressure_rating: float,
        tyre_age: int,
        expected_tyre_life: int
    ) -> Dict[str, Any]:
        """
        Determine strategic mode based on pressure.
        
        Args:
            pressure_rating: Position pressure (0-10)
            tyre_age: Current tyre age
            expected_tyre_life: Expected tyre life
            
        Returns:
            Dict with strategic mode
        """
        # Calculate tyre condition
        tyre_condition = 1.0 - (tyre_age / max(expected_tyre_life, 1))
        
        # High pressure + good tyres = attack mode
        # High pressure + worn tyres = defend mode
        # Low pressure = manage mode
        
        if pressure_rating > 7.0:
            if tyre_condition > 0.5:
                mode = "attack"
                reason = "High pressure, good tyres - push for position"
            else:
                mode = "defend"
                reason = "High pressure, worn tyres - hold position"
        elif pressure_rating > 4.0:
            mode = "balanced"
            reason = "Moderate pressure - balanced approach"
        else:
            mode = "manage"
            reason = "Low pressure - manage tyres and fuel"
        
        return {
            'mode': mode,
            'reason': reason,
            'pressure_rating': pressure_rating,
            'tyre_condition': tyre_condition
        }


# Singleton instance
position_pressure_calc = PositionPressureCalculation()
