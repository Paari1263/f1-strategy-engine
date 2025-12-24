"""
Master test runner for all calculation modules
Run this to test everything at once
"""
import sys
from pathlib import Path

# Add strategy_engines to path
sys.path.insert(0, str(Path(__file__).parent))

# Import all test modules
from calculations.driver import test_driver_calculations
from calculations.car import test_car_calculations
from calculations.tyre import test_tyre_calculations
from calculations.track import test_track_calculations
from calculations.traffic import test_traffic_calculations
from calculations.weather import test_weather_calculations
from calculations.race_state import test_race_state_calculations
from utils import test_utils


def main():
    print("\n" + "=" * 70)
    print("🏎️  F1 STRATEGY ENGINE - COMPREHENSIVE CALCULATION TEST SUITE")
    print("=" * 70)
    
    test_modules = [
        ("Driver", test_driver_calculations),
        ("Car", test_car_calculations),
        ("Tyre", test_tyre_calculations),
        ("Track", test_track_calculations),
        ("Traffic", test_traffic_calculations),
        ("Weather", test_weather_calculations),
        ("Race State", test_race_state_calculations),
        ("Utils", test_utils),
    ]
    
    passed = 0
    failed = 0
    
    for name, module in test_modules:
        try:
            print(f"\n{'='*70}")
            print(f"Running {name} Tests...")
            print('='*70)
            module.run_all_tests()
            passed += 1
        except Exception as e:
            print(f"\n❌ {name} tests FAILED: {e}")
            failed += 1
    
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    print(f"✅ Passed: {passed}/{len(test_modules)} test suites")
    print(f"❌ Failed: {failed}/{len(test_modules)} test suites")
    
    if failed == 0:
        print("\n🎉 ALL CALCULATION TESTS PASSED!")
        print("=" * 70)
        return 0
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
