"""
Pit Strategy Simulator
Simulates pit stop strategies and calculates undercuts/overcuts
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from pydantic import BaseModel, Field


class PitStrategyOutput(BaseModel):
    """Output model for pit strategy analysis"""
    optimal_pit_lap: int = Field(description="Optimal lap to pit")
    pit_window_start: int = Field(description="Earliest recommended pit lap")
    pit_window_end: int = Field(description="Latest recommended pit lap")
    undercut_advantage: float = Field(description="Undercut time gain (seconds)")
    overcut_advantage: float = Field(description="Overcut time gain (seconds)")
    recommended_compound: str = Field(description="Recommended tyre compound")
    expected_stint_length: int = Field(description="Expected stint length (laps)")
    strategy_type: str = Field(description="Strategy classification")
    confidence: float = Field(ge=0, le=1, description="Confidence in recommendation")


class PitStrategySimulator:
    """
    Simulates pit stop strategies and optimizes timing.
    
    LOGIC:
    - Models tyre degradation over stint
    - Calculates pit stop time loss
    - Simulates undercut/overcut scenarios
    - Optimizes pit window based on race position and competitors
    
    ROLE:
    - Provides real-time pit strategy recommendations
    - Calculates undercut/overcut opportunities
    - Predicts optimal tyre compound choice
    
    SIGNIFICANCE:
    - Critical for race wins (strategy > pure pace)
    - Enables position gains through pit strategy
    - Manages tyre life vs track position trade-off
    """
    
    # Tyre degradation rates (seconds per lap loss)
    TYRE_DEGRADATION = {
        'SOFT': 0.05,      # High degradation
        'MEDIUM': 0.03,    # Medium degradation
        'HARD': 0.015      # Low degradation
    }
    
    # Typical stint lengths (laps)
    STINT_LENGTH = {
        'SOFT': 15,
        'MEDIUM': 25,
        'HARD': 35
    }
    
    # Pit stop time loss (seconds)
    PIT_LOSS = 20.0
    
    @staticmethod
    def calculate_optimal_strategy(current_lap: int, total_laps: int,
                                   current_compound: str, current_tyre_age: int,
                                   gap_ahead: Optional[float] = None,
                                   gap_behind: Optional[float] = None) -> PitStrategyOutput:
        """
        Calculate optimal pit strategy.
        
        Args:
            current_lap: Current lap number
            total_laps: Total race laps
            current_compound: Current tyre compound
            current_tyre_age: Current tyre age in laps
            gap_ahead: Gap to car ahead (seconds)
            gap_behind: Gap to car behind (seconds)
            
        Returns:
            PitStrategyOutput with strategy recommendation
        """
        remaining_laps = total_laps - current_lap
        
        # Calculate current tyre degradation
        degradation_rate = PitStrategySimulator.TYRE_DEGRADATION.get(current_compound, 0.03)
        current_pace_loss = current_tyre_age * degradation_rate
        
        # Estimate remaining life
        max_stint = PitStrategySimulator.STINT_LENGTH.get(current_compound, 25)
        remaining_life = max(0, max_stint - current_tyre_age)
        
        # Determine if pit stop needed
        if remaining_life >= remaining_laps:
            # Can finish on current tyres
            return PitStrategyOutput(
                optimal_pit_lap=total_laps + 1,  # No pit needed
                pit_window_start=total_laps + 1,
                pit_window_end=total_laps + 1,
                undercut_advantage=0.0,
                overcut_advantage=0.0,
                recommended_compound=current_compound,
                expected_stint_length=remaining_laps,
                strategy_type="NO_STOP",
                confidence=0.9
            )
        
        # Calculate optimal pit lap
        optimal_lap = current_lap + min(remaining_life, remaining_laps // 2)
        
        # Pit window (±3 laps)
        window_start = max(current_lap + 1, optimal_lap - 3)
        window_end = min(total_laps - 5, optimal_lap + 3)
        
        # Choose compound for next stint
        next_compound = PitStrategySimulator._choose_compound(
            remaining_laps - (optimal_lap - current_lap),
            current_compound
        )
        
        # Calculate undercut advantage
        undercut_gain = PitStrategySimulator._calculate_undercut(
            current_tyre_age, degradation_rate, gap_ahead
        )
        
        # Calculate overcut advantage
        overcut_gain = PitStrategySimulator._calculate_overcut(
            current_tyre_age, degradation_rate, gap_behind
        )
        
        # Determine strategy type
        if undercut_gain > 2.0:
            strategy_type = "UNDERCUT_OPPORTUNITY"
        elif overcut_gain > 2.0:
            strategy_type = "OVERCUT_OPPORTUNITY"
        elif remaining_life < 5:
            strategy_type = "CRITICAL_URGENT_PIT"
        else:
            strategy_type = "STANDARD_STRATEGY"
        
        expected_stint = PitStrategySimulator.STINT_LENGTH.get(next_compound, 25)
        
        return PitStrategyOutput(
            optimal_pit_lap=optimal_lap,
            pit_window_start=window_start,
            pit_window_end=window_end,
            undercut_advantage=undercut_gain,
            overcut_advantage=overcut_gain,
            recommended_compound=next_compound,
            expected_stint_length=expected_stint,
            strategy_type=strategy_type,
            confidence=0.85
        )
    
    @staticmethod
    def _choose_compound(remaining_laps: int, current_compound: str) -> str:
        """Choose optimal compound for next stint"""
        if remaining_laps <= 15:
            return 'SOFT'
        elif remaining_laps <= 25:
            return 'MEDIUM'
        else:
            return 'HARD'
    
    @staticmethod
    def _calculate_undercut(tyre_age: int, degradation_rate: float,
                           gap_ahead: Optional[float]) -> float:
        """
        Calculate undercut advantage.
        
        Undercut works when:
        - You pit earlier than rival
        - Fresh tyres give immediate pace advantage
        - Gain enough time to overtake during their pit stop
        """
        if gap_ahead is None or gap_ahead > 25.0:
            return 0.0
        
        # Fresh tyre advantage (first lap after pit)
        fresh_tyre_gain = 1.5  # ~1.5s faster on fresh tyres
        
        # Rival's degradation while you're on fresh tyres
        rival_degradation = tyre_age * degradation_rate
        
        # Total undercut gain = your fresh tyre pace + rival's degradation - pit loss
        undercut_gain = fresh_tyre_gain + rival_degradation - (gap_ahead - PitStrategySimulator.PIT_LOSS)
        
        return max(0.0, undercut_gain)
    
    @staticmethod
    def _calculate_overcut(tyre_age: int, degradation_rate: float,
                          gap_behind: Optional[float]) -> float:
        """
        Calculate overcut advantage.
        
        Overcut works when:
        - You stay out while rival pits
        - Your degraded tyres still fast enough
        - Gain track position and pit later with clear air
        """
        if gap_behind is None or gap_behind < 3.0:
            return 0.0
        
        # Clear air advantage (no traffic)
        clear_air_gain = 0.3  # ~0.3s per lap in clear air
        
        # Your degradation cost
        degradation_cost = tyre_age * degradation_rate
        
        # Overcut gain = clear air advantage - degradation cost
        overcut_gain = (clear_air_gain * 3) - degradation_cost  # 3 laps advantage
        
        return max(0.0, overcut_gain)
    
    @staticmethod
    def simulate_race_strategy(total_laps: int, 
                              starting_compound: str = 'MEDIUM',
                              num_stops: int = 1) -> List[Dict[str, Any]]:
        """
        Simulate a complete race strategy.
        
        Args:
            total_laps: Total race laps
            starting_compound: Starting tyre compound
            num_stops: Number of pit stops
            
        Returns:
            List of stint plans
        """
        strategy = []
        remaining_laps = total_laps
        current_lap = 0
        compounds_used = [starting_compound]
        
        for stop_num in range(num_stops + 1):
            if stop_num == 0:
                # First stint
                compound = starting_compound
                stint_length = min(
                    PitStrategySimulator.STINT_LENGTH.get(compound, 25),
                    remaining_laps // (num_stops + 1)
                )
            else:
                # Choose next compound
                # Rule: must use 2 different compounds
                available = [c for c in ['SOFT', 'MEDIUM', 'HARD'] if c not in compounds_used]
                if not available:
                    available = ['SOFT', 'MEDIUM', 'HARD']
                
                # Last stint: choose based on remaining laps
                if stop_num == num_stops:
                    compound = PitStrategySimulator._choose_compound(remaining_laps, starting_compound)
                    stint_length = remaining_laps
                else:
                    compound = available[0]
                    stint_length = min(
                        PitStrategySimulator.STINT_LENGTH.get(compound, 25),
                        remaining_laps // (num_stops + 1 - stop_num)
                    )
                
                compounds_used.append(compound)
            
            strategy.append({
                'stint_number': stop_num + 1,
                'start_lap': current_lap + 1,
                'end_lap': current_lap + stint_length,
                'compound': compound,
                'stint_length': stint_length,
                'pit_after': stop_num < num_stops
            })
            
            current_lap += stint_length
            remaining_laps -= stint_length
            
            if remaining_laps <= 0:
                break
        
        return strategy
