"""
Safety Car Engine Schemas - FastF1 Implementation
Track status timeline and safety car period analysis
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class SafetyCarRequest(BaseModel):
    """Request for safety car analysis"""
    year: int = Field(..., ge=2018, le=2025, description="Season year")
    gp: str = Field(..., description="Grand Prix name")
    session: str = Field(..., description="Session type (typically 'R' for race)")


class TrackStatusPeriod(BaseModel):
    """Track status period details"""
    status: str  # "Clear", "Yellow", "SC", "VSC", "Red"
    start_lap: int
    end_lap: Optional[int] = None
    duration_laps: int
    reason: Optional[str] = None


class SafetyCarDeployment(BaseModel):
    """Safety car deployment details"""
    deployment_type: str  # "Full SC" or "VSC"
    start_lap: int
    end_lap: int
    duration_laps: int
    restart_lap: int
    trigger_reason: Optional[str] = None
    field_compression_sec: float


class StrategyImpact(BaseModel):
    """Impact of safety car on strategy"""
    driver_number: int
    driver_name: str
    position_before: int
    position_after: int
    pitted_under_sc: bool
    time_advantage_sec: Optional[float] = None
    strategy_beneficiary: bool


class SafetyCarResponse(BaseModel):
    """Response with safety car analysis"""
    circuit_name: str
    session_type: str
    track_status_timeline: List[TrackStatusPeriod]
    safety_car_deployments: List[SafetyCarDeployment]
    strategy_impacts: List[StrategyImpact]
    total_sc_laps: int
    total_vsc_laps: int
    racing_laps_pct: float
    historical_sc_probability: float = Field(..., ge=0.0, le=1.0)
