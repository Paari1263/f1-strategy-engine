"""
FastF1 Data Loader
Provides unified interface for loading F1 session data from FastF1
"""

import fastf1
import pandas as pd
from typing import Optional, List, Dict, Any
from pathlib import Path


class FastF1DataLoader:
    """
    Unified interface for loading F1 data using FastF1.
    
    Handles session loading, lap data extraction, telemetry access,
    and driver/team information retrieval.
    """
    
    def __init__(self, cache_dir: Optional[str] = None):
        """
        Initialize FastF1 data loader.
        
        Args:
            cache_dir: Directory for FastF1 cache. If None, uses default ~/.fastf1
        """
        if cache_dir:
            cache_path = Path(cache_dir)
            cache_path.mkdir(parents=True, exist_ok=True)
            fastf1.Cache.enable_cache(str(cache_path))
        else:
            # Use default cache location
            fastf1.Cache.enable_cache(str(Path.home() / '.fastf1'))
    
    def get_session(self, year: int, gp: str, session_type: str):
        """
        Load a specific F1 session.
        
        Args:
            year: Season year (e.g., 2024)
            gp: Grand Prix name (e.g., 'Monaco', 'Silverstone') or round number
            session_type: 'FP1', 'FP2', 'FP3', 'Q', 'S', 'R'
            
        Returns:
            FastF1 Session object with loaded data
            
        Example:
            session = loader.get_session(2024, 'Monaco', 'R')
        """
        try:
            session = fastf1.get_session(year, gp, session_type)
            session.load()
            return session
        except Exception as e:
            raise RuntimeError(f"Failed to load session {year} {gp} {session_type}: {e}")
    
    def get_lap_data(self, session, driver: Optional[str] = None) -> pd.DataFrame:
        """
        Extract lap data from session.
        
        Args:
            session: FastF1 Session object
            driver: Driver abbreviation (e.g., 'VER', 'HAM'). If None, returns all drivers.
            
        Returns:
            DataFrame with lap data
            
        Available columns:
            - Time, Driver, DriverNumber, LapTime, LapNumber
            - Stint, PitOutTime, PitInTime, Sector1Time, Sector2Time, Sector3Time
            - SpeedI1, SpeedI2, SpeedFL, SpeedST
            - Compound, TyreLife, FreshTyre, Team, TrackStatus
            - Position, Deleted, DeletedReason, FastF1Generated, IsAccurate
        """
        if driver:
            return session.laps[session.laps['Driver'] == driver].copy()
        return session.laps.copy()
    
    def get_telemetry(self, lap):
        """
        Get telemetry data for a specific lap.
        
        Args:
            lap: Single lap object from session.laps
            
        Returns:
            DataFrame with telemetry (~200Hz sampling)
            
        Available columns:
            - Time, SessionTime, DriverAhead, DistanceToDriverAhead
            - Date, Speed, nGear, Throttle, Brake, DRS
            - RPM, Distance, RelativeDistance, Status, X, Y, Z
        """
        try:
            return lap.get_telemetry()
        except Exception as e:
            raise RuntimeError(f"Failed to get telemetry: {e}")
    
    def get_car_telemetry(self, session, driver: str):
        """
        Get car data (telemetry) for all laps of a driver.
        
        Args:
            session: FastF1 Session object
            driver: Driver abbreviation (e.g., 'VER')
            
        Returns:
            DataFrame with car telemetry data
        """
        try:
            return session.car_data.get(driver)
        except Exception as e:
            raise RuntimeError(f"Failed to get car data for {driver}: {e}")
    
    def get_weather_data(self, session) -> pd.DataFrame:
        """
        Get weather data for the session.
        
        Args:
            session: FastF1 Session object
            
        Returns:
            DataFrame with weather information
            
        Available columns:
            - Time, AirTemp, Humidity, Pressure, Rainfall
            - TrackTemp, WindDirection, WindSpeed
        """
        return session.weather_data.copy()
    
    def get_all_drivers(self, session) -> List[str]:
        """
        Get list of all drivers in the session.
        
        Args:
            session: FastF1 Session object
            
        Returns:
            List of driver abbreviations (e.g., ['VER', 'HAM', 'LEC', ...])
        """
        return session.laps['Driver'].unique().tolist()
    
    def get_teammate(self, session, driver: str) -> Optional[str]:
        """
        Get teammate of specified driver.
        
        Args:
            session: FastF1 Session object
            driver: Driver abbreviation
            
        Returns:
            Teammate abbreviation or None if not found
        """
        driver_laps = session.laps[session.laps['Driver'] == driver]
        if driver_laps.empty:
            return None
        
        team = driver_laps.iloc[0]['Team']
        teammates = session.laps[
            (session.laps['Team'] == team) & 
            (session.laps['Driver'] != driver)
        ]['Driver'].unique()
        
        return teammates[0] if len(teammates) > 0 else None
    
    def get_driver_info(self, session, driver: str) -> Dict[str, Any]:
        """
        Get comprehensive driver information.
        
        Args:
            session: FastF1 Session object
            driver: Driver abbreviation
            
        Returns:
            Dict with driver details (team, number, etc.)
        """
        driver_laps = session.laps[session.laps['Driver'] == driver]
        if driver_laps.empty:
            return {}
        
        first_lap = driver_laps.iloc[0]
        return {
            'driver': driver,
            'team': first_lap['Team'],
            'driver_number': first_lap['DriverNumber'],
            'teammate': self.get_teammate(session, driver)
        }
    
    def get_fastest_lap(self, session, driver: Optional[str] = None):
        """
        Get fastest lap from session.
        
        Args:
            session: FastF1 Session object
            driver: Driver abbreviation. If None, returns overall fastest.
            
        Returns:
            Fastest lap object
        """
        if driver:
            driver_laps = session.laps[session.laps['Driver'] == driver]
            return driver_laps.pick_fastest()
        return session.laps.pick_fastest()
    
    def get_event_schedule(self, year: int) -> pd.DataFrame:
        """
        Get the event schedule for a specific year.
        
        Args:
            year: Season year
            
        Returns:
            DataFrame with event schedule
        """
        return fastf1.get_event_schedule(year)
    
    def get_session_status(self, session) -> pd.DataFrame:
        """
        Get track status data (flags, safety car, etc.).
        
        Args:
            session: FastF1 Session object
            
        Returns:
            DataFrame with status information
            
        Status codes:
            '1' = Track clear (Green flag)
            '2' = Yellow flag
            '4' = Safety Car
            '5' = Red flag
            '6' = Virtual Safety Car
        """
        return session.track_status.copy()
    
    def get_position_changes(self, session, driver: str) -> List[int]:
        """
        Get position progression throughout the race.
        
        Args:
            session: FastF1 Session object
            driver: Driver abbreviation
            
        Returns:
            List of positions per lap
        """
        driver_laps = session.laps[session.laps['Driver'] == driver]
        return driver_laps['Position'].tolist()
    
    def get_pit_stops(self, session, driver: str) -> pd.DataFrame:
        """
        Get pit stop information for a driver.
        
        Args:
            session: FastF1 Session object
            driver: Driver abbreviation
            
        Returns:
            DataFrame with pit stop laps and times
        """
        driver_laps = session.laps[session.laps['Driver'] == driver]
        pit_laps = driver_laps[driver_laps['PitInTime'].notna()].copy()
        
        if pit_laps.empty:
            return pd.DataFrame()
        
        # Calculate pit stop duration
        pit_laps['PitDuration'] = (
            pit_laps['PitOutTime'] - pit_laps['PitInTime']
        ).dt.total_seconds()
        
        return pit_laps[['LapNumber', 'PitInTime', 'PitOutTime', 'PitDuration', 'Compound', 'TyreLife']]
