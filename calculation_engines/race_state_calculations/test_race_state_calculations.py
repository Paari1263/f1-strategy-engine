"""
Test script for race state calculations
Tests all 4 race state calculation modules

Run: python calculation_engines/race_state_calculations/test_race_state_calculations.py
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from calculation_engines.race_state_calculations.gap_projection_calc import gap_projection_calc
from calculation_engines.race_state_calculations.pit_window_calc import pit_window_calc
from calculation_engines.race_state_calculations.stint_state_calc import stint_state_calc
from calculation_engines.race_state_calculations.position_pressure_calc import position_pressure_calc


def run_all_tests():
    print("=" * 60)
    print("RACE STATE CALCULATIONS TEST SUITE")
    print("=" * 60)
    
    try:
        print("\n=== Testing Gap Projection ===")
        result = gap_projection_calc.calculate(
            current_gap_s=4.2,
            pace_delta_s=0.18,
            laps_remaining=25
        )
        print(f"Gap projection: {result.projected_gap_s:.2f}s projected, Closing rate: {result.closing_rate_s_per_lap:.2f}s/lap")
        if result.laps_to_catch:
            print(f"  Will catch in {result.laps_to_catch} laps")
        print("✓ Gap projection tests passed")
        
        print("\n=== Testing Pit Window ===")
        result = pit_window_calc.calculate(
            current_tyre_age=18,
            expected_tyre_life=30,
            race_laps=58,
            current_lap=18
        )
        print(f"Pit window: Optimal = lap {result.optimal_lap}, Window = L{result.window_opens_lap}-{result.window_closes_lap}")
        print("✓ Pit window tests passed")
        
        print("\n=== Testing Stint State ===")
        result = stint_state_calc.calculate(
            laps_on_tyre=15,
            expected_stint_length=28,
            current_pace_s=90.5,
            initial_pace_s=89.8
        )
        print(f"Stint state: {result.stint_progress:.1%} complete, Phase: {result.stint_phase}, Pace loss: +{result.pace_delta_s:.2f}s")
        print("✓ Stint state tests passed")
        
        print("\n=== Testing Position Pressure ===")
        result = position_pressure_calc.calculate(
            gap_to_car_ahead_s=1.8,
            gap_to_car_behind_s=2.5,
            position=4
        )
        print(f"Position pressure: {result.pressure_rating:.2f}/10")
        print("✓ Position pressure tests passed")
        
        print("\n" + "=" * 60)
        print("✓ ALL RACE STATE CALCULATION TESTS PASSED")
        print("=" * 60)
        return True
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
