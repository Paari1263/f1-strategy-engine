# Analysis Engines

## 📊 Overview

The **Analysis Engines** provide high-level analytical capabilities by combining raw telemetry data with domain-specific expertise. They transform FastF1 data into actionable insights about car and driver performance.

---

## 🏗️ Structure

```
analysis_engines/
├── car_analysis/          # Car performance analyzers
│   ├── speed_analyzer.py
│   ├── braking_analyzer.py
│   ├── corner_analyzer.py
│   └── straight_line_analyzer.py
│
└── driver_analysis/       # Driver performance analyzers
    ├── pace_analyzer.py
    └── consistency_analyzer.py
```

---

## 🏎️ Car Analysis

### Speed Analyzer
**File:** `car_analysis/speed_analyzer.py`

**Purpose:** Analyze speed profiles and performance characteristics

**Key Features:**
- Maximum speed detection across straights
- Speed trace comparison between drivers
- Sector-by-sector speed analysis
- Acceleration/deceleration rates

**Usage:**
```python
from analysis_engines.car_analysis import SpeedAnalyzer

analyzer = SpeedAnalyzer()
result = analyzer.analyze_speed_profile(telemetry_data)

print(f"Max speed: {result['max_speed_kmh']} km/h")
print(f"Average speed: {result['avg_speed_kmh']} km/h")
```

**Output Example:**
```python
{
    'max_speed_kmh': 342.5,
    'avg_speed_kmh': 198.3,
    'speed_variance': 45.2,
    'high_speed_sections': [...],
    'low_speed_sections': [...]
}
```

---

### Braking Analyzer
**File:** `car_analysis/braking_analyzer.py`

**Purpose:** Analyze braking performance and characteristics

**Key Features:**
- Braking point identification
- Braking force analysis
- Deceleration rates
- Brake zone comparison

**Usage:**
```python
from analysis_engines.car_analysis import BrakingAnalyzer

analyzer = BrakingAnalyzer()
result = analyzer.analyze_braking(telemetry_data)

print(f"Braking zones: {len(result['braking_zones'])}")
print(f"Avg brake pressure: {result['avg_brake_pressure']}")
```

---

### Corner Analyzer
**File:** `car_analysis/corner_analyzer.py`

**Purpose:** Analyze cornering performance and efficiency

**Key Features:**
- Corner entry/apex/exit speeds
- Minimum speed detection
- Turn-in characteristics
- Cornering G-forces

**Usage:**
```python
from analysis_engines.car_analysis import CornerAnalyzer

analyzer = CornerAnalyzer()
result = analyzer.analyze_corners(telemetry_data)

for corner in result['corners']:
    print(f"Corner {corner['number']}: Min speed {corner['min_speed']} km/h")
```

---

### Straight Line Analyzer
**File:** `car_analysis/straight_line_analyzer.py`

**Purpose:** Analyze straight-line performance and top speed

**Key Features:**
- DRS zone analysis
- Top speed comparisons
- Power unit performance
- Drag characteristics

**Usage:**
```python
from analysis_engines.car_analysis import StraightLineAnalyzer

analyzer = StraightLineAnalyzer()
result = analyzer.analyze_straights(telemetry_data)

print(f"Top speed: {result['top_speed']} km/h")
print(f"DRS gain: {result['drs_advantage']} km/h")
```

---

## 👤 Driver Analysis

### Pace Analyzer
**File:** `driver_analysis/pace_analyzer.py`

**Purpose:** Analyze driver pace and performance trends

**Key Features:**
- Fastest lap identification
- Average pace calculation
- Sector performance
- Lap time progression

**Usage:**
```python
from analysis_engines.driver_analysis import PaceAnalyzer

analyzer = PaceAnalyzer()
result = analyzer.analyze_pace(lap_data, driver='VER')

print(f"Fastest lap: {result['fastest_lap']}")
print(f"Average pace: {result['avg_pace']}")
print(f"Sector 1 best: {result['best_sectors']['sector1']}")
```

**Output Example:**
```python
{
    'fastest_lap': '1:12.345',
    'avg_pace': '1:13.567',
    'best_sectors': {
        'sector1': 23.456,
        'sector2': 28.789,
        'sector3': 20.100
    },
    'pace_trend': 'improving',
    'fuel_corrected_pace': '1:12.890'
}
```

---

### Consistency Analyzer
**File:** `driver_analysis/consistency_analyzer.py`

**Purpose:** Measure driver lap-to-lap consistency

**Key Features:**
- Lap time standard deviation
- Consistency score (0-100)
- Outlier detection
- Performance variance analysis

**Usage:**
```python
from analysis_engines.driver_analysis import ConsistencyAnalyzer

analyzer = ConsistencyAnalyzer()
result = analyzer.analyze_consistency(lap_data, driver='VER')

print(f"Consistency score: {result['consistency_score']}")
print(f"Std deviation: {result['std_dev']} seconds")
print(f"Outliers: {result['outlier_count']}")
```

**Output Example:**
```python
{
    'consistency_score': 99.2,
    'std_dev': 0.124,
    'mean_lap_time': 78.456,
    'outlier_count': 2,
    'coefficient_of_variation': 0.158,
    'best_consecutive_laps': 15
}
```

---

## 🔗 Integration with Other Components

### Used By:
- **Comparison Engine** - Car and driver comparisons
- **API Routers** - REST API endpoints
- **Strategy Engines** - Strategic decision making

### Depends On:
- **Data Access Layer** - FastF1 data loading
- **Calculation Engines** - Low-level calculations
- **Telemetry Processor** - Data preprocessing

### Integration Example:
```python
# Comparison Engine uses multiple analyzers
from comparison_engine import ComparisonEngine

engine = ComparisonEngine()
result = engine.compare_cars(2024, 'Monaco', 'Q', 'VER', 'LEC')

# Internally uses:
# - SpeedAnalyzer for speed comparison
# - BrakingAnalyzer for braking zones
# - CornerAnalyzer for cornering performance
# - PaceAnalyzer for lap times
# - ConsistencyAnalyzer for driver stability
```

---

## 📈 Design Pattern

All analyzers follow a consistent pattern:

```python
class AnalyzerBase:
    def __init__(self, config: Optional[Dict] = None):
        """Initialize with optional configuration"""
        pass
    
    def analyze(self, data: pd.DataFrame, **kwargs) -> Dict[str, Any]:
        """
        Main analysis method
        
        Args:
            data: Telemetry or lap data
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with analysis results
        """
        pass
    
    def _validate_input(self, data: pd.DataFrame) -> bool:
        """Validate input data"""
        pass
    
    def _process_results(self, raw_results: Any) -> Dict[str, Any]:
        """Format results for consumption"""
        pass
```

---

## 🎯 Key Characteristics

### 1. **Domain Expertise**
Each analyzer embeds F1-specific knowledge:
- Car analyzers understand aerodynamics, power units, tyres
- Driver analyzers understand racecraft, consistency, pressure

### 2. **Telemetry Processing**
All analyzers work with high-frequency telemetry:
- 300 Hz GPS data
- Speed, throttle, brake, gear, DRS
- Distance-based and time-based analysis

### 3. **Statistical Rigor**
Analyzers use proven statistical methods:
- Mean, median, standard deviation
- Outlier detection (IQR method)
- Trend analysis (regression)

### 4. **Composability**
Analyzers can be combined:
```python
# Multi-dimensional analysis
speed_result = speed_analyzer.analyze(telemetry)
braking_result = braking_analyzer.analyze(telemetry)
corner_result = corner_analyzer.analyze(telemetry)

# Aggregate results
comprehensive_analysis = {
    'speed': speed_result,
    'braking': braking_result,
    'cornering': corner_result
}
```

---

## 🚀 Performance Considerations

### Optimization Techniques:
- **Vectorized Operations** - NumPy/Pandas for batch processing
- **Lazy Evaluation** - Only compute what's needed
- **Caching** - Cache frequently accessed results
- **Parallel Processing** - Independent analyzers run in parallel

### Typical Processing Times:
- Single lap analysis: 10-50ms
- Full session analysis: 100-500ms
- Multi-driver comparison: 200-1000ms

---

## 🧪 Testing

Each analyzer has comprehensive tests:

```bash
# Run all analysis engine tests
pytest analysis_engines/car_analysis/
pytest analysis_engines/driver_analysis/
```

Test coverage includes:
- Edge cases (empty data, single lap, outliers)
- Known race scenarios (Monaco quali, Monza race)
- Cross-validation with historical data

---

## 📊 Real-World Applications

### 1. **Qualifying Analysis**
```python
# Identify where driver loses time
speed_analysis = speed_analyzer.analyze(quali_telemetry)
corner_analysis = corner_analyzer.analyze(quali_telemetry)

# Find weakest corner
weakest = min(corner_analysis['corners'], 
              key=lambda c: c['time_delta'])
print(f"Losing time in corner {weakest['number']}")
```

### 2. **Race Strategy**
```python
# Analyze pace degradation
pace_analysis = pace_analyzer.analyze(race_laps)

if pace_analysis['pace_trend'] == 'degrading':
    print("Consider pit stop soon")
```

### 3. **Car Development**
```python
# Compare setup changes
baseline = speed_analyzer.analyze(fp1_telemetry)
updated = speed_analyzer.analyze(fp3_telemetry)

delta = updated['max_speed'] - baseline['max_speed']
print(f"Setup change gained {delta} km/h")
```

---

## 🎓 Summary

The **Analysis Engines** transform raw telemetry into racing intelligence:

✅ **6 Specialized Analyzers** - Car (4) + Driver (2)  
✅ **Domain Expertise** - F1-specific analytical knowledge  
✅ **Statistical Rigor** - Proven mathematical methods  
✅ **High Performance** - Optimized for real-time analysis  
✅ **Composable** - Combine for comprehensive insights  

These engines power the comparison engine, API endpoints, and strategic decision-making throughout the platform.
