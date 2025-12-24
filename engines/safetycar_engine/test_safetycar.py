"""
Safety Car Engine Test Script
Tests safety car analysis with FastF1 data
"""
import asyncio
import sysimport jsonfrom pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from engines.shared_services_fastf1 import SafetyCarService
from engines.safetycar_engine.schemas import SafetyCarRequest


async def test_safetycar_engine():
    """Test Safety Car Engine with Bahrain 2024 Race"""
    print("="*70)
    print("SAFETY CAR ENGINE TEST - Bahrain 2024 Race")
    print("="*70)
    
    request = SafetyCarRequest(
        year=2024,
        gp="Bahrain",
        session="R"
    )
    
    print(f"\n🚨 Testing: {request.year} {request.gp} {request.session}")
    print("⏳ Loading track status data...")
    
    try:
        result = await SafetyCarService.analyze_safety_car(request)
        
        print(f"\n✅ SUCCESS - Safety Car Analysis Complete")
        print(f"\n{'='*70}")
        print("SESSION INFORMATION")
        print(f"{'='*70}")
        print(f"Circuit:                  {result.circuit_name}")
        print(f"Session:                  {result.session_type}")
        print(f"Total SC Laps:            {result.total_sc_laps}")
        print(f"Total VSC Laps:           {result.total_vsc_laps}")
        print(f"Racing Laps:              {result.racing_laps_pct:.1f}%")
        print(f"Historical SC Prob:       {result.historical_sc_probability:.1%}")
        
        if result.track_status_timeline:
            print(f"\n{'='*70}")
            print(f"TRACK STATUS TIMELINE ({len(result.track_status_timeline)} periods)")
            print(f"{'='*70}")
            for period in result.track_status_timeline:
                print(f"\n{period.status}:")
                print(f"  Start Lap:           {period.start_lap}")
                print(f"  End Lap:             {period.end_lap if period.end_lap else 'Ongoing'}")
                print(f"  Duration:            {period.duration_laps} laps")
                if period.reason:
                    print(f"  Reason:              {period.reason}")
        
        if result.safety_car_deployments:
            print(f"\n{'='*70}")
            print(f"SAFETY CAR DEPLOYMENTS ({len(result.safety_car_deployments)})")
            print(f"{'='*70}")
            for deployment in result.safety_car_deployments:
                print(f"\n{deployment.deployment_type}:")
                print(f"  Start Lap:           {deployment.start_lap}")
                print(f"  End Lap:             {deployment.end_lap}")
                print(f"  Duration:            {deployment.duration_laps} laps")
                print(f"  Restart Lap:         {deployment.restart_lap}")
                print(f"  Field Compression:   {deployment.field_compression_sec:.1f}s")
                if deployment.trigger_reason:
                    print(f"  Trigger:             {deployment.trigger_reason}")
        
        if result.strategy_impacts:
            print(f"\n{'='*70}")
            print(f"STRATEGY IMPACTS ({len(result.strategy_impacts)} drivers)")
            print(f"{'='*70}")
            for impact in result.strategy_impacts[:10]:  # Show first 10
                print(f"\n{impact.driver_name} (#{impact.driver_number}):")
                print(f"  Position Change:     P{impact.position_before} → P{impact.position_after}")
                print(f"  Pitted under SC:     {'Yes' if impact.pitted_under_sc else 'No'}")
                if impact.time_advantage_sec:
                    print(f"  Time Advantage:      {impact.time_advantage_sec:+.1f}s")
                print(f"  Beneficiary:         {'Yes' if impact.strategy_beneficiary else 'No'}")
        
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
    success = asyncio.run(test_safetycar_engine())
    sys.exit(0 if success else 1)
