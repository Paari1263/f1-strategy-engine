"""
Overtake Cost Calculation
Calculates time/resource cost of overtaking maneuver

LOGIC:
  Two-component cost model:
  - Time cost: dirty air penalty * laps in battle
  - Tyre cost: push degradation * battle duration (in lap equivalents)
  Total cost determines if overtake is worth attempting

ROLE:
  Battle cost-benefit analysis. Quantifies resource expenditure
  for position gain. Enables rational attack/defend decisions.

SIGNIFICANCE:
  Critical for evaluating if chasing position is strategically
  sound. 3-lap battle costing 1.5s + 2 laps tyre life may not
  be worth one position. Influences aggressive vs conservative calls.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import OvertakeCostOutput
from typing import Dict, Any


class OvertakeCostCalculation(BaseCalculation):
    """
    Calculate cost of attempting overtake.
    
    Costs:
    - Time spent in dirty air
    - Tyre degradation from pushing
    - Fuel consumption
    - Risk of damage/incident
    """
    
    @property
    def calculation_name(self) -> str:
        return "overtake_cost"
    
    @property
    def description(self) -> str:
        return "Calculates time/resource cost of overtaking maneuver"
    
    def validate_inputs(
        self,
        laps_in_battle: int = None,
        **kwargs
    ) -> bool:
        """Validate battle duration"""
        if laps_in_battle is None:
            return False
        return laps_in_battle >= 0
    
    def calculate(
        self,
        laps_in_battle: int,
        dirty_air_penalty_s: float = 0.3,
        push_degradation_multiplier: float = 1.2,
        **kwargs
    ) -> OvertakeCostOutput:
        """
        Calculate overtake cost.
        
        Args:
            laps_in_battle: Number of laps spent trying to overtake
            dirty_air_penalty_s: Lap time loss per lap in dirty air
            push_degradation_multiplier: Tyre deg multiplier from pushing
            **kwargs: Additional parameters
            
        Returns:
            OvertakeCostOutput with cost breakdown
        """
        # Clamp inputs
        laps_in_battle = max(0, laps_in_battle)
        dirty_air_penalty_s = max(0.0, min(1.0, dirty_air_penalty_s))
        push_degradation_multiplier = max(1.0, min(2.0, push_degradation_multiplier))
        
        # Time cost from dirty air
        time_cost_s = laps_in_battle * dirty_air_penalty_s
        
        # Tyre life cost (laps of life lost due to pushing)
        # 1.2x degradation over 3 laps = ~0.6 laps of life lost
        extra_degradation = push_degradation_multiplier - 1.0  # e.g., 0.2 for 1.2x
        tyre_life_cost_laps = laps_in_battle * extra_degradation
        
        return OvertakeCostOutput(
            time_cost_s=time_cost_s,
            tyre_life_cost_laps=tyre_life_cost_laps
        )
    
    def evaluate_overtake_viability(
        self,
        time_cost_s: float,
        tyre_life_cost_laps: float,
        expected_time_gain_s: float,
        remaining_stint_laps: int
    ) -> Dict[str, Any]:
        """
        Evaluate if overtake attempt is worthwhile.
        
        Args:
            time_cost_s: Time lost attempting overtake
            tyre_life_cost_laps: Tyre life lost
            expected_time_gain_s: Expected time gain if successful
            remaining_stint_laps: Laps remaining in stint
            
        Returns:
            Dict with viability assessment
        """
        # Net time benefit (if successful)
        net_time_s = expected_time_gain_s - time_cost_s
        
        # Check if tyre life cost is sustainable
        tyre_sustainable = tyre_life_cost_laps < (remaining_stint_laps * 0.2)
        
        # Overall recommendation
        if net_time_s > 5.0 and tyre_sustainable:
            recommendation = "highly_recommended"
            reason = "Large time gain with acceptable tyre cost"
        elif net_time_s > 0 and tyre_sustainable:
            recommendation = "recommended"
            reason = "Positive time gain, manageable tyre cost"
        elif not tyre_sustainable:
            recommendation = "not_recommended"
            reason = "Excessive tyre degradation risk"
        else:
            recommendation = "marginal"
            reason = "Minimal benefit, consider track position value"
        
        return {
            'recommendation': recommendation,
            'reason': reason,
            'net_time_gain_s': net_time_s,
            'tyre_sustainable': tyre_sustainable,
            'tyre_life_cost_laps': tyre_life_cost_laps
        }


# Singleton instance
overtake_cost_calc = OvertakeCostCalculation()
