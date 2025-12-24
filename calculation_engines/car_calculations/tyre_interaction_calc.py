"""
Tyre-Car Interaction Calculation
Models how car characteristics affect tyre performance

LOGIC:
  Car influences tyre behavior through multiple factors:
  - Downforce level affects tyre load and temperature
  - Car weight impacts wear rate (heavier = more wear)
  - Power delivery affects rear tyre degradation
  Calculates wear multipliers and thermal generation rates

ROLE:
  Links car performance to tyre strategy. Explains why some cars
  are easier on tyres than others despite similar pace.

SIGNIFICANCE:
  Critical for understanding car-specific strategy options.
  High downforce car may enable longer stints on softer compounds.
  Determines compound recommendations based on car characteristics.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import TyreInteractionOutput
from typing import Dict, Any


class TyreCarInteractionCalculation(BaseCalculation):
    """
    Calculate car-tyre interaction effects.
    
    Different cars treat tyres differently:
    - High downforce cars: Generate more heat, higher wear
    - Low downforce cars: Struggle to warm up tyres
    - Heavy cars: Increase wear
    - Powerful cars: Stress rear tyres more
    """
    
    @property
    def calculation_name(self) -> str:
        return "tyre_car_interaction"
    
    @property
    def description(self) -> str:
        return "Models how car characteristics affect tyre performance"
    
    def validate_inputs(
        self,
        downforce_level: float = None,
        car_weight_kg: float = None,
        **kwargs
    ) -> bool:
        """Validate car parameters"""
        if downforce_level is None or car_weight_kg is None:
            return False
        return 0.0 <= downforce_level <= 10.0 and 700 <= car_weight_kg <= 800
    
    def calculate(
        self,
        downforce_level: float,
        car_weight_kg: float,
        power_output: float = 5.0,
        **kwargs
    ) -> TyreInteractionOutput:
        """
        Calculate tyre interaction effects.
        
        Args:
            downforce_level: Car downforce rating (0-10)
            car_weight_kg: Car weight including driver (kg)
            power_output: Power unit rating (0-10)
            **kwargs: Additional parameters
            
        Returns:
            TyreInteractionOutput with interaction multipliers
        """
        # Clamp inputs
        downforce_level = max(0.0, min(10.0, downforce_level))
        car_weight_kg = max(700.0, min(800.0, car_weight_kg))
        power_output = max(0.0, min(10.0, power_output))
        
        # Calculate wear multiplier
        # More downforce = more tyre stress = faster wear
        # Baseline at downforce=5, weight=750kg
        baseline_weight = 750.0
        weight_factor = car_weight_kg / baseline_weight
        
        downforce_factor = 0.8 + (downforce_level / 10.0) * 0.4  # 0.8 to 1.2
        
        wear_multiplier = weight_factor * downforce_factor
        
        # Calculate thermal generation
        # High downforce generates more heat through corners
        # More power generates heat through traction zones
        thermal_from_downforce = downforce_level / 10.0  # 0-1
        thermal_from_power = power_output / 10.0  # 0-1
        
        # Combined thermal effect (normalized 0-1)
        thermal_generation = (thermal_from_downforce * 0.6 + thermal_from_power * 0.4)
        
        # Convert to temperature delta
        # High thermal generation can be +5 to +10°C
        temp_delta_c = thermal_generation * 8.0  # 0-8°C increase
        
        # Calculate operating window rating
        # How well car keeps tyres in optimal window
        # Balanced setup (downforce ~5, power ~5) is ideal
        downforce_deviation = abs(downforce_level - 5.0) / 5.0  # 0-1
        power_deviation = abs(power_output - 5.0) / 5.0  # 0-1
        
        balance = 1.0 - ((downforce_deviation + power_deviation) / 2.0)
        operating_window_rating = max(0.0, min(1.0, balance))
        
        return TyreInteractionOutput(
            wear_multiplier=wear_multiplier,
            thermal_generation=thermal_generation,
            temp_delta_c=temp_delta_c,
            operating_window_rating=operating_window_rating
        )
    
    def recommend_tyre_compound(
        self,
        downforce_level: float,
        car_weight_kg: float,
        power_output: float,
        track_temp_c: float
    ) -> Dict[str, Any]:
        """
        Recommend tyre compound based on car characteristics.
        
        Args:
            downforce_level: Car downforce
            car_weight_kg: Car weight
            power_output: Power rating
            track_temp_c: Track temperature
            
        Returns:
            Dict with compound recommendation and reasoning
        """
        interaction = self.calculate(downforce_level, car_weight_kg, power_output)
        
        # High wear cars should avoid softest compounds
        # High thermal cars need compounds that can handle heat
        
        # Calculate effective track temp with car's thermal contribution
        effective_temp = track_temp_c + interaction.temp_delta_c
        
        # Temperature-based recommendation
        if effective_temp < 20:
            temp_recommendation = "SOFT"  # Need heat generation
        elif effective_temp < 30:
            temp_recommendation = "MEDIUM"
        else:
            temp_recommendation = "HARD"  # Too hot for soft compounds
        
        # Wear-based recommendation
        if interaction.wear_multiplier > 1.15:
            wear_recommendation = "HARD"  # High wear car
        elif interaction.wear_multiplier < 0.95:
            wear_recommendation = "SOFT"  # Low wear car
        else:
            wear_recommendation = "MEDIUM"
        
        # Combined recommendation (temperature takes priority)
        if effective_temp > 35:
            recommendation = "HARD"
            reason = "High effective temperature requires durable compound"
        elif effective_temp < 18:
            recommendation = "SOFT"
            reason = "Low temperature requires heat-generating compound"
        elif interaction.wear_multiplier > 1.2:
            recommendation = "HARD" if temp_recommendation != "SOFT" else "MEDIUM"
            reason = "High wear characteristics favor harder compound"
        else:
            recommendation = "MEDIUM"
            reason = "Balanced car characteristics suit medium compound"
        
        return {
            'recommendation': recommendation,
            'reason': reason,
            'temp_recommendation': temp_recommendation,
            'wear_recommendation': wear_recommendation,
            'effective_temp_c': effective_temp,
            'wear_multiplier': interaction.wear_multiplier
        }


# Singleton instance
tyre_car_interaction_calc = TyreCarInteractionCalculation()
