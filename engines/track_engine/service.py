"""
Track Engine Service Layer - FastF1 Implementation
Deep track analysis using FastF1 telemetry and historical data
"""
import logging
import numpy as np
import pandas as pd
from typing import List, Dict, Any
from asgiref.sync import sync_to_async
from shared.clients.fastf1_client import get_session
from shared.middleware import DataNotFoundError, SessionNotAvailableError
from engines.track_engine.schemas import (
    TrackRequest, TrackResponse, SectorAnalysis, 
    DRSZone, TrackEvolution
)

logger = logging.getLogger(__name__)


class TrackService:
    """Service layer for comprehensive track analysis using FastF1"""
    
    @staticmethod
    async def get_track_characteristics(request: TrackRequest) -> TrackResponse:
        """
        Perform comprehensive track analysis using FastF1 data
        
        Args:
            request: TrackRequest with year, gp, session
            
        Returns:
            TrackResponse with detailed track characteristics
            
        Raises:
            SessionNotAvailableError: If session data cannot be loaded
            DataNotFoundError: If required data is missing
        """
        logger.info(f"Analyzing track: {request.year} {request.gp} {request.session}")
        
        try:
            # Load session data (wrapped in sync_to_async)
            session = await sync_to_async(get_session)(
                request.year, request.gp, request.session
            )
        except Exception as e:
            logger.error(f"Failed to load session: {e}")
            raise SessionNotAvailableError(
                f"Session data not available for {request.year} {request.gp} {request.session}",
                details={"error": str(e)}
            )
        
        # Extract circuit information
        circuit_info = TrackService._extract_circuit_info(session)
        
        # Analyze track characteristics
        track_chars = TrackService._analyze_track_characteristics(session)
        
        # Perform sector analysis
        sector_analysis = TrackService._analyze_sectors(session)
        
        # Analyze DRS zones
        drs_zones = TrackService._analyze_drs_zones(session)
        
        # Track evolution across sessions
        track_evolution = await TrackService._analyze_track_evolution(
            request.year, request.gp, request.session
        )
        
        # Advanced metrics
        advanced_metrics = TrackService._calculate_advanced_metrics(session)
        
        # Build response
        response = TrackResponse(
            **circuit_info,
            **track_chars,
            sector_analysis=sector_analysis,
            drs_zones=drs_zones,
            track_evolution=track_evolution,
            **advanced_metrics
        )
        
        logger.info(f"Track analysis complete for {circuit_info['circuit_name']}")
        return response
    
    @staticmethod
    def _extract_circuit_info(session) -> Dict[str, Any]:
        """Extract basic circuit information from session"""
        event = session.event
        laps = session.laps
        
        # Calculate track length
        if not laps.empty and 'Distance' in laps.columns:
            length_km = laps['Distance'].max() / 1000  # Convert to km
        else:
            length_km = 5.0  # Default fallback
        
        return {
            "circuit_name": event.get('EventName', 'Unknown Circuit'),
            "location": event.get('Location', 'Unknown'),
            "country": event.get('Country', 'Unknown'),
            "length_km": round(length_km, 3)
        }
    
    @staticmethod
    def _detect_corners_from_telemetry(session) -> int:
        """
        Detect number of corners by analyzing speed patterns in telemetry
        """
        try:
            # Get fastest lap telemetry
            fastest_lap = session.laps.pick_fastest()
            telemetry = fastest_lap.get_telemetry()
            
            if telemetry.empty or 'Speed' not in telemetry.columns:
                return 15  # Default fallback
            
            # Find local minima in speed (corner apexes)
            from scipy.signal import find_peaks
            
            # Invert speed to find valleys (low speed = corners)
            inverted_speed = -telemetry['Speed'].values
            peaks, _ = find_peaks(inverted_speed, prominence=20, distance=50)
            
            corners = len(peaks)
            logger.debug(f"Detected {corners} corners from telemetry")
            
            return max(corners, 10)  # Minimum 10 corners
            
        except Exception as e:
            logger.warning(f"Corner detection failed: {e}")
            return 15  # Default
    
    @staticmethod
    def _analyze_track_characteristics(session) -> Dict[str, float]:
        """Calculate track-specific multipliers and characteristics"""
        laps = session.laps
        
        if laps.empty:
            # Return default values if no lap data
            return {
                "corners": 15,
                "grip_multiplier": 1.0,
                "tyre_abrasion_level": 0.5,
                "pit_lane_time_loss_sec": 20.0,
                "overtaking_difficulty": 0.5,
                "power_sensitivity": 0.5,
                "corner_sensitivity": 0.5
            }
        
        # Detect corners from telemetry
        corners = TrackService._detect_corners_from_telemetry(session)
        
        # Calculate track characteristics based on actual data
        circuit_length = laps['Distance'].max() / 1000 if 'Distance' in laps.columns else 5.0
        
        # Corner density = corners per km (higher = more technical)
        corner_density = corners / circuit_length
        
        # Power sensitivity (inverse of corner density)
        power_sensitivity = min(1.0, max(0.3, 1.0 - (corner_density / 5.0)))
        
        # Corner sensitivity (proportional to corner density)
        corner_sensitivity = min(1.0, max(0.3, corner_density / 5.0))
        
        # Overtaking difficulty (high corner density = harder to overtake)
        overtaking_difficulty = min(1.0, max(0.2, corner_density / 6.0))
        
        return {
            "corners": corners,
            "grip_multiplier": 1.0,  # Will be refined with weather data
            "tyre_abrasion_level": 0.6,  # Track-specific, can be enhanced
            "pit_lane_time_loss_sec": 22.0,  # Default, can calculate from pit data
            "overtaking_difficulty": round(overtaking_difficulty, 2),
            "power_sensitivity": round(power_sensitivity, 2),
            "corner_sensitivity": round(corner_sensitivity, 2)
        }
    
    @staticmethod
    def _analyze_sectors(session) -> List[SectorAnalysis]:
        """Analyze each sector's characteristics"""
        laps = session.laps
        
        if laps.empty:
            return []
        
        sector_analyses = []
        
        for sector_num in [1, 2, 3]:
            sector_col = f'Sector{sector_num}Time'
            
            if sector_col not in laps.columns:
                continue
            
            # Get valid sector times
            sector_times = laps[laps[sector_col].notna()][sector_col]
            
            if sector_times.empty:
                continue
            
            # Analyze sector speeds from fastest lap
            try:
                fastest_lap = session.laps.pick_fastest()
                telemetry = fastest_lap.get_telemetry()
                
                if not telemetry.empty and 'Speed' in telemetry.columns:
                    # Estimate sector length (total distance / 3)
                    total_distance = telemetry['Distance'].max() if 'Distance' in telemetry.columns else 5000
                    sector_length = (total_distance / 3) / 1000  # km
                    
                    # Get speed stats for this third of the lap
                    sector_start = (sector_num - 1) * len(telemetry) // 3
                    sector_end = sector_num * len(telemetry) // 3
                    sector_telemetry = telemetry.iloc[sector_start:sector_end]
                    
                    avg_speed = sector_telemetry['Speed'].mean()
                    min_speed = sector_telemetry['Speed'].min()
                    max_speed = sector_telemetry['Speed'].max()
                    
                    # Characterize sector
                    if avg_speed > 200:
                        characteristics = "High-speed"
                    elif avg_speed < 150:
                        characteristics = "Technical"
                    else:
                        characteristics = "Mixed"
                    
                    sector_analyses.append(SectorAnalysis(
                        sector_number=sector_num,
                        length_km=round(sector_length, 2),
                        avg_speed_kmh=round(avg_speed, 1),
                        min_speed_kmh=round(min_speed, 1),
                        max_speed_kmh=round(max_speed, 1),
                        characteristics=characteristics
                    ))
            except Exception as e:
                logger.warning(f"Sector {sector_num} analysis failed: {e}")
                continue
        
        return sector_analyses
    
    @staticmethod
    def _analyze_drs_zones(session) -> List[DRSZone]:
        """
        Analyze DRS zones and their effectiveness
        """
        drs_zones = []
        
        try:
            fastest_lap = session.laps.pick_fastest()
            telemetry = fastest_lap.get_telemetry()
            
            if telemetry.empty or 'DRS' not in telemetry.columns:
                return []
            
            # Find DRS activation zones
            drs_active = telemetry['DRS'] > 0
            drs_changes = drs_active.astype(int).diff()
            
            # Find starts and ends of DRS zones
            drs_starts = telemetry[drs_changes == 1]
            drs_ends = telemetry[drs_changes == -1]
            
            for idx, (start_idx, end_idx) in enumerate(zip(drs_starts.index, drs_ends.index)):
                start_data = telemetry.loc[start_idx]
                end_data = telemetry.loc[end_idx]
                
                # Calculate zone characteristics
                activation_distance = start_data.get('Distance', 0)
                zone_length = end_data.get('Distance', 0) - activation_distance
                
                # Speed delta (simplified)
                avg_speed_in_zone = telemetry.loc[start_idx:end_idx, 'Speed'].mean()
                speed_delta = avg_speed_in_zone * 0.1  # DRS typically gives ~10% speed boost
                
                # Effectiveness score (based on zone length and speed gain)
                effectiveness = min(1.0, zone_length / 1000 * 0.5)  # Longer zone = more effective
                
                drs_zones.append(DRSZone(
                    zone_number=idx + 1,
                    activation_distance_m=round(activation_distance, 0),
                    length_m=round(zone_length, 0),
                    speed_delta_kmh=round(speed_delta, 1),
                    effectiveness_score=round(effectiveness, 2)
                ))
        
        except Exception as e:
            logger.warning(f"DRS analysis failed: {e}")
        
        return drs_zones
    
    @staticmethod
    async def _analyze_track_evolution(year: int, gp: str, current_session: str) -> List[TrackEvolution]:
        """Analyze track evolution across practice, quali, and race sessions"""
        session_order = ['FP1', 'FP2', 'FP3', 'Q', 'R']
        evolution_data = []
        
        # Only analyze up to current session
        try:
            current_idx = session_order.index(current_session)
            sessions_to_check = session_order[:current_idx + 1]
        except ValueError:
            sessions_to_check = [current_session]
        
        for session_type in sessions_to_check:
            try:
                session = await sync_to_async(get_session)(year, gp, session_type)
                laps = session.laps
                
                if laps.empty or 'LapTime' not in laps.columns:
                    continue
                
                # Calculate grip evolution (based on lap time improvement)
                valid_laps = laps[laps['LapTime'].notna()]
                
                if len(valid_laps) < 2:
                    continue
                
                # Calculate average grip level (inverse of lap time, normalized)
                avg_lap_time = valid_laps['LapTime'].mean().total_seconds()
                grip_level = round(100.0 / avg_lap_time, 2)  # Arbitrary scale
                
                # Calculate improvement per lap
                lap_numbers = valid_laps['LapNumber'].values
                lap_times_sec = valid_laps['LapTime'].dt.total_seconds().values
                
                if len(lap_times_sec) > 5:
                    # Fit linear trend
                    coeffs = np.polyfit(lap_numbers, lap_times_sec, 1)
                    improvement_per_lap = abs(coeffs[0]) * 1000  # Convert to ms
                    total_improvement = improvement_per_lap * len(lap_times_sec)
                else:
                    improvement_per_lap = 0.0
                    total_improvement = 0.0
                
                evolution_data.append(TrackEvolution(
                    session_type=session_type,
                    avg_grip_level=grip_level,
                    improvement_per_lap_ms=round(improvement_per_lap, 1),
                    total_improvement_ms=round(total_improvement, 1)
                ))
            
            except Exception as e:
                logger.debug(f"Could not load {session_type}: {e}")
                continue
        
        return evolution_data
    
    @staticmethod
    def _calculate_advanced_metrics(session) -> Dict[str, Any]:
        """Calculate advanced track metrics from telemetry"""
        try:
            fastest_lap = session.laps.pick_fastest()
            telemetry = fastest_lap.get_telemetry()
            
            if telemetry.empty or 'Speed' not in telemetry.columns:
                return {
                    "elevation_range_m": None,
                    "top_speed_kmh": 300.0,
                    "slowest_corner_kmh": 80.0,
                    "avg_lap_speed_kmh": 200.0,
                    "historical_safety_car_probability": 0.25,
                    "weather_sensitivity": 0.5
                }
            
            # Calculate speed metrics
            top_speed = telemetry['Speed'].max()
            slowest_corner = telemetry['Speed'].min()
            avg_speed = telemetry['Speed'].mean()
            
            # Elevation (if available from GPS data)
            elevation_range = None
            if 'Z' in telemetry.columns:  # Z coordinate = elevation
                elevation_range = telemetry['Z'].max() - telemetry['Z'].min()
            
            return {
                "elevation_range_m": round(elevation_range, 1) if elevation_range else None,
                "top_speed_kmh": round(top_speed, 1),
                "slowest_corner_kmh": round(slowest_corner, 1),
                "avg_lap_speed_kmh": round(avg_speed, 1),
                "historical_safety_car_probability": 0.25,  # Would need historical analysis
                "weather_sensitivity": 0.5  # Would need weather correlation analysis
            }
        
        except Exception as e:
            logger.warning(f"Advanced metrics calculation failed: {e}")
            return {
                "elevation_range_m": None,
                "top_speed_kmh": 300.0,
                "slowest_corner_kmh": 80.0,
                "avg_lap_speed_kmh": 200.0,
                "historical_safety_car_probability": 0.25,
                "weather_sensitivity": 0.5
            }
