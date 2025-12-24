"""
API Request/Response Models
Pydantic models for API endpoints
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


class SessionType(str, Enum):
    """F1 Session Types"""
    FP1 = "FP1"
    FP2 = "FP2"
    FP3 = "FP3"
    Q = "Q"
    Q1 = "Q1"
    Q2 = "Q2"
    Q3 = "Q3"
    R = "R"
    S = "S"
    SS = "SS"


class CompoundType(str, Enum):
    """Tyre Compound Types"""
    SOFT = "SOFT"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    INTERMEDIATE = "INTERMEDIATE"
    WET = "WET"


# Detailed Car Performance Models

class CarMetadata(BaseModel):
    """Car metadata"""
    team: str
    car: str
    session_key: int
    track: str
    driver: str


class PerformanceProfile(BaseModel):
    """Performance characteristics"""
    powerDelta: float = Field(description="Power unit delta vs baseline (seconds per lap)")
    aeroDelta: float = Field(description="Aero efficiency delta (seconds per lap)")
    dragPenalty: float = Field(description="Drag coefficient delta (seconds per lap)")
    mechanicalGripDelta: float = Field(description="Mechanical grip delta (seconds per lap)")


class TyreInteraction(BaseModel):
    """Tyre-car interaction"""
    tyreEnergyLoad: Dict[str, float] = Field(description="Energy load per compound (0-1 scale)")
    fuelWeightSensitivity: float = Field(description="Fuel weight sensitivity (sec/kg)")


class AeroBehavior(BaseModel):
    """Aerodynamic behavior"""
    downforceSensitivity: float = Field(description="Downforce sensitivity (0-1 scale)")
    dirtyAirAmplification: float = Field(description="Dirty air penalty multiplier (1.0 = baseline)")


class ThermalProfile(BaseModel):
    """Thermal management"""
    coolingSensitivity: Dict[str, float] = Field(description="Cooling sensitivity by component (0-1 scale)")


class ERSProfile(BaseModel):
    """ERS characteristics"""
    ersEfficiency: float = Field(description="ERS deployment efficiency (0-1 scale)")


class ReliabilityProfile(BaseModel):
    """Reliability metrics"""
    reliabilityStress: float = Field(description="Component stress level (0-1 scale)")
    pushFailureRisk: float = Field(description="Failure risk under stress (0-1 probability)")


class SetupProfile(BaseModel):
    """Setup characteristics"""
    kerbCompliance: float = Field(description="Kerb riding capability (0-1 scale)")
    setupFlexibility: float = Field(description="Setup window flexibility (0-1 scale)")


class SessionBias(BaseModel):
    """Session performance bias"""
    qualifyingRaceBias: Dict[str, float] = Field(description="Qualifying vs race bias")


class DetailedCarPerformance(BaseModel):
    """Detailed car performance profile"""
    metadata: CarMetadata
    performance_profile: PerformanceProfile
    tyre_interaction: TyreInteraction
    aero_behavior: AeroBehavior
    thermal_profile: ThermalProfile
    ers_profile: ERSProfile
    reliability_profile: ReliabilityProfile
    setup_profile: SetupProfile
    session_bias: SessionBias


class CarComparisonDetailedResponse(BaseModel):
    """Car vs Car detailed comparison"""
    car1: DetailedCarPerformance
    car2: DetailedCarPerformance
    delta_analysis: Dict[str, Any] = Field(description="Comparative deltas between cars")
    overall_advantage: str = Field(description="Overall performance advantage winner")


# Response Models

class CarPerformanceResponse(BaseModel):
    """Car vs Car Performance Comparison Response"""
    year: int
    event: str
    session: str
    driver1: str
    driver2: str
    
    speed_analysis: Dict[str, Any] = Field(description="Speed comparison metrics")
    braking_analysis: Dict[str, Any] = Field(description="Braking performance comparison")
    cornering_analysis: Dict[str, Any] = Field(description="Cornering performance comparison")
    straight_line_analysis: Dict[str, Any] = Field(description="Straight-line performance comparison")
    
    lap_time_delta: float = Field(description="Lap time delta in seconds")
    winner: str = Field(description="Performance winner")
    overall_rating: Dict[str, float] = Field(description="Overall performance ratings")


class DriverPaceResponse(BaseModel):
    """Driver vs Driver Pace Comparison Response"""
    year: int
    event: str
    session: str
    driver1: str
    driver2: str
    
    fastest_lap: Dict[str, float] = Field(description="Fastest lap times")
    median_pace: Dict[str, float] = Field(description="Median lap times")
    average_pace: Dict[str, float] = Field(description="Average lap times")
    fuel_corrected_pace: Optional[Dict[str, float]] = Field(description="Fuel-corrected pace")
    
    pace_delta: float = Field(description="Pace delta in seconds")
    pace_advantage: str = Field(description="Driver with pace advantage")
    stint_comparison: List[Dict[str, Any]] = Field(description="Stint-by-stint comparison")


class TyrePerformanceResponse(BaseModel):
    """Tyre Performance Comparison Response"""
    year: int
    event: str
    session: str
    driver1: str
    driver2: str
    compound: str
    
    degradation_rate: Dict[str, float] = Field(description="Degradation rate per lap")
    grip_loss: Dict[str, float] = Field(description="Total grip loss percentage")
    pace_falloff: Dict[str, List[float]] = Field(description="Pace over stint laps")
    tyre_life: Dict[str, int] = Field(description="Optimal tyre life in laps")
    
    better_management: str = Field(description="Driver with better tyre management")
    management_score: Dict[str, float] = Field(description="Tyre management scores")


class DriverProfileResponse(BaseModel):
    """Single Driver Performance Profile Response"""
    year: int
    event: str
    session: str
    driver: str
    
    pace_metrics: Dict[str, Any] = Field(description="Pace analysis")
    consistency_metrics: Dict[str, Any] = Field(description="Consistency analysis")
    tyre_management: Dict[str, Any] = Field(description="Tyre management metrics")
    car_performance: Dict[str, Any] = Field(description="Car performance metrics")
    
    strengths: List[str] = Field(description="Performance strengths")
    weaknesses: List[str] = Field(description="Performance weaknesses")
    overall_rating: float = Field(description="Overall performance rating 0-10")


class PitStrategyResponse(BaseModel):
    """Pit Strategy Optimization Response"""
    year: int
    event: str
    driver: str
    current_lap: int
    total_laps: int
    position: int
    
    optimal_pit_lap: int = Field(description="Recommended pit lap")
    pit_window_start: int = Field(description="Earliest pit lap")
    pit_window_end: int = Field(description="Latest pit lap")
    
    recommended_compound: str = Field(description="Recommended tyre compound")
    expected_stint_length: int = Field(description="Expected stint length")
    
    undercut_advantage: float = Field(description="Undercut time advantage in seconds")
    overcut_advantage: float = Field(description="Overcut time advantage in seconds")
    
    strategy_type: str = Field(description="Strategy classification")
    confidence: float = Field(ge=0, le=1, description="Confidence in recommendation")
    alternative_strategies: List[Dict[str, Any]] = Field(description="Alternative strategy options")


class StintAnalysisResponse(BaseModel):
    """Driver Stint Analysis Response"""
    year: int
    event: str
    session: str
    driver: str
    stint_number: int
    
    pace_evolution: List[float] = Field(description="Lap times throughout stint")
    degradation_curve: List[float] = Field(description="Degradation per lap")
    fuel_effect: List[float] = Field(description="Fuel load impact per lap")
    traffic_impact: Dict[str, Any] = Field(description="Traffic-affected laps")
    
    average_pace: float = Field(description="Average stint pace")
    pace_vs_competitors: Dict[str, float] = Field(description="Pace vs other drivers")
    stint_rating: float = Field(description="Stint performance rating 0-10")


class ConsistencyResponse(BaseModel):
    """Driver Consistency Comparison Response"""
    year: int
    event: str
    session: str
    driver1: str
    driver2: str
    
    std_deviation: Dict[str, float] = Field(description="Lap time standard deviation")
    outlier_laps: Dict[str, int] = Field(description="Number of outlier laps")
    clean_lap_percentage: Dict[str, float] = Field(description="Clean lap percentage")
    degradation_management: Dict[str, float] = Field(description="Degradation management score")
    
    more_consistent: str = Field(description="More consistent driver")
    consistency_delta: float = Field(description="Consistency difference")


class BattleForecastResponse(BaseModel):
    """Battle Forecast Response"""
    year: int
    event: str
    session: str
    lap: int
    attacker: str
    defender: str
    
    overtake_probability: float = Field(ge=0, le=1, description="Overtaking probability")
    best_overtaking_zone: str = Field(description="Best zone for overtake")
    recommended_strategy: str = Field(description="ATTACK, PREPARE, or DEFEND")
    
    speed_advantage: float = Field(description="Speed advantage in km/h")
    drs_impact: float = Field(description="DRS speed boost")
    track_difficulty: float = Field(description="Track overtaking difficulty 0-10")
    
    key_factors: List[str] = Field(description="Key factors affecting overtake")
    lap_by_lap_forecast: List[Dict[str, Any]] = Field(description="Next 5 laps forecast")
