"""
Tyre Engine Schemas - FastF1 Implementation
Advanced tyre compound analysis with degradation modeling
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class TyreRequest(BaseModel):
    """Request for tyre performance analysis"""
    year: int = Field(..., ge=2018, le=2025, description="Season year")
    gp: str = Field(..., description="Grand Prix name")
    session: str = Field(..., description="Session type: FP1, FP2, FP3, Q, S, R")
    driver_number: Optional[int] = Field(None, description="Specific driver (None = all)")


class CompoundCharacteristics(BaseModel):
    """Tyre compound characteristics"""
    compound: str  # SOFT, MEDIUM, HARD, INTERMEDIATE, WET
    avg_lifetime_laps: float
    degradation_rate_sec_per_lap: float
    optimal_temp_range_c: str
    performance_window_laps: int
    cliff_lap: Optional[int] = None


class StintAnalysis(BaseModel):
    """Individual stint performance"""
    driver_number: int
    driver_name: str
    compound: str
    stint_number: int
    lap_start: int
    lap_end: int
    total_laps: int
    tyre_age_at_start: int
    avg_lap_time_sec: float
    degradation_observed_sec_per_lap: float
    grip_level_start: float
    grip_level_end: float
    thermal_state: str  # "Optimal", "Underheating", "Overheating", "Graining", "Blistering"


class TyreStrategyRecommendation(BaseModel):
    """Strategic recommendations"""
    optimal_compound_order: List[str]
    estimated_pit_windows: List[int]  # Lap numbers
    risk_assessment: str  # "Low", "Medium", "High"


class TyreResponse(BaseModel):
    """Response with comprehensive tyre analysis"""
    circuit_name: str
    session_type: str
    compound_characteristics: List[CompoundCharacteristics]
    stint_analyses: List[StintAnalysis]
    strategy_recommendation: Optional[TyreStrategyRecommendation] = None
    track_tyre_severity: float = Field(..., ge=0.0, le=1.0, description="0=gentle, 1=severe")
