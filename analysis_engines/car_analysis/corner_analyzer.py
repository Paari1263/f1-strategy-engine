"""
Corner Analyzer
Analyzes cornering performance and characteristics
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class CornerAnalysisOutput(BaseModel):
    """Output model for corner analysis"""
    total_corners: int = Field(description="Number of corners analyzed")
    avg_apex_speed: float = Field(description="Average apex speed (km/h)")
    avg_entry_speed: float = Field(description="Average corner entry speed (km/h)")
    avg_exit_speed: float = Field(description="Average corner exit speed (km/h)")
    corner_efficiency: float = Field(ge=0, le=10, description="Cornering efficiency (0-10)")
    exit_performance: float = Field(ge=0, le=10, description="Exit acceleration performance (0-10)")
    downforce_level: str = Field(description="Estimated downforce level")


class CornerAnalyzer:
    """
    Analyzes car cornering performance.
    
    LOGIC:
    - Identifies corner entry, apex, and exit speeds
    - Calculates cornering efficiency based on minimum time loss
    - Evaluates traction and downforce levels
    
    ROLE:
    - Identifies aerodynamic efficiency
    - Shows mechanical grip vs aero grip balance
    - Reveals driver's cornering technique
    
    SIGNIFICANCE:
    - High corner speeds = good downforce/mechanical grip
    - Good exit speed = critical for lap time (momentum onto straights)
    - Corner performance predicts race pace vs qualifying pace
    """
    
    @staticmethod
    def analyze_corners(telemetry: pd.DataFrame, corners: List[Dict]) -> CornerAnalysisOutput:
        """
        Analyze cornering performance.
        
        Args:
            telemetry: Telemetry DataFrame
            corners: List of corner data from TelemetryProcessor
            
        Returns:
            CornerAnalysisOutput with cornering metrics
        """
        if not corners:
            return CornerAnalysisOutput(
                total_corners=0,
                avg_apex_speed=0.0,
                avg_entry_speed=0.0,
                avg_exit_speed=0.0,
                corner_efficiency=0.0,
                exit_performance=0.0,
                downforce_level="Unknown"
            )
        
        # Extract corner speeds
        apex_speeds = []
        entry_speeds = []
        exit_speeds = []
        
        for corner in corners:
            corner_data = telemetry[
                (telemetry['Distance'] >= corner['start_distance']) &
                (telemetry['Distance'] <= corner['end_distance'])
            ]
            
            if not corner_data.empty:
                # Entry: first 20% of corner
                entry_section = corner_data.head(max(1, len(corner_data) // 5))
                entry_speeds.append(entry_section['Speed'].mean())
                
                # Apex: minimum speed point
                apex_speeds.append(corner_data['Speed'].min())
                
                # Exit: last 20% of corner
                exit_section = corner_data.tail(max(1, len(corner_data) // 5))
                exit_speeds.append(exit_section['Speed'].mean())
        
        avg_apex_speed = np.mean(apex_speeds) if apex_speeds else 0.0
        avg_entry_speed = np.mean(entry_speeds) if entry_speeds else 0.0
        avg_exit_speed = np.mean(exit_speeds) if exit_speeds else 0.0
        
        # Corner efficiency (maintaining higher speeds)
        # High apex speed relative to entry = good efficiency
        if avg_entry_speed > 0:
            corner_efficiency = min(10.0, (avg_apex_speed / avg_entry_speed) * 12)
        else:
            corner_efficiency = 5.0
        
        # Exit performance (acceleration out of corner)
        # Good exit speed gain
        if avg_apex_speed > 0:
            exit_gain = avg_exit_speed - avg_apex_speed
            exit_performance = min(10.0, (exit_gain / 30) * 10)
        else:
            exit_performance = 5.0
        
        # Estimate downforce level based on average apex speed
        if avg_apex_speed > 200:
            downforce_level = "Very High"
        elif avg_apex_speed > 170:
            downforce_level = "High"
        elif avg_apex_speed > 140:
            downforce_level = "Medium"
        else:
            downforce_level = "Low"
        
        return CornerAnalysisOutput(
            total_corners=len(corners),
            avg_apex_speed=avg_apex_speed,
            avg_entry_speed=avg_entry_speed,
            avg_exit_speed=avg_exit_speed,
            corner_efficiency=corner_efficiency,
            exit_performance=exit_performance,
            downforce_level=downforce_level
        )
    
    @staticmethod
    def compare_cornering(tel1: pd.DataFrame, tel2: pd.DataFrame,
                         corners1: List[Dict], corners2: List[Dict],
                         driver1: str, driver2: str) -> Dict[str, Any]:
        """
        Compare cornering performance between two cars/drivers.
        
        Args:
            tel1: Telemetry of first car
            tel2: Telemetry of second car
            corners1: Corner data of first car
            corners2: Corner data of second car
            driver1: First driver identifier
            driver2: Second driver identifier
            
        Returns:
            Dict with comparison metrics
        """
        analysis1 = CornerAnalyzer.analyze_corners(tel1, corners1)
        analysis2 = CornerAnalyzer.analyze_corners(tel2, corners2)
        
        return {
            'driver1': driver1,
            'driver2': driver2,
            'apex_speed_delta': analysis1.avg_apex_speed - analysis2.avg_apex_speed,
            'entry_speed_delta': analysis1.avg_entry_speed - analysis2.avg_entry_speed,
            'exit_speed_delta': analysis1.avg_exit_speed - analysis2.avg_exit_speed,
            'corner_efficiency_delta': analysis1.corner_efficiency - analysis2.corner_efficiency,
            'exit_performance_delta': analysis1.exit_performance - analysis2.exit_performance,
            'downforce_comparison': f"{analysis1.downforce_level} vs {analysis2.downforce_level}",
            'advantage': driver1 if analysis1.corner_efficiency > analysis2.corner_efficiency else driver2
        }
