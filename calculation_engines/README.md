# Calculation Engines

## 🧮 Overview

The **Calculation Engines** are the mathematical core of the F1 Race Strategy Simulator. They provide **29 specialized calculation modules** that transform raw telemetry data into racing metrics and insights.

---

## 📁 Structure

```
calculation_engines/
├── interfaces/                    # Base classes and models
│   ├── base_calculation.py
│   ├── calculation_input_models.py
│   └── calculation_output_models.py
│
├── car_calculations/              # Car performance metrics
│   ├── power_delta_calc.py
│   ├── drag_penalty_calc.py
│   ├── mechanical_grip_delta_calc.py
│   ├── setup_flexibility_calc.py
│   └── kerb_compliance_calc.py
│
├── tyre_calculations/             # Tyre performance & degradation
│   ├── degradation_curve_calc.py
│   ├── compound_delta_calc.py
│   ├── thermal_window_calc.py
│   ├── tyre_life_projection_calc.py
│   └── push_penalty_calc.py
│
├── driver_calculations/           # Driver skill metrics
│   ├── consistency_metrics_calc.py
│   ├── error_risk_calc.py
│   ├── racecraft_score_calc.py
│   ├── pressure_index_calc.py
│   └── adaptability_calc.py
│
├── track_calculations/            # Track-specific metrics
│   ├── track_evolution_calc.py
│   ├── turn_delta_calc.py
│   ├── sector_delta_calc.py
│   └── straight_line_speed_calc.py
│
├── weather_calculations/          # Weather impact
│   ├── grip_evolution_calc.py
│   ├── cooling_margin_calc.py
│   ├── crossover_lap_calc.py
│   └── weather_volatility_calc.py
│
├── traffic_calculations/          # Overtaking & battles
│   ├── overtake_probability_calc.py
│   ├── drs_advantage_calc.py
│   ├── battle_prediction_calc.py
│   └── traffic_impact_calc.py
│
├── race_state_calculations/       # Race strategy metrics
│   ├── fuel_effect_calc.py
│   ├── pit_loss_calc.py
│   ├── undercut_delta_calc.py
│   └── safety_car_probability_calc.py
│
└── aggregation/                   # Multi-calculation aggregators
    └── performance_aggregator.py
```

---

## 🎯 Core Design Principles

### 1. **Pure Functions**
All calculations are pure functions with no side effects:

```python
def calculate(inputs: InputModel) -> OutputModel:
    """
    Pure calculation - same inputs always produce same outputs
    No external dependencies, no state modification
    """
    result = perform_calculation(inputs)
    return OutputModel(**result)
```

### 2. **Type Safety**
Pydantic models ensure data integrity:

```python
class PowerDeltaInput(BaseModel):
    max_speed_car1: float
    max_speed_car2: float
    
class PowerDeltaOutput(BaseModel):
    power_delta_percent: float
    speed_advantage_kmh: float
```

### 3. **Single Responsibility**
Each calculation does exactly ONE thing:
- ✅ `power_delta_calc.py` - Power comparison only
- ✅ `drag_penalty_calc.py` - Drag analysis only
- ❌ NO mixed responsibilities

### 4. **Testability**
Every calculation has isolated unit tests:

```python
def test_power_delta_calculation():
    inputs = PowerDeltaInput(max_speed_car1=350, max_speed_car2=340)
    result = calculate_power_delta(inputs)
    assert result.power_delta_percent == pytest.approx(2.94, rel=0.01)
```

---

## 📊 Calculation Categories

### 🏎️ Car Calculations (5 modules)

**Purpose:** Quantify car performance differences

| Module | Metric | Formula | Output |
|--------|--------|---------|--------|
| `power_delta_calc.py` | Engine power | `(speed1 - speed2) / speed2 * 100` | Percentage delta |
| `drag_penalty_calc.py` | Aero efficiency | `decel_rate / speed²` | Drag coefficient |
| `mechanical_grip_delta_calc.py` | Low-speed grip | `avg_speed_corners(<150kmh)` | Grip delta |
| `setup_flexibility_calc.py` | Setup range | Window analysis | Flexibility score |
| `kerb_compliance_calc.py` | Kerb riding | Impact absorption | Compliance rating |

**Used For:**
- Car-to-car comparison
- Setup optimization
- Qualifying analysis
- Development direction

---

### 🛞 Tyre Calculations (5 modules)

**Purpose:** Model tyre performance and degradation

| Module | Metric | Key Logic | Output |
|--------|--------|-----------|--------|
| `degradation_curve_calc.py` | Lap time loss | Exponential decay model | Time loss/lap |
| `compound_delta_calc.py` | Compound gap | Soft vs Medium vs Hard | Delta seconds |
| `thermal_window_calc.py` | Operating temp | Optimal range 90-110°C | Efficiency % |
| `tyre_life_projection_calc.py` | Stint length | Cliff prediction | Max laps |
| `push_penalty_calc.py` | Push mode cost | Accelerated degradation | Extra deg/lap |

**Used For:**
- Pit strategy optimization
- Compound selection
- Stint length planning
- Qualifying preparation

---

### 👤 Driver Calculations (5 modules)

**Purpose:** Quantify driver skill and characteristics

| Module | Metric | Measurement | Output |
|--------|--------|-------------|--------|
| `consistency_metrics_calc.py` | Lap variation | Std dev of lap times | Score 0-100 |
| `error_risk_calc.py` | Mistake likelihood | Errors per lap | Risk percent |
| `racecraft_score_calc.py` | Combat ability | Overtake success rate | Score 0-100 |
| `pressure_index_calc.py` | Stress handling | Performance under pressure | Index 0-100 |
| `adaptability_calc.py` | Track variance | Track-to-track change | Adaptability score |

**Used For:**
- Driver comparison
- Team orders decisions
- Contract negotiations
- Coaching priorities

---

### 🛣️ Track Calculations (4 modules)

**Purpose:** Analyze track-specific characteristics

| Module | Metric | Analysis | Output |
|--------|--------|----------|--------|
| `track_evolution_calc.py` | Grip progression | Rubber buildup | Lap time gain |
| `turn_delta_calc.py` | Corner performance | Turn-by-turn delta | Seconds/corner |
| `sector_delta_calc.py` | Sector comparison | 3-sector breakdown | Delta/sector |
| `straight_line_speed_calc.py` | Top speed | DRS zones | Max speed |

**Used For:**
- Setup decisions
- Qualifying strategy
- Track position value
- Overtaking zones

---

### 🌦️ Weather Calculations (4 modules)

**Purpose:** Model weather impact on performance

| Module | Metric | Conditions | Output |
|--------|--------|------------|--------|
| `grip_evolution_calc.py` | Drying track | Wet to dry transition | Grip % |
| `cooling_margin_calc.py` | Temperature mgmt | Engine/brake cooling | Margin °C |
| `crossover_lap_calc.py` | Tyre crossover | Inter to slick timing | Lap number |
| `weather_volatility_calc.py` | Condition change | Forecast uncertainty | Risk level |

**Used For:**
- Wet race strategy
- Tyre crossover decisions
- Temperature management
- Risk assessment

---

### 🚗 Traffic Calculations (3 modules)

**Purpose:** Predict overtaking and battles

| Module | Metric | Factors | Output |
|--------|--------|---------|--------|
| `overtake_probability_calc.py` | Pass likelihood | Pace + DRS + track | Probability 0-1 |
| `drs_advantage_calc.py` | DRS benefit | Speed gain | Seconds saved |
| `battle_prediction_calc.py` | Multi-lap battle | Extended combat | Winner prediction |
| `traffic_impact_calc.py` | Backmarker effect | Slower cars | Time loss |

**Used For:**
- Undercut/overcut decisions
- Battle outcome prediction
- Strategic positioning
- Risk/reward analysis

---

### 🏁 Race State Calculations (3 modules)

**Purpose:** Optimize race strategy

| Module | Metric | Components | Output |
|--------|--------|------------|--------|
| `fuel_effect_calc.py` | Fuel load impact | Weight penalty | Seconds/kg |
| `pit_loss_calc.py` | Pit stop cost | Stationary + pit lane | Total loss |
| `undercut_delta_calc.py` | Undercut value | Fresh vs old tyres | Advantage seconds |
| `safety_car_probability_calc.py` | SC likelihood | Historical data | Probability |

**Used For:**
- Pit stop timing
- Strategy selection
- Risk management
- Race simulation

---

## 🔧 Base Calculation Interface

All calculations inherit from `BaseCalculation`:

```python
from abc import ABC, abstractmethod
from pydantic import BaseModel

class BaseCalculation(ABC):
    """Base class for all calculations"""
    
    @abstractmethod
    def calculate(self, inputs: BaseModel) -> BaseModel:
        """
        Execute calculation
        
        Args:
            inputs: Typed input model
            
        Returns:
            Typed output model
        """
        pass
    
    def validate_inputs(self, inputs: BaseModel) -> bool:
        """Validate inputs before calculation"""
        return inputs is not None
    
    def get_metadata(self) -> dict:
        """Return calculation metadata"""
        return {
            'name': self.__class__.__name__,
            'version': '1.0.0',
            'category': self.category
        }
```

---

## 📥 Input Models

Defined in `interfaces/calculation_input_models.py`:

```python
from pydantic import BaseModel, Field

class PowerDeltaInput(BaseModel):
    """Input for power delta calculation"""
    max_speed_car1: float = Field(gt=0, description="Max speed car 1 (km/h)")
    max_speed_car2: float = Field(gt=0, description="Max speed car 2 (km/h)")
    reference_distance: float = Field(default=1000, description="Reference distance (m)")

class DegradationInput(BaseModel):
    """Input for degradation calculation"""
    compound: str = Field(description="Tyre compound")
    tyre_age: int = Field(ge=0, description="Tyre age (laps)")
    track_temp: float = Field(description="Track temperature (°C)")
    fuel_load: float = Field(ge=0, description="Fuel load (kg)")
```

---

## 📤 Output Models

Defined in `interfaces/calculation_output_models.py`:

```python
from pydantic import BaseModel
from typing import Optional

class PowerDeltaOutput(BaseModel):
    """Output from power delta calculation"""
    power_delta_percent: float
    speed_advantage_kmh: float
    drs_overtake_probability: Optional[float] = None
    
class DegradationOutput(BaseModel):
    """Output from degradation calculation"""
    degradation_rate_per_lap: float
    projected_cliff_lap: int
    current_lap_time_loss: float
    optimal_pit_window: tuple[int, int]
```

---

## 🔗 Calculation Dependencies

Some calculations depend on others:

```
PitStrategySimulator
  │
  ├─> DegradationCurveCalc
  │     └─> Requires: compound, age, temp
  │
  ├─> CompoundDeltaCalc
  │     └─> Requires: lap times per compound
  │
  ├─> PitLossCalc
  │     └─> Requires: pit lane length
  │
  └─> UnderCutDeltaCalc
        └─> Requires: pace delta, tyre delta
```

**Dependency Management:**
- Calculations are ordered by dependency
- Independent calcs can run in parallel
- Aggregator combines multi-calc results

---

## 🚀 Usage Examples

### Basic Calculation
```python
from calculation_engines.car_calculations import PowerDeltaCalc
from calculation_engines.interfaces.calculation_input_models import PowerDeltaInput

# Create calculator
calc = PowerDeltaCalc()

# Prepare input
inputs = PowerDeltaInput(
    max_speed_car1=350.5,
    max_speed_car2=342.1
)

# Execute
result = calc.calculate(inputs)

print(f"Power delta: {result.power_delta_percent:.2f}%")
print(f"Speed advantage: {result.speed_advantage_kmh:.1f} km/h")
```

### Multi-Calculation Analysis
```python
from calculation_engines.aggregation import PerformanceAggregator

aggregator = PerformanceAggregator()

# Run all car calculations
results = aggregator.aggregate_car_performance(
    telemetry_car1=telemetry1,
    telemetry_car2=telemetry2
)

print(f"Power delta: {results['power_delta']}")
print(f"Grip delta: {results['grip_delta']}")
print(f"Overall advantage: {results['overall_winner']}")
```

---

## 🧪 Testing

Each calculation has comprehensive tests:

```bash
# Test specific category
pytest calculation_engines/car_calculations/test_car_calculations.py

# Test all calculations
pytest calculation_engines/test_all_calculations.py

# Test with coverage
pytest --cov=calculation_engines calculation_engines/
```

Test structure:
```python
def test_power_delta_basic():
    """Test basic power delta calculation"""
    calc = PowerDeltaCalc()
    inputs = PowerDeltaInput(max_speed_car1=350, max_speed_car2=340)
    result = calc.calculate(inputs)
    
    assert result.power_delta_percent > 0
    assert result.speed_advantage_kmh == pytest.approx(10.0)

def test_power_delta_edge_cases():
    """Test edge cases"""
    calc = PowerDeltaCalc()
    
    # Equal speeds
    inputs = PowerDeltaInput(max_speed_car1=350, max_speed_car2=350)
    result = calc.calculate(inputs)
    assert result.power_delta_percent == 0
    
    # Negative delta
    inputs = PowerDeltaInput(max_speed_car1=340, max_speed_car2=350)
    result = calc.calculate(inputs)
    assert result.power_delta_percent < 0
```

---

## ⚡ Performance

### Optimization Techniques
- **Vectorization:** NumPy for batch operations
- **Caching:** Memoization of expensive calculations
- **Lazy Evaluation:** Compute only when needed
- **JIT Compilation:** Numba for hot paths

### Benchmarks
| Calculation Type | Avg Time | Max Time |
|-----------------|----------|----------|
| Simple (power delta) | <1ms | 2ms |
| Medium (degradation) | 2-5ms | 10ms |
| Complex (battle prediction) | 10-20ms | 50ms |
| Aggregated (full analysis) | 50-100ms | 200ms |

---

## 📚 Documentation

Each calculation module includes:

```python
"""
Power Delta Calculation

Quantifies straight-line speed advantage between two cars.

Formula:
    power_delta = (max_speed_car1 - max_speed_car2) / max_speed_car2 * 100

Inputs:
    - max_speed_car1: Maximum speed of car 1 (km/h)
    - max_speed_car2: Maximum speed of car 2 (km/h)
    
Outputs:
    - power_delta_percent: Power advantage as percentage
    - speed_advantage_kmh: Absolute speed difference
    
Use Cases:
    - DRS overtaking prediction
    - Power unit comparison
    - Straight-line performance analysis
    
Limitations:
    - Assumes equal drag coefficients
    - Does not account for slipstream
    - Requires representative max speed data
"""
```

---

## 🎯 Real-World Applications

### 1. Qualifying Analysis
```python
# Find performance gaps
power = calculate_power_delta(telemetry)
grip = calculate_grip_delta(telemetry)

if power.delta < 0 and grip.delta > 0:
    print("Strong in corners, weak on straights")
    recommendation = "Low-drag setup for qualifying"
```

### 2. Race Strategy
```python
# Determine pit timing
degradation = calculate_degradation_curve(stint_data)
compound_delta = calculate_compound_delta(lap_times)

if degradation.cliff_lap - current_lap < 3:
    print("Pit window opening")
    optimal_compound = compound_delta.fastest_compound
```

### 3. Battle Prediction
```python
# Predict overtake success
overtake_prob = calculate_overtake_probability(
    pace_delta=0.3,
    drs_advantage=0.4,
    track_difficulty=7
)

if overtake_prob > 0.7:
    print("Stay out and defend")
else:
    print("Pit and undercut")
```

---

## 🎓 Summary

The **Calculation Engines** provide the mathematical foundation:

✅ **29 Specialized Modules** - Pure calculation logic  
✅ **Type-Safe I/O** - Pydantic models throughout  
✅ **Single Responsibility** - One calculation, one purpose  
✅ **Fully Tested** - Comprehensive unit test coverage  
✅ **High Performance** - Optimized for real-time use  
✅ **Composable** - Combine for complex analysis  

These calculations power every analysis, comparison, and strategic decision in the F1 Race Strategy Simulator.
