"""
Pit Window Calculation
Determines optimal pit stop timing window

LOGIC:
  Optimal window based on tyre life:
  - Opens at 60% of expected tyre life
  - Closes at 85% of expected tyre life
  - Optimal lap at 70-75% (middle of window)
  - Adjusted for traffic and race position

ROLE:
  Pit timing optimization. Balances extracting tyre life vs
  avoiding tyre cliff. Prevents too-early or too-late stops.

SIGNIFICANCE:
  Core strategy tool. Stopping outside window either wastes
  tyre life (too early) or risks cliff/damage (too late).
  Traffic considerations may override pure tyre-based timing.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import PitWindowOutput
from typing import Dict, Any, Optional


class PitWindowCalculation(BaseCalculation):
    """
    Calculate optimal pit window.
    
    Considers:
    - Tyre life limits
    - Undercut/overcut opportunities
    - Traffic avoidance
    - Race position
    """
    
    @property
    def calculation_name(self) -> str:
        return "pit_window"
    
    @property
    def description(self) -> str:
        return "Determines optimal pit stop timing window"
    
    def validate_inputs(
        self,
        current_tyre_age: int = None,
        expected_tyre_life: int = None,
        **kwargs
    ) -> bool:
        """Validate tyre parameters"""
        if current_tyre_age is None or expected_tyre_life is None:
            return False
        return current_tyre_age >= 0 and expected_tyre_life > 0
    
    def calculate(
        self,
        current_tyre_age: int,
        expected_tyre_life: int,
        race_laps: int,
        current_lap: int,
        **kwargs
    ) -> PitWindowOutput:
        """
        Calculate pit window.
        
        Args:
            current_tyre_age: Laps on current tyres
            expected_tyre_life: Expected total tyre life
            race_laps: Total race distance
            current_lap: Current lap number
            **kwargs: Additional parameters
            
        Returns:
            PitWindowOutput with pit window
        """
        # Calculate earliest pit lap (minimum stint length)
        # Don't pit too early (waste tyre life)
        min_stint = max(10, int(expected_tyre_life * 0.6))
        earliest_lap = current_lap + max(0, min_stint - current_tyre_age)
        
        # Calculate latest pit lap (before tyre failure)
        # Leave safety margin (85% of expected life)
        max_safe_stint = int(expected_tyre_life * 0.85)
        latest_lap = current_lap + max(0, max_safe_stint - current_tyre_age)
        
        # Optimal lap (middle of window, biased toward later)
        optimal_lap = int((earliest_lap + latest_lap * 2) / 3)
        
        # Ensure window is valid
        if earliest_lap > race_laps or latest_lap > race_laps:
            # Can't pit, must go to end
            return PitWindowOutput(
                optimal_lap=None,
                window_opens_lap=None,
                window_closes_lap=None
            )
        
        # Clamp to race length
        earliest_lap = min(earliest_lap, race_laps - 2)
        latest_lap = min(latest_lap, race_laps - 2)
        optimal_lap = min(optimal_lap, race_laps - 2)
        
        return PitWindowOutput(
            optimal_lap=optimal_lap,
            window_opens_lap=earliest_lap,
            window_closes_lap=latest_lap
        )
    
    def adjust_for_traffic(
        self,
        optimal_lap: Optional[int],
        traffic_laps: list,
        window_flexibility: int = 3
    ) -> Dict[str, Any]:
        """
        Adjust pit timing to avoid traffic.
        
        Args:
            optimal_lap: Calculated optimal lap
            traffic_laps: Laps where traffic is expected
            window_flexibility: How many laps we can shift
            
        Returns:
            Dict with adjusted pit lap
        """
        if optimal_lap is None:
            return {'adjusted_lap': None, 'reason': 'No pit required'}
        
        # Check if optimal lap has traffic
        if optimal_lap not in traffic_laps:
            return {
                'adjusted_lap': optimal_lap,
                'reason': 'Optimal lap is clear'
            }
        
        # Try to find clear lap within window
        for offset in range(1, window_flexibility + 1):
            # Try later first (preserve tyre life)
            later_lap = optimal_lap + offset
            if later_lap not in traffic_laps:
                return {
                    'adjusted_lap': later_lap,
                    'reason': f'Delayed {offset} laps to avoid traffic'
                }
            
            # Try earlier
            earlier_lap = optimal_lap - offset
            if earlier_lap not in traffic_laps and earlier_lap > 0:
                return {
                    'adjusted_lap': earlier_lap,
                    'reason': f'Advanced {offset} laps to avoid traffic'
                }
        
        # No clear window found
        return {
            'adjusted_lap': optimal_lap,
            'reason': 'No clear window available, accepting traffic'
        }


# Singleton instance
pit_window_calc = PitWindowCalculation()
