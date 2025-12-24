"""
Driver Engine Test Script
Tests driver performance analysis with FastF1 data
"""
import asyncio
import sysimport jsonfrom pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from engines.shared_services_fastf1 import DriverService
from engines.driver_engine.schemas import DriverRequest


async def test_driver_engine():
    """Test Driver Engine with Bahrain 2024 Race"""
    print("="*70)
    print("DRIVER ENGINE TEST - Bahrain 2024 Race")
    print("="*70)
    
    request = DriverRequest(
        year=2024,
        gp="Bahrain",
        session="R"
    )
    
    print(f"\n👤 Testing: {request.year} {request.gp} {request.session}")
    print("⏳ Loading driver performance data...")
    
    try:
        result = await DriverService.analyze_driver_performance(request)
        
        print(f"\n✅ SUCCESS - Driver Analysis Complete")
        print(f"\n{'='*70}")
        print("SESSION INFORMATION")
        print(f"{'='*70}")
        print(f"Circuit:              {result.circuit_name}")
        print(f"Session:              {result.session_type}")
        print(f"Drivers Analyzed:     {len(result.driver_profiles)}")
        if result.session_winner:
            print(f"Session Winner:       Driver #{result.session_winner}")
        if result.most_consistent_driver:
            print(f"Most Consistent:      Driver #{result.most_consistent_driver}")
        if result.best_racecraft_driver:
            print(f"Best Racecraft:       Driver #{result.best_racecraft_driver}")
        
        if result.driver_profiles:
            # Show top 5 drivers
            top_profiles = result.driver_profiles[:5]
            
            print(f"\n{'='*70}")
            print(f"TOP {len(top_profiles)} DRIVER PROFILES")
            print(f"{'='*70}")
            
            for idx, profile in enumerate(top_profiles, 1):
                print(f"\n{idx}. {profile.driver_name} (#{profile.driver_number}) - {profile.team}")
                print(f"   {'─'*66}")
                print(f"   Overall Rating:      {profile.overall_rating:.1f}/10")
                
                print(f"\n   CONSISTENCY:")
                print(f"     Valid Laps:        {profile.consistency.valid_laps}")
                print(f"     Lap Time Std Dev:  {profile.consistency.lap_time_std_dev_sec:.3f}s")
                print(f"     Mistakes:          {profile.consistency.mistakes_count}")
                print(f"     Consistency Score: {profile.consistency.consistency_score:.2f}")
                
                print(f"\n   RACECRAFT:")
                print(f"     Overtakes Made:    {profile.racecraft.overtakes_made}")
                print(f"     Overtakes Defended:{profile.racecraft.overtakes_defended}")
                print(f"     Positions Gained:  {profile.racecraft.positions_gained}")
                print(f"     Positions Lost:    {profile.racecraft.positions_lost}")
                print(f"     Battle Win Rate:   {profile.racecraft.battle_win_rate:.1%}")
                
                print(f"\n   TYRE MANAGEMENT:")
                print(f"     Avg Stint Length:  {profile.tyre_management.avg_stint_length_laps:.1f} laps")
                print(f"     Deg vs Teammate:   {profile.tyre_management.degradation_vs_teammate:+.3f}s/lap")
                print(f"     Temp Maintenance:  {profile.tyre_management.optimal_temp_maintenance_score:.2f}")
                if profile.tyre_management.compound_preference:
                    print(f"     Compound Pref:     {profile.tyre_management.compound_preference}")
                
                print(f"\n   SECTOR PERFORMANCE:")
                print(f"     Sector 1 Avg:      {profile.sector_performance.sector_1_avg_sec:.3f}s")
                print(f"     Sector 2 Avg:      {profile.sector_performance.sector_2_avg_sec:.3f}s")
                print(f"     Sector 3 Avg:      {profile.sector_performance.sector_3_avg_sec:.3f}s")
                print(f"     Best Sector:       {profile.sector_performance.best_sector}")
                print(f"     Worst Sector:      {profile.sector_performance.worst_sector}")
                
                if profile.historical_stats:
                    print(f"\n   HISTORICAL AT THIS CIRCUIT:")
                    print(f"     Races:             {profile.historical_stats.races_at_circuit}")
                    print(f"     Podiums:           {profile.historical_stats.podiums_at_circuit}")
                    print(f"     Avg Finish:        P{profile.historical_stats.avg_finish_position:.1f}")
                    print(f"     Best Finish:       P{profile.historical_stats.best_finish}")
                    print(f"     Avg Quali:         P{profile.historical_stats.avg_quali_position:.1f}")
        
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
    success = asyncio.run(test_driver_engine())
    sys.exit(0 if success else 1)
