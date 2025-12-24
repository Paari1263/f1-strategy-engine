"""
Compound Delta Calculation
Calculates lap time delta between tyre compounds

LOGIC:
  Uses empirical baseline deltas for each compound relative to MEDIUM compound:
  - SOFT: -0.4s per lap (faster, less durable)
  - MEDIUM: 0.0s baseline
  - HARD: +0.3s per lap (slower, more durable)
  Simple lookup table based on compound type.

ROLE:
  Foundation for tyre strategy decisions. Enables comparison of pace
  vs degradation trade-offs across different compound choices.

SIGNIFICANCE:
  Critical for pit strategy - determines if pace advantage of softer
  compound justifies shorter stint length. Used in every strategy
  calculation involving tyre choice.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_input_models import TyreCompoundInput
from calculation_engines.interfaces.calculation_output_models import CompoundDeltaOutput
from typing import Dict, Any


# Baseline compound deltas (seconds per lap relative to MEDIUM)
COMPOUND_DELTAS = {
    "SOFT": -0.4,      # 0.4s faster than MEDIUM
    "MEDIUM": 0.0,     # Baseline
    "HARD": 0.3,       # 0.3s slower than MEDIUM
    "INTERMEDIATE": 0.0,  # Context-dependent (wet conditions)
    "WET": 0.0        # Context-dependent (heavy rain)
}


class CompoundDeltaCalculation(BaseCalculation):
    """
    Calculate lap time delta between tyre compounds.
    
    Pure mathematical calculation based on compound characteristics.
    SOFT is fastest but degrades quickest, HARD is slowest but lasts longest.
    """
    
    @property
    def calculation_name(self) -> str:
        return "compound_delta"
    
    @property
    def description(self) -> str:
        return "Calculates lap time difference between tyre compounds"
    
    def validate_inputs(self, compound: str = None, **kwargs) -> bool:
        """Validate compound name is recognized"""
        if compound is None:
            return False
        return compound.upper() in COMPOUND_DELTAS
    
    def calculate(self, compound: str, **kwargs) -> CompoundDeltaOutput:
        """
        Calculate lap time delta for given compound.
        
        Args:
            compound: Tyre compound name (SOFT/MEDIUM/HARD/INTERMEDIATE/WET)
            **kwargs: Additional parameters (ignored)
        
        Returns:
            CompoundDeltaOutput with lap time delta
        """
        compound_upper = compound.upper()
        delta = COMPOUND_DELTAS.get(compound_upper, 0.0)
        
        return CompoundDeltaOutput(
            compound_name=compound_upper,
            lap_time_delta_s=delta,
            baseline_compound="MEDIUM"
        )
    
    def calculate_relative_delta(
        self, 
        compound_a: str, 
        compound_b: str
    ) -> float:
        """
        Calculate delta between two specific compounds.
        
        Args:
            compound_a: First compound
            compound_b: Second compound
            
        Returns:
            Lap time delta (positive = compound_a is slower)
        """
        delta_a = COMPOUND_DELTAS.get(compound_a.upper(), 0.0)
        delta_b = COMPOUND_DELTAS.get(compound_b.upper(), 0.0)
        return delta_a - delta_b


# Singleton instance for easy access
compound_delta_calc = CompoundDeltaCalculation()
