"""
Driver Engine Schemas - FastF1 Implementation
Driver performance, consistency, and racecraft analysis
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class DriverRequest(BaseModel):
    """Request for driver analysis"""
    year: int = Field(..., ge=2018, le=2025, description="Season year")
    gp: str = Field(..., description="Grand Prix name")
    session: str = Field(..., description="Session type: FP1, FP2, FP3, Q, S, R")
    driver_number: Optional[int] = Field(None, description="Specific driver (None = all)")


class ConsistencyMetrics(BaseModel):
    """Driver consistency analysis"""
    driver_number: int
    driver_name: str
    lap_time_std_dev_sec: float
    valid_laps: int
    mistakes_count: int  # Laps significantly slower than average
    consistency_score: float = Field(..., ge=0.0, le=1.0)


class RacecraftMetrics(BaseModel):
    """Racecraft and wheel-to-wheel performance"""
    driver_number: int
    overtakes_made: int
    overtakes_defended: int
    positions_gained: int
    positions_lost: int
    battle_win_rate: float


class TyreManagementMetrics(BaseModel):
    """Tyre management capability"""
    driver_number: int
    avg_stint_length_laps: float
    degradation_vs_teammate: float  # Negative = better than teammate
    optimal_temp_maintenance_score: float
    compound_preference: Optional[str] = None


class SectorPerformance(BaseModel):
    """Sector-by-sector performance"""
    driver_number: int
    sector_1_avg_sec: float
    sector_2_avg_sec: float
    sector_3_avg_sec: float
    best_sector: int
    worst_sector: int


class HistoricalStats(BaseModel):
    """Historical performance at this circuit"""
    driver_number: int
    races_at_circuit: int
    podiums_at_circuit: int
    avg_finish_position: float
    best_finish: int
    avg_quali_position: float


class DriverProfile(BaseModel):
    """Comprehensive driver profile"""
    driver_number: int
    driver_name: str
    team: str
    consistency: ConsistencyMetrics
    racecraft: RacecraftMetrics
    tyre_management: TyreManagementMetrics
    sector_performance: SectorPerformance
    historical_stats: Optional[HistoricalStats] = None
    overall_rating: float = Field(..., ge=0.0, le=10.0)


class DriverResponse(BaseModel):
    """Response with comprehensive driver analysis"""
    circuit_name: str
    session_type: str
    driver_profiles: List[DriverProfile]
    session_winner: Optional[int] = None
    most_consistent_driver: Optional[int] = None
    best_racecraft_driver: Optional[int] = None
