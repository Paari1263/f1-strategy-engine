"""
Crossover Lap Calculation
Determines when to switch tyre compounds in changing conditions

LOGIC:
  Finds intersection point where compound B becomes faster:
  - Compound A pace degrades over time
  - Compound B starts slower but degrades slower
  - Crossover = lap where pace_A > pace_B
  - Considers degradation rate differences

ROLE:
  Optimal compound switch timing. Critical for mixed weather
  strategy (inter to slick, soft to hard transitions).

SIGNIFICANCE:
  Game-critical in changing conditions. Switching too early =
  slow pace on suboptimal compound. Too late = losing time on
  degraded tyres. Can determine race outcome in transitional weather.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import CrossoverLapOutput
from typing import Dict, Any, Optional


class CrossoverLapCalculation(BaseCalculation):
    """
    Calculate tyre compound crossover point.
    
    Crossover = lap when one compound becomes faster than another
    due to degradation or weather changes
    """
    
    @property
    def calculation_name(self) -> str:
        return "crossover_lap"
    
    @property
    def description(self) -> str:
        return "Determines when to switch tyre compounds"
    
    def validate_inputs(
        self,
        compound_a_initial_pace: float = None,
        compound_b_initial_pace: float = None,
        **kwargs
    ) -> bool:
        """Validate pace inputs"""
        if compound_a_initial_pace is None or compound_b_initial_pace is None:
            return False
        return compound_a_initial_pace > 0 and compound_b_initial_pace > 0
    
    def calculate(
        self,
        compound_a_initial_pace: float,
        compound_b_initial_pace: float,
        compound_a_deg_rate: float = 0.05,
        compound_b_deg_rate: float = 0.03,
        **kwargs
    ) -> CrossoverLapOutput:
        """
        Calculate crossover lap.
        
        Args:
            compound_a_initial_pace: Compound A initial lap time (s)
            compound_b_initial_pace: Compound B initial lap time (s)
            compound_a_deg_rate: Compound A degradation (s/lap/lap)
            compound_b_deg_rate: Compound B degradation (s/lap/lap)
            **kwargs: Additional parameters
            
        Returns:
            CrossoverLapOutput with crossover point
        """
        # Typically: Soft is faster initially but degrades faster
        # Hard is slower initially but degrades slower
        
        # If A starts faster (lower lap time)
        if compound_a_initial_pace < compound_b_initial_pace:
            pace_advantage = compound_b_initial_pace - compound_a_initial_pace
            
            # If A also degrades slower, it's always better
            if compound_a_deg_rate <= compound_b_deg_rate:
                return CrossoverLapOutput(
                    crossover_lap=None,
                    compound_a_faster_until=None,
                    compound_b_faster_from=None
                )
            
            # Calculate when degradation difference overcomes initial advantage
            # Pace A = initial_a + (lap * deg_a)
            # Pace B = initial_b + (lap * deg_b)
            # Crossover when: initial_a + lap*deg_a = initial_b + lap*deg_b
            # lap = (initial_b - initial_a) / (deg_a - deg_b)
            
            deg_diff = compound_a_deg_rate - compound_b_deg_rate
            if deg_diff > 0:
                crossover_lap = int(pace_advantage / deg_diff)
                crossover_lap = max(1, crossover_lap)
                
                return CrossoverLapOutput(
                    crossover_lap=crossover_lap,
                    compound_a_faster_until=crossover_lap,
                    compound_b_faster_from=crossover_lap + 1
                )
        else:
            # B starts faster
            pace_advantage = compound_a_initial_pace - compound_b_initial_pace
            
            if compound_b_deg_rate <= compound_a_deg_rate:
                # B always better
                return CrossoverLapOutput(
                    crossover_lap=None,
                    compound_a_faster_until=None,
                    compound_b_faster_from=1
                )
            
            deg_diff = compound_b_deg_rate - compound_a_deg_rate
            if deg_diff > 0:
                crossover_lap = int(pace_advantage / deg_diff)
                crossover_lap = max(1, crossover_lap)
                
                return CrossoverLapOutput(
                    crossover_lap=crossover_lap,
                    compound_a_faster_until=None,
                    compound_b_faster_from=crossover_lap + 1
                )
        
        # No crossover
        return CrossoverLapOutput(
            crossover_lap=None,
            compound_a_faster_until=None,
            compound_b_faster_from=None
        )
    
    def optimal_stint_length(
        self,
        crossover_lap: Optional[int],
        max_tyre_life: int,
        race_laps_remaining: int
    ) -> Dict[str, Any]:
        """
        Determine optimal stint length based on crossover.
        
        Args:
            crossover_lap: Lap when compounds cross over
            max_tyre_life: Maximum tyre life
            race_laps_remaining: Laps left in race
            
        Returns:
            Dict with stint recommendation
        """
        if crossover_lap is None:
            # No crossover, run to life limit or race end
            optimal_length = min(max_tyre_life, race_laps_remaining)
            return {
                'optimal_stint_length': optimal_length,
                'reasoning': 'No crossover point, maximize stint'
            }
        
        # Stop before crossover if possible
        if crossover_lap < max_tyre_life:
            return {
                'optimal_stint_length': crossover_lap - 1,
                'reasoning': f'Stop before crossover at lap {crossover_lap}'
            }
        else:
            return {
                'optimal_stint_length': max_tyre_life,
                'reasoning': 'Run to tyre life before crossover'
            }


# Singleton instance
crossover_lap_calc = CrossoverLapCalculation()
