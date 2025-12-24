"""
Error Risk Calculation
Predicts likelihood of driver mistakes under pressure

LOGIC:
  Multi-factor error probability model:
  - Base: pressure_level * 0.01 (1% per pressure unit)
  - Fatigue multiplier: 1.0 + fatigue_factor
  - Track difficulty multiplier: 1.0 + track_difficulty
  - Driver proneness factor (default 1.0)
  Combined probability per lap

ROLE:
  Risk assessment for high-pressure situations. Models increased
  mistake likelihood when defending/attacking or late in race.

SIGNIFICANCE:
  Influences strategy decisions about when to push vs when to
  consolidate. High error risk may favor conservative approach.
  Critical for Safety Car restart and final lap scenarios.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import ErrorRiskOutput
from typing import Dict, Any


class ErrorRiskCalculation(BaseCalculation):
    """
    Calculate driver error probability.
    
    Factors affecting error risk:
    - Pressure level (wheel-to-wheel racing, championship pressure)
    - Fatigue (stint length, race duration)
    - Track difficulty
    - Driver's error history
    """
    
    # Base error rates (errors per 100 laps)
    BASE_ERROR_RATE = 2.0  # Average driver makes mistake every 50 laps
    
    @property
    def calculation_name(self) -> str:
        return "error_risk"
    
    @property
    def description(self) -> str:
        return "Predicts likelihood of driver mistakes under pressure"
    
    def validate_inputs(
        self,
        pressure_level: float = None,
        **kwargs
    ) -> bool:
        """Validate pressure parameter"""
        if pressure_level is None:
            return False
        return 0.0 <= pressure_level <= 1.0
    
    def calculate(
        self,
        pressure_level: float,
        fatigue_factor: float = 0.0,
        track_difficulty: float = 0.5,
        driver_error_proneness: float = 1.0,
        **kwargs
    ) -> ErrorRiskOutput:
        """
        Calculate error probability.
        
        Args:
            pressure_level: Situational pressure (0=none, 1=maximum)
            fatigue_factor: Driver fatigue (0=fresh, 1=exhausted)
            track_difficulty: Track's error-punishing nature (0-1)
            driver_error_proneness: Driver's error tendency (1.0=average, <1=better, >1=worse)
            **kwargs: Additional parameters
            
        Returns:
            ErrorRiskOutput with error probability
        """
        # Clamp inputs
        pressure_level = max(0.0, min(1.0, pressure_level))
        fatigue_factor = max(0.0, min(1.0, fatigue_factor))
        track_difficulty = max(0.0, min(1.0, track_difficulty))
        driver_error_proneness = max(0.1, min(3.0, driver_error_proneness))
        
        # Calculate pressure multiplier
        # Low pressure (0.0): 0.5x error rate
        # Medium pressure (0.5): 1.0x error rate
        # High pressure (1.0): 2.0x error rate
        pressure_multiplier = 0.5 + (pressure_level * 1.5)
        
        # Fatigue multiplier
        # Fresh (0.0): 1.0x
        # Tired (1.0): 1.5x
        fatigue_multiplier = 1.0 + (fatigue_factor * 0.5)
        
        # Track multiplier
        # Easy track (0.0): 0.7x
        # Difficult track (1.0): 1.3x
        track_multiplier = 0.7 + (track_difficulty * 0.6)
        
        # Calculate overall error probability (per lap)
        error_rate_per_100_laps = (
            self.BASE_ERROR_RATE *
            pressure_multiplier *
            fatigue_multiplier *
            track_multiplier *
            driver_error_proneness
        )
        
        # Convert to probability per lap
        error_probability_per_lap = error_rate_per_100_laps / 100.0
        
        # Clamp to reasonable range
        error_probability_per_lap = max(0.0, min(0.2, error_probability_per_lap))
        
        # Classify risk level
        if error_probability_per_lap < 0.01:
            risk_level = "low"
        elif error_probability_per_lap < 0.03:
            risk_level = "medium"
        elif error_probability_per_lap < 0.06:
            risk_level = "high"
        else:
            risk_level = "critical"
        
        return ErrorRiskOutput(
            error_probability_per_lap=error_probability_per_lap,
            risk_level=risk_level
        )
    
    def calculate_stint_error_probability(
        self,
        pressure_level: float,
        stint_length: int,
        fatigue_factor: float = 0.0,
        track_difficulty: float = 0.5,
        driver_error_proneness: float = 1.0
    ) -> Dict[str, Any]:
        """
        Calculate probability of at least one error in stint.
        
        Args:
            pressure_level: Pressure level
            stint_length: Number of laps in stint
            fatigue_factor: Fatigue level
            track_difficulty: Track difficulty
            driver_error_proneness: Driver error tendency
            
        Returns:
            Dict with stint error analysis
        """
        result = self.calculate(
            pressure_level=pressure_level,
            fatigue_factor=fatigue_factor,
            track_difficulty=track_difficulty,
            driver_error_proneness=driver_error_proneness
        )
        
        # Probability of NO error in stint: (1 - p)^n
        # Probability of AT LEAST ONE error: 1 - (1 - p)^n
        p_no_error_stint = (1.0 - result.error_probability_per_lap) ** stint_length
        p_error_in_stint = 1.0 - p_no_error_stint
        
        # Expected number of errors
        expected_errors = result.error_probability_per_lap * stint_length
        
        return {
            'error_probability_per_lap': result.error_probability_per_lap,
            'error_probability_stint': p_error_in_stint,
            'expected_errors': expected_errors,
            'risk_level': result.risk_level,
            'stint_length': stint_length
        }


# Singleton instance
error_risk_calc = ErrorRiskCalculation()
