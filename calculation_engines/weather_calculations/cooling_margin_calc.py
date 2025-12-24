"""
Cooling Margin Calculation
Assesses thermal management headroom

LOGIC:
  Calculates cooling system capacity vs demand:
  - High ambient/track temps increase heat stress
  - Cooling specification (0-1) = installed cooling capacity
  - Margin = (spec - heat_stress) normalized
  - Status: comfortable/adequate/tight/critical

ROLE:
  Thermal reliability assessment. Determines if car can run
  full race distance without overheating issues.

SIGNIFICANCE:
  Critical for hot races (Singapore, Bahrain). Low cooling margin
  may force pace management or impact on reliability. Influences
  setup decisions (more cooling = more drag = slower).
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import CoolingMarginOutput
from typing import Dict, Any


class CoolingMarginCalculation(BaseCalculation):
    """
    Calculate car cooling margin.
    
    Hot conditions stress cooling systems:
    - Engine/PU cooling
    - Brake cooling
    - Tyre temperature management
    """
    
    # Critical temperature thresholds
    CRITICAL_AMBIENT_TEMP_C = 35.0
    CRITICAL_TRACK_TEMP_C = 50.0
    
    @property
    def calculation_name(self) -> str:
        return "cooling_margin"
    
    @property
    def description(self) -> str:
        return "Assesses thermal management headroom"
    
    def validate_inputs(
        self,
        ambient_temp_c: float = None,
        track_temp_c: float = None,
        **kwargs
    ) -> bool:
        """Validate temperature inputs"""
        if ambient_temp_c is None or track_temp_c is None:
            return False
        return -10 <= ambient_temp_c <= 50 and 0 <= track_temp_c <= 70
    
    def calculate(
        self,
        ambient_temp_c: float,
        track_temp_c: float,
        cooling_spec: float = 0.5,
        **kwargs
    ) -> CoolingMarginOutput:
        """
        Calculate cooling margin.
        
        Args:
            ambient_temp_c: Ambient air temperature
            track_temp_c: Track surface temperature
            cooling_spec: Cooling package size (0=minimal, 1=maximum)
            **kwargs: Additional parameters
            
        Returns:
            CoolingMarginOutput with margin assessment
        """
        # Clamp inputs
        ambient_temp_c = max(-10.0, min(50.0, ambient_temp_c))
        track_temp_c = max(0.0, min(70.0, track_temp_c))
        cooling_spec = max(0.0, min(1.0, cooling_spec))
        
        # Calculate thermal stress (0-1, higher = more stress)
        ambient_stress = max(0.0, ambient_temp_c - 20) / 20  # 20°C baseline
        track_stress = max(0.0, track_temp_c - 30) / 30  # 30°C baseline
        
        overall_stress = (ambient_stress * 0.4 + track_stress * 0.6)
        overall_stress = max(0.0, min(1.0, overall_stress))
        
        # Calculate margin (cooling capacity - thermal load)
        # Larger cooling package provides more margin
        base_margin = 0.3 + (cooling_spec * 0.4)  # 0.3 to 0.7
        
        # Subtract thermal load
        margin = base_margin - overall_stress
        
        # Classify margin
        if margin > 0.3:
            margin_status = "comfortable"
        elif margin > 0.1:
            margin_status = "adequate"
        elif margin > -0.1:
            margin_status = "tight"
        else:
            margin_status = "critical"
        
        return CoolingMarginOutput(
            margin=margin,
            status=margin_status
        )
    
    def recommend_cooling_mode(
        self,
        margin: float,
        race_phase: str = "race"
    ) -> Dict[str, Any]:
        """
        Recommend cooling mode setting.
        
        Args:
            margin: Cooling margin (-1 to 1)
            race_phase: Phase of race (quali/race/cooldown)
            
        Returns:
            Dict with cooling recommendation
        """
        if race_phase == "quali" and margin > 0:
            # Can afford minimal cooling for speed
            return {
                'mode': 'minimum',
                'reason': 'Maximize speed in qualifying',
                'risk': 'low' if margin > 0.2 else 'medium'
            }
        
        if margin < 0:
            # Need maximum cooling
            return {
                'mode': 'maximum',
                'reason': 'Thermal stress critical',
                'risk': 'high'
            }
        elif margin < 0.1:
            return {
                'mode': 'high',
                'reason': 'Limited thermal margin',
                'risk': 'medium'
            }
        else:
            return {
                'mode': 'medium',
                'reason': 'Comfortable thermal margin',
                'risk': 'low'
            }


# Singleton instance
cooling_margin_calc = CoolingMarginCalculation()
