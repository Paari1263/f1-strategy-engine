"""
Tyre-Car Fusion Calculation  
Combines tyre and car characteristics for performance prediction

LOGIC:
  Integrated tyre-car performance model:
  - Compound base delta (from lookup table)
  - Car downforce affects tyre loading and temperature
  - Car weight impacts degradation rate
  - Track temperature influences compound selection
  - Outputs: expected pace delta and degradation rate

ROLE:
  Car-specific tyre strategy calculator. Different cars suit
  different compounds based on characteristics.

SIGNIFICANCE:
  Explains why Red Bull can run HARD while Mercedes needs MEDIUM.
  High downforce cars enable longer stints on soft compounds.
  Critical for optimizing compound choice per car/track combination.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import TyreCarFusionOutput
from typing import Dict, Any


class TyreCarFusionCalculation(BaseCalculation):
    """
    Fuse tyre and car characteristics.
    
    Different cars treat tyres differently, affecting:
    - Optimal compound choice
    - Degradation rate
    - Performance window
    """
    
    @property
    def calculation_name(self) -> str:
        return "tyre_car_fusion"
    
    @property
    def description(self) -> str:
        return "Combines tyre and car characteristics"
    
    def validate_inputs(
        self,
        tyre_compound: str = None,
        car_characteristics: Dict = None,
        **kwargs
    ) -> bool:
        """Validate inputs"""
        if tyre_compound is None:
            return False
        return tyre_compound.upper() in ["SOFT", "MEDIUM", "HARD", "INTERMEDIATE", "WET"]
    
    def calculate(
        self,
        tyre_compound: str,
        car_downforce: float = 5.0,
        car_weight_kg: float = 750.0,
        track_temp_c: float = 30.0,
        **kwargs
    ) -> TyreCarFusionOutput:
        """
        Calculate tyre-car interaction.
        
        Args:
            tyre_compound: Tyre compound name
            car_downforce: Car downforce level (0-10)
            car_weight_kg: Car weight (kg)
            track_temp_c: Track temperature
            **kwargs: Additional parameters
            
        Returns:
            TyreCarFusionOutput with interaction analysis
        """
        # Compound base characteristics
        compound_map = {
            "SOFT": {"base_pace": -0.4, "base_deg": 0.08, "opt_temp": 90},
            "MEDIUM": {"base_pace": 0.0, "base_deg": 0.05, "opt_temp": 95},
            "HARD": {"base_pace": 0.3, "base_deg": 0.03, "opt_temp": 100},
            "INTERMEDIATE": {"base_pace": 0.5, "base_deg": 0.04, "opt_temp": 80},
            "WET": {"base_pace": 1.0, "base_deg": 0.02, "opt_temp": 65}
        }
        
        compound_upper = tyre_compound.upper()
        compound_data = compound_map.get(compound_upper, compound_map["MEDIUM"])
        
        # Car interaction effects
        
        # High downforce generates heat, increases wear
        downforce_factor = car_downforce / 10.0  # 0-1
        thermal_effect = downforce_factor * 8.0  # Up to +8°C
        wear_multiplier = 1.0 + (downforce_factor * 0.3)  # Up to 1.3x
        
        # Weight effect on wear
        weight_factor = (car_weight_kg - 700) / 100  # Normalized
        wear_multiplier *= (1.0 + weight_factor * 0.1)  # Weight adds wear
        
        # Temperature matching
        effective_temp = track_temp_c + thermal_effect
        optimal_temp = compound_data["opt_temp"]
        temp_deviation = abs(effective_temp - optimal_temp)
        
        # Temp penalty
        if temp_deviation < 5:
            temp_penalty_s = 0.0
        else:
            temp_penalty_s = (temp_deviation - 5) * 0.02  # 0.02s per °C over 5°C
        
        # Calculate expected pace
        expected_pace_delta = (
            compound_data["base_pace"] +
            temp_penalty_s
        )
        
        # Calculate degradation
        expected_degradation = compound_data["base_deg"] * wear_multiplier
        
        return TyreCarFusionOutput(
            expected_pace_delta_s=expected_pace_delta,
            expected_degradation_rate=expected_degradation
        )
    
    def recommend_optimal_compound(
        self,
        car_downforce: float,
        car_weight_kg: float,
        track_temp_c: float,
        target_stint_length: int
    ) -> Dict[str, Any]:
        """
        Recommend best compound for conditions.
        
        Args:
            car_downforce: Car downforce
            car_weight_kg: Car weight
            track_temp_c: Track temperature
            target_stint_length: Desired stint length
            
        Returns:
            Dict with compound recommendation
        """
        compounds = ["SOFT", "MEDIUM", "HARD"]
        results = []
        
        for compound in compounds:
            fusion = self.calculate(
                tyre_compound=compound,
                car_downforce=car_downforce,
                car_weight_kg=car_weight_kg,
                track_temp_c=track_temp_c
            )
            
            # Estimate stint viability
            # Soft: ~20 laps, Medium: ~30 laps, Hard: ~40 laps base
            base_life = {"SOFT": 20, "MEDIUM": 30, "HARD": 40}[compound]
            adjusted_life = int(base_life / fusion.expected_degradation_rate * 0.05)
            
            # Score compound
            # Pace component (faster = better)
            pace_score = -fusion.expected_pace_delta_s  # Negative delta = faster
            
            # Life component (can it do the stint?)
            if adjusted_life >= target_stint_length:
                life_score = 10.0
            else:
                life_score = (adjusted_life / target_stint_length) * 10.0
            
            # Combined score
            total_score = pace_score * 0.6 + life_score * 0.4
            
            results.append({
                'compound': compound,
                'score': total_score,
                'expected_pace': fusion.expected_pace_delta_s,
                'expected_life': adjusted_life,
                'can_complete_stint': adjusted_life >= target_stint_length
            })
        
        # Sort by score
        results.sort(key=lambda x: x['score'], reverse=True)
        best = results[0]
        
        return {
            'recommended_compound': best['compound'],
            'expected_pace_delta_s': best['expected_pace'],
            'expected_life_laps': best['expected_life'],
            'can_complete_stint': best['can_complete_stint'],
            'all_options': results
        }


# Singleton instance
tyre_car_fusion_calc = TyreCarFusionCalculation()
