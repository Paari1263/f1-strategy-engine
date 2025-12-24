"""
Calculation Output Models
Pydantic models defining standardized outputs for all calculation modules
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


# ============================================================================
# TYRE CALCULATION OUTPUTS
# ============================================================================

class CompoundDeltaOutput(BaseModel):
    """Output from compound delta calculation"""
    compound_name: str
    lap_time_delta_s: float = Field(..., description="Seconds per lap vs baseline (negative = faster)")
    baseline_compound: str = "MEDIUM"


class DegradationCurveOutput(BaseModel):
    """Output from degradation curve calculation"""
    degradation_rate_s_per_lap: float = Field(..., ge=0.0)
    wear_multiplier: float = Field(..., ge=1.0)
    thermal_penalty_s: float = Field(0.0, ge=0.0)


class PushPenaltyOutput(BaseModel):
    """Output from push penalty calculation"""
    push_multiplier: float = Field(..., ge=1.0, le=2.0, description="Degradation multiplier")
    estimated_life_reduction_laps: int = Field(..., ge=0)


class ThermalWindowOutput(BaseModel):
    """Output from thermal window calculation"""
    temp_penalty_s_per_lap: float = Field(..., ge=0.0)
    is_in_window: bool
    temp_delta_c: float


class TyreLifeProjectionOutput(BaseModel):
    """Output from tyre life projection"""
    remaining_laps: int = Field(..., ge=0)
    cliff_lap_estimate: Optional[int] = None
    confidence: float = Field(..., ge=0.0, le=1.0)


# ============================================================================
# CAR CALCULATION OUTPUTS
# ============================================================================

class CarPerformanceIndexOutput(BaseModel):
    """Output from car performance index calculation"""
    performance_index: float = Field(..., ge=0.0, le=10.0)
    power_contribution: float
    aero_contribution: float
    drag_penalty: float
    grip_contribution: float


class AeroDragBalanceOutput(BaseModel):
    """Output from aero vs drag balance"""
    balance_score: float = Field(..., ge=0.0, le=10.0, description="Balance score 0-10")
    efficiency_ratio: float = Field(..., ge=0.0, description="Downforce/drag ratio")
    recommendation: str = Field(..., description="Setup recommendation")


class FuelEffectOutput(BaseModel):
    """Output from fuel weight calculation"""
    fuel_penalty_s: float = Field(..., ge=0.0, description="Lap time penalty from fuel weight")
    fuel_load_kg: float = Field(..., ge=0.0, description="Current fuel load in kg")


class ReliabilityRiskOutput(BaseModel):
    """Output from reliability risk calculation"""
    failure_probability: float = Field(..., ge=0.0, le=1.0, description="Component failure probability")
    risk_level: str = Field(..., description="LOW/MEDIUM/HIGH/CRITICAL")


class TyreInteractionOutput(BaseModel):
    """Output from car-tyre interaction"""
    wear_multiplier: float = Field(..., ge=1.0, description="Wear rate multiplier")
    thermal_generation: float = Field(..., ge=0.0, description="Heat generation rate")
    temp_delta_c: float = Field(..., description="Temperature delta in Celsius")
    operating_window_rating: float = Field(..., ge=0.0, le=1.0, description="Operating window suitability 0-1")



# ============================================================================
# DRIVER CALCULATION OUTPUTS
# ============================================================================

class PaceDeltaOutput(BaseModel):
    """Output from pace delta calculation"""
    pace_delta_s: float = Field(..., description="vs field avg (negative = faster)")
    percentile_rank: float = Field(..., ge=0.0, le=100.0, description="Percentile ranking")


class ConsistencyOutput(BaseModel):
    """Output from consistency calculation"""
    consistency_score: float = Field(..., ge=0.0, le=1.0, description="Higher = more consistent")
    std_dev_s: float = Field(..., ge=0.0, description="Standard deviation")
    coefficient_of_variation: float = Field(..., ge=0.0)


class DriverFormOutput(BaseModel):
    """Output from driver form calculation"""
    form_rating: float = Field(..., ge=0.0, le=10.0, description="Form rating 0-10")
    form_trend: str = Field(..., description="improving/stable/declining")


class ErrorRiskOutput(BaseModel):
    """Output from error risk calculation"""
    error_probability_per_lap: float = Field(..., ge=0.0, le=1.0, description="Error probability per lap")
    risk_level: str = Field(..., description="low/medium/high/critical")


class RacecraftOutput(BaseModel):
    """Output from racecraft calculation"""
    racecraft_score: float = Field(..., ge=0.0, le=10.0)
    overtaking_rating: float = Field(..., ge=0.0, le=10.0)
    defensive_rating: float = Field(..., ge=0.0, le=10.0)
    battle_efficiency: float = Field(..., ge=0.0, le=10.0)


# ============================================================================
# TRACK CALCULATION OUTPUTS
# ============================================================================

class PitLossOutput(BaseModel):
    """Output from pit loss calculation"""
    total_loss_s: float = Field(..., gt=0.0, description="Total pit stop time loss")
    stationary_time_s: float = Field(..., gt=0.0)


class OvertakingDifficultyOutput(BaseModel):
    """Output from overtaking difficulty"""
    difficulty_rating: float = Field(..., ge=0.0, le=10.0, description="Difficulty 0-10")
    difficulty_class: str = Field(..., description="easy/moderate/difficult/very_difficult")


class DirtyAirPenaltyOutput(BaseModel):
    """Output from dirty air penalty"""
    penalty_s_per_lap: float = Field(..., ge=0.0)
    gap_s: float = Field(..., ge=0.0)


class TrackDifficultyOutput(BaseModel):
    """Output from track difficulty index"""
    difficulty_rating: float = Field(..., ge=0.0, le=10.0, description="Difficulty 0-10")


class SafetyCarProbabilityOutput(BaseModel):
    """Output from SC probability calculation"""
    probability: float = Field(..., ge=0.0, le=1.0, description="SC deployment probability")


# ============================================================================
# TRAFFIC CALCULATION OUTPUTS
# ============================================================================

class TrafficDensityOutput(BaseModel):
    """Output from traffic density calculation"""
    density_cars_per_km: float = Field(..., ge=0.0)
    density_level: str = Field(..., description="sparse/moderate/dense")


class DefenseEffectivenessOutput(BaseModel):
    """Output from defense effectiveness"""
    effectiveness_rating: float = Field(..., ge=0.0, le=10.0)


class OvertakeCostOutput(BaseModel):
    """Output from overtake time cost"""
    time_cost_s: float = Field(..., ge=0.0)
    tyre_life_cost_laps: float = Field(..., ge=0.0)


class TrainProbabilityOutput(BaseModel):
    """Output from DRS train probability"""
    train_probability: float = Field(..., ge=0.0, le=1.0)



# ============================================================================
# WEATHER CALCULATION OUTPUTS
# ============================================================================

class GripEvolutionOutput(BaseModel):
    """Output from grip evolution calculation"""
    current_grip_level: float = Field(..., ge=0.0, le=1.0)
    lap_time_delta_s: float = Field(..., description="Lap time impact from grip level")


class CoolingMarginOutput(BaseModel):
    """Output from cooling margin calculation"""
    margin: float = Field(..., description="Cooling margin rating")
    status: str = Field(..., description="comfortable/adequate/tight/critical")


class CrossoverLapOutput(BaseModel):
    """Output from crossover lap calculation"""
    crossover_lap: Optional[int] = Field(None, description="Lap where compounds cross over")
    compound_a_faster_until: Optional[int] = None
    compound_b_faster_from: Optional[int] = None


class WeatherVolatilityOutput(BaseModel):
    """Output from weather volatility"""
    volatility_score: float = Field(..., ge=0.0, le=1.0)
    volatility_level: str = Field(..., description="stable/moderate/high")


# ============================================================================
# RACE STATE CALCULATION OUTPUTS
# ============================================================================

class GapProjectionOutput(BaseModel):
    """Output from gap projection calculation"""
    projected_gap_s: float
    closing_rate_s_per_lap: float
    laps_to_catch: Optional[int] = None


class PitWindowOutput(BaseModel):
    """Output from pit window calculation"""
    optimal_lap: Optional[int] = None
    window_opens_lap: Optional[int] = None
    window_closes_lap: Optional[int] = None


class StintStateOutput(BaseModel):
    """Output from stint state tracking"""
    stint_progress: float = Field(..., ge=0.0, le=1.0, description="0=start, 1=end")
    pace_delta_s: float = Field(..., description="Current pace vs initial pace")
    stint_phase: str = Field(..., description="early/mid/late/critical")


class PositionPressureOutput(BaseModel):
    """Output from position pressure calculation"""
    pressure_rating: float = Field(..., ge=0.0, le=10.0)


# ============================================================================
# AGGREGATION OUTPUTS
# ============================================================================

class DriverCarFusionOutput(BaseModel):
    """Output from driver-car fusion"""
    combined_performance: float = Field(..., ge=0.0, le=10.0)



class TyreCarFusionOutput(BaseModel):
    """Output from tyre-car fusion"""
    expected_pace_delta_s: float = Field(..., description="Expected pace delta")
    expected_degradation_rate: float = Field(..., ge=0.0)


class RaceContextOutput(BaseModel):
    """Output from race context builder"""
    race_phase: str = Field(..., description="opening/middle/late/closing")
    context_data: Dict[str, Any] = Field(default_factory=dict)
