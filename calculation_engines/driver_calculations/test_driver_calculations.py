"""
Test script for driver calculations
Tests all 5 driver calculation modules

Run: python calculation_engines/driver_calculations/test_driver_calculations.py
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from calculation_engines.driver_calculations.pace_delta_calc import driver_pace_calc
from calculation_engines.driver_calculations.consistency_calc import driver_consistency_calc
from calculation_engines.driver_calculations.driver_form_calc import driver_form_calc
from calculation_engines.driver_calculations.error_risk_calc import error_risk_calc
from calculation_engines.driver_calculations.racecraft_score_calc import racecraft_calc


def test_driver_pace():
    print("\n=== Testing Driver Pace Delta ===")
    
    # Elite driver
    result = driver_pace_calc.calculate(
        lap_times=[89.2, 89.1, 89.3, 89.0, 89.2],
        field_average=89.8
    )
    print(f"Elite driver: Pace delta = {result.pace_delta_s:.3f}s, Percentile = {result.percentile_rank:.1f}")
    assert result.pace_delta_s < 0  # Faster than average
    assert result.percentile_rank > 90
    
    # Average driver
    result = driver_pace_calc.calculate(
        lap_times=[90.0, 89.9, 90.1, 90.0],
        field_average=90.0
    )
    print(f"Average driver: Pace delta = {result.pace_delta_s:.3f}s, Percentile = {result.percentile_rank:.1f}")
    
    print("✓ Driver pace tests passed")


def test_driver_consistency():
    print("\n=== Testing Driver Consistency ===")
    
    # Consistent driver
    result = driver_consistency_calc.calculate(
        lap_times=[90.0, 90.1, 89.9, 90.0, 90.1, 89.9]
    )
    print(f"Consistent driver: Score = {result.consistency_score:.3f}, StdDev = {result.std_dev_s:.3f}s, CV = {result.coefficient_of_variation:.4f}")
    assert result.consistency_score > 0.5
    
    # Inconsistent driver
    result = driver_consistency_calc.calculate(
        lap_times=[89.0, 91.5, 88.5, 92.0, 89.5, 90.5]
    )
    print(f"Inconsistent driver: Score = {result.consistency_score:.3f}, StdDev = {result.std_dev_s:.3f}s")
    assert result.consistency_score < 0.6
    
    print("✓ Driver consistency tests passed")


def test_driver_form():
    print("\n=== Testing Driver Form ===")
    
    # Improving form
    result = driver_form_calc.calculate(recent_positions=[8, 7, 5, 4, 3])
    print(f"Improving: Trend = {result.form_trend}, Rating = {result.form_rating:.2f}/10")
    assert result.form_trend == "improving"
    
    # Declining form
    result = driver_form_calc.calculate(recent_positions=[3, 5, 7, 9, 10])
    print(f"Declining: Trend = {result.form_trend}, Rating = {result.form_rating:.2f}/10")
    assert result.form_trend == "declining"
    
    print("✓ Driver form tests passed")


def test_error_risk():
    print("\n=== Testing Error Risk ===")
    
    # Low pressure
    result = error_risk_calc.calculate(
        pressure_level=0.2,
        fatigue_factor=0.1,
        track_difficulty=0.3
    )
    print(f"Low pressure: Error prob = {result.error_probability_per_lap:.4f}, Risk = {result.risk_level}")
    assert result.risk_level in ['low', 'medium']
    
    # High pressure
    result = error_risk_calc.calculate(
        pressure_level=0.9,
        fatigue_factor=0.7,
        track_difficulty=0.8,
        driver_error_proneness=1.5
    )
    print(f"High pressure: Error prob = {result.error_probability_per_lap:.4f}, Risk = {result.risk_level}")
    assert result.error_probability_per_lap > 0.02
    
    print("✓ Error risk tests passed")


def test_racecraft():
    print("\n=== Testing Racecraft Score ===")
    
    # Strong racer
    result = racecraft_calc.calculate(
        overtaking_success_rate=0.75,
        defensive_success_rate=0.80,
        battles_fought=15,
        avg_time_lost_per_battle=0.3
    )
    print(f"Strong racer: Score = {result.racecraft_score:.2f}/10")
    print(f"  Overtaking: {result.overtaking_rating:.1f}, Defense: {result.defensive_rating:.1f}, Efficiency: {result.battle_efficiency:.1f}")
    assert result.racecraft_score > 6.0
    
    # Struggling racer
    result = racecraft_calc.calculate(
        overtaking_success_rate=0.3,
        defensive_success_rate=0.4,
        battles_fought=8,
        avg_time_lost_per_battle=0.9
    )
    print(f"Struggling racer: Score = {result.racecraft_score:.2f}/10")
    
    print("✓ Racecraft tests passed")


def run_all_tests():
    print("=" * 60)
    print("DRIVER CALCULATIONS TEST SUITE")
    print("=" * 60)
    
    try:
        test_driver_pace()
        test_driver_consistency()
        test_driver_form()
        test_error_risk()
        test_racecraft()
        
        print("\n" + "=" * 60)
        print("✓ ALL DRIVER CALCULATION TESTS PASSED")
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
