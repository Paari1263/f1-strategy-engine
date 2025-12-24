"""
Test script for aggregation calculations
Tests all 3 aggregation calculation modules

Run: python calculation_engines/aggregation/test_aggregation_calculations.py
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from calculation_engines.aggregation.driver_car_fusion_calc import driver_car_fusion_calc
from calculation_engines.aggregation.tyre_car_fusion_calc import tyre_car_fusion_calc
from calculation_engines.aggregation.race_context_builder import race_context_builder


def run_all_tests():
    print("=" * 60)
    print("AGGREGATION CALCULATIONS TEST SUITE")
    print("=" * 60)
    
    try:
        print("\n=== Testing Driver-Car Fusion ===")
        result = driver_car_fusion_calc.calculate(
            driver_rating=8.0,
            car_rating=7.5,
            synergy_factor=0.3
        )
        print(f"Driver-Car fusion: Combined performance = {result.combined_performance:.2f}/10")
        
        pace_est = driver_car_fusion_calc.estimate_race_pace(result.combined_performance, baseline_lap_time_s=90.0)
        print(f"  Estimated pace: {pace_est['estimated_lap_time_s']:.2f}s, Tier: {pace_est['performance_tier']}")
        print("✓ Driver-car fusion tests passed")
        
        print("\n=== Testing Tyre-Car Fusion ===")
        result = tyre_car_fusion_calc.calculate(
            tyre_compound="MEDIUM",
            car_downforce=7.0,
            car_weight_kg=758,
            track_temp_c=34
        )
        print(f"Tyre-Car fusion: Pace delta = {result.expected_pace_delta_s:.3f}s, Deg rate = {result.expected_degradation_rate:.3f}")
        
        recommendation = tyre_car_fusion_calc.recommend_optimal_compound(
            car_downforce=7.0,
            car_weight_kg=758,
            track_temp_c=34,
            target_stint_length=25
        )
        print(f"  Recommended: {recommendation['recommended_compound']}")
        print("✓ Tyre-car fusion tests passed")
        
        print("\n=== Testing Race Context Builder ===")
        result = race_context_builder.calculate(
            current_lap=35,
            total_laps=58,
            current_position=5,
            gap_ahead_s=2.8,
            gap_behind_s=3.5,
            tyre_age=20,
            tyre_compound="MEDIUM",
            weather_condition="DRY"
        )
        print(f"Race context: Phase = {result.race_phase}")
        
        summary = race_context_builder.generate_situation_summary(result)
        print(f"  Summary: {summary}")
        print("✓ Race context builder tests passed")
        
        print("\n" + "=" * 60)
        print("✓ ALL AGGREGATION CALCULATION TESTS PASSED")
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
