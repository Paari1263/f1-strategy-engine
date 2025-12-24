"""
Weather Volatility Calculation
Assesses weather unpredictability and risk

LOGIC:
  Multi-factor volatility score (0-1):
  - Forecast confidence (inverted - low confidence = high volatility)
  - Cloud cover instability
  - Wind variability
  - Historical weather patterns at circuit
  Combined into single risk metric

ROLE:
  Weather uncertainty quantification. Determines reliability
  of weather-based strategy decisions.

SIGNIFICANCE:
  High volatility = higher strategy risk. May favor conservative
  approach or have backup compound ready. Critical for deciding
  between committed dry/wet strategy vs flexible approach.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import WeatherVolatilityOutput
from typing import Dict, Any


class WeatherVolatilityCalculation(BaseCalculation):
    """
    Calculate weather volatility and change probability.
    
    High volatility = unpredictable conditions, high strategic risk
    """
    
    @property
    def calculation_name(self) -> str:
        return "weather_volatility"
    
    @property
    def description(self) -> str:
        return "Assesses weather unpredictability and risk"
    
    def validate_inputs(
        self,
        forecast_confidence: float = None,
        **kwargs
    ) -> bool:
        """Validate confidence input"""
        if forecast_confidence is None:
            return False
        return 0.0 <= forecast_confidence <= 1.0
    
    def calculate(
        self,
        forecast_confidence: float,
        cloud_cover: float = 0.5,
        wind_variability: float = 0.3,
        historical_volatility: float = 0.5,
        **kwargs
    ) -> WeatherVolatilityOutput:
        """
        Calculate weather volatility.
        
        Args:
            forecast_confidence: Weather forecast confidence (0-1, higher = more certain)
            cloud_cover: Cloud coverage (0-1)
            wind_variability: Wind speed variability (0-1)
            historical_volatility: Track's historical weather variability (0-1)
            **kwargs: Additional parameters
            
        Returns:
            WeatherVolatilityOutput with volatility assessment
        """
        # Clamp inputs
        forecast_confidence = max(0.0, min(1.0, forecast_confidence))
        cloud_cover = max(0.0, min(1.0, cloud_cover))
        wind_variability = max(0.0, min(1.0, wind_variability))
        historical_volatility = max(0.0, min(1.0, historical_volatility))
        
        # Calculate volatility components
        
        # Forecast uncertainty (inverse of confidence)
        forecast_uncertainty = 1.0 - forecast_confidence
        
        # Cloud instability (more clouds = more potential for change)
        # 50% clouds = maximum volatility (transitional)
        cloud_instability = 1.0 - abs(cloud_cover - 0.5) * 2  # Peak at 0.5
        
        # Calculate overall volatility (0-1)
        volatility = (
            forecast_uncertainty * 0.40 +
            cloud_instability * 0.25 +
            wind_variability * 0.15 +
            historical_volatility * 0.20
        )
        
        volatility = max(0.0, min(1.0, volatility))
        
        # Classify volatility
        if volatility < 0.3:
            volatility_level = "stable"
        elif volatility < 0.6:
            volatility_level = "moderate"
        else:
            volatility_level = "high"
        
        return WeatherVolatilityOutput(
            volatility_score=volatility,
            volatility_level=volatility_level
        )
    
    def calculate_strategy_risk(
        self,
        volatility_score: float,
        committed_stint_length: int,
        tyre_flexibility: bool = True
    ) -> Dict[str, Any]:
        """
        Assess strategic risk from weather volatility.
        
        Args:
            volatility_score: Weather volatility (0-1)
            committed_stint_length: How many laps committed to plan
            tyre_flexibility: Whether team has tyre options available
            
        Returns:
            Dict with risk assessment
        """
        # Longer commitment in volatile weather = higher risk
        base_risk = volatility_score
        
        # Commitment penalty (longer stints = more risk)
        # 10 laps = 1.0x, 30 laps = 1.5x
        commitment_multiplier = 1.0 + min(0.5, (committed_stint_length - 10) / 40)
        
        # Flexibility reduction
        flexibility_reduction = 0.7 if tyre_flexibility else 1.0
        
        strategic_risk = base_risk * commitment_multiplier * flexibility_reduction
        strategic_risk = max(0.0, min(1.0, strategic_risk))
        
        # Recommendation
        if strategic_risk > 0.7:
            recommendation = "conservative"
            reason = "High weather risk - shorter stints, retain flexibility"
        elif strategic_risk > 0.4:
            recommendation = "balanced"
            reason = "Moderate risk - plan for multiple scenarios"
        else:
            recommendation = "committed"
            reason = "Low risk - can commit to long-term strategy"
        
        return {
            'strategic_risk': strategic_risk,
            'recommendation': recommendation,
            'reason': reason,
            'volatility': volatility_score
        }


# Singleton instance
weather_volatility_calc = WeatherVolatilityCalculation()
