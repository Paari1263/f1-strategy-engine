# Comparison Engine

## 🔍 Overview

The **Comparison Engine** provides a unified, high-level interface for comparing F1 cars and drivers. It orchestrates multiple analyzers and calculations to deliver comprehensive performance comparisons.

---

## 📁 Structure

```
comparison_engine/
├── __init__.py
└── comparison_engine.py      # Main engine class
```

---

## 🎯 Purpose

The Comparison Engine serves as the **primary interface** for:

1. **Car vs Car Comparison** - Performance, setup, characteristics
2. **Driver vs Driver Comparison** - Pace, consistency, racecraft
3. **Detailed Analysis** - Multi-dimensional performance profiles

It abstracts away the complexity of:
- Data loading from FastF1
- Telemetry processing
- Running multiple analyzers
- Aggregating results
- Formatting output

---

## 🏗️ Architecture

```
ComparisonEngine
     │
     ├─> FastF1DataLoader (data access)
     │     └─> Loads session, lap, telemetry data
     │
     ├─> TelemetryProcessor (preprocessing)
     │     └─> Cleans and prepares telemetry
     │
     ├─> Analysis Engines
     │     ├─> SpeedAnalyzer
     │     ├─> BrakingAnalyzer
     │     ├─> CornerAnalyzer
     │     ├─> StraightLineAnalyzer
     │     ├─> PaceAnalyzer
     │     └─> ConsistencyAnalyzer
     │
     └─> Calculation Engines
           ├─> PowerDeltaCalc
           ├─> DragPenaltyCalc
           ├─> MechanicalGripDeltaCalc
           └─> (26 more calculations...)
```

---

## 🚀 Quick Start

### Initialize Engine

```python
from comparison_engine import ComparisonEngine

# Create engine with default cache
engine = ComparisonEngine()

# Or specify custom cache directory
engine = ComparisonEngine(cache_dir='./my_cache')
```

### Compare Cars

```python
result = engine.compare_cars(
    year=2024,
    gp='Monaco',
    session_type='Q',
    driver1='VER',
    driver2='LEC'
)

print(f"Winner: {result['winner']}")
print(f"Delta: {result['delta_seconds']:.3f}s")
print(f"Power advantage: {result['power_delta_percent']:.1f}%")
```

### Compare Drivers

```python
result = engine.compare_drivers(
    year=2024,
    gp='Monaco',
    session_type='Q',
    driver1='VER',
    driver2='HAM'
)

print(f"Consistency: VER {result['driver1']['consistency_score']}")
print(f"Consistency: HAM {result['driver2']['consistency_score']}")
print(f"Racecraft winner: {result['racecraft_winner']}")
```

---

## 📊 Comparison Types

### 1. Standard Car Comparison

**Method:** `compare_cars(year, gp, session_type, driver1, driver2)`

**Returns:**
```python
{
    'driver1': 'VER',
    'driver2': 'LEC',
    'fastest_lap1': '1:12.345',
    'fastest_lap2': '1:12.567',
    'delta_seconds': -0.222,
    'winner': 'VER',
    
    # Performance metrics
    'power_delta_percent': 1.5,
    'drag_penalty_percent': -2.3,
    'mechanical_grip_delta_percent': 0.8,
    
    # Speed analysis
    'max_speed_delta_kmh': 5.2,
    'avg_speed_delta_kmh': 2.1,
    
    # Sector breakdown
    'sector1_delta': -0.082,
    'sector2_delta': -0.055,
    'sector3_delta': -0.085,
    
    # Metadata
    'metadata': {
        'year': 2024,
        'event': 'Monaco',
        'session': 'Q',
        'timestamp': '2024-05-25T14:30:00Z'
    }
}
```

**Use Cases:**
- Quick performance comparison
- Identify car strengths/weaknesses
- Setup optimization
- Qualifying analysis

---

### 2. Detailed Car Comparison

**Method:** `compare_cars_detailed(year, gp, session_type, driver1, driver2)`

**Returns Structured Profiles:**
```python
{
    'car1': {
        'metadata': {
            'team': 'Red Bull Racing',
            'car': 'RB20',
            'driver': 'VER',
            'session_key': 9472
        },
        'performance_profile': {
            'powerDelta': 1.5,
            'aeroDelta': -0.8,
            'dragPenalty': -2.3,
            'mechanicalGripDelta': 0.8
        },
        'tyre_interaction': {
            'tyreEnergyLoad': {
                'soft': 85,
                'medium': 78,
                'hard': 72
            },
            'fuelWeightSensitivity': 0.035
        },
        'aero_behavior': {
            'downforceSensitivity': 7.2,
            'dirtyAirAmplification': 1.25
        },
        'thermal_profile': {
            'coolingSensitivity': {
                'engine': 0.8,
                'brakes': 0.9
            }
        },
        'ers_profile': {
            'ersEfficiency': 92
        },
        'reliability_profile': {
            'reliabilityStress': 65,
            'pushFailureRisk': 0.08
        },
        'setup_profile': {
            'kerbCompliance': 75,
            'setupFlexibility': 8
        },
        'session_bias': {
            'qualifyingBias': 0.6,
            'raceBias': 0.4
        }
    },
    'car2': { /* same structure */ },
    
    'delta_analysis': {
        'powerDelta': 0.3,
        'aeroDelta': -0.5,
        'mechanicalGripDelta': 0.2,
        /* ... more deltas ... */
    },
    
    'overall_advantage': 'VER'
}
```

**Use Cases:**
- Comprehensive car analysis
- Development direction
- Setup window understanding
- Detailed technical reports

---

### 3. Driver Comparison

**Method:** `compare_drivers(year, gp, session_type, driver1, driver2)`

**Returns:**
```python
{
    'driver1': {
        'name': 'VER',
        'fastest_lap': '1:12.345',
        'avg_lap_time': '1:13.567',
        'consistency_score': 99.2,
        'error_risk_percent': 3.5,
        'racecraft_score': 88,
        'pressure_index': 95,
        'pace_trend': 'stable'
    },
    'driver2': {
        'name': 'HAM',
        'fastest_lap': '1:12.456',
        'avg_lap_time': '1:13.678',
        'consistency_score': 98.8,
        'error_risk_percent': 4.2,
        'racecraft_score': 92,
        'pressure_index': 93,
        'pace_trend': 'improving'
    },
    
    'delta_analysis': {
        'lap_time_delta': -0.111,
        'consistency_delta': 0.4,
        'racecraft_delta': -4,
        'pressure_delta': 2
    },
    
    'winner': 'VER',
    'racecraft_winner': 'HAM',
    'consistency_winner': 'VER',
    
    'battle_prediction': {
        'overtake_probability': 0.65,
        'confidence': 0.82
    }
}
```

**Use Cases:**
- Driver skill assessment
- Head-to-head prediction
- Team orders decisions
- Coaching priorities

---

## 🔧 Configuration

### Cache Management

```python
# Default cache (./cache)
engine = ComparisonEngine()

# Custom cache directory
engine = ComparisonEngine(cache_dir='/path/to/cache')

# No cache (slower, always fresh data)
engine = ComparisonEngine(cache_dir=None)
```

### Session Types

```python
# Qualifying
result = engine.compare_cars(..., session_type='Q')

# Race
result = engine.compare_cars(..., session_type='R')

# Practice sessions
result = engine.compare_cars(..., session_type='FP1')
result = engine.compare_cars(..., session_type='FP2')
result = engine.compare_cars(..., session_type='FP3')

# Sprint
result = engine.compare_cars(..., session_type='S')
```

---

## 🎨 Advanced Usage

### Custom Analysis Pipeline

```python
from comparison_engine import ComparisonEngine
from analysis_engines.car_analysis import SpeedAnalyzer, BrakingAnalyzer

engine = ComparisonEngine()

# Get raw data
session = engine.loader.load_session(2024, 'Monaco', 'Q')
driver1_laps = session.laps.pick_driver('VER')
driver2_laps = session.laps.pick_driver('LEC')

# Get fastest laps
fastest1 = driver1_laps.pick_fastest()
fastest2 = driver2_laps.pick_fastest()

# Get telemetry
telemetry1 = fastest1.get_telemetry()
telemetry2 = fastest2.get_telemetry()

# Run custom analyzers
speed_analyzer = SpeedAnalyzer()
speed_result = speed_analyzer.analyze(telemetry1, telemetry2)

braking_analyzer = BrakingAnalyzer()
braking_result = braking_analyzer.analyze(telemetry1, telemetry2)

# Combine results
custom_comparison = {
    'speed_analysis': speed_result,
    'braking_analysis': braking_result
}
```

### Batch Comparisons

```python
# Compare multiple driver pairs
pairs = [
    ('VER', 'LEC'),
    ('HAM', 'RUS'),
    ('NOR', 'PIA')
]

results = {}
for driver1, driver2 in pairs:
    result = engine.compare_cars(2024, 'Monaco', 'Q', driver1, driver2)
    results[f"{driver1}_vs_{driver2}"] = result
    
# Find biggest delta
max_delta = max(results.values(), key=lambda r: abs(r['delta_seconds']))
print(f"Biggest gap: {max_delta['driver1']} vs {max_delta['driver2']}")
```

### Multi-Session Analysis

```python
# Compare across sessions
sessions = ['FP1', 'FP2', 'FP3', 'Q']
evolution = {}

for session in sessions:
    result = engine.compare_cars(2024, 'Monaco', session, 'VER', 'LEC')
    evolution[session] = result['delta_seconds']

# Track improvement
print(f"Delta evolution: {evolution}")
```

---

## 🔗 Integration Points

### Used By:
- **API Routers** (`api/comparison_router.py`)
- **Strategy Engines** (for car performance input)
- **CLI Tools** (interactive comparisons)
- **Test Suites** (validation)

### Example API Integration:

```python
# In api/comparison_router.py
from comparison_engine import ComparisonEngine

engine = ComparisonEngine()

@router.get("/compare/cars")
async def compare_cars(year: int, event: str, session: str, 
                       driver1: str, driver2: str):
    result = engine.compare_cars(year, event, session, driver1, driver2)
    return result
```

---

## 🧪 Testing

### Unit Tests

```python
import pytest
from comparison_engine import ComparisonEngine

def test_car_comparison():
    engine = ComparisonEngine()
    result = engine.compare_cars(2024, 'Monaco', 'Q', 'VER', 'LEC')
    
    assert 'winner' in result
    assert 'delta_seconds' in result
    assert result['delta_seconds'] != 0

def test_driver_comparison():
    engine = ComparisonEngine()
    result = engine.compare_drivers(2024, 'Monaco', 'Q', 'VER', 'HAM')
    
    assert result['driver1']['consistency_score'] > 0
    assert result['driver2']['consistency_score'] > 0
```

### Integration Tests

```bash
# Run comparison engine tests
pytest comparison_engine/

# Run with real data (cached)
pytest comparison_engine/ --use-real-data

# Test all comparison endpoints
pytest api/test_comparison_router.py
```

---

## ⚡ Performance

### Optimization Features:
- **FastF1 Caching** - Session data cached permanently
- **Lazy Loading** - Only load data when needed
- **Parallel Analysis** - Independent analyzers run concurrently
- **Result Caching** - Frequent comparisons cached

### Typical Response Times:
| Operation | First Call | Cached Call |
|-----------|-----------|-------------|
| Standard comparison | 2-5s | 100-300ms |
| Detailed comparison | 3-8s | 200-500ms |
| Driver comparison | 1-3s | 50-150ms |

---

## 🎯 Real-World Examples

### Example 1: Qualifying Analysis
```python
engine = ComparisonEngine()

# Compare teammates
result = engine.compare_cars(2024, 'Monaco', 'Q', 'VER', 'PER')

if result['winner'] == 'VER':
    delta = result['delta_seconds']
    print(f"Verstappen ahead by {delta:.3f}s")
    
    # Analyze gap
    if result['power_delta_percent'] > 0:
        print("Advantage: Straight-line speed")
    if result['mechanical_grip_delta_percent'] > 0:
        print("Advantage: Cornering")
```

### Example 2: Development Testing
```python
# Compare FP1 (baseline) vs FP3 (new parts)
baseline = engine.compare_cars(2024, 'Monaco', 'FP1', 'VER', 'VER')
updated = engine.compare_cars(2024, 'Monaco', 'FP3', 'VER', 'VER')

# Track improvement
speed_gain = updated['max_speed_delta_kmh']
corner_gain = updated['mechanical_grip_delta_percent']

print(f"Upgrade gained {speed_gain} km/h in straights")
print(f"Upgrade gained {corner_gain}% in corners")
```

### Example 3: Battle Prediction
```python
# Predict race battle outcome
comparison = engine.compare_drivers(2024, 'Monaco', 'Q', 'VER', 'LEC')

overtake_prob = comparison['battle_prediction']['overtake_probability']

if overtake_prob > 0.7:
    strategy = "Aggressive - try overtake"
elif overtake_prob > 0.4:
    strategy = "Balanced - wait for mistake"
else:
    strategy = "Defensive - pit and undercut"
    
print(f"Recommended strategy: {strategy}")
```

---

## 🐛 Error Handling

The engine handles common errors gracefully:

```python
try:
    result = engine.compare_cars(2024, 'Monaco', 'Q', 'VER', 'LEC')
except SessionNotFoundError:
    print("Session data not available")
except DriverNotFoundError:
    print("Driver did not participate in session")
except TelemetryNotAvailableError:
    print("Telemetry data not available for this session")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## 🎓 Summary

The **Comparison Engine** is the unified interface for F1 analysis:

✅ **Single Entry Point** - All comparisons through one engine  
✅ **Multi-Dimensional** - Car performance + driver skill  
✅ **Flexible Output** - Standard or detailed formats  
✅ **Production Ready** - Used by API, CLI, tests  
✅ **High Performance** - Cached and optimized  
✅ **Well Tested** - Comprehensive test coverage  

It orchestrates **6 analyzers** and **29 calculations** to deliver comprehensive F1 performance comparisons in a simple, intuitive interface.

---

## 📚 Further Reading

- [Analysis Engines README](../analysis_engines/README.md) - Underlying analyzers
- [Calculation Engines README](../calculation_engines/README.md) - Core calculations
- [API Examples](../API_EXAMPLES.md) - REST API usage
- [Architecture Guide](../ARCHITECTURE.md) - System design
