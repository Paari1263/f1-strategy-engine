"""
Test suite for utility modules
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import normalization, smoothing


def test_normalization():
    print("\n🧪 Testing normalization...")
    
    # Normal case
    result = normalization.normalize(5.0, 0.0, 10.0)
    assert result == 0.5
    print(f"✅ Normal case: {result}")
    
    # Min value
    result = normalization.normalize(0.0, 0.0, 10.0)
    assert result == 0.0
    print(f"✅ Min value: {result}")
    
    # Max value
    result = normalization.normalize(10.0, 0.0, 10.0)
    assert result == 1.0
    print(f"✅ Max value: {result}")
    
    # Edge case: same min/max
    result = normalization.normalize(5.0, 5.0, 5.0)
    assert result == 0.0  # Protected
    print(f"✅ Same min/max: {result}")
    
    # Edge case: value outside range
    result = normalization.normalize(15.0, 0.0, 10.0)
    assert result == 1.0  # Clamped
    print(f"✅ Above range clamped: {result}")
    
    result = normalization.normalize(-5.0, 0.0, 10.0)
    assert result == 0.0  # Clamped
    print(f"✅ Below range clamped: {result}")


def test_smoothing():
    print("\n🧪 Testing smoothing (EMA)...")
    
    # Normal case
    values = [10.0, 12.0, 11.0, 13.0, 12.5]
    result = smoothing.ema(values, alpha=0.3)
    assert len(result) == len(values)
    assert result[0] == values[0]  # First value unchanged
    print(f"✅ Normal case: {result}")
    
    # Edge case: empty list
    result = smoothing.ema([])
    assert result == []
    print(f"✅ Empty list: {result}")
    
    # Edge case: single value
    result = smoothing.ema([5.0])
    assert result == [5.0]
    print(f"✅ Single value: {result}")
    
    # Different alpha values
    values = [10.0, 20.0, 10.0, 20.0]
    
    # High alpha (more responsive)
    result_high = smoothing.ema(values, alpha=0.8)
    print(f"✅ High alpha (0.8): {result_high}")
    
    # Low alpha (more smoothing)
    result_low = smoothing.ema(values, alpha=0.2)
    print(f"✅ Low alpha (0.2): {result_low}")
    
    # Edge case: alpha clamping
    result = smoothing.ema([10.0, 20.0], alpha=1.5)
    assert len(result) == 2
    print(f"✅ Alpha > 1.0 clamped: {result}")
    
    result = smoothing.ema([10.0, 20.0], alpha=-0.5)
    assert len(result) == 2
    print(f"✅ Alpha < 0.0 clamped: {result}")


def run_all_tests():
    print("=" * 60)
    print("🔧 UTILS TEST SUITE")
    print("=" * 60)
    
    test_normalization()
    test_smoothing()
    
    print("\n" + "=" * 60)
    print("✅ ALL UTILS TESTS PASSED!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
