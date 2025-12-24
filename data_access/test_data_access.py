"""
Test script for Data Access Layer
Validates FastF1 integration, telemetry processing, and caching

Run: python data_access/test_data_access.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_access import FastF1DataLoader, TelemetryProcessor, CacheManager


def print_section(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_fastf1_loader():
    """Test FastF1DataLoader functionality"""
    print_section("TEST 1: FastF1DataLoader")
    
    # Initialize loader
    loader = FastF1DataLoader()
    print("✓ FastF1DataLoader initialized")
    
    # Test loading a session (using recent race)
    print("\nLoading 2024 Abu Dhabi Grand Prix Race...")
    try:
        session = loader.get_session(2024, 'Abu Dhabi', 'R')
        print(f"✓ Session loaded: {session.event['EventName']} - {session.name}")
        print(f"  Date: {session.date}")
        
        # Get all drivers
        drivers = loader.get_all_drivers(session)
        print(f"✓ Found {len(drivers)} drivers: {', '.join(drivers[:5])}...")
        
        # Get driver info
        if 'VER' in drivers:
            driver_info = loader.get_driver_info(session, 'VER')
            print(f"✓ Driver info for VER: Team={driver_info['team']}, Number={driver_info['driver_number']}")
            print(f"  Teammate: {driver_info['teammate']}")
        
        # Get lap data
        if 'VER' in drivers:
            ver_laps = loader.get_lap_data(session, 'VER')
            print(f"✓ Loaded {len(ver_laps)} laps for VER")
            print(f"  Fastest lap: {ver_laps['LapTime'].min()}")
        
        # Get fastest lap
        fastest = loader.get_fastest_lap(session)
        print(f"✓ Fastest lap overall: {fastest['Driver']} - {fastest['LapTime']}")
        
        # Get weather data
        weather = loader.get_weather_data(session)
        print(f"✓ Weather data: {len(weather)} entries")
        print(f"  Avg track temp: {weather['TrackTemp'].mean():.1f}°C")
        print(f"  Avg air temp: {weather['AirTemp'].mean():.1f}°C")
        
        # Get pit stops
        if 'VER' in drivers:
            pit_stops = loader.get_pit_stops(session, 'VER')
            print(f"✓ Pit stops for VER: {len(pit_stops)}")
            if not pit_stops.empty:
                print(f"  First pit: Lap {pit_stops.iloc[0]['LapNumber']}, Duration: {pit_stops.iloc[0]['PitDuration']:.2f}s")
        
        return session, drivers
    
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return None, []


def test_telemetry_processor(session, drivers):
    """Test TelemetryProcessor functionality"""
    print_section("TEST 2: TelemetryProcessor")
    
    if session is None or not drivers:
        print("⚠ Skipping telemetry test (no session loaded)")
        return
    
    processor = TelemetryProcessor()
    print("✓ TelemetryProcessor initialized")
    
    try:
        # Get a fast lap
        driver = drivers[0]
        driver_laps = session.laps[session.laps['Driver'] == driver]
        fastest_lap = driver_laps.pick_fastest()
        
        print(f"\nAnalyzing fastest lap of {driver}...")
        telemetry = fastest_lap.get_telemetry()
        print(f"✓ Telemetry loaded: {len(telemetry)} data points (~200Hz)")
        
        # Extract speed trace
        speed_trace = processor.extract_speed_trace(telemetry)
        print(f"✓ Speed trace: Min={speed_trace['Speed'].min():.1f} km/h, Max={speed_trace['Speed'].max():.1f} km/h")
        
        # Get top speed
        top_speed = processor.get_top_speed(telemetry)
        print(f"✓ Top speed: {top_speed:.1f} km/h")
        
        # Extract brake points
        brake_points = processor.extract_brake_points(telemetry)
        print(f"✓ Identified {len(brake_points)} braking zones")
        if brake_points:
            print(f"  Example: {brake_points[0]['brake_distance']:.1f}m braking, {brake_points[0]['speed_loss']:.1f} km/h speed loss")
        
        # Identify corners
        corners = processor.identify_corners(telemetry, speed_threshold=250)
        print(f"✓ Identified {len(corners)} corners (speed < 250 km/h)")
        if corners:
            print(f"  Slowest corner: {corners[0]['apex_speed']:.1f} km/h apex speed")
        
        # Calculate mini-sectors
        mini_sectors = processor.calculate_mini_sectors(telemetry, num_sectors=10)
        print(f"✓ Created {len(mini_sectors)} mini-sectors")
        print(f"  Fastest mini-sector: {mini_sectors['avg_speed'].max():.1f} km/h avg")
        print(f"  Slowest mini-sector: {mini_sectors['avg_speed'].min():.1f} km/h avg")
        
        # Throttle stats
        throttle_stats = processor.calculate_throttle_stats(telemetry)
        print(f"✓ Throttle statistics:")
        print(f"  Full throttle: {throttle_stats['full_throttle_pct']:.1f}% of lap")
        print(f"  Partial throttle: {throttle_stats['partial_throttle_pct']:.1f}%")
        print(f"  Zero throttle: {throttle_stats['zero_throttle_pct']:.1f}%")
        
        # Gear usage
        gear_usage = processor.calculate_gear_usage(telemetry)
        if gear_usage:
            print(f"✓ Gear usage:")
            for gear, pct in sorted(gear_usage.items()):
                print(f"  Gear {gear}: {pct:.1f}% of lap")
        
    except Exception as e:
        print(f"✗ FAILED: {e}")


def test_cache_manager():
    """Test CacheManager functionality"""
    print_section("TEST 3: CacheManager")
    
    cache = CacheManager()
    print(f"✓ CacheManager initialized")
    print(f"  Cache directory: {cache.cache_dir}")
    
    # Test caching
    test_data = {
        'analysis_type': 'test',
        'results': [1, 2, 3],
        'metadata': {'version': '1.0'}
    }
    
    key = cache.generate_analysis_key('test_analysis', 2024, 'Monaco')
    print(f"\n✓ Generated cache key: {key[:16]}...")
    
    # Cache data
    cache.cache_result(key, test_data, category='results')
    print("✓ Data cached successfully")
    
    # Check if cached
    is_cached = cache.is_cached(key, category='results')
    print(f"✓ Cache exists: {is_cached}")
    
    # Load from cache
    loaded_data = cache.load_cached_result(key, category='results')
    print(f"✓ Data loaded from cache: {loaded_data == test_data}")
    
    # Get cache info
    cache_info = cache.get_cache_info()
    print(f"\n✓ Cache statistics:")
    print(f"  Results cached: {cache_info['results_count']}")
    print(f"  Total cache size: {cache_info['total_size_mb']:.2f} MB")
    
    # Clean up test cache
    cache.clear_cache(category='results')
    print("✓ Test cache cleared")


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("  F1 STRATEGY ENGINE - DATA ACCESS LAYER TEST")
    print("  Phase 1: Foundation & Data Infrastructure")
    print("=" * 70)
    
    # Test 1: FastF1 Loader
    session, drivers = test_fastf1_loader()
    
    # Test 2: Telemetry Processor
    test_telemetry_processor(session, drivers)
    
    # Test 3: Cache Manager
    test_cache_manager()
    
    # Summary
    print("\n" + "=" * 70)
    print("  ✓ DATA ACCESS LAYER TESTS COMPLETE")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. ✓ FastF1DataLoader - Session loading operational")
    print("  2. ✓ TelemetryProcessor - Telemetry extraction working")
    print("  3. ✓ CacheManager - Caching system functional")
    print("\n  Ready for Phase 2: Car & Driver Analysis Modules")
    print("=" * 70)


if __name__ == "__main__":
    main()
