"""
Car Engine Schemas - FastF1 Implementation
Detailed car performance analysis from high-resolution telemetry
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class CarRequest(BaseModel):
    """Request for car performance analysis"""
    year: int = Field(..., ge=2018, le=2025, description="Season year")
    gp: str = Field(..., description="Grand Prix name (e.g., 'Bahrain')")
    session: str = Field(..., description="Session type: FP1, FP2, FP3, Q, S, R")
    driver_number: Optional[int] = Field(None, description="Specific driver number (None = all drivers)")


class TelemetryStats(BaseModel):
    """Statistical analysis of telemetry channel"""
    avg: float
    min: float
    max: float
    std: float


class PowerUnitMetrics(BaseModel):
    """Power unit performance metrics"""
    avg_rpm: float
    max_rpm: float
    avg_throttle_pct: float
    full_throttle_time_pct: float
    gear_changes_per_lap: float
    top_speed_kmh: float


class AerodynamicsMetrics(BaseModel):
    """Aerodynamic performance indicators"""
    drs_usage_pct: float
    drs_speed_gain_kmh: float
    avg_speed_fast_corners_kmh: float
    avg_speed_slow_corners_kmh: float
    downforce_estimate: str  # "High", "Medium", "Low"


class BrakingMetrics(BaseModel):
    """Braking performance analysis"""
    avg_brake_pressure: float
    max_brake_pressure: float
    braking_zones_per_lap: int
    brake_efficiency_score: float


class CarPerformanceProfile(BaseModel):
    """Comprehensive car performance profile"""
    driver_number: int
    driver_name: str
    team: str
    power_unit: PowerUnitMetrics
    aerodynamics: AerodynamicsMetrics
    braking: BrakingMetrics
    consistency_score: float
    lap_time_avg_sec: float
    lap_time_best_sec: float


class CarResponse(BaseModel):
    """Response with detailed car performance analysis"""
    circuit_name: str
    session_type: str
    car_profiles: List[CarPerformanceProfile]
    fastest_car: Optional[str] = None
    comparative_analysis: Optional[dict] = None
