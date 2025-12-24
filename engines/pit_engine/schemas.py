"""
Pit Engine Schemas - FastF1 Implementation
Pit stop analysis with exact durations and strategy impact
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class PitRequest(BaseModel):
    """Request for pit stop analysis"""
    year: int = Field(..., ge=2018, le=2025, description="Season year")
    gp: str = Field(..., description="Grand Prix name")
    session: str = Field(..., description="Session type (typically 'R' for race)")
    driver_number: Optional[int] = Field(None, description="Specific driver (None = all)")


class PitStopDetail(BaseModel):
    """Individual pit stop details"""
    driver_number: int
    driver_name: str
    team: str
    lap_number: int
    pit_duration_sec: float
    tyre_change_time_sec: float
    in_lap_time_sec: float
    out_lap_time_sec: float
    positions_lost: int
    positions_gained: int
    compound_fitted: str


class TeamPitPerformance(BaseModel):
    """Team-level pit performance"""
    team: str
    avg_pit_duration_sec: float
    fastest_stop_sec: float
    slowest_stop_sec: float
    consistency_score: float
    total_stops: int


class PitStrategyAnalysis(BaseModel):
    """Strategic pit stop analysis"""
    driver_number: int
    total_stops: int
    stop_laps: List[int]
    total_time_lost_sec: float
    strategy_type: str  # "1-stop", "2-stop", "3-stop", etc.
    undercut_attempts: int
    overcut_attempts: int
    effective_strategy: bool


class PitResponse(BaseModel):
    """Response with comprehensive pit analysis"""
    circuit_name: str
    session_type: str
    pit_stops: List[PitStopDetail]
    team_performance: List[TeamPitPerformance]
    strategy_analyses: List[PitStrategyAnalysis]
    fastest_stop_overall: Optional[PitStopDetail] = None
    avg_pit_lane_time_loss_sec: float
    pit_window_recommendations: List[int]  # Optimal lap numbers
