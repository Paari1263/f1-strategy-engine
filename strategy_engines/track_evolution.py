"""
Track Evolution Tracker
Tracks grip and performance changes across practice, qualifying, and race sessions
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class TrackEvolutionOutput(BaseModel):
    """Output model for track evolution analysis"""
    grip_improvement: float = Field(description="Grip improvement from baseline (%)")
    lap_time_improvement: float = Field(description="Lap time improvement (seconds)")
    evolution_rate: float = Field(description="Rate of track evolution (s/session)")
    track_condition: str = Field(description="Current track condition")
    optimal_session: str = Field(description="Session with best conditions")
    confidence: float = Field(ge=0, le=1, description="Confidence in prediction")


class TrackEvolutionTracker:
    """
    Tracks track evolution across multiple sessions.
    
    LOGIC:
    - Compares lap times across FP1, FP2, FP3, Q, R
    - Accounts for fuel load, tyre compound differences
    - Models grip progression as track rubbers in
    - Predicts optimal session for performance
    
    ROLE:
    - Helps teams understand track improvement
    - Predicts qualifying and race pace potential
    - Informs setup decisions based on session progression
    
    SIGNIFICANCE:
    - Track evolves 1-3 seconds from FP1 to Qualifying
    - Critical for setup optimization
    - Predicts race day conditions
    """
    
    @staticmethod
    def analyze_evolution(sessions_data: Dict[str, pd.DataFrame],
                         reference_driver: str = None) -> TrackEvolutionOutput:
        """
        Analyze track evolution across sessions.
        
        Args:
            sessions_data: Dict mapping session names to lap DataFrames
                          e.g., {'FP1': fp1_laps, 'FP2': fp2_laps, 'Q': q_laps}
            reference_driver: Optional driver to use as reference
            
        Returns:
            TrackEvolutionOutput with evolution analysis
        """
        # Extract best lap times from each session
        session_times = {}
        
        for session_name, laps in sessions_data.items():
            if laps.empty:
                continue
            
            # Filter for reference driver if specified
            if reference_driver:
                laps = laps[laps['Driver'] == reference_driver]
            
            # Get fastest valid lap
            valid_laps = laps[
                (laps['LapTime'].notna()) &
                (~laps.get('Deleted', False))
            ]
            
            if not valid_laps.empty:
                fastest = valid_laps['LapTime'].min().total_seconds()
                session_times[session_name] = fastest
        
        if len(session_times) < 2:
            return TrackEvolutionOutput(
                grip_improvement=0.0,
                lap_time_improvement=0.0,
                evolution_rate=0.0,
                track_condition="Unknown",
                optimal_session="Unknown",
                confidence=0.0
            )
        
        # Define session order
        session_order = ['FP1', 'FP2', 'FP3', 'Q', 'S', 'R']
        ordered_times = []
        ordered_sessions = []
        
        for session in session_order:
            if session in session_times:
                ordered_sessions.append(session)
                ordered_times.append(session_times[session])
        
        # Calculate improvement
        baseline = ordered_times[0]
        best_time = min(ordered_times)
        lap_time_improvement = baseline - best_time
        
        # Grip improvement (estimate: 1s = ~2% grip gain)
        grip_improvement = (lap_time_improvement / baseline) * 100
        
        # Evolution rate (improvement per session)
        if len(ordered_times) > 1:
            total_improvement = ordered_times[0] - ordered_times[-1]
            evolution_rate = total_improvement / (len(ordered_times) - 1)
        else:
            evolution_rate = 0.0
        
        # Determine track condition
        if lap_time_improvement > 2.0:
            condition = "Highly evolved - significant rubber buildup"
        elif lap_time_improvement > 1.0:
            condition = "Well evolved - normal progression"
        elif lap_time_improvement > 0.3:
            condition = "Moderately evolved"
        else:
            condition = "Green track - limited evolution"
        
        # Optimal session
        optimal_idx = ordered_times.index(min(ordered_times))
        optimal_session = ordered_sessions[optimal_idx]
        
        # Confidence based on data availability
        confidence = min(1.0, len(session_times) / 5.0)
        
        return TrackEvolutionOutput(
            grip_improvement=grip_improvement,
            lap_time_improvement=lap_time_improvement,
            evolution_rate=evolution_rate,
            track_condition=condition,
            optimal_session=optimal_session,
            confidence=confidence
        )
    
    @staticmethod
    def predict_race_pace(qualifying_laps: pd.DataFrame,
                         practice_laps: pd.DataFrame,
                         fuel_load_laps: int = 50) -> Dict[str, float]:
        """
        Predict race pace from qualifying and practice data.
        
        Args:
            qualifying_laps: Qualifying lap data
            practice_laps: Practice lap data (FP2/FP3 long runs)
            fuel_load_laps: Estimated race fuel load
            
        Returns:
            Dict with race pace predictions
        """
        # Get qualifying pace (low fuel)
        q_pace = qualifying_laps['LapTime'].min().total_seconds()
        
        # Get practice long run pace (high fuel)
        # Filter for long runs (consecutive laps > 5)
        practice_laps = practice_laps.sort_values('LapNumber')
        long_run_laps = []
        
        for stint in practice_laps['Stint'].unique():
            stint_laps = practice_laps[practice_laps['Stint'] == stint]
            if len(stint_laps) >= 5:
                # Take middle laps (avoid in/out laps)
                long_run_laps.append(stint_laps.iloc[2:-1])
        
        if long_run_laps:
            long_run_data = pd.concat(long_run_laps)
            practice_pace = long_run_data['LapTime'].mean().total_seconds()
        else:
            # Estimate: race pace ~3-4% slower than qualifying
            practice_pace = q_pace * 1.035
        
        # Fuel effect: ~0.03s per lap of fuel
        fuel_effect = fuel_load_laps * 0.03
        
        # Predicted race start pace (full fuel)
        race_start_pace = q_pace + fuel_effect
        
        # Predicted race average pace
        race_avg_pace = (race_start_pace + q_pace) / 2
        
        return {
            'qualifying_pace': q_pace,
            'practice_long_run_pace': practice_pace,
            'predicted_race_start': race_start_pace,
            'predicted_race_average': race_avg_pace,
            'fuel_effect': fuel_effect
        }
    
    @staticmethod
    def compare_session_conditions(session1_laps: pd.DataFrame,
                                   session2_laps: pd.DataFrame,
                                   session1_name: str,
                                   session2_name: str) -> Dict[str, Any]:
        """
        Compare conditions between two sessions.
        
        Args:
            session1_laps: Laps from first session
            session2_laps: Laps from second session
            session1_name: Name of first session
            session2_name: Name of second session
            
        Returns:
            Dict with comparison metrics
        """
        # Get best laps
        s1_best = session1_laps['LapTime'].min().total_seconds()
        s2_best = session2_laps['LapTime'].min().total_seconds()
        
        improvement = s1_best - s2_best
        improvement_pct = (improvement / s1_best) * 100
        
        # Session with better conditions
        better_session = session2_name if s2_best < s1_best else session1_name
        
        return {
            'session1': session1_name,
            'session2': session2_name,
            'session1_best': s1_best,
            'session2_best': s2_best,
            'improvement': improvement,
            'improvement_percent': improvement_pct,
            'better_session': better_session,
            'track_evolved': improvement > 0
        }
