"""
Driver Form Calculation
Tracks recent performance trend

LOGIC:
  Analyzes recent race positions to identify trend:
  - Linear regression on last 5 results
  - Improving: positions trending upward
  - Declining: positions trending downward
  - Stable: minimal trend
  Form rating weighted toward recent races

ROLE:
  Momentum indicator. Captures current driver confidence and
  performance trajectory beyond baseline skill level.

SIGNIFICANCE:
  Driver in good form may outperform normal expectations. Declining
  form suggests underlying issues (confidence, car adaptation).
  Influences realistic performance predictions.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import DriverFormOutput
from typing import List, Dict, Any


class DriverFormCalculation(BaseCalculation):
    """
    Calculate driver's current form/momentum.
    
    Analyzes recent results to determine if driver is:
    - On upward trend (improving)
    - On downward trend (struggling)
    - Stable
    """
    
    @property
    def calculation_name(self) -> str:
        return "driver_form"
    
    @property
    def description(self) -> str:
        return "Tracks recent performance trend and momentum"
    
    def validate_inputs(
        self,
        recent_positions: List[int] = None,
        **kwargs
    ) -> bool:
        """Validate position data"""
        if not recent_positions:
            return False
        return len(recent_positions) > 0 and all(1 <= p <= 20 for p in recent_positions)
    
    def calculate(
        self,
        recent_positions: List[int],
        recent_points: List[float] = None,
        window_races: int = 5,
        **kwargs
    ) -> DriverFormOutput:
        """
        Calculate driver form.
        
        Args:
            recent_positions: Finishing positions in recent races (chronological)
            recent_points: Points scored in recent races (optional)
            window_races: Number of races to consider for trend
            **kwargs: Additional parameters
            
        Returns:
            DriverFormOutput with form analysis
        """
        if not recent_positions:
            return DriverFormOutput(
                form_trend="stable",
                form_rating=5.0
            )
        
        # Use only most recent races within window
        positions = recent_positions[-window_races:]
        
        # Calculate form rating (0-10, higher is better)
        # Convert positions to inverse scale (1st = 10 points, 20th = 0 points)
        position_scores = [max(0, 10 - (pos - 1) / 2) for pos in positions]
        avg_score = sum(position_scores) / len(position_scores)
        
        # Calculate trend
        if len(positions) >= 3:
            # Compare first half vs second half
            mid = len(positions) // 2
            first_half_avg = sum(positions[:mid]) / max(mid, 1)
            second_half_avg = sum(positions[mid:]) / max(len(positions) - mid, 1)
            
            # Lower positions = better, so invert for trend
            position_change = first_half_avg - second_half_avg
            
            if position_change > 2.0:
                trend = "improving"  # Positions getting better (lower numbers)
            elif position_change < -2.0:
                trend = "declining"  # Positions getting worse (higher numbers)
            else:
                trend = "stable"
        else:
            trend = "stable"
        
        return DriverFormOutput(
            form_trend=trend,
            form_rating=avg_score
        )
    
    def predict_next_race_performance(
        self,
        recent_positions: List[int],
        baseline_performance: float = None
    ) -> Dict[str, Any]:
        """
        Predict expected performance in next race based on form.
        
        Args:
            recent_positions: Recent finishing positions
            baseline_performance: Driver's typical position (if known)
            
        Returns:
            Dict with prediction
        """
        form = self.calculate(recent_positions=recent_positions)
        
        if not recent_positions:
            return {
                'predicted_position': baseline_performance or 10,
                'confidence': 0.3,
                'reasoning': "Insufficient data"
            }
        
        # Calculate expected position from recent form
        recent_avg = sum(recent_positions[-3:]) / min(len(recent_positions), 3)
        
        # Adjust based on trend
        if form.form_trend == "improving":
            adjustment = -1.0  # Expect 1 position better
            confidence = 0.7
        elif form.form_trend == "declining":
            adjustment = 1.0  # Expect 1 position worse
            confidence = 0.7
        else:
            adjustment = 0.0
            confidence = 0.6
        
        predicted_position = max(1, min(20, int(recent_avg + adjustment)))
        
        return {
            'predicted_position': predicted_position,
            'confidence': confidence,
            'reasoning': f"Form trend: {form.form_trend}, rating: {form.form_rating:.1f}"
        }


# Singleton instance
driver_form_calc = DriverFormCalculation()
