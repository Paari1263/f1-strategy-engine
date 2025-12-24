"""
Gap Projection Calculation
Projects time gap evolution between cars

LOGIC:
  Linear gap evolution model:
  - Closing rate = pace delta between cars (s/lap)
  - Projected gap = current_gap - (closing_rate * laps_remaining)
  - Calculates laps to catch if closing
  - Includes undercut viability assessment (gap < pit_loss)

ROLE:
  Future state prediction. Determines if chase is viable and
  when catch will occur. Core calculation for strategy decisions.

SIGNIFICANCE:
  Essential for undercut/overcut timing. If gap < pit loss, undercut
  is viable. If closing rate shows catch in 10 laps, informs
  urgency of response. Fundamental to race strategy dynamics.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_input_models import GapProjectionInput
from calculation_engines.interfaces.calculation_output_models import GapProjectionOutput
from typing import Dict, Any


class GapProjectionCalculation(BaseCalculation):
    """
    Project how gap between cars will evolve.
    
    Used for:
    - Undercut/overcut decisions
    - Catchup probability
    - Defending position
    """
    
    @property
    def calculation_name(self) -> str:
        return "gap_projection"
    
    @property
    def description(self) -> str:
        return "Projects time gap evolution between cars"
    
    def validate_inputs(
        self,
        current_gap_s: float = None,
        pace_delta_s: float = None,
        **kwargs
    ) -> bool:
        """Validate gap and pace inputs"""
        return current_gap_s is not None and pace_delta_s is not None
    
    def calculate(
        self,
        current_gap_s: float,
        pace_delta_s: float,
        laps_remaining: int,
        **kwargs
    ) -> GapProjectionOutput:
        """
        Project gap evolution.
        
        Args:
            current_gap_s: Current time gap (seconds, positive = ahead)
            pace_delta_s: Pace difference per lap (positive = faster)
            laps_remaining: Laps left to project
            **kwargs: Additional parameters
            
        Returns:
            GapProjectionOutput with projected gap
        """
        # Calculate closing rate (how much gap closes per lap)
        closing_rate_s_per_lap = pace_delta_s
        
        # Project gap at race end
        projected_gap_s = current_gap_s - (closing_rate_s_per_lap * laps_remaining)
        
        # Calculate laps to catch/escape
        if abs(closing_rate_s_per_lap) > 0.01:
            laps_to_catch = abs(current_gap_s / closing_rate_s_per_lap)
            
            # Will they catch before race ends?
            if closing_rate_s_per_lap > 0 and laps_to_catch < laps_remaining:
                laps_to_catch_actual = int(laps_to_catch)
            else:
                laps_to_catch_actual = None
        else:
            laps_to_catch_actual = None  # Gap stable
        
        return GapProjectionOutput(
            projected_gap_s=projected_gap_s,
            closing_rate_s_per_lap=closing_rate_s_per_lap,
            laps_to_catch=laps_to_catch_actual
        )
    
    def evaluate_undercut_viability(
        self,
        gap_to_car_ahead_s: float,
        pit_loss_s: float,
        new_tyre_advantage_s: float,
        laps_until_opponent_pits: int
    ) -> Dict[str, Any]:
        """
        Evaluate if undercut will work.
        
        Args:
            gap_to_car_ahead_s: Current gap to car ahead
            pit_loss_s: Time lost in pit stop
            new_tyre_advantage_s: Pace advantage on fresh tyres per lap
            laps_until_opponent_pits: How many laps until they pit
            
        Returns:
            Dict with undercut viability
        """
        # After pitting, we're behind by: gap + pit_loss
        gap_after_pit = gap_to_car_ahead_s + pit_loss_s
        
        # We gain new_tyre_advantage per lap while they're still out
        time_gained = new_tyre_advantage_s * laps_until_opponent_pits
        
        # When they pit, we gain another pit_loss
        time_gained += pit_loss_s
        
        # Net position after both have pitted
        net_gap = gap_after_pit - time_gained
        
        if net_gap < 0:
            outcome = "successful_undercut"
            position_change = "gained"
        elif net_gap < 2.0:
            outcome = "marginal"
            position_change = "very_close"
        else:
            outcome = "failed"
            position_change = "lost"
        
        return {
            'outcome': outcome,
            'position_change': position_change,
            'net_gap_s': net_gap,
            'time_gained_s': time_gained,
            'viability': 'high' if net_gap < -1.0 else 'medium' if net_gap < 1.0 else 'low'
        }


# Singleton instance
gap_projection_calc = GapProjectionCalculation()
