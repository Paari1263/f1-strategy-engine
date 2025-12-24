from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class TrackRequest(BaseModel):
    year: int = Field(..., ge=2018, le=2025, description="Season year")
    gp: str = Field(..., description="Grand Prix name (e.g., 'Bahrain') or round number")
    session: str = Field(..., description="Session type: FP1, FP2, FP3, Q, SQ, R, S")


class SectorAnalysis(BaseModel):
    sector_number: int
    length_km: float
    avg_speed_kmh: float
    min_speed_kmh: float
    max_speed_kmh: float
    characteristics: str  # "High-speed", "Technical", "Mixed"


class DRSZone(BaseModel):
    zone_number: int
    activation_distance_m: float
    length_m: float
    speed_delta_kmh: float
    effectiveness_score: float  # 0-1


class TrackEvolution(BaseModel):
    session_type: str
    avg_grip_level: float
    improvement_per_lap_ms: float
    total_improvement_ms: float


class TrackResponse(BaseModel):
    # Circuit Information
    circuit_name: str
    location: str
    country: str
    length_km: float
    corners: int
    lap_record_seconds: Optional[float] = None
    
    # Track Characteristics
    grip_multiplier: float = Field(..., description="Track grip level (0.8-1.2)")
    tyre_abrasion_level: float = Field(..., description="Surface abrasiveness (0.0-1.0)")
    pit_lane_time_loss_sec: float = Field(..., description="Time lost in pit stops")
    overtaking_difficulty: float = Field(..., description="How hard to overtake (0.0-1.0)")
    power_sensitivity: float = Field(..., description="How much power matters (0.0-1.0)")
    corner_sensitivity: float = Field(..., description="How much cornering matters (0.0-1.0)")
    
    # Detailed Analysis
    sector_analysis: List[SectorAnalysis]
    drs_zones: List[DRSZone]
    track_evolution: List[TrackEvolution]
    
    # Advanced Metrics
    elevation_range_m: Optional[float] = None
    top_speed_kmh: float
    slowest_corner_kmh: float
    avg_lap_speed_kmh: float
    
    # Historical Context
    historical_safety_car_probability: float
    weather_sensitivity: float  # How much weather affects this track
