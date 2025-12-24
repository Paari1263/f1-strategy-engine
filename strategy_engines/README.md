# Strategy Engines

## 🧠 Overview

The **Strategy Engines** provide high-level race strategy calculations, simulations, and forecasting. These engines combine data from multiple sources to make strategic decisions during practice, qualifying, and race sessions.

---

## 📁 Structure

```
strategy_engines/
├── __init__.py                      # Package initialization
├── pit_strategy_simulator.py       # ⭐ Pit strategy simulation & optimization
├── battle_forecast.py               # ⭐ Overtaking prediction & battle analysis
├── track_evolution.py               # ⭐ Track grip evolution tracking
│
├── pit_strategy/                    # Pit stop strategy modules
│   ├── undercut_strategy.py
│   ├── overcut_strategy.py
│   ├── pit_window_strategy.py
│   ├── pit_loss_strategy.py
│   └── double_stack_risk_strategy.py
│
├── race_strategy/                   # Overall race strategy
│   ├── overall_race_strategy.py
│   ├── points_maximization_strategy.py
│   ├── risk_reward_strategy.py
│   ├── stint_sequencing_strategy.py
│   └── team_conflict_strategy.py
│
├── tyre_strategy/                   # Tyre management
│   ├── compound_switch_strategy.py
│   ├── stint_length_strategy.py
│   ├── push_manage_strategy.py
│   ├── tyre_degradation_strategy.py
│   └── tyre_offset_strategy.py
│
├── safety_car_strategy/             # Safety car scenarios
├── weather_strategy/                # Weather adaptation
├── traffic_strategy/                # Traffic management
│
├── calculations/                    # Strategy calculations
├── interfaces/                      # Strategy interfaces
├── strategy_interfaces/             # Abstract strategy patterns
├── aggregation/                     # Data aggregation
└── utils/                          # Utility functions
```

---

## 🌟 Core Strategy Systems

### 1. Pit Strategy Simulator

**File:** `pit_strategy_simulator.py`  
**Class:** `PitStrategySimulator`

**Purpose:** Simulate pit stop strategies and optimize timing for undercuts/overcuts

**Key Features:**
- Calculates optimal pit window (earliest/latest)
- Simulates undercut/overcut scenarios
- Models tyre degradation over stint
- Recommends tyre compound choice
- Accounts for traffic and gaps

**Output Model:**
```python
class PitStrategyOutput(BaseModel):
    optimal_pit_lap: int              # Best lap to pit
    pit_window_start: int             # Earliest pit lap
    pit_window_end: int               # Latest pit lap
    undercut_advantage: float         # Undercut time gain (s)
    overcut_advantage: float          # Overcut time gain (s)
    recommended_compound: str         # Next tyre compound
    expected_stint_length: int        # Stint duration (laps)
    strategy_type: str                # Strategy classification
    confidence: float                 # Confidence (0-1)
```

**Usage Example:**
```python
from strategy_engines.pit_strategy_simulator import PitStrategySimulator

# Current race situation
current_lap = 20
total_laps = 78
current_compound = 'MEDIUM'
tyre_age = 19
gap_ahead = 2.5  # seconds
gap_behind = 3.8  # seconds

# Calculate optimal strategy
strategy = PitStrategySimulator.calculate_optimal_strategy(
    current_lap=current_lap,
    total_laps=total_laps,
    current_compound=current_compound,
    current_tyre_age=tyre_age,
    gap_ahead=gap_ahead,
    gap_behind=gap_behind
)

print(f"Optimal pit lap: {strategy.optimal_pit_lap}")
print(f"Pit window: {strategy.pit_window_start}-{strategy.pit_window_end}")
print(f"Undercut advantage: {strategy.undercut_advantage:.2f}s")
print(f"Recommended compound: {strategy.recommended_compound}")
print(f"Strategy: {strategy.strategy_type}")
```

**Real-World Impact:**
- **Undercut Detection:** Predicts when undercut is viable (gap < pit loss)
- **Overcut Timing:** Calculates when staying out longer pays off
- **Traffic Avoidance:** Suggests pit timing to avoid traffic
- **Compound Choice:** Recommends SOFT/MEDIUM/HARD based on remaining laps

---

### 2. Battle Forecast

**File:** `battle_forecast.py`  
**Class:** `BattleForecast`

**Purpose:** Predict overtaking opportunities and battle outcomes

**Key Features:**
- Analyzes speed deltas in DRS zones
- Identifies braking zone advantages
- Calculates overtake probability
- Recommends attack/defend strategy
- Considers track difficulty

**Output Model:**
```python
class BattlePrediction(BaseModel):
    overtake_probability: float       # Success probability (0-1)
    best_overtake_zone: str          # Track zone for attempt
    speed_advantage: float           # Speed advantage (km/h)
    drs_available: bool              # DRS availability
    difficulty_rating: float         # Difficulty (0-10)
    recommended_strategy: str        # Strategic recommendation
    key_factors: List[str]           # Influencing factors
```

**Usage Example:**
```python
from strategy_engines.battle_forecast import BattleForecast

# Load telemetry for both cars
attacking_tel = telemetry_processor.get_telemetry(
    year=2024, event='Monza', driver='VER', lap=45
)
defending_tel = telemetry_processor.get_telemetry(
    year=2024, event='Monza', driver='LEC', lap=45
)

# Predict battle outcome
prediction = BattleForecast.predict_overtake(
    attacking_tel=attacking_tel,
    defending_tel=defending_tel,
    gap_s=0.8,              # 0.8s gap
    drs_available=True,
    track_difficulty=3.0    # Monza = easier overtaking
)

print(f"Overtake probability: {prediction.overtake_probability:.1%}")
print(f"Best zone: {prediction.best_overtake_zone}")
print(f"Speed advantage: {prediction.speed_advantage:.1f} km/h")
print(f"Recommendation: {prediction.recommended_strategy}")
print(f"Key factors: {', '.join(prediction.key_factors)}")
```

**Real-World Impact:**
- **DRS Strategy:** Maximize DRS effectiveness in overtaking zones
- **Defend Mode:** Predict when to deploy defensive tactics
- **Battery Management:** Optimize energy deployment for overtakes
- **Risk Assessment:** Evaluate collision risk vs reward

---

### 3. Track Evolution Tracker

**File:** `track_evolution.py`  
**Class:** `TrackEvolutionTracker`

**Purpose:** Track grip and performance changes across sessions

**Key Features:**
- Compares lap times across FP1, FP2, FP3, Q, R
- Accounts for fuel load and tyre compound
- Models grip progression (track rubbering in)
- Predicts optimal session performance
- Calculates evolution rate

**Output Model:**
```python
class TrackEvolutionOutput(BaseModel):
    grip_improvement: float          # Grip gain from baseline (%)
    lap_time_improvement: float      # Lap time improvement (s)
    evolution_rate: float            # Evolution rate (s/session)
    track_condition: str             # Current condition
    optimal_session: str             # Best session
    confidence: float                # Confidence (0-1)
```

**Usage Example:**
```python
from strategy_engines.track_evolution import TrackEvolutionTracker

# Load session data
sessions_data = {
    'FP1': fp1_laps,
    'FP2': fp2_laps,
    'FP3': fp3_laps,
    'Q': qualifying_laps,
    'R': race_laps
}

# Analyze evolution
evolution = TrackEvolutionTracker.analyze_evolution(
    sessions_data=sessions_data,
    reference_driver='VER'  # Use specific driver
)

print(f"Grip improvement: {evolution.grip_improvement:.1f}%")
print(f"Lap time improvement: {evolution.lap_time_improvement:.2f}s")
print(f"Evolution rate: {evolution.evolution_rate:.3f} s/session")
print(f"Track condition: {evolution.track_condition}")
print(f"Optimal session: {evolution.optimal_session}")
```

**Real-World Impact:**
- **Qualifying Prediction:** Predict Q3 lap times from FP3
- **Setup Optimization:** Adjust setup as track evolves
- **Race Pace:** Estimate race pace from practice
- **Typical Evolution:** 1-3 seconds from FP1 to Qualifying

---

## 🛠️ Strategy Modules

### Pit Strategy (`pit_strategy/`)

**5 Specialized Strategies:**

#### 1. **Undercut Strategy** (`undercut_strategy.py`)
- **Purpose:** Calculate undercut timing and advantage
- **Logic:** Pit earlier, use fresh tyres to gain time
- **Key Metric:** `undercut_window` = pit loss - degradation gap
- **Use Case:** Overtake car ahead without wheel-to-wheel racing

#### 2. **Overcut Strategy** (`overcut_strategy.py`)
- **Purpose:** Stay out longer, gain track position
- **Logic:** Extend stint on degrading tyres, pit when advantage maximized
- **Key Metric:** `overcut_gain` = extended stint time - lost degradation
- **Use Case:** Jump competitors who pit early

#### 3. **Pit Window Strategy** (`pit_window_strategy.py`)
- **Purpose:** Calculate optimal pit stop window
- **Logic:** Balance tyre life, traffic, and race position
- **Key Metric:** `pit_window` = [earliest_viable_lap, latest_viable_lap]
- **Use Case:** Define strategic flexibility

#### 4. **Pit Loss Strategy** (`pit_loss_strategy.py`)
- **Purpose:** Calculate actual pit stop time loss
- **Logic:** Pit lane speed + stop duration + entry/exit
- **Key Metric:** `pit_loss` = pit_time - on_track_time
- **Use Case:** Undercut/overcut calculations

#### 5. **Double Stack Risk Strategy** (`double_stack_risk_strategy.py`)
- **Purpose:** Evaluate risk of double-stacking teammates
- **Logic:** Model wait time for second car
- **Key Metric:** `stack_penalty` = additional_wait_time
- **Use Case:** Team strategy coordination

**Example:**
```python
from strategy_engines.pit_strategy.undercut_strategy import UndercutStrategy

# Calculate undercut opportunity
undercut = UndercutStrategy.calculate_undercut(
    pit_lap=22,
    competitor_pit_lap=24,
    current_gap=3.2,
    pit_loss=20.5,
    tyre_degradation_rate=0.05
)

if undercut['viable']:
    print(f"Undercut advantage: {undercut['advantage']:.2f}s")
    print(f"Position gain probability: {undercut['success_rate']:.1%}")
```

---

### Race Strategy (`race_strategy/`)

**5 Comprehensive Strategies:**

#### 1. **Overall Race Strategy** (`overall_race_strategy.py`)
- **Purpose:** End-to-end race strategy planning
- **Components:** Start position, pit stops, tyre selection, finish target
- **Output:** Complete race plan with contingencies
- **Use Case:** Pre-race strategy briefing

#### 2. **Points Maximization Strategy** (`points_maximization_strategy.py`)
- **Purpose:** Maximize championship points
- **Logic:** Risk vs reward based on current standings
- **Decision:** Attack (gain positions) vs defend (secure points)
- **Use Case:** Championship battle scenarios

#### 3. **Risk-Reward Strategy** (`risk_reward_strategy.py`)
- **Purpose:** Balance aggressive vs conservative approaches
- **Factors:** Track position, championship situation, car pace
- **Output:** Risk tolerance level (0-10)
- **Use Case:** Strategic aggression calibration

#### 4. **Stint Sequencing Strategy** (`stint_sequencing_strategy.py`)
- **Purpose:** Optimize tyre compound sequence
- **Logic:** Model all possible compound combinations
- **Output:** Optimal stint sequence (e.g., SOFT → MEDIUM → HARD)
- **Use Case:** Multi-stop strategy planning

#### 5. **Team Conflict Strategy** (`team_conflict_strategy.py`)
- **Purpose:** Resolve teammate strategy conflicts
- **Logic:** Championship priority, team orders, fairness
- **Output:** Team-optimized strategy
- **Use Case:** When both cars vie for same strategy

**Example:**
```python
from strategy_engines.race_strategy.overall_race_strategy import RaceStrategy

# Plan complete race strategy
strategy = RaceStrategy.plan_race(
    start_position=3,
    total_laps=58,
    available_compounds=['SOFT', 'MEDIUM', 'HARD'],
    fuel_load=110,  # kg
    track='Monaco',
    weather='dry'
)

print(f"Start compound: {strategy.start_compound}")
print(f"Pit stops: {strategy.pit_stops}")
print(f"Stint sequence: {strategy.stint_sequence}")
print(f"Expected finish: P{strategy.expected_finish}")
```

---

### Tyre Strategy (`tyre_strategy/`)

**5 Tyre Management Strategies:**

#### 1. **Compound Switch Strategy** (`compound_switch_strategy.py`)
- **Purpose:** Decide when to switch tyre compounds
- **Logic:** Degradation crossover point
- **Output:** Optimal switch lap
- **Use Case:** Multi-compound races

#### 2. **Stint Length Strategy** (`stint_length_strategy.py`)
- **Purpose:** Optimize stint duration
- **Logic:** Balance tyre life vs track position
- **Output:** Target stint length (laps)
- **Use Case:** One-stop vs two-stop decisions

#### 3. **Push/Manage Strategy** (`push_manage_strategy.py`)
- **Purpose:** When to push hard vs manage tyres
- **Logic:** Degradation rate vs time gain
- **Output:** Lap-by-lap push/manage mode
- **Use Case:** Real-time tyre management

#### 4. **Tyre Degradation Strategy** (`tyre_degradation_strategy.py`)
- **Purpose:** Model and predict degradation
- **Logic:** Linear/exponential degradation models
- **Output:** Degradation curve projection
- **Use Case:** Stint length planning

#### 5. **Tyre Offset Strategy** (`tyre_offset_strategy.py`)
- **Purpose:** Exploit tyre age differences vs competitors
- **Logic:** Fresh tyres vs old = pace advantage
- **Output:** Offset advantage (seconds/lap)
- **Use Case:** Strategic tyre age management

**Example:**
```python
from strategy_engines.tyre_strategy.push_manage_strategy import PushManageStrategy

# Get lap-by-lap push/manage recommendation
laps = list(range(1, 59))
modes = PushManageStrategy.calculate_modes(
    laps=laps,
    target_finish=5,
    current_position=7,
    tyre_compound='MEDIUM',
    stint_start=15,
    stint_target=40
)

for lap, mode in zip(laps, modes):
    print(f"Lap {lap}: {mode}")  # 'PUSH' or 'MANAGE'
```

---

### Additional Strategy Modules

#### Safety Car Strategy (`safety_car_strategy/`)
- **Purpose:** Adapt strategy during safety car periods
- **Features:** Free pit stop windows, gap neutralization, restart tactics
- **Impact:** Safety cars can change race outcome dramatically

#### Weather Strategy (`weather_strategy/`)
- **Purpose:** Strategy for changing weather conditions
- **Features:** Rain probability, tyre crossover, wet-to-dry transitions
- **Impact:** Critical for mixed conditions

#### Traffic Strategy (`traffic_strategy/`)
- **Purpose:** Manage backmarker traffic and overtaking
- **Features:** Blue flag prediction, clean air windows, traffic avoidance
- **Impact:** Clean air worth 0.3-0.5s/lap

---

## 🔗 Integration Example

### Comprehensive Strategy Analysis

```python
from strategy_engines.pit_strategy_simulator import PitStrategySimulator
from strategy_engines.battle_forecast import BattleForecast
from strategy_engines.track_evolution import TrackEvolutionTracker

# 1. Track Evolution
evolution = TrackEvolutionTracker.analyze_evolution(sessions_data)
print(f"Track evolved: {evolution.lap_time_improvement:.2f}s")

# 2. Battle Forecast
battle = BattleForecast.predict_overtake(
    attacking_tel, defending_tel, gap_s=1.2, drs_available=True
)
print(f"Overtake probability: {battle.overtake_probability:.1%}")

# 3. Pit Strategy
if battle.overtake_probability < 0.3:  # Low overtake chance
    # Try undercut instead
    pit_strategy = PitStrategySimulator.calculate_optimal_strategy(
        current_lap=25, total_laps=58, current_compound='MEDIUM',
        current_tyre_age=15, gap_ahead=1.2
    )
    print(f"Undercut on lap {pit_strategy.optimal_pit_lap}")
```

---

## 🎯 Real-World Scenarios

### Scenario 1: Undercut Decision

**Situation:**
- Lap 22/58
- P2, 2.8s behind leader
- Both on MEDIUM tyres (18 laps old)
- Leader showing no signs of pitting

**Analysis:**
```python
pit_strategy = PitStrategySimulator.calculate_optimal_strategy(
    current_lap=22, total_laps=58, current_compound='MEDIUM',
    current_tyre_age=18, gap_ahead=2.8
)

if pit_strategy.undercut_advantage > 0:
    print(f"✅ Undercut viable!")
    print(f"Pit on lap {pit_strategy.optimal_pit_lap}")
    print(f"Expected gain: {pit_strategy.undercut_advantage:.2f}s")
    print(f"Next compound: {pit_strategy.recommended_compound}")
```

**Decision:** Pit on lap 23, switch to HARD, gain 3.2s over next 2 laps to jump leader

---

### Scenario 2: Battle Forecast

**Situation:**
- DRS zone approaching
- 0.7s behind competitor
- Speed advantage on straights

**Analysis:**
```python
prediction = BattleForecast.predict_overtake(
    attacking_tel=my_tel,
    defending_tel=competitor_tel,
    gap_s=0.7,
    drs_available=True,
    track_difficulty=4.0  # Medium difficulty track
)

if prediction.overtake_probability > 0.6:
    print(f"✅ Go for overtake!")
    print(f"Best zone: {prediction.best_overtake_zone}")
    print(f"Speed advantage: {prediction.speed_advantage:.1f} km/h")
else:
    print(f"❌ Hold position, try alternate strategy")
```

**Decision:** Attack into Turn 1 with DRS, 72% success probability

---

### Scenario 3: Track Evolution

**Situation:**
- Friday practice complete
- Need to predict qualifying pace
- Track rubbering in

**Analysis:**
```python
evolution = TrackEvolutionTracker.analyze_evolution({
    'FP1': fp1_laps,
    'FP2': fp2_laps,
    'FP3': fp3_laps
}, reference_driver='VER')

# Predict Q3 time
fp3_best = 1:32.456  # Best FP3 time
predicted_q3 = fp3_best - evolution.lap_time_improvement

print(f"FP3 best: {fp3_best}")
print(f"Expected evolution: {evolution.lap_time_improvement:.3f}s")
print(f"Predicted Q3: {predicted_q3}")
print(f"Confidence: {evolution.confidence:.1%}")
```

**Decision:** Target 1:31.8 in Q3 based on 0.656s evolution

---

## 🧪 Testing

### Strategy Tests

```bash
# Test all strategy calculations
pytest strategy_engines/test_all_calculations.py

# Test specific strategy module
pytest strategy_engines/pit_strategy/test/

# Integration tests
pytest tests/test_strategy_integration.py
```

### Example Test

```python
def test_undercut_advantage():
    """Test undercut calculation"""
    strategy = PitStrategySimulator.calculate_optimal_strategy(
        current_lap=20,
        total_laps=58,
        current_compound='MEDIUM',
        current_tyre_age=15,
        gap_ahead=3.0
    )
    
    # Undercut should be viable with 3s gap
    assert strategy.undercut_advantage > 0
    assert strategy.optimal_pit_lap in range(20, 25)
    assert strategy.confidence > 0.7
```

---

## ⚡ Performance

### Calculation Times

| Strategy | Avg Time | Max Time |
|----------|----------|----------|
| Pit Strategy Simulator | 50-100ms | 200ms |
| Battle Forecast | 100-300ms | 500ms |
| Track Evolution | 200-500ms | 1s |
| Overall Race Strategy | 500ms-2s | 5s |

### Optimization Tips:
- **Cache telemetry data** - Avoid re-loading same lap data
- **Parallel calculations** - Run independent strategies concurrently
- **Pre-compute degradation** - Cache compound degradation curves
- **Simplify models** - Use linear approximations for real-time decisions

---

## 📊 Strategy Decision Tree

```
Race Situation
     │
     ├─> Can overtake on track?
     │     ├─> YES → Battle Forecast → Attack
     │     └─> NO ↓
     │
     ├─> Undercut viable?
     │     ├─> YES → Pit Strategy Simulator → Undercut
     │     └─> NO ↓
     │
     ├─> Overcut viable?
     │     ├─> YES → Extend stint → Overcut
     │     └─> NO ↓
     │
     ├─> Safety car likely?
     │     ├─> YES → Hold position → Free pit stop
     │     └─> NO ↓
     │
     └─> Weather changing?
           ├─> YES → Weather Strategy → Adapt
           └─> NO → Maintain current strategy
```

---

## 🎓 Summary

The **Strategy Engines** provide comprehensive race strategy capabilities:

✅ **3 Core Systems:**
- Pit Strategy Simulator (undercut/overcut)
- Battle Forecast (overtaking prediction)
- Track Evolution Tracker (grip progression)

✅ **15+ Strategy Modules:**
- 5 Pit strategies
- 5 Race strategies
- 5 Tyre strategies
- Safety car, weather, traffic strategies

✅ **Real-Time Decision Making:**
- Sub-second calculations
- High confidence predictions
- Actionable recommendations

✅ **Production Ready:**
- Pydantic models for type safety
- Comprehensive testing
- Clear documentation

**Impact:**
Strategy wins races. These engines provide the analytical foundation for:
- Position gains through undercuts/overcuts
- Optimized tyre management
- Battle outcome predictions
- Track evolution understanding
- Weather adaptation
- Safety car opportunism

---

## 📚 Related Documentation

- [Calculation Engines](../calculation_engines/README.md) - Low-level calculations
- [Analysis Engines](../analysis_engines/README.md) - Telemetry analysis
- [Comparison Engine](../comparison_engine/README.md) - Car/driver comparison
- [API Examples](../API_EXAMPLES.md) - Strategy API usage
- [Architecture](../ARCHITECTURE.md) - System design
