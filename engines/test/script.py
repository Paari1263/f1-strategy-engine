"""
FastF1 Migration Test Script
Tests all 8 engines with FastF1 data
"""
import asyncio
import sysimport jsonfrom pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from engines.track_engine.service import TrackService
from engines.car_engine.service import CarService
from engines.shared_services_fastf1 import (
    TyreService, WeatherService, TrafficService,
    PitService, SafetyCarService, DriverService
)
from engines.track_engine.schemas import TrackRequest
from engines.car_engine.schemas import CarRequest
from engines.tyre_engine.schemas import TyreRequest
from engines.weather_engine.schemas import WeatherRequest
from engines.traffic_engine.schemas import TrafficRequest
from engines.pit_engine.schemas import PitRequest
from engines.safetycar_engine.schemas import SafetyCarRequest
from engines.driver_engine.schemas import DriverRequest


async def test_track_engine():
    """Test Track Engine"""
    print("\n" + "="*60)
    print("Testing TRACK ENGINE")
    print("="*60)
    
    request = TrackRequest(year=2024, gp="Bahrain", session="R")
    result = await TrackService.get_track_characteristics(request)
    
    print(f"✓ Circuit: {result.circuit_name}")
    print(f"✓ Length: {result.length_km} km")
    print(f"✓ Corners: {result.corners}")
    print(f"✓ Sectors analyzed: {len(result.sector_analysis)}")
    print(f"✓ DRS zones: {len(result.drs_zones)}")
    print(f"✓ Track evolution periods: {len(result.track_evolution)}")
    print(f"\n📦 Full Response:")
    print(json.dumps(result.dict(), indent=2, default=str))
    return True


async def test_car_engine():
    """Test Car Engine"""
    print("\n" + "="*60)
    print("Testing CAR ENGINE")
    print("="*60)
    
    request = CarRequest(year=2024, gp="Bahrain", session="R", driver_number=1)
    result = await CarService.analyze_car_performance(request)
    
    print(f"✓ Circuit: {result.circuit_name}")
    print(f"✓ Drivers analyzed: {len(result.car_profiles)}")
    print(f"✓ Fastest car: {result.fastest_car}")
    if result.car_profiles:
        profile = result.car_profiles[0]
        print(f"✓ Example - Driver: {profile.driver_name}")
        print(f"  - Top speed: {profile.power_unit.top_speed_kmh} km/h")
        print(f"  - DRS usage: {profile.aerodynamics.drs_usage_pct}%")
    print(f"\n📦 Full Response:")
    print(json.dumps(result.dict(), indent=2, default=str))
    return True


async def test_tyre_engine():
    """Test Tyre Engine"""
    print("\n" + "="*60)
    print("Testing TYRE ENGINE")
    print("="*60)
    
    request = TyreRequest(year=2024, gp="Bahrain", session="R")
    result = await TyreService.analyze_tyre_performance(request)
    
    print(f"✓ Circuit: {result.circuit_name}")
    print(f"✓ Compounds analyzed: {len(result.compound_characteristics)}")
    print(f"✓ Stints analyzed: {len(result.stint_analyses)}")
    print(f"✓ Track tyre severity: {result.track_tyre_severity}")
    if result.compound_characteristics:
        comp = result.compound_characteristics[0]
        print(f"✓ Example - {comp.compound}: {comp.avg_lifetime_laps} laps avg life")
    print(f"\n📦 Full Response:")
    print(json.dumps(result.dict(), indent=2, default=str))
    return True


async def test_weather_engine():
    """Test Weather Engine"""
    print("\n" + "="*60)
    print("Testing WEATHER ENGINE")
    print("="*60)
    
    request = WeatherRequest(year=2024, gp="Bahrain", session="R")
    result = await WeatherService.analyze_weather(request)
    
    print(f"✓ Circuit: {result.circuit_name}")
    print(f"✓ Conditions: {result.conditions_summary}")
    print(f"✓ Weather snapshots: {len(result.lap_snapshots)}")
    print(f"✓ Weather trends: {len(result.weather_trends)}")
    if result.lap_snapshots:
        snap = result.lap_snapshots[0]
        print(f"✓ Air temp: {snap.air_temp_c}°C, Track temp: {snap.track_temp_c}°C")
    print(f"\n📦 Full Response:")
    print(json.dumps(result.dict(), indent=2, default=str))
    return True


async def test_traffic_engine():
    """Test Traffic Engine"""
    print("\n" + "="*60)
    print("Testing TRAFFIC ENGINE")
    print("="*60)
    
    request = TrafficRequest(year=2024, gp="Bahrain", session="R")
    result = await TrafficService.analyze_traffic(request)
    
    print(f"✓ Circuit: {result.circuit_name}")
    print(f"✓ Gap evolution points: {len(result.gap_evolution)}")
    print(f"✓ Overtaking difficulty: {result.overtaking_difficulty_score}")
    print(f"✓ Avg overtakes/lap: {result.avg_overtakes_per_lap}")
    print(f"\n📦 Full Response:")
    print(json.dumps(result.dict(), indent=2, default=str))
    return True


async def test_pit_engine():
    """Test Pit Engine"""
    print("\n" + "="*60)
    print("Testing PIT ENGINE")
    print("="*60)
    
    request = PitRequest(year=2024, gp="Bahrain", session="R")
    result = await PitService.analyze_pit_stops(request)
    
    print(f"✓ Circuit: {result.circuit_name}")
    print(f"✓ Pit stops detected: {len(result.pit_stops)}")
    print(f"✓ Avg pit lane loss: {result.avg_pit_lane_time_loss_sec}s")
    print(f"✓ Pit windows: {result.pit_window_recommendations}")
    print(f"\n📦 Full Response:")
    print(json.dumps(result.dict(), indent=2, default=str))
    return True


async def test_safetycar_engine():
    """Test Safety Car Engine"""
    print("\n" + "="*60)
    print("Testing SAFETY CAR ENGINE")
    print("="*60)
    
    request = SafetyCarRequest(year=2024, gp="Bahrain", session="R")
    result = await SafetyCarService.analyze_safety_car(request)
    
    print(f"✓ Circuit: {result.circuit_name}")
    print(f"✓ SC deployments: {len(result.safety_car_deployments)}")
    print(f"✓ Total SC laps: {result.total_sc_laps}")
    print(f"✓ Racing laps: {result.racing_laps_pct}%")
    print(f"✓ Historical SC probability: {result.historical_sc_probability}")
    print(f"\n📦 Full Response:")
    print(json.dumps(result.dict(), indent=2, default=str))
    return True


async def test_driver_engine():
    """Test Driver Engine"""
    print("\n" + "="*60)
    print("Testing DRIVER ENGINE")
    print("="*60)
    
    request = DriverRequest(year=2024, gp="Bahrain", session="R")
    result = await DriverService.analyze_driver_performance(request)
    
    print(f"✓ Circuit: {result.circuit_name}")
    print(f"✓ Drivers analyzed: {len(result.driver_profiles)}")
    if result.driver_profiles:
        driver = result.driver_profiles[0]
        print(f"✓ Example - {driver.driver_name} ({driver.team})")
        print(f"  - Consistency: {driver.consistency.consistency_score}")
        print(f"  - Overall rating: {driver.overall_rating}/10")
    print(f"\n📦 Full Response:")
    print(json.dumps(result.dict(), indent=2, default=str))
    return True


async def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("FastF1 Migration Test Suite")
    print("Testing Bahrain 2024 Race")
    print("="*60)
    
    tests = [
        ("Track Engine", test_track_engine),
        ("Car Engine", test_car_engine),
        ("Tyre Engine", test_tyre_engine),
        ("Weather Engine", test_weather_engine),
        ("Traffic Engine", test_traffic_engine),
        ("Pit Engine", test_pit_engine),
        ("Safety Car Engine", test_safetycar_engine),
        ("Driver Engine", test_driver_engine),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            await test_func()
            passed += 1
            print(f"✓ {name} PASSED")
        except Exception as e:
            failed += 1
            print(f"✗ {name} FAILED: {e}")
    
    print("\n" + "="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60)
    
    return failed == 0


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
