"""
Calculation Engines Package
Pure mathematical calculations for F1 strategy simulation
"""

# This package provides mathematical calculations separated from data fetching.
# All calculations are pure functions with well-defined inputs and outputs.

__version__ = "1.0.0"
__all__ = [
    # Interfaces
    "BaseCalculation",
    "CalculationResult",
    
    # Tyre Calculations
    "compound_delta_calc",
    "thermal_window_calc",
    "push_penalty_calc",
    "degradation_curve_calc",
    "tyre_life_projection_calc",
    
    # Car Calculations
    "car_performance_index_calc",
    "aero_drag_balance_calc",
    "fuel_effect_calc",
    "reliability_risk_calc",
    "tyre_car_interaction_calc",
    
    # Driver Calculations
    "driver_pace_calc",
    "driver_consistency_calc",
    "driver_form_calc",
    "error_risk_calc",
    "racecraft_calc",
    
    # Track Calculations
    "pit_loss_calc",
    "overtaking_difficulty_calc",
    "dirty_air_penalty_calc",
    "track_difficulty_calc",
    "safety_car_probability_calc",
    
    # Traffic Calculations
    "traffic_density_calc",
    "defense_effectiveness_calc",
    "overtake_cost_calc",
    "drs_train_probability_calc",
    
    # Weather Calculations
    "grip_evolution_calc",
    "cooling_margin_calc",
    "crossover_lap_calc",
    "weather_volatility_calc",
    
    # Race State Calculations
    "gap_projection_calc",
    "pit_window_calc",
    "stint_state_calc",
    "position_pressure_calc",
    
    # Aggregation
    "driver_car_fusion_calc",
    "tyre_car_fusion_calc",
    "race_context_builder",
]

# Import base classes
from calculation_engines.interfaces.base_calculation import BaseCalculation, CalculationResult

# Import all calculation modules
from calculation_engines.tyre_calculations.compound_delta_calc import compound_delta_calc
from calculation_engines.tyre_calculations.thermal_window_calc import thermal_window_calc
from calculation_engines.tyre_calculations.push_penalty_calc import push_penalty_calc
from calculation_engines.tyre_calculations.degradation_curve_calc import degradation_curve_calc
from calculation_engines.tyre_calculations.tyre_life_projection_calc import tyre_life_projection_calc

from calculation_engines.car_calculations.car_performance_index_calc import car_performance_index_calc
from calculation_engines.car_calculations.aero_vs_drag_balance_calc import aero_drag_balance_calc
from calculation_engines.car_calculations.fuel_effect_calc import fuel_effect_calc
from calculation_engines.car_calculations.reliability_risk_calc import reliability_risk_calc
from calculation_engines.car_calculations.tyre_interaction_calc import tyre_car_interaction_calc

from calculation_engines.driver_calculations.pace_delta_calc import driver_pace_calc
from calculation_engines.driver_calculations.consistency_calc import driver_consistency_calc
from calculation_engines.driver_calculations.driver_form_calc import driver_form_calc
from calculation_engines.driver_calculations.error_risk_calc import error_risk_calc
from calculation_engines.driver_calculations.racecraft_score_calc import racecraft_calc

from calculation_engines.track_calculations.pit_loss_calc import pit_loss_calc
from calculation_engines.track_calculations.overtaking_difficulty_calc import overtaking_difficulty_calc
from calculation_engines.track_calculations.dirty_air_penalty_calc import dirty_air_penalty_calc
from calculation_engines.track_calculations.track_difficulty_calc import track_difficulty_calc
from calculation_engines.track_calculations.safety_car_probability_calc import safety_car_probability_calc

from calculation_engines.traffic_calculations.traffic_density_calc import traffic_density_calc
from calculation_engines.traffic_calculations.defense_effectiveness_calc import defense_effectiveness_calc
from calculation_engines.traffic_calculations.overtake_cost_calc import overtake_cost_calc
from calculation_engines.traffic_calculations.train_probability_calc import drs_train_probability_calc

from calculation_engines.weather_calculations.grip_evolution_calc import grip_evolution_calc
from calculation_engines.weather_calculations.cooling_margin_calc import cooling_margin_calc
from calculation_engines.weather_calculations.crossover_lap_calc import crossover_lap_calc
from calculation_engines.weather_calculations.weather_volatility_calc import weather_volatility_calc

from calculation_engines.race_state_calculations.gap_projection_calc import gap_projection_calc
from calculation_engines.race_state_calculations.pit_window_calc import pit_window_calc
from calculation_engines.race_state_calculations.stint_state_calc import stint_state_calc
from calculation_engines.race_state_calculations.position_pressure_calc import position_pressure_calc

from calculation_engines.aggregation.driver_car_fusion_calc import driver_car_fusion_calc
from calculation_engines.aggregation.tyre_car_fusion_calc import tyre_car_fusion_calc
from calculation_engines.aggregation.race_context_builder import race_context_builder
