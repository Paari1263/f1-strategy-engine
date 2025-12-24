"""
Aero vs Drag Balance Calculation
Analyzes trade-off between downforce and drag for track characteristics

LOGIC:
  Evaluates setup appropriateness for track type:
  - High downforce tracks (Monaco): favor downforce over drag
  - Low downforce tracks (Monza): favor low drag over downforce
  - Balanced tracks: optimal middle ground
  Efficiency ratio = downforce / drag
  Balance score considers track type weighting

ROLE:
  Setup optimization tool. Determines if car setup matches circuit
  requirements. Guides wing angle and configuration decisions.

SIGNIFICANCE:
  Prevents running wrong setup (e.g., high downforce at Monza).
  Can be worth 0.5-1.0s per lap when optimized correctly.
  Critical for qualifying and race pace optimization.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import AeroDragBalanceOutput
from typing import Dict, Any


class AeroDragBalanceCalculation(BaseCalculation):
    """
    Calculate optimal aero/drag balance for track type.
    
    Different tracks require different setups:
    - High downforce tracks (Monaco): Prioritize downforce
    - Low downforce tracks (Monza): Minimize drag
    - Balanced tracks: Optimize trade-off
    """
    
    # Track type coefficients (how much to favor downforce vs low drag)
    TRACK_TYPE_FACTORS = {
        'high_downforce': 0.8,    # Monaco, Hungary, Singapore
        'balanced': 0.5,           # Most circuits
        'low_downforce': 0.2       # Monza, Spa
    }
    
    @property
    def calculation_name(self) -> str:
        return "aero_drag_balance"
    
    @property
    def description(self) -> str:
        return "Analyzes aero/drag trade-off for track characteristics"
    
    def validate_inputs(
        self,
        downforce_level: float = None,
        drag_level: float = None,
        **kwargs
    ) -> bool:
        """Validate aero parameters are in range"""
        if downforce_level is None or drag_level is None:
            return False
        return 0.0 <= downforce_level <= 10.0 and 0.0 <= drag_level <= 10.0
    
    def calculate(
        self,
        downforce_level: float,
        drag_level: float,
        track_type: str = 'balanced',
        **kwargs
    ) -> AeroDragBalanceOutput:
        """
        Calculate aero/drag balance efficiency.
        
        Args:
            downforce_level: Current downforce level (0-10)
            drag_level: Current drag level (0-10)
            track_type: Track category (high_downforce/balanced/low_downforce)
            **kwargs: Additional parameters
            
        Returns:
            AeroDragBalanceOutput with balance analysis
        """
        # Clamp inputs
        downforce_level = max(0.0, min(10.0, downforce_level))
        drag_level = max(0.0, min(10.0, drag_level))
        
        # Get track type factor
        track_factor = self.TRACK_TYPE_FACTORS.get(track_type, 0.5)
        
        # Calculate efficiency ratio (downforce per unit drag)
        # Avoid division by zero
        if drag_level > 0:
            efficiency_ratio = downforce_level / drag_level
        else:
            efficiency_ratio = downforce_level * 10.0  # Maximum efficiency with zero drag
        
        # Calculate optimality score for this track type
        # For high downforce tracks: favor more downforce even if drag increases
        # For low downforce tracks: heavily penalize drag
        
        # Ideal downforce for track type
        ideal_downforce = track_factor * 10.0
        
        # Ideal drag (always want lower, but tolerance varies by track)
        ideal_drag = (1.0 - track_factor) * 5.0  # Low downforce tracks tolerate less drag
        
        # Calculate deviations
        downforce_delta = abs(downforce_level - ideal_downforce)
        drag_delta = abs(drag_level - ideal_drag)
        
        # Balance score (0-10, higher is better)
        # Penalize both deviations, weight by track type
        downforce_penalty = downforce_delta * track_factor
        drag_penalty = drag_delta * (1.0 - track_factor)
        
        total_penalty = downforce_penalty + drag_penalty
        balance_score = max(0.0, 10.0 - total_penalty)
        
        # Determine recommendation
        if downforce_level < ideal_downforce - 1.0:
            recommendation = "increase_downforce"
        elif downforce_level > ideal_downforce + 1.0:
            recommendation = "reduce_downforce"
        elif drag_level > ideal_drag + 1.0:
            recommendation = "reduce_drag"
        else:
            recommendation = "optimal"
        
        return AeroDragBalanceOutput(
            balance_score=balance_score,
            efficiency_ratio=efficiency_ratio,
            recommendation=recommendation
        )
    
    def estimate_lap_time_delta(
        self,
        current_downforce: float,
        current_drag: float,
        new_downforce: float,
        new_drag: float,
        track_type: str = 'balanced'
    ) -> float:
        """
        Estimate lap time change from setup adjustment.
        
        Args:
            current_downforce, current_drag: Current setup
            new_downforce, new_drag: Proposed setup
            track_type: Track category
            
        Returns:
            Estimated lap time delta in seconds (negative = faster)
        """
        # Calculate balance scores
        current_balance = self.calculate(current_downforce, current_drag, track_type)
        new_balance = self.calculate(new_downforce, new_drag, track_type)
        
        # Each point of balance score worth ~0.05s per lap
        balance_improvement = new_balance.balance_score - current_balance.balance_score
        lap_time_delta = -balance_improvement * 0.05
        
        return lap_time_delta


# Singleton instance
aero_drag_balance_calc = AeroDragBalanceCalculation()
