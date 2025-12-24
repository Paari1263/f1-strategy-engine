"""
Weather Engine Schemas - FastF1 Implementation
Lap-by-lap weather tracking and performance correlation
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class WeatherRequest(BaseModel):
    """Request for weather analysis"""
    year: int = Field(..., ge=2018, le=2025, description="Season year")
    gp: str = Field(..., description="Grand Prix name")
    session: str = Field(..., description="Session type: FP1, FP2, FP3, Q, S, R")


class LapWeatherSnapshot(BaseModel):
    """Weather conditions at specific lap"""
    lap_number: int
    air_temp_c: float
    track_temp_c: float
    humidity_pct: int
    pressure_mbar: float
    rainfall: bool
    wind_speed_ms: float
    wind_direction_deg: int


class WeatherTrend(BaseModel):
    """Weather evolution trend"""
    parameter: str  # "air_temp", "track_temp", "humidity", etc.
    start_value: float
    end_value: float
    change_rate_per_lap: float
    trend: str  # "Increasing", "Decreasing", "Stable"


class WeatherImpactAnalysis(BaseModel):
    """Performance impact of weather"""
    lap_time_impact_sec: float
    tyre_deg_multiplier: float
    grip_level_multiplier: float
    rainfall_probability_next_10_laps: float


class WeatherResponse(BaseModel):
    """Response with detailed weather analysis"""
    circuit_name: str
    session_type: str
    session_start_time: str
    session_end_time: str
    lap_snapshots: List[LapWeatherSnapshot]
    weather_trends: List[WeatherTrend]
    impact_analysis: WeatherImpactAnalysis
    conditions_summary: str  # "Dry", "Wet", "Mixed", "Changing"
    track_evolution_favorable: bool
