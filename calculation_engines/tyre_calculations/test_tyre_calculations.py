"""
Test script for tyre calculations
Tests all 5 tyre calculation modules

Run: python calculation_engines/tyre_calculations/test_tyre_calculations.py
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from calculation_engines.tyre_calculations.compound_delta_calc import compound_delta_calc
from calculation_engines.tyre_calculations.thermal_window_calc import thermal_window_calc
from calculation_engines.tyre_calculations.push_penalty_calc import push_penalty_calc
from calculation_engines.tyre_calculations.degradation_curve_calc import degradation_curve_calc
from calculation_engines.tyre_calculations.tyre_life_projection_calc import tyre_life_projection_calc


def test_compound_delta():
    print("\n=== Testing Compound Delta Calculation ===")
    
    # Test SOFT compound
    result = compound_delta_calc.calculate(compound="SOFT")
    print(f"SOFT: {result.lap_time_delta_s}s vs MEDIUM")
    assert result.compound_name == "SOFT"
    assert result.lap_time_delta_s == -0.4
    
    # Test HARD compound
    result = compound_delta_calc.calculate(compound="HARD")
    print(f"HARD: {result.lap_time_delta_s}s vs MEDIUM")
    assert result.lap_time_delta_s == 0.3
    
    # Test relative delta
    delta = compound_delta_calc.calculate_relative_delta("SOFT", "HARD")
    print(f"SOFT vs HARD: {delta}s")
    assert delta == -0.7
    
    print("✓ Compound delta tests passed")


def test_thermal_window():
    print("\n=== Testing Thermal Window Calculation ===")
    
    # Test optimal temperature
    result = thermal_window_calc.calculate(track_temp_c=92, compound="MEDIUM")
    print(f"Optimal temp (92°C): Penalty = {result.temp_penalty_s_per_lap}s, In window: {result.is_in_window}")
    assert result.is_in_window == True
    assert result.temp_penalty_s_per_lap == 0.0
    
    # Test too hot
    result = thermal_window_calc.calculate(track_temp_c=110, compound="MEDIUM")
    print(f"Too hot (110°C): Penalty = {result.temp_penalty_s_per_lap}s")
    assert result.is_in_window == False
    assert result.temp_penalty_s_per_lap > 0
    
    print("✓ Thermal window tests passed")


def test_push_penalty():
    print("\n=== Testing Push Penalty Calculation ===")
    
    # Test no push
    result = push_penalty_calc.calculate(push_level=0.0)
    print(f"No push: Multiplier = {result.push_multiplier}x")
    assert result.push_multiplier == 1.0
    
    # Test maximum push
    result = push_penalty_calc.calculate(push_level=1.0, base_stint_length=20)
    print(f"Max push: Multiplier = {result.push_multiplier}x, Life reduction = {result.estimated_life_reduction_laps} laps")
    assert result.push_multiplier == 1.5
    assert result.estimated_life_reduction_laps > 0
    
    print("✓ Push penalty tests passed")


def test_degradation_curve():
    print("\n=== Testing Degradation Curve Calculation ===")
    
    # Test fresh tyres
    result = degradation_curve_calc.calculate(
        wear_level=0.1,
        temp_factor=1.0,
        track_abrasion=0.5,
        push_multiplier=1.0
    )
    print(f"Fresh tyres: Deg rate = {result.degradation_rate_s_per_lap:.3f}s/lap")
    
    # Test worn tyres
    result = degradation_curve_calc.calculate(
        wear_level=0.8,
        temp_factor=1.2,
        track_abrasion=0.8,
        push_multiplier=1.3
    )
    print(f"Worn tyres: Deg rate = {result.degradation_rate_s_per_lap:.3f}s/lap, Multiplier = {result.wear_multiplier:.2f}x")
    assert result.degradation_rate_s_per_lap > 0.05
    
    print("✓ Degradation curve tests passed")


def test_tyre_life_projection():
    print("\n=== Testing Tyre Life Projection Calculation ===")
    
    # Test early stint
    result = tyre_life_projection_calc.calculate(
        total_expected_life=25,
        laps_completed=10,
        current_degradation_rate=0.05
    )
    print(f"Remaining life: {result.remaining_laps} laps, Cliff at lap: {result.cliff_lap_estimate}, Confidence: {result.confidence:.2f}")
    assert result.remaining_laps == 15
    assert result.cliff_lap_estimate is not None
    
    # Test near end of life
    result = tyre_life_projection_calc.calculate(
        total_expected_life=25,
        laps_completed=23,
        current_degradation_rate=0.15
    )
    print(f"Near end: {result.remaining_laps} laps remaining")
    
    print("✓ Tyre life projection tests passed")


def run_all_tests():
    print("=" * 60)
    print("TYRE CALCULATIONS TEST SUITE")
    print("=" * 60)
    
    try:
        test_compound_delta()
        test_thermal_window()
        test_push_penalty()
        test_degradation_curve()
        test_tyre_life_projection()
        
        print("\n" + "=" * 60)
        print("✓ ALL TYRE CALCULATION TESTS PASSED")
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
