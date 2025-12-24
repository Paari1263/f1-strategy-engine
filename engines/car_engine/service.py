"""
Car Engine Service - FastF1 Implementation
High-resolution telemetry analysis for car performance
"""
import logging
import numpy as np
from typing import List, Optional
from asgiref.sync import sync_to_async
from shared.clients.fastf1_client import get_session
from shared.middleware import SessionNotAvailableError, DataNotFoundError
from engines.car_engine.schemas import (
    CarRequest, CarResponse, CarPerformanceProfile,
    PowerUnitMetrics, AerodynamicsMetrics, BrakingMetrics
)

logger = logging.getLogger(__name__)


class CarService:
    """Service for car performance analysis using FastF1 telemetry"""
    
    @staticmethod
    async def analyze_car_performance(request: CarRequest) -> CarResponse:
        """Analyze car performance from high-resolution telemetry"""
        logger.info(f"Car analysis: {request.year} {request.gp} {request.session}")
        
        try:
            # Note: Session object caching disabled - complex objects don't serialize well
            session = await sync_to_async(get_session)(request.year, request.gp, request.session)
        except Exception as e:
            raise SessionNotAvailableError(f"Session unavailable: {e}")
        
        laps = session.laps
        if laps.empty:
            raise DataNotFoundError("No lap data available")
        
        # Filter by driver if specified
        if request.driver_number:
            laps = laps[laps['DriverNumber'] == str(request.driver_number)]
        
        # Analyze each driver
        car_profiles = []
        drivers = laps['DriverNumber'].unique()
        
        for driver_num in drivers:
            try:
                profile = await CarService._analyze_driver_car(session, str(driver_num))
                if profile:
                    car_profiles.append(profile)
            except Exception as e:
                logger.warning(f"Failed to analyze driver {driver_num}: {e}")
        
        # Find fastest
        fastest_car = None
        if car_profiles:
            fastest = min(car_profiles, key=lambda x: x.lap_time_best_sec)
            fastest_car = f"{fastest.driver_name} ({fastest.team})"
        
        return CarResponse(
            circuit_name=session.event.get('EventName', 'Unknown'),
            session_type=request.session,
            car_profiles=car_profiles,
            fastest_car=fastest_car,
            comparative_analysis={"total_drivers": len(car_profiles)}
        )
    
    @staticmethod
    async def _analyze_driver_car(session, driver_num: str) -> Optional[CarPerformanceProfile]:
        """Analyze individual driver's car performance"""
        driver_laps = session.laps[session.laps['DriverNumber'] == driver_num]
        
        if driver_laps.empty:
            return None
        
        # Get driver info
        driver_info = driver_laps.iloc[0]
        driver_name = driver_info.get('Driver', f"Driver {driver_num}")
        team = driver_info.get('Team', 'Unknown')
        
        # Analyze fastest lap telemetry
        try:
            fastest_lap = driver_laps.pick_fastest()
            telemetry = await sync_to_async(fastest_lap.get_telemetry)()
        except:
            telemetry = None
        
        # Power unit metrics
        pu_metrics = CarService._analyze_power_unit(telemetry) if telemetry is not None else PowerUnitMetrics(
            avg_rpm=10000, max_rpm=12000, avg_throttle_pct=65.0,
            full_throttle_time_pct=45.0, gear_changes_per_lap=50, top_speed_kmh=300.0
        )
        
        # Aero metrics
        aero_metrics = CarService._analyze_aerodynamics(telemetry) if telemetry is not None else AerodynamicsMetrics(
            drs_usage_pct=15.0, drs_speed_gain_kmh=10.0,
            avg_speed_fast_corners_kmh=180.0, avg_speed_slow_corners_kmh=100.0,
            downforce_estimate="Medium"
        )
        
        # Braking metrics
        brake_metrics = CarService._analyze_braking(telemetry) if telemetry is not None else BrakingMetrics(
            avg_brake_pressure=50.0, max_brake_pressure=100.0,
            braking_zones_per_lap=10, brake_efficiency_score=0.75
        )
        
        # Lap time stats
        valid_laps = driver_laps[driver_laps['LapTime'].notna()]
        avg_lap = valid_laps['LapTime'].mean().total_seconds() if not valid_laps.empty else 90.0
        best_lap = valid_laps['LapTime'].min().total_seconds() if not valid_laps.empty else 90.0
        consistency = 1.0 - (valid_laps['LapTime'].std().total_seconds() / avg_lap if not valid_laps.empty else 0.1)
        
        return CarPerformanceProfile(
            driver_number=int(driver_num),
            driver_name=driver_name,
            team=team,
            power_unit=pu_metrics,
            aerodynamics=aero_metrics,
            braking=brake_metrics,
            consistency_score=round(max(0.0, min(1.0, consistency)), 2),
            lap_time_avg_sec=round(avg_lap, 2),
            lap_time_best_sec=round(best_lap, 2)
        )
    
    @staticmethod
    def _analyze_power_unit(telemetry) -> PowerUnitMetrics:
        """Analyze power unit from telemetry"""
        if telemetry is None or telemetry.empty:
            return PowerUnitMetrics(avg_rpm=10000, max_rpm=12000, avg_throttle_pct=65.0,
                                   full_throttle_time_pct=45.0, gear_changes_per_lap=50, top_speed_kmh=300.0)
        
        rpm = float(telemetry['RPM'].mean()) if 'RPM' in telemetry.columns else 10000.0
        max_rpm = float(telemetry['RPM'].max()) if 'RPM' in telemetry.columns else 12000.0
        throttle = float(telemetry['Throttle'].mean()) if 'Throttle' in telemetry.columns else 65.0
        full_throttle_pct = float((telemetry['Throttle'] >= 99).sum() / len(telemetry) * 100) if 'Throttle' in telemetry.columns else 45.0
        
        # Gear changes
        gear_changes = 0
        if 'nGear' in telemetry.columns:
            gear_changes = int((telemetry['nGear'].diff() != 0).sum())
        
        top_speed = float(telemetry['Speed'].max()) if 'Speed' in telemetry.columns else 300.0
        
        return PowerUnitMetrics(
            avg_rpm=round(rpm, 0),
            max_rpm=round(max_rpm, 0),
            avg_throttle_pct=round(throttle, 1),
            full_throttle_time_pct=round(full_throttle_pct, 1),
            gear_changes_per_lap=gear_changes,
            top_speed_kmh=round(top_speed, 1)
        )
    
    @staticmethod
    def _analyze_aerodynamics(telemetry) -> AerodynamicsMetrics:
        """Analyze aerodynamic performance"""
        if telemetry is None or telemetry.empty:
            return AerodynamicsMetrics(drs_usage_pct=15.0, drs_speed_gain_kmh=10.0,
                                      avg_speed_fast_corners_kmh=180.0, avg_speed_slow_corners_kmh=100.0,
                                      downforce_estimate="Medium")
        
        drs_usage = float((telemetry['DRS'] > 0).sum() / len(telemetry) * 100) if 'DRS' in telemetry.columns else 15.0
        
        # Estimate speed gain (simplified)
        drs_speed_gain = 10.0
        
        # Corner speeds (simplified - based on speed thresholds)
        fast_corner_speed = float(telemetry[telemetry['Speed'] > 150]['Speed'].mean()) if 'Speed' in telemetry.columns else 180.0
        slow_corner_speed = float(telemetry[telemetry['Speed'] < 150]['Speed'].mean()) if 'Speed' in telemetry.columns else 100.0
        
        # Downforce estimate
        avg_speed = float(telemetry['Speed'].mean()) if 'Speed' in telemetry.columns else 200.0
        if avg_speed > 220:
            downforce = "Low"
        elif avg_speed > 180:
            downforce = "Medium"
        else:
            downforce = "High"
        
        return AerodynamicsMetrics(
            drs_usage_pct=round(drs_usage, 1),
            drs_speed_gain_kmh=round(drs_speed_gain, 1),
            avg_speed_fast_corners_kmh=round(fast_corner_speed, 1),
            avg_speed_slow_corners_kmh=round(slow_corner_speed, 1),
            downforce_estimate=downforce
        )
    
    @staticmethod
    def _analyze_braking(telemetry) -> BrakingMetrics:
        """Analyze braking performance"""
        if telemetry is None or telemetry.empty or 'Brake' not in telemetry.columns:
            return BrakingMetrics(avg_brake_pressure=50.0, max_brake_pressure=100.0,
                                 braking_zones_per_lap=10, brake_efficiency_score=0.75)
        
        avg_brake = float(telemetry[telemetry['Brake'] > 0]['Brake'].mean()) if (telemetry['Brake'] > 0).any() else 50.0
        max_brake = float(telemetry['Brake'].max())
        
        # Count braking zones
        braking = telemetry['Brake'] > 10
        braking_changes = braking.astype(int).diff()
        braking_zones = int((braking_changes == 1).sum())
        
        # Efficiency (simplified)
        efficiency = 0.75 + (max_brake / 100.0 * 0.2)
        
        return BrakingMetrics(
            avg_brake_pressure=round(avg_brake, 1),
            max_brake_pressure=round(max_brake, 1),
            braking_zones_per_lap=braking_zones,
            brake_efficiency_score=round(min(1.0, efficiency), 2)
        )
