"""
Defense Effectiveness Calculation
Evaluates ability to hold position under attack

LOGIC:
  Composite effectiveness rating (0-10) from:
  - Track overtaking difficulty (50% weight)
  - Car straight-line speed (30% - defend on straights)
  - Driver defensive skill (20% - positioning ability)
  Higher rating = harder to pass

ROLE:
  Position holding assessment. Determines if car can realistically
  defend position or will lose it regardless of strategy.

SIGNIFICANCE:
  Influences whether to prioritize track position or pace.
  Low effectiveness = favor pace-based strategies. High
  effectiveness enables aggressive position-defense strategies.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import DefenseEffectivenessOutput
from typing import Dict, Any


class DefenseEffectivenessCalculation(BaseCalculation):
    """
    Calculate defensive position holding effectiveness.
    
    Combines:
    - Track overtaking difficulty
    - Car characteristics
    - Driver defensive skill
    """
    
    @property
    def calculation_name(self) -> str:
        return "defense_effectiveness"
    
    @property
    def description(self) -> str:
        return "Evaluates ability to hold position under attack"
    
    def validate_inputs(
        self,
        overtaking_difficulty: float = None,
        **kwargs
    ) -> bool:
        """Validate difficulty parameter"""
        if overtaking_difficulty is None:
            return False
        return 0.0 <= overtaking_difficulty <= 10.0
    
    def calculate(
        self,
        overtaking_difficulty: float,
        car_straight_speed: float = 5.0,
        driver_defensive_skill: float = 5.0,
        **kwargs
    ) -> DefenseEffectivenessOutput:
        """
        Calculate defense effectiveness.
        
        Args:
            overtaking_difficulty: Track overtaking difficulty (0-10)
            car_straight_speed: Car's straight line speed (0-10)
            driver_defensive_skill: Driver's defensive ability (0-10)
            **kwargs: Additional parameters
            
        Returns:
            DefenseEffectivenessOutput with effectiveness rating
        """
        # Clamp inputs
        overtaking_difficulty = max(0.0, min(10.0, overtaking_difficulty))
        car_straight_speed = max(0.0, min(10.0, car_straight_speed))
        driver_defensive_skill = max(0.0, min(10.0, driver_defensive_skill))
        
        # Track difficulty contributes 50%
        track_component = overtaking_difficulty * 0.50
        
        # Car speed contributes 30% (faster in straight = harder to overtake)
        car_component = car_straight_speed * 0.30
        
        # Driver skill contributes 20%
        driver_component = driver_defensive_skill * 0.20
        
        # Calculate effectiveness (0-10, higher = harder to overtake)
        effectiveness = track_component + car_component + driver_component
        
        # Clamp
        effectiveness = max(0.0, min(10.0, effectiveness))
        
        return DefenseEffectivenessOutput(
            effectiveness_rating=effectiveness
        )
    
    def estimate_defense_duration(
        self,
        effectiveness: float,
        pace_deficit_s: float
    ) -> Dict[str, Any]:
        """
        Estimate how many laps position can be held.
        
        Args:
            effectiveness: Defense effectiveness (0-10)
            pace_deficit_s: Pace disadvantage per lap (seconds, positive = slower)
            
        Returns:
            Dict with defense duration estimate
        """
        if pace_deficit_s <= 0:
            # Faster or equal pace - can defend indefinitely
            return {
                'laps_held': 999,
                'outcome': 'indefinite',
                'reasoning': 'Equal or faster pace'
            }
        
        # High effectiveness (8+) = hold for many laps even with deficit
        # Low effectiveness (2-) = lose position quickly
        
        # Base laps = effectiveness * 2
        base_laps = effectiveness * 2
        
        # Pace deficit penalty
        # 0.1s deficit = -1 lap, 0.5s deficit = -5 laps
        pace_penalty = pace_deficit_s * 10
        
        laps_can_hold = max(0, int(base_laps - pace_penalty))
        
        if laps_can_hold == 0:
            outcome = 'immediate_loss'
        elif laps_can_hold < 3:
            outcome = 'brief_defense'
        elif laps_can_hold < 8:
            outcome = 'moderate_defense'
        else:
            outcome = 'strong_defense'
        
        return {
            'laps_held': laps_can_hold,
            'outcome': outcome,
            'effectiveness': effectiveness,
            'pace_deficit_s': pace_deficit_s
        }


# Singleton instance
defense_effectiveness_calc = DefenseEffectivenessCalculation()
