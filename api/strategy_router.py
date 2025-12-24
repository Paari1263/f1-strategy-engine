"""
Strategy Analysis APIs
GET endpoints for race strategy insights
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from api.models import (
    PitStrategyResponse,
    BattleForecastResponse,
    SessionType,
    CompoundType
)
from strategy_engines import PitStrategySimulator, BattleForecast


router = APIRouter(prefix="/api/v1/strategy")


@router.get("/pit-optimization", response_model=PitStrategyResponse)
async def optimize_pit_strategy(
    year: int = Query(..., description="Season year"),
    event: str = Query(..., description="Grand Prix name"),
    driver: str = Query(..., description="Driver code"),
    current_lap: int = Query(..., ge=1, description="Current lap number"),
    total_laps: int = Query(..., ge=1, description="Total race laps"),
    current_compound: CompoundType = Query(..., description="Current tyre compound"),
    tyre_age: int = Query(..., ge=0, description="Current tyre age in laps"),
    position: int = Query(..., ge=1, le=20, description="Current race position"),
    gap_ahead: Optional[float] = Query(None, description="Gap to car ahead (seconds)"),
    gap_behind: Optional[float] = Query(None, description="Gap to car behind (seconds)")
):
    """
    Optimize pit stop strategy for current race situation.
    
    Uses calculation_engines:
    - tyre_calculations/optimal_pit_window.py
    - race_state_calculations/undercut_calculator.py
    - race_state_calculations/overcut_calculator.py
    - tyre_calculations/compound_recommendation.py
    
    Returns optimal pit lap, pit window, undercut/overcut advantages,
    and compound recommendation.
    """
    try:
        simulator = PitStrategySimulator()
        
        strategy = simulator.calculate_optimal_strategy(
            current_lap=current_lap,
            total_laps=total_laps,
            current_compound=current_compound.value,
            current_tyre_age=tyre_age,
            gap_ahead=gap_ahead,
            gap_behind=gap_behind
        )
        
        # Calculate alternative strategies
        alternatives = []
        
        # 1-stop alternative
        if strategy.strategy_type != "ONE_STOP":
            alternatives.append({
                'type': 'ONE_STOP',
                'pit_lap': current_lap + 10,
                'compound': 'HARD',
                'expected_finish': position
            })
        
        # 2-stop alternative
        if total_laps - current_lap > 30:
            alternatives.append({
                'type': 'TWO_STOP',
                'pit_laps': [current_lap + 8, current_lap + 25],
                'compounds': ['MEDIUM', 'SOFT'],
                'expected_finish': position - 1 if strategy.undercut_advantage > 1.5 else position
            })
        
        return PitStrategyResponse(
            year=year,
            event=event,
            driver=driver,
            current_lap=current_lap,
            total_laps=total_laps,
            position=position,
            optimal_pit_lap=strategy.optimal_pit_lap,
            pit_window_start=strategy.pit_window_start,
            pit_window_end=strategy.pit_window_end,
            recommended_compound=strategy.recommended_compound,
            expected_stint_length=strategy.expected_stint_length,
            undercut_advantage=strategy.undercut_advantage,
            overcut_advantage=strategy.overcut_advantage,
            strategy_type=strategy.strategy_type,
            confidence=strategy.confidence,
            alternative_strategies=alternatives
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error optimizing pit strategy: {str(e)}")


@router.get("/battle-forecast", response_model=BattleForecastResponse)
async def forecast_battle(
    year: int = Query(..., description="Season year"),
    event: str = Query(..., description="Grand Prix name"),
    session: SessionType = Query(..., description="Session type"),
    lap: int = Query(..., ge=1, description="Current lap number"),
    attacker: str = Query(..., description="Attacking driver code"),
    defender: str = Query(..., description="Defending driver code"),
    gap: float = Query(..., ge=0, description="Current gap in seconds"),
    drs_available: bool = Query(False, description="DRS available for attacker")
):
    """
    Forecast battle outcome and overtaking probability.
    
    Uses calculation_engines:
    - traffic_calculations/overtaking_probability.py
    - car_calculations/drs_advantage.py
    - track_calculations/overtaking_zones.py
    
    Returns overtake probability, best zones, and strategic recommendation.
    """
    try:
        # Note: BattleForecast requires telemetry data
        # This is a simplified version for API demonstration
        
        # Simulate telemetry data would be loaded here
        # For now, return calculated probabilities
        
        # Track difficulty mapping
        track_difficulty = {
            'Monaco': 9.0,
            'Singapore': 8.5,
            'Hungary': 7.5,
            'Barcelona': 5.0,
            'Silverstone': 4.5,
            'Spa': 3.5,
            'Monza': 2.5
        }.get(event, 5.0)
        
        # Calculate probability based on gap and DRS
        base_probability = max(0, 1 - (gap / 2.0))  # Closer gap = higher probability
        drs_boost = 0.25 if drs_available else 0.0
        track_penalty = track_difficulty / 20.0  # Higher difficulty = lower probability
        
        probability = min(1.0, max(0.0, base_probability + drs_boost - track_penalty))
        
        # Determine strategy
        if probability > 0.6:
            strategy = "ATTACK"
        elif probability > 0.3:
            strategy = "PREPARE"
        else:
            strategy = "DEFEND"
        
        # Best overtaking zone
        if track_difficulty < 5.0:
            best_zone = "Main Straight with DRS"
        elif track_difficulty < 7.0:
            best_zone = "Heavy Braking Zone Turn 1"
        else:
            best_zone = "Limited opportunities - be patient"
        
        # Speed advantage estimation
        speed_advantage = 8.0 if drs_available else 3.0
        drs_impact = 12.0 if drs_available else 0.0
        
        # Key factors
        key_factors = []
        if gap < 1.0:
            key_factors.append("Close gap favorable for attack")
        if drs_available:
            key_factors.append("DRS provides significant advantage")
        if track_difficulty > 7.0:
            key_factors.append("Track layout makes overtaking difficult")
        
        # Lap-by-lap forecast (next 5 laps)
        lap_forecast = []
        projected_gap = gap
        for i in range(1, 6):
            if probability > 0.5:
                projected_gap = max(0.3, projected_gap - 0.15)  # Closing
            else:
                projected_gap = projected_gap + 0.05  # Opening
                
            lap_forecast.append({
                'lap': lap + i,
                'projected_gap': round(projected_gap, 2),
                'overtake_probability': round(min(1.0, probability + (i * 0.05)), 2)
            })
        
        return BattleForecastResponse(
            year=year,
            event=event,
            session=session.value,
            lap=lap,
            attacker=attacker,
            defender=defender,
            overtake_probability=round(probability, 3),
            best_overtaking_zone=best_zone,
            recommended_strategy=strategy,
            speed_advantage=speed_advantage,
            drs_impact=drs_impact,
            track_difficulty=track_difficulty,
            key_factors=key_factors,
            lap_by_lap_forecast=lap_forecast
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error forecasting battle: {str(e)}")
