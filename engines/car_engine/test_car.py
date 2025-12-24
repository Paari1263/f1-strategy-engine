"""
Car Engine Test Script
Tests car performance analysis with FastF1 telemetry
"""
import asyncio
import sysimport jsonfrom pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from engines.car_engine.service import CarService
from engines.car_engine.schemas import CarRequest


async def test_car_engine():
    """Test Car Engine with Bahrain 2024 Race"""
    print("="*70)
    print("CAR ENGINE TEST - Bahrain 2024 Race")
    print("="*70)
    
    # Test data - analyze all cars
    request = CarRequest(
        year=2024,
        gp="Bahrain",
        session="R"
    )
    
    print(f"\n🏎️  Testing: {request.year} {request.gp} {request.session}")
    print("⏳ Loading session and telemetry data...")
    
    try:
        result = await CarService.analyze_car_performance(request)
        
        print(f"\n✅ SUCCESS - Car Analysis Complete")
        print(f"\n{'='*70}")
        print("SESSION INFORMATION")
        print(f"{'='*70}")
        print(f"Circuit:          {result.circuit_name}")
        print(f"Session:          {result.session_type}")
        print(f"Cars Analyzed:    {len(result.car_profiles)}")
        print(f"Fastest Car:      {result.fastest_car}")
        
        if result.car_profiles:
            # Show top 3 cars
            sorted_profiles = sorted(result.car_profiles, key=lambda x: x.lap_time_best_sec)[:3]
            
            print(f"\n{'='*70}")
            print("TOP 3 CARS - PERFORMANCE PROFILES")
            print(f"{'='*70}")
            
            for idx, profile in enumerate(sorted_profiles, 1):
                print(f"\n{idx}. {profile.driver_name} (#{profile.driver_number}) - {profile.team}")
                print(f"   {'─'*66}")
                
                print(f"   Best Lap Time:      {profile.lap_time_best_sec:.3f}s")
                print(f"   Avg Lap Time:       {profile.lap_time_avg_sec:.3f}s")
                print(f"   Consistency Score:  {profile.consistency_score:.2f}")
                
                print(f"\n   POWER UNIT:")
                print(f"     Avg RPM:          {profile.power_unit.avg_rpm:,.0f}")
                print(f"     Max RPM:          {profile.power_unit.max_rpm:,.0f}")
                print(f"     Avg Throttle:     {profile.power_unit.avg_throttle_pct:.1f}%")
                print(f"     Full Throttle:    {profile.power_unit.full_throttle_time_pct:.1f}%")
                print(f"     Gear Changes:     {profile.power_unit.gear_changes_per_lap}")
                print(f"     Top Speed:        {profile.power_unit.top_speed_kmh:.1f} km/h")
                
                print(f"\n   AERODYNAMICS:")
                print(f"     DRS Usage:        {profile.aerodynamics.drs_usage_pct:.1f}%")
                print(f"     DRS Speed Gain:   {profile.aerodynamics.drs_speed_gain_kmh:.1f} km/h")
                print(f"     Fast Corners:     {profile.aerodynamics.avg_speed_fast_corners_kmh:.1f} km/h")
                print(f"     Slow Corners:     {profile.aerodynamics.avg_speed_slow_corners_kmh:.1f} km/h")
                print(f"     Downforce:        {profile.aerodynamics.downforce_estimate}")
                
                print(f"\n   BRAKING:")
                print(f"     Avg Pressure:     {profile.braking.avg_brake_pressure:.1f}")
                print(f"     Max Pressure:     {profile.braking.max_brake_pressure:.1f}")
                print(f"     Braking Zones:    {profile.braking.braking_zones_per_lap}")
                print(f"     Efficiency:       {profile.braking.brake_efficiency_score:.2f}")
        
        print(f"\n{'='*70}")
        print("📦 FULL RESPONSE")
        print(f"{'='*70}")
        print(json.dumps(result.dict(), indent=2, default=str))
        
        print(f"\n{'='*70}")
        print("✅ TEST PASSED")
        print(f"{'='*70}\n")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_car_engine())
    sys.exit(0 if success else 1)
