"""
Test script for car calculations
Tests all 5 car calculation modules

Run: python calculation_engines/car_calculations/test_car_calculations.py
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from calculation_engines.car_calculations.car_performance_index_calc import car_performance_index_calc
from calculation_engines.car_calculations.aero_vs_drag_balance_calc import aero_drag_balance_calc
from calculation_engines.car_calculations.fuel_effect_calc import fuel_effect_calc
from calculation_engines.car_calculations.reliability_risk_calc import reliability_risk_calc
from calculation_engines.car_calculations.tyre_interaction_calc import tyre_car_interaction_calc


def test_car_performance_index():
    print("\n=== Testing Car Performance Index ===")
    
    result = car_performance_index_calc.calculate(
        power=8.0,
        aero_efficiency=7.5,
        drag_coefficient=4.0,
        mechanical_grip=7.0
    )
    print(f"Performance Index: {result.index:.2f}/10")
    print(f"Components - Power: {result.power_contribution:.2f}, Aero: {result.aero_contribution:.2f}, Drag: {result.drag_contribution:.2f}, Grip: {result.grip_contribution:.2f}")
    assert 0 <= result.index <= 10
    
    print("✓ Car performance index tests passed")


def test_aero_drag_balance():
    print("\n=== Testing Aero/Drag Balance ===")
    
    # High downforce track
    result = aero_drag_balance_calc.calculate(
        downforce_level=8.5,
        drag_level=7.0,
        track_type='high_downforce'
    )
    print(f"High downforce track: Balance = {result.balance_score:.2f}/10, Efficiency = {result.efficiency_ratio:.2f}, Rec: {result.recommendation}")
    
    # Low downforce track
    result = aero_drag_balance_calc.calculate(
        downforce_level=4.0,
        drag_level=3.0,
        track_type='low_downforce'
    )
    print(f"Low downforce track: Balance = {result.balance_score:.2f}/10, Rec: {result.recommendation}")
    
    print("✓ Aero/drag balance tests passed")


def test_fuel_effect():
    print("\n=== Testing Fuel Effect ===")
    
    # Heavy fuel load
    result = fuel_effect_calc.calculate(fuel_load_kg=100.0)
    print(f"Heavy fuel (100kg): Penalty = {result.fuel_penalty_s:.2f}s")
    assert result.fuel_penalty_s > 2.0
    
    # Light fuel load
    result = fuel_effect_calc.calculate(fuel_load_kg=20.0)
    print(f"Light fuel (20kg): Penalty = {result.fuel_penalty_s:.2f}s")
    assert result.fuel_penalty_s < 1.0
    
    # Stint analysis
    stint_data = fuel_effect_calc.calculate_stint_fuel_effect(stint_length=25)
    print(f"Stint analysis: Avg penalty = {stint_data['average_penalty_s']:.2f}s, Fuel saving = {stint_data['total_fuel_effect_reduction_s']:.2f}s")
    
    print("✓ Fuel effect tests passed")


def test_reliability_risk():
    print("\n=== Testing Reliability Risk ===")
    
    # New component
    result = reliability_risk_calc.calculate(
        component_age_events=2,
        max_component_life=7,
        stress_level=0.5,
        base_failure_rate=0.05
    )
    print(f"New component: Risk = {result.failure_probability:.3f}, Level: {result.risk_level}")
    assert result.risk_level in ['low', 'medium']
    
    # Old component
    result = reliability_risk_calc.calculate(
        component_age_events=8,
        max_component_life=7,
        stress_level=0.8,
        base_failure_rate=0.05
    )
    print(f"Worn component (over limit): Risk = {result.failure_probability:.3f}, Level: {result.risk_level}")
    assert result.failure_probability > 0.1
    
    print("✓ Reliability risk tests passed")


def test_tyre_car_interaction():
    print("\n=== Testing Tyre-Car Interaction ===")
    
    result = tyre_car_interaction_calc.calculate(
        downforce_level=7.5,
        car_weight_kg=760,
        power_output=8.0
    )
    print(f"Interaction: Wear multiplier = {result.wear_multiplier:.2f}x, Thermal gen = {result.thermal_generation:.2f}, Temp delta = {result.temp_delta_c:.1f}°C")
    
    # Compound recommendation
    recommendation = tyre_car_interaction_calc.recommend_tyre_compound(
        downforce_level=7.5,
        car_weight_kg=760,
        power_output=8.0,
        track_temp_c=35
    )
    print(f"Recommended compound: {recommendation['recommendation']} - {recommendation['reason']}")
    
    print("✓ Tyre-car interaction tests passed")


def run_all_tests():
    print("=" * 60)
    print("CAR CALCULATIONS TEST SUITE")
    print("=" * 60)
    
    try:
        test_car_performance_index()
        test_aero_drag_balance()
        test_fuel_effect()
        test_reliability_risk()
        test_tyre_car_interaction()
        
        print("\n" + "=" * 60)
        print("✓ ALL CAR CALCULATION TESTS PASSED")
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
