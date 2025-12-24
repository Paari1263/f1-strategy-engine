"""
Stint State Calculation
Tracks current stint status and projections

LOGIC:
  Comprehensive stint monitoring:
  - Progress percentage (laps_on_tyre / expected_stint_length)
  - Phase classification: early (0-40%), mid (40-70%), late (70-90%), critical (>90%)
  - Current degradation (current_pace - initial_pace)
  - Remaining stint potential

ROLE:
  Real-time stint health monitoring. Provides context for
  all strategy decisions during active stint.

SIGNIFICANCE:
  Informs pit stop urgency and alternative strategy viability.
  Critical phase = must pit soon. Early phase = flexibility for
  undercut/overcut. Essential for live strategy adaptation.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import StintStateOutput
from typing import Dict, Any


class StintStateCalculation(BaseCalculation):
    """
    Calculate current stint state.
    
    Tracks:
    - Stint progress
    - Tyre condition
    - Fuel load
    - Performance trend
    """
    
    @property
    def calculation_name(self) -> str:
        return "stint_state"
    
    @property
    def description(self) -> str:
        return "Tracks current stint status and projections"
    
    def validate_inputs(
        self,
        laps_on_tyre: int = None,
        **kwargs
    ) -> bool:
        """Validate lap count"""
        return laps_on_tyre is not None and laps_on_tyre >= 0
    
    def calculate(
        self,
        laps_on_tyre: int,
        expected_stint_length: int = 20,
        current_pace_s: float = 90.0,
        initial_pace_s: float = 89.5,
        **kwargs
    ) -> StintStateOutput:
        """
        Calculate stint state.
        
        Args:
            laps_on_tyre: Laps completed on current tyres
            expected_stint_length: Target stint length
            current_pace_s: Current lap time
            initial_pace_s: Initial stint lap time
            **kwargs: Additional parameters
            
        Returns:
            StintStateOutput with stint analysis
        """
        # Calculate progress percentage
        progress = min(1.0, laps_on_tyre / max(expected_stint_length, 1))
        
        # Calculate pace degradation
        pace_loss_s = current_pace_s - initial_pace_s
        
        # Classify stint phase
        if progress < 0.3:
            phase = "early"
        elif progress < 0.7:
            phase = "mid"
        elif progress < 0.9:
            phase = "late"
        else:
            phase = "critical"
        
        return StintStateOutput(
            stint_progress=progress,
            pace_delta_s=pace_loss_s,
            stint_phase=phase
        )
    
    def predict_remaining_performance(
        self,
        current_stint_state: StintStateOutput,
        laps_remaining_in_stint: int
    ) -> Dict[str, Any]:
        """
        Predict performance for remainder of stint.
        
        Args:
            current_stint_state: Current stint state
            laps_remaining_in_stint: Laps left in planned stint
            
        Returns:
            Dict with performance prediction
        """
        # Current degradation rate
        current_deg = current_stint_state.pace_delta_s
        
        # Assume degradation accelerates (non-linear)
        # Current phase affects projection
        if current_stint_state.stint_phase == "early":
            acceleration_factor = 1.2
        elif current_stint_state.stint_phase == "mid":
            acceleration_factor = 1.5
        elif current_stint_state.stint_phase == "late":
            acceleration_factor = 2.0
        else:  # critical
            acceleration_factor = 3.0
        
        # Project additional degradation
        additional_deg = current_deg * acceleration_factor * (laps_remaining_in_stint / 10)
        
        # Total expected pace loss by end of stint
        total_pace_loss = current_deg + additional_deg
        
        # Recommendation
        if total_pace_loss > 2.0:
            recommendation = "pit_soon"
            reason = "Severe degradation expected"
        elif total_pace_loss > 1.0:
            recommendation = "monitor"
            reason = "Significant degradation expected"
        else:
            recommendation = "continue"
            reason = "Performance acceptable"
        
        return {
            'recommendation': recommendation,
            'reason': reason,
            'expected_total_pace_loss_s': total_pace_loss,
            'laps_remaining': laps_remaining_in_stint,
            'stint_phase': current_stint_state.stint_phase
        }


# Singleton instance
stint_state_calc = StintStateCalculation()
