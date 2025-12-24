"""
Weather Engine Test Script
Tests weather analysis with FastF1 data
"""
import asyncio
import sysimport jsonfrom pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from engines.shared_services_fastf1 import WeatherService
from engines.weather_engine.schemas import WeatherRequest


async def test_weather_engine():
    """Test Weather Engine with Bahrain 2024 Race"""
    print("="*70)
    print("WEATHER ENGINE TEST - Bahrain 2024 Race")
    print("="*70)
    
    request = WeatherRequest(
        year=2024,
        gp="Bahrain",
        session="R"
    )
    
    print(f"\n🌤️  Testing: {request.year} {request.gp} {request.session}")
    print("⏳ Loading weather data...")
    
    try:
        result = await WeatherService.analyze_weather(request)
        
        print(f"\n✅ SUCCESS - Weather Analysis Complete")
        print(f"\n{'='*70}")
        print("SESSION INFORMATION")
        print(f"{'='*70}")
        print(f"Circuit:                 {result.circuit_name}")
        print(f"Session:                 {result.session_type}")
        print(f"Start Time:              {result.session_start_time}")
        print(f"End Time:                {result.session_end_time}")
        print(f"Conditions:              {result.conditions_summary}")
        print(f"Track Evolution:         {'Favorable' if result.track_evolution_favorable else 'Unfavorable'}")
        
        if result.lap_snapshots:
            print(f"\n{'='*70}")
            print(f"WEATHER SNAPSHOTS ({len(result.lap_snapshots)} samples)")
            print(f"{'='*70}")
            for snapshot in result.lap_snapshots[:5]:  # Show first 5
                print(f"\nLap {snapshot.lap_number}:")
                print(f"  Air Temperature:     {snapshot.air_temp_c}°C")
                print(f"  Track Temperature:   {snapshot.track_temp_c}°C")
                print(f"  Humidity:            {snapshot.humidity_pct}%")
                print(f"  Pressure:            {snapshot.pressure_mbar} mbar")
                print(f"  Rainfall:            {'Yes' if snapshot.rainfall else 'No'}")
                print(f"  Wind Speed:          {snapshot.wind_speed_ms} m/s")
                print(f"  Wind Direction:      {snapshot.wind_direction_deg}°")
        
        if result.weather_trends:
            print(f"\n{'='*70}")
            print(f"WEATHER TRENDS ({len(result.weather_trends)} parameters)")
            print(f"{'='*70}")
            for trend in result.weather_trends:
                print(f"\n{trend.parameter}:")
                print(f"  Start:          {trend.start_value}")
                print(f"  End:            {trend.end_value}")
                print(f"  Change Rate:    {trend.change_rate_per_lap}/lap")
                print(f"  Trend:          {trend.trend}")
        
        print(f"\n{'='*70}")
        print("PERFORMANCE IMPACT")
        print(f"{'='*70}")
        print(f"Lap Time Impact:         {result.impact_analysis.lap_time_impact_sec:+.3f}s")
        print(f"Tyre Deg Multiplier:     {result.impact_analysis.tyre_deg_multiplier:.2f}x")
        print(f"Grip Multiplier:         {result.impact_analysis.grip_level_multiplier:.2f}x")
        print(f"Rainfall Prob (10 laps): {result.impact_analysis.rainfall_probability_next_10_laps:.1%}")
        
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
    success = asyncio.run(test_weather_engine())
    sys.exit(0 if success else 1)
