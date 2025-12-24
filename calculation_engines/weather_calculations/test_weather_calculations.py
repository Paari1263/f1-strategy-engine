"""
Test script for weather calculations
Tests all 4 weather calculation modules

Run: python calculation_engines/weather_calculations/test_weather_calculations.py
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from calculation_engines.weather_calculations.grip_evolution_calc import grip_evolution_calc
from calculation_engines.weather_calculations.cooling_margin_calc import cooling_margin_calc
from calculation_engines.weather_calculations.crossover_lap_calc import crossover_lap_calc
from calculation_engines.weather_calculations.weather_volatility_calc import weather_volatility_calc


def run_all_tests():
    print("=" * 60)
    print("WEATHER CALCULATIONS TEST SUITE")
    print("=" * 60)
    
    try:
        print("\n=== Testing Grip Evolution ===")
        result = grip_evolution_calc.calculate(laps_completed=20, total_laps=58, initial_grip=0.86)
        print(f"Grip evolution: {result.current_grip_level:.3f} grip level, {result.lap_time_delta_s:.3f}s delta")
        print("✓ Grip evolution tests passed")
        
        print("\n=== Testing Cooling Margin ===")
        result = cooling_margin_calc.calculate(ambient_temp_c=35, track_temp_c=52, cooling_spec=0.5)
        print(f"Cooling margin: {result.margin:.3f}, Status: {result.status}")
        print("✓ Cooling margin tests passed")
        
        print("\n=== Testing Crossover Lap ===")
        result = crossover_lap_calc.calculate(
            compound_a_initial_pace=89.3,
            compound_b_initial_pace=89.8,
            compound_a_deg_rate=0.09,
            compound_b_deg_rate=0.04
        )
        print(f"Crossover lap: {result.crossover_lap if result.crossover_lap else 'No crossover'}")
        print("✓ Crossover lap tests passed")
        
        print("\n=== Testing Weather Volatility ===")
        result = weather_volatility_calc.calculate(
            forecast_confidence=0.65,
            cloud_cover=0.6,
            wind_variability=0.4,
            historical_volatility=0.5
        )
        print(f"Weather volatility: {result.volatility_score:.3f}, Level: {result.volatility_level}")
        print("✓ Weather volatility tests passed")
        
        print("\n" + "=" * 60)
        print("✓ ALL WEATHER CALCULATION TESTS PASSED")
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
