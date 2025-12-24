"""
Pace Analyzer
Analyzes driver pace and lap time performance
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class PaceAnalysisOutput(BaseModel):
    """Output model for pace analysis"""
    fastest_lap: float = Field(description="Fastest lap time (seconds)")
    median_lap: float = Field(description="Median lap time (seconds)")
    avg_lap: float = Field(description="Average lap time (seconds)")
    pace_rating: float = Field(ge=0, le=10, description="Overall pace rating (0-10)")
    ultimate_pace: float = Field(description="Ultimate theoretical pace (best sectors combined)")
    pace_vs_teammate: Optional[float] = Field(default=None, description="Gap to teammate (seconds)")
    fuel_corrected_pace: Optional[float] = Field(default=None, description="Fuel-corrected average pace")


class PaceAnalyzer:
    """
    Analyzes driver pace performance.
    
    LOGIC:
    - Filters clean laps (no traffic, no mistakes)
    - Calculates representative pace metrics
    - Compares against teammate and field
    - Accounts for fuel load effects
    
    ROLE:
    - Identifies true pace potential
    - Shows race pace vs qualifying pace
    - Reveals consistency in performance
    
    SIGNIFICANCE:
    - Core metric for driver evaluation
    - Predicts race outcome potential
    - Critical for strategy decisions
    """
    
    @staticmethod
    def analyze_pace(laps: pd.DataFrame, fuel_correction: bool = False) -> PaceAnalysisOutput:
        """
        Analyze driver pace from lap times.
        
        Args:
            laps: DataFrame with lap data
            fuel_correction: Whether to apply fuel load correction
            
        Returns:
            PaceAnalysisOutput with pace metrics
        """
        # Filter for valid laps (not deleted, not pit laps)
        valid_laps = laps[
            (laps['LapTime'].notna()) &
            (~laps.get('Deleted', False)) &
            (laps['PitInTime'].isna())
        ].copy()
        
        if valid_laps.empty:
            return PaceAnalysisOutput(
                fastest_lap=0.0,
                median_lap=0.0,
                avg_lap=0.0,
                pace_rating=0.0,
                ultimate_pace=0.0
            )
        
        # Convert lap times to seconds
        valid_laps['LapTimeSeconds'] = valid_laps['LapTime'].dt.total_seconds()
        
        fastest_lap = valid_laps['LapTimeSeconds'].min()
        median_lap = valid_laps['LapTimeSeconds'].median()
        avg_lap = valid_laps['LapTimeSeconds'].mean()
        
        # Calculate ultimate pace (best sectors)
        if all(col in valid_laps.columns for col in ['Sector1Time', 'Sector2Time', 'Sector3Time']):
            best_s1 = valid_laps['Sector1Time'].min().total_seconds()
            best_s2 = valid_laps['Sector2Time'].min().total_seconds()
            best_s3 = valid_laps['Sector3Time'].min().total_seconds()
            ultimate_pace = best_s1 + best_s2 + best_s3
        else:
            ultimate_pace = fastest_lap
        
        # Pace rating (how close to ultimate pace)
        if ultimate_pace > 0:
            pace_rating = max(0.0, min(10.0, (1 - (fastest_lap - ultimate_pace) / ultimate_pace) * 10))
        else:
            pace_rating = 5.0
        
        # Fuel correction (approximate 0.03s per lap for fuel burn)
        fuel_corrected_pace = None
        if fuel_correction and len(valid_laps) > 10:
            # Estimate fuel effect
            lap_numbers = valid_laps['LapNumber'].values
            lap_times = valid_laps['LapTimeSeconds'].values
            
            # Simple linear regression to account for fuel burn
            if len(lap_numbers) > 1:
                fuel_effect_per_lap = 0.03  # ~0.03s per lap
                corrected_times = lap_times - (lap_numbers * fuel_effect_per_lap)
                fuel_corrected_pace = np.mean(corrected_times)
        
        return PaceAnalysisOutput(
            fastest_lap=fastest_lap,
            median_lap=median_lap,
            avg_lap=avg_lap,
            pace_rating=pace_rating,
            ultimate_pace=ultimate_pace,
            fuel_corrected_pace=fuel_corrected_pace
        )
    
    @staticmethod
    def compare_pace(laps1: pd.DataFrame, laps2: pd.DataFrame,
                    driver1: str, driver2: str) -> Dict[str, Any]:
        """
        Compare pace between two drivers.
        
        Args:
            laps1: Lap data of first driver
            laps2: Lap data of second driver
            driver1: First driver identifier
            driver2: Second driver identifier
            
        Returns:
            Dict with comparison metrics
        """
        analysis1 = PaceAnalyzer.analyze_pace(laps1)
        analysis2 = PaceAnalyzer.analyze_pace(laps2)
        
        fastest_delta = analysis1.fastest_lap - analysis2.fastest_lap
        median_delta = analysis1.median_lap - analysis2.median_lap
        avg_delta = analysis1.avg_lap - analysis2.avg_lap
        
        return {
            'driver1': driver1,
            'driver2': driver2,
            'fastest_lap_delta': fastest_delta,
            'median_lap_delta': median_delta,
            'avg_lap_delta': avg_delta,
            'ultimate_pace_delta': analysis1.ultimate_pace - analysis2.ultimate_pace,
            'pace_rating_delta': analysis1.pace_rating - analysis2.pace_rating,
            'advantage': driver1 if fastest_delta < 0 else driver2,
            'gap_percentage': abs(fastest_delta / analysis2.fastest_lap * 100) if analysis2.fastest_lap > 0 else 0
        }
