"""
Calculation Input Models
Pydantic models defining standardized inputs for all calculation modules
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Literal


# ============================================================================
# TYRE CALCULATION INPUTS
# ============================================================================

class TyreCompoundInput(BaseModel):
    """Input for compound-related calculations"""
    compound: Literal["SOFT", "MEDIUM", "HARD", "INTERMEDIATE", "WET"]
    avg_lifetime_laps: Optional[float] = None
    degradation_rate: Optional[float] = None
    optimal_temp_c: Optional[float] = 90.0


class TyreDegradationInput(BaseModel):
    """Input for degradation curve calculations"""
    wear_level: float = Field(..., ge=0.0, le=1.0, description="Tyre wear (0=new, 1=dead)")
    temp_factor: float = Field(1.0, ge=0.0, le=2.0, description="Temperature multiplier")
    push_level: float = Field(0.5, ge=0.0, le=1.0, description="Driver push intensity")
    track_abrasion: float = Field(0.5, ge=0.0, le=1.0, description="Track surface severity")


class TyreLifeInput(BaseModel):
    """Input for tyre life projection"""
    total_expected_life: int = Field(..., gt=0, description="Expected tyre life in laps")
    laps_completed: int = Field(..., ge=0, description="Laps already done on this tyre")
    current_degradation_rate: float = Field(..., ge=0.0, description="Current deg rate (s/lap)")


# ============================================================================
# CAR CALCULATION INPUTS
# ============================================================================

class CarPerformanceInput(BaseModel):
    """Input for car performance index calculation"""
    power_rating: float = Field(..., ge=0.0, le=10.0, description="Power unit performance")
    aero_rating: float = Field(..., ge=0.0, le=10.0, description="Aerodynamic efficiency")
    drag_coefficient: float = Field(..., ge=0.0, le=10.0, description="Drag level")
    mechanical_grip: float = Field(..., ge=0.0, le=10.0, description="Mechanical grip")


class FuelEffectInput(BaseModel):
    """Input for fuel weight effect calculation"""
    fuel_load_kg: float = Field(..., ge=0.0, le=110.0, description="Current fuel load")
    fuel_sensitivity: float = Field(0.03, ge=0.0, description="Seconds per kg penalty")


class AeroDragInput(BaseModel):
    """Input for aero vs drag balance"""
    downforce_level: float = Field(..., ge=0.0, le=10.0)
    drag_level: float = Field(..., ge=0.0, le=10.0)


class ReliabilityInput(BaseModel):
    """Input for reliability risk calculation"""
    reliability_score: float = Field(..., ge=0.0, le=1.0, description="Reliability rating")
    age_factor: float = Field(1.0, ge=0.5, le=2.0, description="Component age multiplier")


# ============================================================================
# DRIVER CALCULATION INPUTS
# ============================================================================

class DriverPaceInput(BaseModel):
    """Input for driver pace delta calculation"""
    driver_lap_times: List[float] = Field(..., min_items=1, description="Driver lap times")
    field_average_lap_time: float = Field(..., gt=0.0, description="Field average")


class ConsistencyInput(BaseModel):
    """Input for consistency calculation"""
    lap_times: List[float] = Field(..., min_items=3, description="Lap time samples")


class DriverFormInput(BaseModel):
    """Input for recent form calculation"""
    recent_lap_times: List[float] = Field(..., min_items=5, description="Last 5-10 laps")
    window_size: int = Field(10, ge=5, le=20, description="Laps to consider")


class ErrorRiskInput(BaseModel):
    """Input for error/incident risk"""
    incidents_count: int = Field(..., ge=0, description="Number of mistakes")
    total_laps: int = Field(..., gt=0, description="Total laps completed")


class RacecraftInput(BaseModel):
    """Input for racecraft score"""
    overtakes_made: int = Field(..., ge=0)
    overtakes_defended: int = Field(..., ge=0)
    positions_gained: int = Field(0, description="Net positions gained")
    positions_lost: int = Field(0, description="Net positions lost")


# ============================================================================
# TRACK CALCULATION INPUTS
# ============================================================================

class PitLossInput(BaseModel):
    """Input for pit lane time loss"""
    pit_lane_length_m: float = Field(..., gt=0.0, description="Pit lane length")
    pit_speed_limit_kmh: float = Field(60.0, gt=0.0, description="Speed limit")
    entry_exit_time_s: float = Field(5.0, ge=0.0, description="Entry/exit time loss")


class OvertakingDifficultyInput(BaseModel):
    """Input for overtaking difficulty score"""
    drs_zones_count: int = Field(..., ge=0, le=3)
    corner_count: int = Field(..., ge=0)
    straight_length_m: float = Field(..., ge=0.0)


class DirtyAirInput(BaseModel):
    """Input for dirty air penalty"""
    aero_sensitivity: float = Field(..., ge=0.0, le=1.0, description="Car aero dependence")
    track_aero_factor: float = Field(0.5, ge=0.0, le=1.0, description="Track downforce need")


class TrackDifficultyInput(BaseModel):
    """Input for track difficulty index"""
    corners: int = Field(..., gt=0)
    lap_length_km: float = Field(..., gt=0.0)


# ============================================================================
# TRAFFIC CALCULATION INPUTS
# ============================================================================

class TrafficDensityInput(BaseModel):
    """Input for traffic density calculation"""
    gap_times_seconds: List[float] = Field(..., description="Gaps to cars ahead/behind")
    drs_threshold_s: float = Field(1.0, gt=0.0, description="DRS activation gap")


class DefenseEffectivenessInput(BaseModel):
    """Input for defensive driving effectiveness"""
    driver_skill: float = Field(..., ge=0.0, le=1.0)
    track_width_m: float = Field(12.0, gt=0.0)


class OvertakeCostInput(BaseModel):
    """Input for overtake time cost"""
    overtake_difficulty: float = Field(..., ge=0.0, le=1.0, description="From track calc")
    speed_delta_kmh: float = Field(..., ge=0.0, description="Speed advantage")


class TrainProbabilityInput(BaseModel):
    """Input for DRS train formation probability"""
    traffic_density: int = Field(..., ge=0, description="Cars within DRS range")
    lap_count: int = Field(..., gt=0, description="Current lap number")


# ============================================================================
# WEATHER CALCULATION INPUTS
# ============================================================================

class GripEvolutionInput(BaseModel):
    """Input for track grip evolution"""
    rubber_buildup: float = Field(..., ge=0.0, le=1.0, description="Track rubbering")
    track_temp_c: float = Field(..., description="Track temperature")
    session_progress: float = Field(..., ge=0.0, le=1.0, description="Session completion")


class CoolingMarginInput(BaseModel):
    """Input for engine cooling margin"""
    ambient_temp_c: float = Field(..., description="Air temperature")
    humidity_pct: float = Field(..., ge=0.0, le=100.0)
    altitude_m: float = Field(0.0, ge=0.0, description="Track altitude")


class CrossoverLapInput(BaseModel):
    """Input for wet/dry crossover lap"""
    track_wetness: float = Field(..., ge=0.0, le=1.0, description="0=dry, 1=soaked")
    drying_rate: float = Field(..., ge=0.0, description="Wetness reduction per lap")
    rainfall_intensity: float = Field(0.0, ge=0.0, description="Current rainfall")


class WeatherVolatilityInput(BaseModel):
    """Input for weather volatility score"""
    weather_changes_count: int = Field(..., ge=0, description="Weather change events")
    forecast_confidence: float = Field(0.7, ge=0.0, le=1.0)


# ============================================================================
# RACE STATE CALCULATION INPUTS
# ============================================================================

class GapProjectionInput(BaseModel):
    """Input for future gap projection"""
    current_gap_s: float = Field(..., description="Current gap to target")
    pace_delta_s_per_lap: float = Field(..., description="Pace difference per lap")
    laps_remaining: int = Field(..., gt=0)


class PitWindowInput(BaseModel):
    """Input for pit window calculation"""
    tyre_remaining_life_laps: int = Field(..., ge=0)
    minimum_stint_laps: int = Field(10, ge=1)
    maximum_stint_laps: int = Field(30, ge=1)


class StintStateInput(BaseModel):
    """Input for stint progress tracking"""
    laps_completed: int = Field(..., ge=0)
    planned_stint_length: int = Field(..., gt=0)


class PositionPressureInput(BaseModel):
    """Input for track position pressure/value"""
    current_position: int = Field(..., ge=1, le=20)
    points_positions: int = Field(10, ge=1, le=20, description="Points-paying positions")


# ============================================================================
# AGGREGATION INPUTS
# ============================================================================

class DriverCarFusionInput(BaseModel):
    """Input for combining driver + car performance"""
    driver_skill: float = Field(..., ge=0.0, le=10.0)
    car_performance: float = Field(..., ge=0.0, le=10.0)
    synergy_factor: float = Field(1.0, ge=0.5, le=1.5, description="Driver-car fit")


class TyreCarFusionInput(BaseModel):
    """Input for tyre-car interaction"""
    tyre_degradation_rate: float = Field(..., ge=0.0)
    car_downforce: float = Field(..., ge=0.0, le=10.0)
    tyre_energy_factor: float = Field(..., ge=0.0)
