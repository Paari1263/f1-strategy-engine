"""
Traffic Engine Test Script
Tests traffic analysis with FastF1 data
"""
import asyncio
import sysimport jsonfrom pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from engines.shared_services_fastf1 import TrafficService
from engines.traffic_engine.schemas import TrafficRequest


async def test_traffic_engine():
    """Test Traffic Engine with Bahrain 2024 Race"""
    print("="*70)
    print("TRAFFIC ENGINE TEST - Bahrain 2024 Race")
    print("="*70)
    
    request = TrafficRequest(
        year=2024,
        gp="Bahrain",
        session="R",
        focus_driver=1  # Max Verstappen
    )
    
    print(f"\n🚦 Testing: {request.year} {request.gp} {request.session}")
    if request.focus_driver:
        print(f"   Focus Driver: #{request.focus_driver}")
    print("⏳ Loading traffic data...")
    
    try:
        result = await TrafficService.analyze_traffic(request)
        
        print(f"\n✅ SUCCESS - Traffic Analysis Complete")
        print(f"\n{'='*70}")
        print("SESSION INFORMATION")
        print(f"{'='*70}")
        print(f"Circuit:                 {result.circuit_name}")
        print(f"Session:                 {result.session_type}")
        if result.focus_driver_number:
            print(f"Focus Driver:            #{result.focus_driver_number}")
        print(f"Overtaking Difficulty:   {result.overtaking_difficulty_score:.2f}")
        print(f"Avg Overtakes/Lap:       {result.avg_overtakes_per_lap:.2f}")
        
        if result.gap_evolution:
            print(f"\n{'='*70}")
            print(f"GAP EVOLUTION ({len(result.gap_evolution)} data points)")
            print(f"{'='*70}")
            for gap in result.gap_evolution[:5]:  # Show first 5 laps
                print(f"\nLap {gap.lap_number}:")
                print(f"  Leader:              Driver #{gap.leader_driver}")
                print(f"  Position:            P{gap.position}")
                print(f"  Gap to Leader:       {gap.gap_to_leader_sec:.3f}s")
                print(f"  Gap to Ahead:        {gap.gap_to_ahead_sec:.3f}s")
                print(f"  Gap to Behind:       {gap.gap_to_behind_sec:.3f}s")
        
        if result.overtake_events:
            print(f"\n{'='*70}")
            print(f"OVERTAKE EVENTS ({len(result.overtake_events)})")
            print(f"{'='*70}")
            for overtake in result.overtake_events:
                print(f"\nLap {overtake.lap_number} - {overtake.location}:")
                print(f"  Driver #{overtake.overtaking_driver} passed Driver #{overtake.overtaken_driver}")
                print(f"  DRS Enabled:         {'Yes' if overtake.drs_enabled else 'No'}")
                print(f"  Gap Before:          {overtake.gap_before_sec:.3f}s")
                print(f"  Gap After:           {overtake.gap_after_sec:.3f}s")
        
        if result.drs_trains:
            print(f"\n{'='*70}")
            print(f"DRS TRAINS ({len(result.drs_trains)})")
            print(f"{'='*70}")
            for train in result.drs_trains:
                print(f"\nLap {train.lap_number}:")
                print(f"  Leader:              Driver #{train.leader}")
                print(f"  Train Members:       {train.train_members}")
                print(f"  Train Length:        {train.train_length} cars")
                print(f"  Avg Gap:             {train.avg_gap_within_train_sec:.3f}s")
                print(f"  Duration:            {train.laps_in_formation} laps")
        
        if result.traffic_density:
            print(f"\n{'='*70}")
            print(f"TRAFFIC DENSITY ({len(result.traffic_density)} samples)")
            print(f"{'='*70}")
            for density in result.traffic_density[:3]:
                print(f"\nLap {density.lap_number}:")
                print(f"  Cars within 1s:      {density.cars_within_1sec}")
                print(f"  Cars within 3s:      {density.cars_within_3sec}")
                print(f"  Avg Gap to Ahead:    {density.avg_gap_to_car_ahead_sec:.3f}s")
                print(f"  Overtake Chances:    {density.overtaking_opportunities}")
        
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
    success = asyncio.run(test_traffic_engine())
    sys.exit(0 if success else 1)
