"""
Braking Analyzer
Analyzes braking performance and characteristics
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class BrakingAnalysisOutput(BaseModel):
    """Output model for braking analysis"""
    total_brake_zones: int = Field(description="Number of braking zones")
    avg_brake_distance: float = Field(description="Average braking distance (m)")
    max_deceleration: float = Field(description="Maximum deceleration rate (m/s²)")
    avg_deceleration: float = Field(description="Average deceleration rate (m/s²)")
    late_braking_score: float = Field(ge=0, le=10, description="Late braking capability (0-10)")
    brake_stability: float = Field(ge=0, le=10, description="Braking stability rating (0-10)")
    braking_efficiency: float = Field(ge=0, le=10, description="Braking efficiency (0-10)")


class BrakingAnalyzer:
    """
    Analyzes car braking performance.
    
    LOGIC:
    - Identifies all braking zones in a lap
    - Calculates deceleration rates and braking distances
    - Evaluates braking consistency and stability
    
    ROLE:
    - Identifies braking system performance
    - Reveals driver confidence in brakes
    - Shows car's ability to late-brake (critical for overtaking)
    
    SIGNIFICANCE:
    - Late braking = overtaking opportunity
    - Braking stability = driver confidence
    - Critical for qualifying lap times
    """
    
    @staticmethod
    def analyze_braking(telemetry: pd.DataFrame, brake_zones: List[Dict]) -> BrakingAnalysisOutput:
        """
        Analyze braking performance.
        
        Args:
            telemetry: Telemetry DataFrame
            brake_zones: List of brake zones from TelemetryProcessor
            
        Returns:
            BrakingAnalysisOutput with braking metrics
        """
        if not brake_zones:
            # No brake zones identified
            return BrakingAnalysisOutput(
                total_brake_zones=0,
                avg_brake_distance=0.0,
                max_deceleration=0.0,
                avg_deceleration=0.0,
                late_braking_score=0.0,
                brake_stability=0.0,
                braking_efficiency=0.0
            )
        
        # Calculate metrics from brake zones
        brake_distances = [zone['brake_distance'] for zone in brake_zones]
        avg_brake_distance = np.mean(brake_distances)
        
        # Estimate deceleration rates
        decel_rates = []
        for zone in brake_zones:
            speed_before = zone['speed_before'] / 3.6  # Convert to m/s
            speed_after = zone['speed_after'] / 3.6
            distance = zone['brake_distance']
            
            if distance > 0:
                # Using v² = u² + 2as → a = (v² - u²) / (2s)
                decel = abs((speed_after**2 - speed_before**2) / (2 * distance))
                decel_rates.append(decel)
        
        max_deceleration = max(decel_rates) if decel_rates else 0.0
        avg_deceleration = np.mean(decel_rates) if decel_rates else 0.0
        
        # Late braking score (shorter brake distance = higher score)
        # Typical F1 braking distance: 60-100m for heavy braking
        late_braking_score = max(0.0, min(10.0, 10 - (avg_brake_distance - 50) / 10))
        
        # Brake stability (consistency in deceleration)
        if len(decel_rates) > 1:
            decel_std = np.std(decel_rates)
            brake_stability = max(0.0, 10 - decel_std * 2)
        else:
            brake_stability = 5.0
        
        # Braking efficiency (high deceleration with short distance)
        # F1 cars can achieve ~5-6 g's deceleration
        braking_efficiency = min(10.0, (max_deceleration / 50.0) * 10)
        
        return BrakingAnalysisOutput(
            total_brake_zones=len(brake_zones),
            avg_brake_distance=avg_brake_distance,
            max_deceleration=max_deceleration,
            avg_deceleration=avg_deceleration,
            late_braking_score=late_braking_score,
            brake_stability=brake_stability,
            braking_efficiency=braking_efficiency
        )
    
    @staticmethod
    def compare_braking(tel1: pd.DataFrame, tel2: pd.DataFrame, 
                        zones1: List[Dict], zones2: List[Dict],
                        driver1: str, driver2: str) -> Dict[str, Any]:
        """
        Compare braking performance between two cars/drivers.
        
        Args:
            tel1: Telemetry of first car
            tel2: Telemetry of second car
            zones1: Brake zones of first car
            zones2: Brake zones of second car
            driver1: First driver identifier
            driver2: Second driver identifier
            
        Returns:
            Dict with comparison metrics
        """
        analysis1 = BrakingAnalyzer.analyze_braking(tel1, zones1)
        analysis2 = BrakingAnalyzer.analyze_braking(tel2, zones2)
        
        return {
            'driver1': driver1,
            'driver2': driver2,
            'brake_distance_delta': analysis1.avg_brake_distance - analysis2.avg_brake_distance,
            'max_decel_delta': analysis1.max_deceleration - analysis2.max_deceleration,
            'late_braking_delta': analysis1.late_braking_score - analysis2.late_braking_score,
            'stability_delta': analysis1.brake_stability - analysis2.brake_stability,
            'advantage': driver1 if analysis1.late_braking_score > analysis2.late_braking_score else driver2,
            'advantage_reason': 'Later braking point' if analysis1.late_braking_score > analysis2.late_braking_score else 'More stable braking'
        }
