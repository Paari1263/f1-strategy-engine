"""
Test script for traffic calculations
Tests all 4 traffic calculation modules

Run: python calculation_engines/traffic_calculations/test_traffic_calculations.py
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from calculation_engines.traffic_calculations.traffic_density_calc import traffic_density_calc
from calculation_engines.traffic_calculations.defense_effectiveness_calc import defense_effectiveness_calc
from calculation_engines.traffic_calculations.overtake_cost_calc import overtake_cost_calc
from calculation_engines.traffic_calculations.train_probability_calc import drs_train_probability_calc


def run_all_tests():
    print("=" * 60)
    print("TRAFFIC CALCULATIONS TEST SUITE")
    print("=" * 60)
    
    try:
        print("\n=== Testing Traffic Density ===")
        result = traffic_density_calc.calculate(cars_on_track=20, track_length_km=5.4, avg_gap_s=1.2)
        print(f"Density: {result.density_cars_per_km:.2f} cars/km, Level: {result.density_level}")
        print("✓ Traffic density tests passed")
        
        print("\n=== Testing Defense Effectiveness ===")
        result = defense_effectiveness_calc.calculate(
            overtaking_difficulty=7.0,
            car_straight_speed=8.0,
            driver_defensive_skill=7.5
        )
        print(f"Defense effectiveness: {result.effectiveness_rating:.2f}/10")
        print("✓ Defense effectiveness tests passed")
        
        print("\n=== Testing Overtake Cost ===")
        result = overtake_cost_calc.calculate(
            laps_in_battle=4,
            dirty_air_penalty_s=0.35,
            push_degradation_multiplier=1.3
        )
        print(f"Overtake cost: {result.time_cost_s:.2f}s time, {result.tyre_life_cost_laps:.2f} laps life")
        print("✓ Overtake cost tests passed")
        
        print("\n=== Testing DRS Train Probability ===")
        result = drs_train_probability_calc.calculate(
            cars_within_1s=4,
            field_spread_s=7.5,
            overtaking_difficulty=6.5
        )
        print(f"Train probability: {result.train_probability:.2%}")
        print("✓ DRS train probability tests passed")
        
        print("\n" + "=" * 60)
        print("✓ ALL TRAFFIC CALCULATION TESTS PASSED")
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
