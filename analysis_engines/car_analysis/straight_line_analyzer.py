"""
Straight Line Analyzer
Analyzes straight-line performance (power unit and drag)
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class StraightLineAnalysisOutput(BaseModel):
    """Output model for straight-line analysis"""
    max_straight_speed: float = Field(description="Maximum speed in straights (km/h)")
    avg_straight_speed: float = Field(description="Average speed in straights (km/h)")
    acceleration_rating: float = Field(ge=0, le=10, description="Acceleration performance (0-10)")
    power_rating: float = Field(ge=0, le=10, description="Power unit rating (0-10)")
    drag_level: str = Field(description="Aerodynamic drag classification")
    drs_advantage: Optional[float] = Field(default=None, description="DRS speed gain (km/h)")


class StraightLineAnalyzer:
    """
    Analyzes straight-line performance.
    
    LOGIC:
    - Identifies straight sections (continuous high speed)
    - Calculates acceleration rates
    - Estimates power unit performance and drag levels
    - Analyzes DRS effectiveness
    
    ROLE:
    - Identifies power unit competitiveness
    - Shows drag vs downforce trade-off
    - Reveals top speed capability
    
    SIGNIFICANCE:
    - Critical for overtaking opportunities
    - Shows setup philosophy (quali vs race)
    - Power unit performance indicator
    """
    
    @staticmethod
    def analyze_straights(telemetry: pd.DataFrame, speed_threshold: float = 280.0) -> StraightLineAnalysisOutput:
        """
        Analyze straight-line performance.
        
        Args:
            telemetry: Telemetry DataFrame
            speed_threshold: Minimum speed to be considered a straight (km/h)
            
        Returns:
            StraightLineAnalysisOutput with straight-line metrics
        """
        # Identify straight sections
        straight_data = telemetry[telemetry['Speed'] >= speed_threshold]
        
        if straight_data.empty:
            return StraightLineAnalysisOutput(
                max_straight_speed=telemetry['Speed'].max(),
                avg_straight_speed=telemetry['Speed'].mean(),
                acceleration_rating=5.0,
                power_rating=5.0,
                drag_level="Unknown",
                drs_advantage=None
            )
        
        max_straight_speed = straight_data['Speed'].max()
        avg_straight_speed = straight_data['Speed'].mean()
        
        # Calculate acceleration rating (speed gained per distance in straights)
        acceleration_zones = []
        in_acceleration = False
        accel_start_speed = None
        accel_start_dist = None
        
        for idx, row in straight_data.iterrows():
            # Simplified acceleration detection
            if row['Throttle'] == 100 and not in_acceleration:
                in_acceleration = True
                accel_start_speed = row['Speed']
                accel_start_dist = row['Distance']
            elif row['Throttle'] < 100 and in_acceleration:
                in_acceleration = False
                if accel_start_speed and accel_start_dist:
                    speed_gain = row['Speed'] - accel_start_speed
                    distance = row['Distance'] - accel_start_dist
                    if distance > 0:
                        acceleration_zones.append(speed_gain / distance)
        
        if acceleration_zones:
            avg_acceleration = np.mean(acceleration_zones)
            acceleration_rating = min(10.0, avg_acceleration * 20)
        else:
            acceleration_rating = 5.0
        
        # Power rating (based on top speed and acceleration)
        # F1 top speeds typically 330-360 km/h
        power_rating = min(10.0, (max_straight_speed / 350.0) * 10)
        
        # Drag level estimation
        if max_straight_speed > 340:
            drag_level = "Very Low (Low downforce setup)"
        elif max_straight_speed > 325:
            drag_level = "Low"
        elif max_straight_speed > 310:
            drag_level = "Medium"
        else:
            drag_level = "High (High downforce setup)"
        
        # DRS advantage (if DRS column available)
        drs_advantage = None
        if 'DRS' in telemetry.columns:
            drs_active = telemetry[telemetry['DRS'] > 0]
            drs_inactive = telemetry[telemetry['DRS'] == 0]
            
            if not drs_active.empty and not drs_inactive.empty:
                drs_speed = drs_active['Speed'].max()
                non_drs_speed = drs_inactive[drs_inactive['Speed'] > speed_threshold]['Speed'].max()
                if not np.isnan(non_drs_speed):
                    drs_advantage = drs_speed - non_drs_speed
        
        return StraightLineAnalysisOutput(
            max_straight_speed=max_straight_speed,
            avg_straight_speed=avg_straight_speed,
            acceleration_rating=acceleration_rating,
            power_rating=power_rating,
            drag_level=drag_level,
            drs_advantage=drs_advantage
        )
    
    @staticmethod
    def compare_straight_line(tel1: pd.DataFrame, tel2: pd.DataFrame,
                             driver1: str, driver2: str) -> Dict[str, Any]:
        """
        Compare straight-line performance between two cars/drivers.
        
        Args:
            tel1: Telemetry of first car
            tel2: Telemetry of second car
            driver1: First driver identifier
            driver2: Second driver identifier
            
        Returns:
            Dict with comparison metrics
        """
        analysis1 = StraightLineAnalyzer.analyze_straights(tel1)
        analysis2 = StraightLineAnalyzer.analyze_straights(tel2)
        
        return {
            'driver1': driver1,
            'driver2': driver2,
            'top_speed_delta': analysis1.max_straight_speed - analysis2.max_straight_speed,
            'avg_speed_delta': analysis1.avg_straight_speed - analysis2.avg_straight_speed,
            'acceleration_delta': analysis1.acceleration_rating - analysis2.acceleration_rating,
            'power_delta': analysis1.power_rating - analysis2.power_rating,
            'drag_comparison': f"{analysis1.drag_level} vs {analysis2.drag_level}",
            'drs_delta': (analysis1.drs_advantage - analysis2.drs_advantage) if (analysis1.drs_advantage and analysis2.drs_advantage) else None,
            'advantage': driver1 if analysis1.max_straight_speed > analysis2.max_straight_speed else driver2
        }
