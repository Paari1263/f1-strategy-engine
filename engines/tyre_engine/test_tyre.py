"""
Tyre Engine Test Script
Tests tyre compound analysis with FastF1 data
"""
import asyncio
import sysimport jsonfrom pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from engines.shared_services_fastf1 import TyreService
from engines.tyre_engine.schemas import TyreRequest


async def test_tyre_engine():
    """Test Tyre Engine with Bahrain 2024 Race"""
    print("="*70)
    print("TYRE ENGINE TEST - Bahrain 2024 Race")
    print("="*70)
    
    request = TyreRequest(
        year=2024,
        gp="Bahrain",
        session="R"
    )
    
    print(f"\n🛞 Testing: {request.year} {request.gp} {request.session}")
    print("⏳ Loading tyre stint data...")
    
    try:
        result = await TyreService.analyze_tyre_performance(request)
        
        print(f"\n✅ SUCCESS - Tyre Analysis Complete")
        print(f"\n{'='*70}")
        print("SESSION INFORMATION")
        print(f"{'='*70}")
        print(f"Circuit:              {result.circuit_name}")
        print(f"Session:              {result.session_type}")
        print(f"Track Tyre Severity:  {result.track_tyre_severity:.2f}")
        
        if result.compound_characteristics:
            print(f"\n{'='*70}")
            print(f"COMPOUND CHARACTERISTICS ({len(result.compound_characteristics)} compounds)")
            print(f"{'='*70}")
            for compound in result.compound_characteristics:
                print(f"\n{compound.compound}:")
                print(f"  Avg Lifetime:        {compound.avg_lifetime_laps:.1f} laps")
                print(f"  Degradation Rate:    {compound.degradation_rate_sec_per_lap:.3f}s/lap")
                print(f"  Optimal Temp:        {compound.optimal_temp_range_c}")
                print(f"  Performance Window:  {compound.performance_window_laps} laps")
                if compound.cliff_lap:
                    print(f"  Cliff Lap:           ~{compound.cliff_lap}")
        
        if result.stint_analyses:
            print(f"\n{'='*70}")
            print(f"STINT ANALYSES ({len(result.stint_analyses)} stints)")
            print(f"{'='*70}")
            for stint in result.stint_analyses[:5]:  # Show first 5
                print(f"\n{stint.driver_name} - Stint {stint.stint_number} ({stint.compound}):")
                print(f"  Laps:                {stint.lap_start} → {stint.lap_end} ({stint.total_laps} laps)")
                print(f"  Tyre Age at Start:   {stint.tyre_age_at_start} laps")
                print(f"  Avg Lap Time:        {stint.avg_lap_time_sec:.3f}s")
                print(f"  Degradation:         {stint.degradation_observed_sec_per_lap:.3f}s/lap")
                print(f"  Grip Level:          {stint.grip_level_start:.2f} → {stint.grip_level_end:.2f}")
                print(f"  Thermal State:       {stint.thermal_state}")
        
        if result.strategy_recommendation:
            print(f"\n{'='*70}")
            print("STRATEGY RECOMMENDATION")
            print(f"{'='*70}")
            print(f"Optimal Order:    {' → '.join(result.strategy_recommendation.optimal_compound_order)}")
            print(f"Pit Windows:      {result.strategy_recommendation.estimated_pit_windows}")
            print(f"Risk Assessment:  {result.strategy_recommendation.risk_assessment}")
        
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
    success = asyncio.run(test_tyre_engine())
    sys.exit(0 if success else 1)
