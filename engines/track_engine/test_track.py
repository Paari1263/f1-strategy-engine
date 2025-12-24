"""
Track Engine Test Script
Tests track analysis with FastF1 data
"""
import asyncio
import sysimport jsonfrom pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from engines.track_engine.service import TrackService
from engines.track_engine.schemas import TrackRequest


async def test_track_engine():
    """Test Track Engine with Bahrain 2024 Race"""
    print("="*70)
    print("TRACK ENGINE TEST - Bahrain 2024 Race")
    print("="*70)
    
    # Test data
    request = TrackRequest(
        year=2024,
        gp="Bahrain",
        session="R"
    )
    
    print(f"\n📍 Testing: {request.year} {request.gp} {request.session}")
    print("⏳ Loading session data (may take 30-60s on first run)...")
    
    try:
        result = await TrackService.get_track_characteristics(request)
        
        print(f"\n✅ SUCCESS - Track Analysis Complete")
        print(f"\n{'='*70}")
        print("TRACK INFORMATION")
        print(f"{'='*70}")
        print(f"Circuit Name:     {result.circuit_name}")
        print(f"Location:         {result.location}")
        print(f"Country:          {result.country}")
        print(f"Length:           {result.length_km} km")
        print(f"Corners:          {result.corners}")
        
        print(f"\n{'='*70}")
        print("TRACK CHARACTERISTICS")
        print(f"{'='*70}")
        print(f"Grip Multiplier:         {result.grip_multiplier}")
        print(f"Tyre Abrasion:           {result.tyre_abrasion_level}")
        print(f"Pit Lane Loss:           {result.pit_lane_time_loss_sec}s")
        print(f"Overtaking Difficulty:   {result.overtaking_difficulty}")
        print(f"Power Sensitivity:       {result.power_sensitivity}")
        print(f"Corner Sensitivity:      {result.corner_sensitivity}")
        
        if result.sector_analysis:
            print(f"\n{'='*70}")
            print(f"SECTOR ANALYSIS ({len(result.sector_analysis)} sectors)")
            print(f"{'='*70}")
            for sector in result.sector_analysis:
                print(f"\nSector {sector.sector_number}:")
                print(f"  Length:          {sector.length_km} km")
                print(f"  Avg Speed:       {sector.avg_speed_kmh} km/h")
                print(f"  Speed Range:     {sector.min_speed_kmh} - {sector.max_speed_kmh} km/h")
                print(f"  Characteristics: {sector.characteristics}")
        
        if result.drs_zones:
            print(f"\n{'='*70}")
            print(f"DRS ZONES ({len(result.drs_zones)} zones)")
            print(f"{'='*70}")
            for zone in result.drs_zones:
                print(f"\nDRS Zone {zone.zone_number}:")
                print(f"  Activation:      {zone.activation_distance_m}m")
                print(f"  Length:          {zone.length_m}m")
                print(f"  Speed Delta:     {zone.speed_delta_kmh} km/h")
                print(f"  Effectiveness:   {zone.effectiveness_score}")
        
        if result.track_evolution:
            print(f"\n{'='*70}")
            print(f"TRACK EVOLUTION ({len(result.track_evolution)} sessions)")
            print(f"{'='*70}")
            for evolution in result.track_evolution:
                print(f"\n{evolution.session_type}:")
                print(f"  Grip Level:           {evolution.avg_grip_level}")
                print(f"  Improvement/Lap:      {evolution.improvement_per_lap_ms}ms")
                print(f"  Total Improvement:    {evolution.total_improvement_ms}ms")
        
        print(f"\n{'='*70}")
        print("ADVANCED METRICS")
        print(f"{'='*70}")
        print(f"Top Speed:               {result.top_speed_kmh} km/h")
        print(f"Slowest Corner:          {result.slowest_corner_kmh} km/h")
        print(f"Avg Lap Speed:           {result.avg_lap_speed_kmh} km/h")
        if result.elevation_range_m:
            print(f"Elevation Range:         {result.elevation_range_m}m")
        print(f"Safety Car Probability:  {result.historical_safety_car_probability}")
        print(f"Weather Sensitivity:     {result.weather_sensitivity}")
        
        print(f"\n{'='*70}")        print("📦 FULL RESPONSE")
        print(f"{'='*70}")
        print(json.dumps(result.dict(), indent=2, default=str))
        
        print(f"\n{'='*70}")        print("✅ TEST PASSED")
        print(f"{'='*70}\n")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_track_engine())
    sys.exit(0 if success else 1)
