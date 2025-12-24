"""
Pit Engine Test Script
Tests pit stop analysis with FastF1 data
"""
import asyncio
import sysimport jsonfrom pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from engines.shared_services_fastf1 import PitService
from engines.pit_engine.schemas import PitRequest


async def test_pit_engine():
    """Test Pit Engine with Bahrain 2024 Race"""
    print("="*70)
    print("PIT ENGINE TEST - Bahrain 2024 Race")
    print("="*70)
    
    request = PitRequest(
        year=2024,
        gp="Bahrain",
        session="R"
    )
    
    print(f"\n🔧 Testing: {request.year} {request.gp} {request.session}")
    print("⏳ Loading pit stop data...")
    
    try:
        result = await PitService.analyze_pit_stops(request)
        
        print(f"\n✅ SUCCESS - Pit Stop Analysis Complete")
        print(f"\n{'='*70}")
        print("SESSION INFORMATION")
        print(f"{'='*70}")
        print(f"Circuit:              {result.circuit_name}")
        print(f"Session:              {result.session_type}")
        print(f"Total Pit Stops:      {len(result.pit_stops)}")
        print(f"Avg Pit Lane Loss:    {result.avg_pit_lane_time_loss_sec:.1f}s")
        print(f"Pit Windows:          {result.pit_window_recommendations}")
        
        if result.pit_stops:
            print(f"\n{'='*70}")
            print(f"PIT STOP DETAILS ({len(result.pit_stops)} stops)")
            print(f"{'='*70}")
            for stop in result.pit_stops[:10]:  # Show first 10
                print(f"\nLap {stop.lap_number} - {stop.driver_name} ({stop.team}):")
                print(f"  Pit Duration:        {stop.pit_duration_sec:.3f}s")
                print(f"  Tyre Change Time:    {stop.tyre_change_time_sec:.3f}s")
                print(f"  In Lap:              {stop.in_lap_time_sec:.3f}s")
                print(f"  Out Lap:             {stop.out_lap_time_sec:.3f}s")
                print(f"  Positions Lost:      {stop.positions_lost}")
                print(f"  Positions Gained:    {stop.positions_gained}")
                print(f"  Compound Fitted:     {stop.compound_fitted}")
        
        if result.team_performance:
            print(f"\n{'='*70}")
            print(f"TEAM PERFORMANCE ({len(result.team_performance)} teams)")
            print(f"{'='*70}")
            for team in result.team_performance:
                print(f"\n{team.team}:")
                print(f"  Total Stops:         {team.total_stops}")
                print(f"  Avg Duration:        {team.avg_pit_duration_sec:.3f}s")
                print(f"  Fastest Stop:        {team.fastest_stop_sec:.3f}s")
                print(f"  Slowest Stop:        {team.slowest_stop_sec:.3f}s")
                print(f"  Consistency:         {team.consistency_score:.2f}")
        
        if result.strategy_analyses:
            print(f"\n{'='*70}")
            print(f"STRATEGY ANALYSES ({len(result.strategy_analyses)} drivers)")
            print(f"{'='*70}")
            for strategy in result.strategy_analyses[:5]:  # Show first 5
                print(f"\nDriver #{strategy.driver_number}:")
                print(f"  Strategy Type:       {strategy.strategy_type}")
                print(f"  Total Stops:         {strategy.total_stops}")
                print(f"  Stop Laps:           {strategy.stop_laps}")
                print(f"  Time Lost:           {strategy.total_time_lost_sec:.1f}s")
                print(f"  Undercuts:           {strategy.undercut_attempts}")
                print(f"  Overccuts:           {strategy.overcut_attempts}")
                print(f"  Effective:           {'Yes' if strategy.effective_strategy else 'No'}")
        
        if result.fastest_stop_overall:
            print(f"\n{'='*70}")
            print("FASTEST STOP")
            print(f"{'='*70}")
            print(f"Driver:              {result.fastest_stop_overall.driver_name}")
            print(f"Team:                {result.fastest_stop_overall.team}")
            print(f"Lap:                 {result.fastest_stop_overall.lap_number}")
            print(f"Duration:            {result.fastest_stop_overall.pit_duration_sec:.3f}s")
        
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
    success = asyncio.run(test_pit_engine())
    sys.exit(0 if success else 1)
