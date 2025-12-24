"""
Speed Analyzer
Analyzes speed characteristics across different track sections
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class SpeedAnalysisOutput(BaseModel):
    """Output model for speed analysis"""
    top_speed: float = Field(description="Maximum speed reached (km/h)")
    avg_speed: float = Field(description="Average speed across lap (km/h)")
    min_speed: float = Field(description="Minimum speed in lap (km/h)")
    speed_variance: float = Field(description="Speed variance across lap")
    straight_line_speed: float = Field(description="Average speed in straights (km/h)")
    corner_speed: float = Field(description="Average speed in corners (km/h)")
    speed_efficiency: float = Field(ge=0, le=10, description="Speed efficiency rating (0-10)")
    speed_profile: str = Field(description="Speed profile classification")


class SpeedAnalyzer:
    """
    Analyzes car speed characteristics.
    
    LOGIC:
    - Processes telemetry to identify speed patterns across track sections
    - Distinguishes between straight-line speed and corner speed
    - Calculates speed efficiency based on theoretical maximum
    
    ROLE:
    - Identifies car performance in different track zones
    - Helps understand power unit vs aerodynamic balance
    - Reveals setup characteristics (low drag vs high downforce)
    
    SIGNIFICANCE:
    - Critical for car-to-car comparison
    - Identifies strengths/weaknesses in car setup
    - Informs strategy decisions (qualifying vs race setups)
    """
    
    @staticmethod
    def analyze_speed_profile(telemetry: pd.DataFrame, corners: List[Dict] = None) -> SpeedAnalysisOutput:
        """
        Analyze speed profile from telemetry.
        
        Args:
            telemetry: Telemetry DataFrame with Speed and Distance
            corners: Optional list of corner locations
            
        Returns:
            SpeedAnalysisOutput with speed metrics
        """
        # Basic speed metrics
        top_speed = telemetry['Speed'].max()
        avg_speed = telemetry['Speed'].mean()
        min_speed = telemetry['Speed'].min()
        speed_variance = telemetry['Speed'].var()
        
        # Identify straights (speed > 250 km/h) and corners
        straight_data = telemetry[telemetry['Speed'] > 250]
        corner_data = telemetry[telemetry['Speed'] < 200]
        
        straight_line_speed = straight_data['Speed'].mean() if not straight_data.empty else avg_speed
        corner_speed = corner_data['Speed'].mean() if not corner_data.empty else min_speed
        
        # Calculate speed efficiency (compared to theoretical maximum ~370 km/h)
        theoretical_max = 370.0
        speed_efficiency = min(10.0, (top_speed / theoretical_max) * 10)
        
        # Classify speed profile
        if top_speed > 340:
            speed_profile = "High-speed specialist"
        elif corner_speed > 180:
            speed_profile = "High-downforce setup"
        elif straight_line_speed > 310 and corner_speed < 160:
            speed_profile = "Low-drag setup"
        else:
            speed_profile = "Balanced configuration"
        
        return SpeedAnalysisOutput(
            top_speed=top_speed,
            avg_speed=avg_speed,
            min_speed=min_speed,
            speed_variance=speed_variance,
            straight_line_speed=straight_line_speed,
            corner_speed=corner_speed,
            speed_efficiency=speed_efficiency,
            speed_profile=speed_profile
        )
    
    @staticmethod
    def compare_speed_profiles(tel1: pd.DataFrame, tel2: pd.DataFrame, 
                               driver1: str, driver2: str) -> Dict[str, Any]:
        """
        Compare speed profiles of two cars/drivers.
        
        Args:
            tel1: Telemetry of first car
            tel2: Telemetry of second car
            driver1: First driver identifier
            driver2: Second driver identifier
            
        Returns:
            Dict with comparison metrics
        """
        analysis1 = SpeedAnalyzer.analyze_speed_profile(tel1)
        analysis2 = SpeedAnalyzer.analyze_speed_profile(tel2)
        
        return {
            'driver1': driver1,
            'driver2': driver2,
            'top_speed_delta': analysis1.top_speed - analysis2.top_speed,
            'avg_speed_delta': analysis1.avg_speed - analysis2.avg_speed,
            'straight_speed_delta': analysis1.straight_line_speed - analysis2.straight_line_speed,
            'corner_speed_delta': analysis1.corner_speed - analysis2.corner_speed,
            'efficiency_delta': analysis1.speed_efficiency - analysis2.speed_efficiency,
            'profile1': analysis1.speed_profile,
            'profile2': analysis2.speed_profile,
            'advantage': driver1 if analysis1.avg_speed > analysis2.avg_speed else driver2
        }
