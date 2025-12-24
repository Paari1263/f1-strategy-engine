"""
Traffic Engine Schemas - FastF1 Implementation
Gap analysis, overtaking patterns, and DRS train detection
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class TrafficRequest(BaseModel):
    """Request for traffic analysis"""
    year: int = Field(..., ge=2018, le=2025, description="Season year")
    gp: str = Field(..., description="Grand Prix name")
    session: str = Field(..., description="Session type: FP1, FP2, FP3, Q, S, R")
    focus_driver: Optional[int] = Field(None, description="Driver number to focus on")


class GapEvolution(BaseModel):
    """Gap evolution between drivers"""
    lap_number: int
    leader_driver: int
    gap_to_leader_sec: float
    gap_to_ahead_sec: float
    gap_to_behind_sec: float
    position: int


class OvertakeEvent(BaseModel):
    """Overtaking maneuver details"""
    lap_number: int
    overtaking_driver: int
    overtaken_driver: int
    location: str  # Corner/sector where overtake occurred
    drs_enabled: bool
    gap_before_sec: float
    gap_after_sec: float


class DRSTrainAnalysis(BaseModel):
    """DRS train formation analysis"""
    lap_number: int
    train_members: List[int]  # Driver numbers
    leader: int
    train_length: int
    avg_gap_within_train_sec: float
    laps_in_formation: int


class TrafficDensityMetric(BaseModel):
    """Traffic density indicators"""
    lap_number: int
    cars_within_1sec: int
    cars_within_3sec: int
    avg_gap_to_car_ahead_sec: float
    overtaking_opportunities: int


class TrafficResponse(BaseModel):
    """Response with comprehensive traffic analysis"""
    circuit_name: str
    session_type: str
    focus_driver_number: Optional[int] = None
    gap_evolution: List[GapEvolution]
    overtake_events: List[OvertakeEvent]
    drs_trains: List[DRSTrainAnalysis]
    traffic_density: List[TrafficDensityMetric]
    overtaking_difficulty_score: float = Field(..., ge=0.0, le=1.0)
    avg_overtakes_per_lap: float
