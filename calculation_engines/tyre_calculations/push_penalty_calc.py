"""
Push Penalty Calculation
Calculates additional tyre degradation from aggressive driving

LOGIC:
  Aggressive driving increases degradation exponentially:
  - Push level 0.0 (coasting) = 1.0x degradation
  - Push level 1.0 (maximum attack) = 1.5x degradation
  - Linear interpolation between levels
  Also estimates total stint life reduction in laps

ROLE:
  Models driver behavior impact on tyre management. Enables
  simulation of attack/defend scenarios and fuel saving modes.

SIGNIFICANCE:
  Critical for tactical decisions - determines cost of pushing to
  close gaps, defend position, or build safety margin. Balances
  short-term pace gain vs long-term tyre preservation.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import PushPenaltyOutput
from typing import Dict, Any


class PushPenaltyCalculation(BaseCalculation):
    """
    Calculate degradation penalty from pushing tyres hard.
    
    Aggressive driving (qualifying pace in race, overtaking pushes) 
    increases tyre degradation rate.
    """
    
    # Maximum degradation multiplier from maximum push
    MAX_PUSH_MULTIPLIER = 1.5  # 50% faster degradation when pushing flat out
    
    @property
    def calculation_name(self) -> str:
        return "push_penalty"
    
    @property
    def description(self) -> str:
        return "Calculates tyre degradation penalty from aggressive driving"
    
    def validate_inputs(self, push_level: float = None, **kwargs) -> bool:
        """Validate push level is in valid range"""
        if push_level is None:
            return False
        return 0.0 <= push_level <= 1.0
    
    def calculate(
        self,
        push_level: float,
        base_stint_length: int = 20,
        **kwargs
    ) -> PushPenaltyOutput:
        """
        Calculate push penalty multiplier.
        
        Args:
            push_level: Intensity of push (0.0 = cruising, 1.0 = maximum attack)
            base_stint_length: Expected stint length without pushing (laps)
            **kwargs: Additional parameters
            
        Returns:
            PushPenaltyOutput with degradation multiplier
        """
        # Clamp push_level to valid range
        push_level = max(0.0, min(1.0, push_level))
        
        # Calculate degradation multiplier
        # Linear relationship: 1.0 at push_level=0, MAX_PUSH_MULTIPLIER at push_level=1
        multiplier = 1.0 + (push_level * (self.MAX_PUSH_MULTIPLIER - 1.0))
        
        # Estimate life reduction in laps
        life_reduction = int(base_stint_length * (multiplier - 1.0))
        
        return PushPenaltyOutput(
            push_multiplier=multiplier,
            estimated_life_reduction_laps=life_reduction
        )
    
    def calculate_sustained_push_effect(
        self,
        push_level: float,
        push_duration_laps: int,
        total_stint_laps: int
    ) -> float:
        """
        Calculate overall stint degradation multiplier from sustained push.
        
        Args:
            push_level: Push intensity
            push_duration_laps: How many laps pushing
            total_stint_laps: Total stint length
            
        Returns:
            Effective degradation multiplier for entire stint
        """
        if total_stint_laps == 0:
            return 1.0
        
        # Calculate multiplier for push period
        push_mult = 1.0 + (push_level * (self.MAX_PUSH_MULTIPLIER - 1.0))
        
        # Normal pace for remaining laps
        normal_laps = total_stint_laps - push_duration_laps
        
        # Weighted average
        effective_mult = (
            (push_mult * push_duration_laps + 1.0 * normal_laps) / 
            total_stint_laps
        )
        
        return effective_mult


# Singleton instance
push_penalty_calc = PushPenaltyCalculation()
