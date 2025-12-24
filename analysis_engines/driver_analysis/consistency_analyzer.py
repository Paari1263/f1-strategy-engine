"""
Consistency Analyzer
Analyzes driver consistency and variation in performance
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class ConsistencyAnalysisOutput(BaseModel):
    """Output model for consistency analysis"""
    lap_time_std_dev: float = Field(description="Lap time standard deviation (seconds)")
    lap_time_variance: float = Field(description="Lap time variance")
    consistency_rating: float = Field(ge=0, le=10, description="Consistency rating (0-10)")
    outlier_laps: int = Field(description="Number of outlier laps (>1.5 std dev)")
    clean_lap_percentage: float = Field(ge=0, le=100, description="Percentage of clean laps")
    degradation_consistency: float = Field(ge=0, le=10, description="Tyre degradation consistency (0-10)")


class ConsistencyAnalyzer:
    """
    Analyzes driver consistency.
    
    LOGIC:
    - Calculates lap time variability
    - Identifies outlier laps (mistakes)
    - Evaluates consistency across stint
    - Analyzes degradation management
    
    ROLE:
    - Shows driver reliability
    - Identifies race pace sustainability
    - Reveals pressure handling
    
    SIGNIFICANCE:
    - Consistent drivers = predictable strategy
    - Low variance = championship material
    - Critical for long races and tyre management
    """
    
    @staticmethod
    def analyze_consistency(laps: pd.DataFrame) -> ConsistencyAnalysisOutput:
        """
        Analyze driver consistency from lap times.
        
        Args:
            laps: DataFrame with lap data
            
        Returns:
            ConsistencyAnalysisOutput with consistency metrics
        """
        # Filter valid laps
        valid_laps = laps[
            (laps['LapTime'].notna()) &
            (~laps.get('Deleted', False)) &
            (laps['PitInTime'].isna())
        ].copy()
        
        if len(valid_laps) < 3:
            return ConsistencyAnalysisOutput(
                lap_time_std_dev=0.0,
                lap_time_variance=0.0,
                consistency_rating=0.0,
                outlier_laps=0,
                clean_lap_percentage=0.0,
                degradation_consistency=0.0
            )
        
        # Convert to seconds
        valid_laps['LapTimeSeconds'] = valid_laps['LapTime'].dt.total_seconds()
        
        # Calculate basic statistics
        lap_time_std_dev = valid_laps['LapTimeSeconds'].std()
        lap_time_variance = valid_laps['LapTimeSeconds'].var()
        mean_lap_time = valid_laps['LapTimeSeconds'].mean()
        
        # Identify outliers (laps > 1.5 std dev from mean)
        outlier_threshold = mean_lap_time + (1.5 * lap_time_std_dev)
        outlier_laps = len(valid_laps[valid_laps['LapTimeSeconds'] > outlier_threshold])
        
        # Consistency rating (lower std dev = higher rating)
        # F1 lap times typically vary by 0.2-0.5s per lap in race trim
        consistency_rating = max(0.0, min(10.0, 10 - (lap_time_std_dev * 20)))
        
        # Clean lap percentage
        total_laps = len(laps[laps['LapTime'].notna()])
        clean_lap_percentage = (len(valid_laps) / total_laps * 100) if total_laps > 0 else 0.0
        
        # Degradation consistency (analyze pace loss over stint)
        degradation_consistency = ConsistencyAnalyzer._analyze_degradation_consistency(valid_laps)
        
        return ConsistencyAnalysisOutput(
            lap_time_std_dev=lap_time_std_dev,
            lap_time_variance=lap_time_variance,
            consistency_rating=consistency_rating,
            outlier_laps=outlier_laps,
            clean_lap_percentage=clean_lap_percentage,
            degradation_consistency=degradation_consistency
        )
    
    @staticmethod
    def _analyze_degradation_consistency(laps: pd.DataFrame) -> float:
        """
        Analyze how consistently driver manages tyre degradation.
        
        Args:
            laps: DataFrame with lap data
            
        Returns:
            Degradation consistency rating (0-10)
        """
        if 'Stint' not in laps.columns or len(laps) < 5:
            return 5.0
        
        # Analyze each stint separately
        stint_consistencies = []
        
        for stint in laps['Stint'].unique():
            stint_laps = laps[laps['Stint'] == stint]
            
            if len(stint_laps) < 5:
                continue
            
            stint_laps = stint_laps.sort_values('LapNumber')
            lap_times = stint_laps['LapTimeSeconds'].values
            
            # Calculate pace loss rate (linear regression slope)
            lap_indices = np.arange(len(lap_times))
            if len(lap_times) > 1:
                # Fit linear trend
                slope = np.polyfit(lap_indices, lap_times, 1)[0]
                
                # Residuals from trend (consistency around degradation curve)
                trend_line = np.poly1d(np.polyfit(lap_indices, lap_times, 1))(lap_indices)
                residuals = lap_times - trend_line
                residual_std = np.std(residuals)
                
                # Lower residual std = more consistent degradation
                stint_consistency = max(0.0, 10 - (residual_std * 20))
                stint_consistencies.append(stint_consistency)
        
        if stint_consistencies:
            return np.mean(stint_consistencies)
        return 5.0
    
    @staticmethod
    def compare_consistency(laps1: pd.DataFrame, laps2: pd.DataFrame,
                           driver1: str, driver2: str) -> Dict[str, Any]:
        """
        Compare consistency between two drivers.
        
        Args:
            laps1: Lap data of first driver
            laps2: Lap data of second driver
            driver1: First driver identifier
            driver2: Second driver identifier
            
        Returns:
            Dict with comparison metrics
        """
        analysis1 = ConsistencyAnalyzer.analyze_consistency(laps1)
        analysis2 = ConsistencyAnalyzer.analyze_consistency(laps2)
        
        return {
            'driver1': driver1,
            'driver2': driver2,
            'std_dev_delta': analysis1.lap_time_std_dev - analysis2.lap_time_std_dev,
            'consistency_rating_delta': analysis1.consistency_rating - analysis2.consistency_rating,
            'outlier_laps_delta': analysis1.outlier_laps - analysis2.outlier_laps,
            'clean_lap_pct_delta': analysis1.clean_lap_percentage - analysis2.clean_lap_percentage,
            'degradation_consistency_delta': analysis1.degradation_consistency - analysis2.degradation_consistency,
            'advantage': driver1 if analysis1.consistency_rating > analysis2.consistency_rating else driver2,
            'advantage_reason': 'More consistent lap times' if analysis1.consistency_rating > analysis2.consistency_rating else 'Fewer outliers'
        }
