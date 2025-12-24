"""
Safety Car Probability Calculation
Predicts likelihood of safety car deployment

LOGIC:
  Risk assessment from multiple factors:
  - Barrier proximity (tight tracks = higher risk)
  - Weather risk (rain increases incident probability)
  - Field competitiveness (close racing = more contact)
  - Historical incident rate at circuit
  Combined probability estimate

ROLE:
  Strategic uncertainty modeling. SC deployment dramatically
  changes optimal strategy. Enables probabilistic planning.

SIGNIFICANCE:
  Game-changing event in race strategy. High SC probability
  may favor later pit stops or aggressive early strategies.
  Critical for understanding strategy risk/reward.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import SafetyCarProbabilityOutput
from typing import Dict, Any


class SafetyCarProbabilityCalculation(BaseCalculation):
    """
    Calculate safety car probability.
    
    Factors:
    - Track characteristics (barriers, runoff)
    - Historical SC rate
    - Weather conditions
    - Field competitiveness
    """
    
    # Base probability for average track
    BASE_SC_PROBABILITY = 0.30  # 30% chance in typical race
    
    @property
    def calculation_name(self) -> str:
        return "safety_car_probability"
    
    @property
    def description(self) -> str:
        return "Predicts likelihood of safety car deployment"
    
    def validate_inputs(self, **kwargs) -> bool:
        """All inputs have defaults"""
        return True
    
    def calculate(
        self,
        barrier_proximity: float = 0.5,
        historical_sc_rate: float = None,
        weather_risk: float = 0.0,
        field_competitiveness: float = 0.5,
        **kwargs
    ) -> SafetyCarProbabilityOutput:
        """
        Calculate safety car probability.
        
        Args:
            barrier_proximity: How close barriers are (0-1, higher = more likely)
            historical_sc_rate: Track's historical SC rate (0-1, overrides base)
            weather_risk: Weather risk factor (0-1, higher = more likely)
            field_competitiveness: Field spread (0-1, tighter = more incidents)
            **kwargs: Additional parameters
            
        Returns:
            SafetyCarProbabilityOutput with probability
        """
        # Clamp inputs
        barrier_proximity = max(0.0, min(1.0, barrier_proximity))
        weather_risk = max(0.0, min(1.0, weather_risk))
        field_competitiveness = max(0.0, min(1.0, field_competitiveness))
        
        # Use historical rate if provided, else calculate
        if historical_sc_rate is not None:
            base_prob = max(0.0, min(1.0, historical_sc_rate))
        else:
            base_prob = self.BASE_SC_PROBABILITY
        
        # Barrier proximity multiplier
        # Monaco (1.0) = 2.0x, Open track (0.0) = 0.5x
        barrier_multiplier = 0.5 + (barrier_proximity * 1.5)
        
        # Weather multiplier
        # Dry (0.0) = 1.0x, Wet (1.0) = 2.5x
        weather_multiplier = 1.0 + (weather_risk * 1.5)
        
        # Field competitiveness multiplier
        # Spread out field (0.0) = 0.8x, Tight field (1.0) = 1.3x
        competition_multiplier = 0.8 + (field_competitiveness * 0.5)
        
        # Calculate overall probability
        sc_probability = (
            base_prob *
            barrier_multiplier *
            weather_multiplier *
            competition_multiplier
        )
        
        # Clamp to 0-1
        sc_probability = max(0.0, min(1.0, sc_probability))
        
        return SafetyCarProbabilityOutput(
            probability=sc_probability
        )
    
    def estimate_expected_sc_laps(
        self,
        sc_probability: float,
        race_laps: int,
        avg_sc_duration_laps: int = 5
    ) -> Dict[str, Any]:
        """
        Estimate expected SC laps in race.
        
        Args:
            sc_probability: Probability of SC (0-1)
            race_laps: Total race distance
            avg_sc_duration_laps: Average SC period length
            
        Returns:
            Dict with SC expectations
        """
        # Expected number of SC periods
        # Simplified: probability of at least one SC
        expected_sc_periods = sc_probability * 1.5  # Can be multiple SCs
        
        # Expected total SC laps
        expected_sc_laps = int(expected_sc_periods * avg_sc_duration_laps)
        
        # Strategic implications
        if sc_probability > 0.6:
            strategy_note = "High SC risk - consider aggressive strategy"
        elif sc_probability > 0.3:
            strategy_note = "Moderate SC risk - have contingency plans"
        else:
            strategy_note = "Low SC risk - plan for clean race"
        
        return {
            'sc_probability': sc_probability,
            'expected_sc_periods': expected_sc_periods,
            'expected_sc_laps': expected_sc_laps,
            'race_laps': race_laps,
            'strategy_note': strategy_note
        }


# Singleton instance
safety_car_probability_calc = SafetyCarProbabilityCalculation()
