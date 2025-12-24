"""
Comparison Engine
Unified interface for car-to-car and driver-to-driver comparisons
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict, List, Optional, Any
import pandas as pd

from data_access import FastF1DataLoader, TelemetryProcessor
from analysis_engines.car_analysis import (
    SpeedAnalyzer, BrakingAnalyzer, CornerAnalyzer, StraightLineAnalyzer
)
from analysis_engines.driver_analysis import (
    PaceAnalyzer, ConsistencyAnalyzer
)


class ComparisonEngine:
    """
    Unified comparison engine for F1 analysis.
    
    Provides high-level interface for:
    - Car vs Car comparison
    - Driver vs Driver comparison
    - Individual driver/car analysis
    """
    
    def __init__(self, cache_dir: Optional[str] = None):
        """
        Initialize comparison engine.
        
        Args:
            cache_dir: Optional cache directory for FastF1 data
        """
        self.loader = FastF1DataLoader(cache_dir=cache_dir)
        self.processor = TelemetryProcessor()
    
    def compare_cars(self, year: int, gp: str, session_type: str,
                    driver1: str, driver2: str) -> Dict[str, Any]:
        """
        Comprehensive car-to-car comparison.
        
        Args:
            year: Season year
            gp: Grand Prix name
            session_type: Session type ('Q' or 'R')
            driver1: First driver abbreviation
            driver2: Second driver abbreviation
            
        Returns:
            Dict with comprehensive comparison results
        """
        # Load session
        session = self.loader.get_session(year, gp, session_type)
        
        # Get fastest laps for both drivers
        lap1 = self.loader.get_fastest_lap(session, driver1)
        lap2 = self.loader.get_fastest_lap(session, driver2)
        
        # Get telemetry
        tel1 = lap1.get_telemetry()
        tel2 = lap2.get_telemetry()
        
        # Identify corners and brake zones
        corners1 = self.processor.identify_corners(tel1)
        corners2 = self.processor.identify_corners(tel2)
        
        brake_zones1 = self.processor.extract_brake_points(tel1)
        brake_zones2 = self.processor.extract_brake_points(tel2)
        
        # Perform all analyses
        speed_comparison = SpeedAnalyzer.compare_speed_profiles(
            tel1, tel2, driver1, driver2
        )
        
        braking_comparison = BrakingAnalyzer.compare_braking(
            tel1, tel2, brake_zones1, brake_zones2, driver1, driver2
        )
        
        corner_comparison = CornerAnalyzer.compare_cornering(
            tel1, tel2, corners1, corners2, driver1, driver2
        )
        
        straight_comparison = StraightLineAnalyzer.compare_straight_line(
            tel1, tel2, driver1, driver2
        )
        
        # Lap time delta
        lap_time_delta = (lap1['LapTime'] - lap2['LapTime']).total_seconds()
        
        return {
            'session_info': {
                'year': year,
                'gp': gp,
                'session': session_type,
                'driver1': driver1,
                'driver2': driver2,
                'lap_time_delta': lap_time_delta
            },
            'speed_analysis': speed_comparison,
            'braking_analysis': braking_comparison,
            'corner_analysis': corner_comparison,
            'straight_line_analysis': straight_comparison,
            'overall_advantage': driver1 if lap_time_delta < 0 else driver2,
            'advantage_areas': {
                'speed': speed_comparison['advantage'],
                'braking': braking_comparison['advantage'],
                'cornering': corner_comparison['advantage'],
                'straight_line': straight_comparison['advantage']
            }
        }
    
    def compare_drivers(self, year: int, gp: str, session_type: str,
                       driver1: str, driver2: str) -> Dict[str, Any]:
        """
        Comprehensive driver-to-driver comparison.
        
        Args:
            year: Season year
            gp: Grand Prix name
            session_type: Session type
            driver1: First driver abbreviation
            driver2: Second driver abbreviation
            
        Returns:
            Dict with comprehensive driver comparison
        """
        # Load session
        session = self.loader.get_session(year, gp, session_type)
        
        # Get lap data
        laps1 = self.loader.get_lap_data(session, driver1)
        laps2 = self.loader.get_lap_data(session, driver2)
        
        # Perform analyses
        pace_comparison = PaceAnalyzer.compare_pace(
            laps1, laps2, driver1, driver2
        )
        
        consistency_comparison = ConsistencyAnalyzer.compare_consistency(
            laps1, laps2, driver1, driver2
        )
        
        # Get fastest laps for car comparison
        lap1 = laps1.pick_fastest()
        lap2 = laps2.pick_fastest()
        
        return {
            'session_info': {
                'year': year,
                'gp': gp,
                'session': session_type,
                'driver1': driver1,
                'driver2': driver2
            },
            'pace_analysis': pace_comparison,
            'consistency_analysis': consistency_comparison,
            'overall_advantage': pace_comparison['advantage'],
            'advantage_areas': {
                'pace': pace_comparison['advantage'],
                'consistency': consistency_comparison['advantage']
            },
            'lap_data': {
                'driver1_laps': len(laps1),
                'driver2_laps': len(laps2),
                'driver1_fastest': lap1['LapTime'].total_seconds(),
                'driver2_fastest': lap2['LapTime'].total_seconds()
            }
        }
    
    def analyze_individual_driver(self, year: int, gp: str, session_type: str,
                                  driver: str) -> Dict[str, Any]:
        """
        Comprehensive individual driver analysis.
        
        Args:
            year: Season year
            gp: Grand Prix name
            session_type: Session type
            driver: Driver abbreviation
            
        Returns:
            Dict with comprehensive driver analysis
        """
        # Load session
        session = self.loader.get_session(year, gp, session_type)
        
        # Get data
        laps = self.loader.get_lap_data(session, driver)
        fastest_lap = laps.pick_fastest()
        telemetry = fastest_lap.get_telemetry()
        
        # Identify features
        corners = self.processor.identify_corners(telemetry)
        brake_zones = self.processor.extract_brake_points(telemetry)
        
        # Perform analyses
        pace_analysis = PaceAnalyzer.analyze_pace(laps)
        consistency_analysis = ConsistencyAnalyzer.analyze_consistency(laps)
        speed_analysis = SpeedAnalyzer.analyze_speed_profile(telemetry, corners)
        braking_analysis = BrakingAnalyzer.analyze_braking(telemetry, brake_zones)
        corner_analysis = CornerAnalyzer.analyze_corners(telemetry, corners)
        straight_analysis = StraightLineAnalyzer.analyze_straights(telemetry)
        
        # Get driver info
        driver_info = self.loader.get_driver_info(session, driver)
        
        return {
            'session_info': {
                'year': year,
                'gp': gp,
                'session': session_type,
                'driver': driver,
                'team': driver_info.get('team'),
                'teammate': driver_info.get('teammate')
            },
            'pace_metrics': pace_analysis.model_dump(),
            'consistency_metrics': consistency_analysis.model_dump(),
            'car_performance': {
                'speed': speed_analysis.model_dump(),
                'braking': braking_analysis.model_dump(),
                'cornering': corner_analysis.model_dump(),
                'straight_line': straight_analysis.model_dump()
            },
            'lap_stats': {
                'total_laps': len(laps),
                'fastest_lap': fastest_lap['LapTime'].total_seconds(),
                'corners_identified': len(corners),
                'brake_zones': len(brake_zones)
            }
        }
    
    def get_season_comparison(self, year: int, driver1: str, driver2: str,
                             races: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Season-wide comparison between two drivers.
        
        Args:
            year: Season year
            driver1: First driver abbreviation
            driver2: Second driver abbreviation
            races: Optional list of specific races to analyze
            
        Returns:
            Dict with season-wide comparison
        """
        schedule = self.loader.get_event_schedule(year)
        
        if races is None:
            # Use all races
            races = schedule['EventName'].tolist()
        
        race_results = []
        
        for race in races[:5]:  # Limit to first 5 races for demo
            try:
                comparison = self.compare_drivers(year, race, 'R', driver1, driver2)
                race_results.append({
                    'race': race,
                    'advantage': comparison['overall_advantage'],
                    'pace_delta': comparison['pace_analysis']['fastest_lap_delta']
                })
            except Exception as e:
                print(f"Warning: Could not analyze {race}: {e}")
                continue
        
        # Calculate season statistics
        driver1_wins = sum(1 for r in race_results if r['advantage'] == driver1)
        driver2_wins = sum(1 for r in race_results if r['advantage'] == driver2)
        
        avg_pace_delta = sum(r['pace_delta'] for r in race_results) / len(race_results) if race_results else 0
        
        return {
            'season': year,
            'driver1': driver1,
            'driver2': driver2,
            'races_analyzed': len(race_results),
            'driver1_advantages': driver1_wins,
            'driver2_advantages': driver2_wins,
            'avg_pace_delta': avg_pace_delta,
            'race_by_race': race_results,
            'season_winner': driver1 if driver1_wins > driver2_wins else driver2
        }
