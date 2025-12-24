"""
Telemetry Processor
Processes and extracts specific data from FastF1 telemetry
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional, Any


class TelemetryProcessor:
    """
    Processes telemetry data to extract meaningful metrics.
    
    Handles speed traces, throttle/brake analysis, corner detection,
    and telemetry-based calculations.
    """
    
    @staticmethod
    def extract_speed_trace(telemetry: pd.DataFrame) -> pd.DataFrame:
        """
        Extract clean speed trace from telemetry.
        
        Args:
            telemetry: Telemetry DataFrame
            
        Returns:
            DataFrame with Distance and Speed columns
        """
        return telemetry[['Distance', 'Speed']].copy()
    
    @staticmethod
    def extract_throttle_trace(telemetry: pd.DataFrame) -> pd.DataFrame:
        """
        Extract throttle application trace.
        
        Args:
            telemetry: Telemetry DataFrame
            
        Returns:
            DataFrame with Distance and Throttle (0-100%)
        """
        return telemetry[['Distance', 'Throttle']].copy()
    
    @staticmethod
    def extract_brake_trace(telemetry: pd.DataFrame) -> pd.DataFrame:
        """
        Extract brake application trace.
        
        Args:
            telemetry: Telemetry DataFrame
            
        Returns:
            DataFrame with Distance and Brake (boolean)
        """
        return telemetry[['Distance', 'Brake']].copy()
    
    @staticmethod
    def extract_brake_points(telemetry: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Identify all braking points in the lap.
        
        Args:
            telemetry: Telemetry DataFrame
            
        Returns:
            List of brake zones with start/end distances and metrics
        """
        brake_zones = []
        in_brake_zone = False
        brake_start = None
        speed_before = None
        
        for idx, row in telemetry.iterrows():
            if row['Brake'] and not in_brake_zone:
                # Start of brake zone
                in_brake_zone = True
                brake_start = row['Distance']
                speed_before = row['Speed']
            elif not row['Brake'] and in_brake_zone:
                # End of brake zone
                in_brake_zone = False
                brake_zones.append({
                    'start_distance': brake_start,
                    'end_distance': row['Distance'],
                    'brake_distance': row['Distance'] - brake_start,
                    'speed_before': speed_before,
                    'speed_after': row['Speed'],
                    'speed_loss': speed_before - row['Speed']
                })
        
        return brake_zones
    
    @staticmethod
    def identify_corners(telemetry: pd.DataFrame, speed_threshold: float = 200.0) -> List[Dict[str, Any]]:
        """
        Identify corners based on speed reduction.
        
        Args:
            telemetry: Telemetry DataFrame
            speed_threshold: Speed below which is considered a corner (km/h)
            
        Returns:
            List of corners with location and characteristics
        """
        corners = []
        in_corner = False
        corner_start = None
        corner_speeds = []
        
        for idx, row in telemetry.iterrows():
            if row['Speed'] < speed_threshold and not in_corner:
                # Start of corner
                in_corner = True
                corner_start = row['Distance']
                corner_speeds = [row['Speed']]
            elif row['Speed'] < speed_threshold and in_corner:
                # Continue in corner
                corner_speeds.append(row['Speed'])
            elif row['Speed'] >= speed_threshold and in_corner:
                # Exit corner
                in_corner = False
                if corner_speeds:
                    corners.append({
                        'start_distance': corner_start,
                        'end_distance': row['Distance'],
                        'apex_speed': min(corner_speeds),
                        'avg_speed': np.mean(corner_speeds),
                        'corner_length': row['Distance'] - corner_start
                    })
        
        return corners
    
    @staticmethod
    def calculate_mini_sectors(telemetry: pd.DataFrame, num_sectors: int = 20) -> pd.DataFrame:
        """
        Divide lap into mini-sectors for granular analysis.
        
        Args:
            telemetry: Telemetry DataFrame
            num_sectors: Number of mini-sectors to create
            
        Returns:
            DataFrame with mini-sector boundaries and metrics
        """
        total_distance = telemetry['Distance'].max()
        sector_length = total_distance / num_sectors
        
        mini_sectors = []
        for i in range(num_sectors):
            start_dist = i * sector_length
            end_dist = (i + 1) * sector_length
            
            sector_data = telemetry[
                (telemetry['Distance'] >= start_dist) & 
                (telemetry['Distance'] < end_dist)
            ]
            
            if not sector_data.empty:
                mini_sectors.append({
                    'sector_num': i + 1,
                    'start_distance': start_dist,
                    'end_distance': end_dist,
                    'avg_speed': sector_data['Speed'].mean(),
                    'max_speed': sector_data['Speed'].max(),
                    'min_speed': sector_data['Speed'].min(),
                    'throttle_percentage': sector_data['Throttle'].mean(),
                    'brake_usage': sector_data['Brake'].sum() / len(sector_data) * 100
                })
        
        return pd.DataFrame(mini_sectors)
    
    @staticmethod
    def calculate_acceleration(telemetry: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate acceleration/deceleration from speed data.
        
        Args:
            telemetry: Telemetry DataFrame
            
        Returns:
            DataFrame with acceleration values (m/s²)
        """
        tel = telemetry.copy()
        
        # Convert speed from km/h to m/s
        speed_ms = tel['Speed'] / 3.6
        
        # Calculate time delta (assuming SessionTime is in seconds)
        if 'SessionTime' in tel.columns:
            time_delta = tel['SessionTime'].diff().dt.total_seconds()
        else:
            # Estimate from distance and speed
            time_delta = tel['Distance'].diff() / speed_ms
        
        # Calculate acceleration
        tel['Acceleration'] = speed_ms.diff() / time_delta
        
        return tel[['Distance', 'Speed', 'Acceleration']].copy()
    
    @staticmethod
    def calculate_deceleration_rate(telemetry: pd.DataFrame, brake_zones: List[Dict]) -> List[float]:
        """
        Calculate deceleration rate in braking zones.
        
        Args:
            telemetry: Telemetry DataFrame
            brake_zones: List of brake zones from extract_brake_points
            
        Returns:
            List of average deceleration rates (m/s²) for each zone
        """
        decel_rates = []
        
        for zone in brake_zones:
            zone_data = telemetry[
                (telemetry['Distance'] >= zone['start_distance']) &
                (telemetry['Distance'] <= zone['end_distance'])
            ]
            
            if len(zone_data) > 1:
                # Speed in m/s
                speed_before = zone['speed_before'] / 3.6
                speed_after = zone['speed_after'] / 3.6
                
                # Time estimate (assuming constant deceleration)
                avg_speed = (speed_before + speed_after) / 2
                time_taken = zone['brake_distance'] / avg_speed if avg_speed > 0 else 0
                
                # Deceleration = (v_final - v_initial) / time
                decel = (speed_after - speed_before) / time_taken if time_taken > 0 else 0
                decel_rates.append(abs(decel))
            else:
                decel_rates.append(0.0)
        
        return decel_rates
    
    @staticmethod
    def compare_speed_traces(tel1: pd.DataFrame, tel2: pd.DataFrame) -> pd.DataFrame:
        """
        Compare speed traces of two laps.
        
        Args:
            tel1: Telemetry of first lap
            tel2: Telemetry of second lap
            
        Returns:
            DataFrame with distance and speed delta
        """
        # Merge on distance (approximate matching)
        merged = pd.merge_asof(
            tel1[['Distance', 'Speed']].rename(columns={'Speed': 'Speed1'}),
            tel2[['Distance', 'Speed']].rename(columns={'Speed': 'Speed2'}),
            on='Distance',
            direction='nearest'
        )
        
        merged['SpeedDelta'] = merged['Speed1'] - merged['Speed2']
        return merged
    
    @staticmethod
    def get_top_speed(telemetry: pd.DataFrame) -> float:
        """
        Get maximum speed reached in the lap.
        
        Args:
            telemetry: Telemetry DataFrame
            
        Returns:
            Maximum speed in km/h
        """
        return telemetry['Speed'].max()
    
    @staticmethod
    def get_corner_speeds(telemetry: pd.DataFrame, corners: List[Dict]) -> List[Dict[str, Any]]:
        """
        Extract detailed speed information for each corner.
        
        Args:
            telemetry: Telemetry DataFrame
            corners: List of corners from identify_corners
            
        Returns:
            List of corner speed analysis
        """
        corner_analysis = []
        
        for idx, corner in enumerate(corners):
            corner_data = telemetry[
                (telemetry['Distance'] >= corner['start_distance']) &
                (telemetry['Distance'] <= corner['end_distance'])
            ]
            
            if not corner_data.empty:
                # Entry speed (first 10% of corner)
                entry_section = corner_data.head(max(1, len(corner_data) // 10))
                entry_speed = entry_section['Speed'].mean()
                
                # Apex speed (minimum speed)
                apex_speed = corner_data['Speed'].min()
                
                # Exit speed (last 10% of corner)
                exit_section = corner_data.tail(max(1, len(corner_data) // 10))
                exit_speed = exit_section['Speed'].mean()
                
                corner_analysis.append({
                    'corner_num': idx + 1,
                    'entry_speed': entry_speed,
                    'apex_speed': apex_speed,
                    'exit_speed': exit_speed,
                    'speed_loss': entry_speed - apex_speed,
                    'speed_gain': exit_speed - apex_speed,
                    **corner
                })
        
        return corner_analysis
    
    @staticmethod
    def calculate_throttle_stats(telemetry: pd.DataFrame) -> Dict[str, float]:
        """
        Calculate throttle usage statistics.
        
        Args:
            telemetry: Telemetry DataFrame
            
        Returns:
            Dict with throttle metrics
        """
        return {
            'avg_throttle': telemetry['Throttle'].mean(),
            'max_throttle': telemetry['Throttle'].max(),
            'full_throttle_pct': (telemetry['Throttle'] == 100).sum() / len(telemetry) * 100,
            'partial_throttle_pct': ((telemetry['Throttle'] > 0) & (telemetry['Throttle'] < 100)).sum() / len(telemetry) * 100,
            'zero_throttle_pct': (telemetry['Throttle'] == 0).sum() / len(telemetry) * 100
        }
    
    @staticmethod
    def calculate_gear_usage(telemetry: pd.DataFrame) -> Dict[int, float]:
        """
        Calculate time spent in each gear.
        
        Args:
            telemetry: Telemetry DataFrame
            
        Returns:
            Dict with gear number and percentage of lap
        """
        if 'nGear' not in telemetry.columns:
            return {}
        
        total_points = len(telemetry)
        gear_usage = {}
        
        for gear in telemetry['nGear'].unique():
            if pd.notna(gear):
                gear_count = (telemetry['nGear'] == gear).sum()
                gear_usage[int(gear)] = (gear_count / total_points) * 100
        
        return gear_usage
