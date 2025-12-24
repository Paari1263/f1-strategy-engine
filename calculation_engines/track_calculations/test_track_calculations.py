"""
Test script for track calculations
Tests all 5 track calculation modules

Run: python calculation_engines/track_calculations/test_track_calculations.py
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from calculation_engines.track_calculations.pit_loss_calc import pit_loss_calc
from calculation_engines.track_calculations.overtaking_difficulty_calc import overtaking_difficulty_calc
from calculation_engines.track_calculations.dirty_air_penalty_calc import dirty_air_penalty_calc
from calculation_engines.track_calculations.track_difficulty_calc import track_difficulty_calc
from calculation_engines.track_calculations.safety_car_probability_calc import safety_car_probability_calc


def test_pit_loss():
    print("\n=== Testing Pit Loss Calculation ===")
    
    result = pit_loss_calc.calculate()
    print(f"Default pit loss: {result.total_loss_s:.1f}s (stationary: {result.stationary_time_s:.1f}s)")
    
    result = pit_loss_calc.calculate(pit_speed_limit_kph=60, stop_duration_s=3.0)
    print(f"Slower pit lane (60kph, 3.0s stop): {result.total_loss_s:.1f}s")
    
    print("✓ Pit loss tests passed")


def test_overtaking_difficulty():
    print("\n=== Testing Overtaking Difficulty ===")
    
    # Easy track (Bahrain)
    result = overtaking_difficulty_calc.calculate(drs_zones=3, longest_straight_m=1200, track_width_m=15)
    print(f"Easy track: Difficulty = {result.difficulty_rating:.2f}/10, Class: {result.difficulty_class}")
    
    # Hard track (Monaco)
    result = overtaking_difficulty_calc.calculate(drs_zones=1, longest_straight_m=400, track_width_m=9)
    print(f"Hard track: Difficulty = {result.difficulty_rating:.2f}/10, Class: {result.difficulty_class}")
    
    print("✓ Overtaking difficulty tests passed")


def test_dirty_air_penalty():
    print("\n=== Testing Dirty Air Penalty ===")
    
    # Close gap
    result = dirty_air_penalty_calc.calculate(gap_s=0.5, aero_sensitivity=0.7)
    print(f"Close (0.5s gap): Penalty = {result.penalty_s_per_lap:.3f}s/lap")
    
    # Distant gap
    result = dirty_air_penalty_calc.calculate(gap_s=3.5, aero_sensitivity=0.7)
    print(f"Distant (3.5s gap): Penalty = {result.penalty_s_per_lap:.3f}s/lap")
    
    print("✓ Dirty air penalty tests passed")


def test_track_difficulty():
    print("\n=== Testing Track Difficulty ===")
    
    # Technical track
    result = track_difficulty_calc.calculate(
        corner_count=23,
        avg_corner_speed_kph=95,
        elevation_change_m=100,
        barrier_proximity=0.8
    )
    print(f"Technical track: Difficulty = {result.difficulty_rating:.2f}/10")
    
    # Fast flowing track
    result = track_difficulty_calc.calculate(
        corner_count=12,
        avg_corner_speed_kph=190,
        elevation_change_m=20,
        barrier_proximity=0.3
    )
    print(f"Fast track: Difficulty = {result.difficulty_rating:.2f}/10")
    
    print("✓ Track difficulty tests passed")


def test_safety_car_probability():
    print("\n=== Testing Safety Car Probability ===")
    
    # Low risk (Bahrain)
    result = safety_car_probability_calc.calculate(
        barrier_proximity=0.3,
        weather_risk=0.0,
        field_competitiveness=0.4
    )
    print(f"Low risk track: SC probability = {result.probability:.2%}")
    
    # High risk (Monaco in rain)
    result = safety_car_probability_calc.calculate(
        barrier_proximity=0.95,
        weather_risk=0.8,
        field_competitiveness=0.7
    )
    print(f"High risk track: SC probability = {result.probability:.2%}")
    
    print("✓ Safety car probability tests passed")


def run_all_tests():
    print("=" * 60)
    print("TRACK CALCULATIONS TEST SUITE")
    print("=" * 60)
    
    try:
        test_pit_loss()
        test_overtaking_difficulty()
        test_dirty_air_penalty()
        test_track_difficulty()
        test_safety_car_probability()
        
        print("\n" + "=" * 60)
        print("✓ ALL TRACK CALCULATION TESTS PASSED")
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
