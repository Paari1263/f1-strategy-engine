# F1 Strategy Engine - API Documentation

## Overview
REST APIs providing comprehensive F1 race strategy insights and analysis.

## Available Endpoints

### 🏎️ Car Comparisons

#### 1. Car Performance Comparison (Detailed)
**GET** `/api/v1/compare/cars/performance/detailed`

Get comprehensive car performance analysis with detailed metrics in structured format.

**Parameters:**
- `year` (int): Season year
- `event` (str): Grand Prix name (e.g., "Monaco", "Silverstone")
- `session` (SessionType): Session type (FP1, FP2, FP3, Q, R)
- `driver1` (str): First driver code (e.g., "VER")
- `driver2` (str): Second driver code (e.g., "LEC")

**Returns:**
Structured JSON with detailed profiles for both cars:
- **metadata**: Team, car, session_key, track, driver
- **performance_profile**: powerDelta, aeroDelta, dragPenalty, mechanicalGripDelta
- **tyre_interaction**: tyreEnergyLoad (soft/medium/hard), fuelWeightSensitivity
- **aero_behavior**: downforceSensitivity, dirtyAirAmplification
- **thermal_profile**: coolingSensitivity (engine, brakes)
- **ers_profile**: ersEfficiency
- **reliability_profile**: reliabilityStress, pushFailureRisk
- **setup_profile**: kerbCompliance, setupFlexibility
- **session_bias**: qualifyingRaceBias (qualifyingBias, raceBias)
- **delta_analysis**: Comparative deltas between both cars
- **overall_advantage**: Winner determination

**Example:**
```bash
curl "http://localhost:8001/api/v1/compare/cars/performance/detailed?year=2024&event=Monaco&session=Q&driver1=VER&driver2=LEC"
```

**Response Format:**
```json
{
  "car1": {
    "metadata": {
      "team": "McLaren",
      "car": "MCL24",
      "session_key": 9472,
      "track": "Monaco",
      "driver": "VER"
    },
    "performance_profile": {
      "powerDelta": 1.0,
      "aeroDelta": 0.85,
      "dragPenalty": 1.0,
      "mechanicalGripDelta": 1.0
    },
    "tyre_interaction": {
      "tyreEnergyLoad": {
        "soft": 0.59,
        "medium": 0.53,
        "hard": 0.47
      },
      "fuelWeightSensitivity": 0.029
    },
    "aero_behavior": {
      "downforceSensitivity": 0.6,
      "dirtyAirAmplification": 1.19
    },
    "thermal_profile": {
      "coolingSensitivity": {
        "engine": 0.7,
        "brakes": 0.6
      }
    },
    "ers_profile": {
      "ersEfficiency": 0.8
    },
    "reliability_profile": {
      "reliabilityStress": 0.0,
      "pushFailureRisk": 0.0
    },
    "setup_profile": {
      "kerbCompliance": 0.75,
      "setupFlexibility": 0.55
    },
    "session_bias": {
      "qualifyingRaceBias": {
        "qualifyingBias": 0.75,
        "raceBias": 0.95
      }
    }
  },
  "car2": { ... },
  "delta_analysis": {
    "power_delta": 0.0,
    "aero_delta": 0.0,
    ...
  },
  "overall_advantage": "VER"
}
```

#### 2. Car Performance Comparison (Legacy)
**GET** `/api/v1/compare/cars/performance`

Compare detailed car performance between two drivers.

**Parameters:**
- `year` (int): Season year
- `event` (str): Grand Prix name (e.g., "Monaco", "Silverstone")
- `session` (SessionType): Session type (FP1, FP2, FP3, Q, R)
- `driver1` (str): First driver code (e.g., "VER")
- `driver2` (str): Second driver code (e.g., "LEC")

**Returns:**
- Speed analysis (top speed, average, straight-line, cornering)
- Braking performance comparison
- Cornering analysis
- Lap time delta
- Overall winner

**Example:**
```bash
curl "http://localhost:8001/api/v1/compare/cars/performance?year=2024&event=Monaco&session=Q&driver1=VER&driver2=LEC"
```

#### 3. Tyre Performance Comparison
**GET** `/api/v1/compare/cars/tyre-performance`

Compare tyre management and degradation between two drivers.

**Parameters:**
- `year` (int): Season year
- `event` (str): Grand Prix name
- `session` (SessionType): Session type
- `driver1` (str): First driver code
- `driver2` (str): Second driver code
- `compound` (CompoundType): Tyre compound (SOFT, MEDIUM, HARD)

**Returns:**
- Degradation rate per lap
- Grip loss percentage
- Pace falloff over stint
- Optimal tyre life
- Better management score

**Example:**
```bash
curl "http://localhost:8001/api/v1/compare/cars/tyre-performance?year=2024&event=Barcelona&session=R&driver1=HAM&driver2=RUS&compound=HARD"
```

### 👥 Driver Comparisons

#### 4. Driver Pace Comparison
**GET** `/api/v1/compare/drivers/pace`

Compare driver pace across different metrics.

**Parameters:**
- `year` (int): Season year
- `event` (str): Grand Prix name
- `session` (SessionType): Session type
- `driver1` (str): First driver code
- `driver2` (str): Second driver code
- `fuel_corrected` (bool, optional): Apply fuel correction (default: false)

**Returns:**
- Fastest lap times
- Median and average pace
- Fuel-corrected pace
- Pace delta
- Stint-by-stint comparison

**Example:**
```bash
curl "http://localhost:8001/api/v1/compare/drivers/pace?year=2024&event=Silverstone&session=R&driver1=VER&driver2=NOR&fuel_corrected=true"
```

#### 5. Driver Consistency Comparison
**GET** `/api/v1/compare/drivers/consistency`

Compare driver consistency and lap time variance.

**Parameters:**
- `year` (int): Season year
- `event` (str): Grand Prix name
- `session` (SessionType): Session type
- `driver1` (str): First driver code
- `driver2` (str): Second driver code

**Returns:**
- Standard deviation
- Outlier lap count
- Clean lap percentage
- Consistency metrics

**Example:**
```bash
curl "http://localhost:8001/api/v1/compare/drivers/consistency?year=2024&event=Silverstone&session=R&driver1=VER&driver2=NOR"
```

### 🔍 Driver Insights

#### 6. Driver Performance Profile
**GET** `/api/v1/driver/performance-profile`

Detailed performance profile for a single driver.

**Parameters:**
- `year` (int): Season year
- `event` (str): Grand Prix name
- `session` (SessionType): Session type
- `driver` (str): Driver code

**Returns:**
- Pace metrics (fastest, median, average)
- Consistency analysis
- Tyre management scores
- Car performance metrics
- Strengths and weaknesses
- Overall performance rating (0-10)

**Example:**
```bash
curl "http://localhost:8001/api/v1/driver/performance-profile?year=2024&event=Monaco&session=Q&driver=VER"
```

#### 7. Driver Stint Analysis
**GET** `/api/v1/driver/stint-analysis`

Analyze stint-specific performance and degradation.

**Parameters:**
- `year` (int): Season year
- `event` (str): Grand Prix name
- `session` (SessionType): Session type
- `driver` (str): Driver code
- `stint_number` (int): Stint number to analyze

**Returns:**
- Pace evolution throughout stint
- Degradation curve
- Fuel effect on pace
- Stint statistics

### ⚡ Strategy Optimization

#### 8. Pit Strategy Optimization
**GET** `/api/v1/strategy/pit-optimization`

Calculate optimal pit stop strategy for current race situation.

**Parameters:**
- `year` (int): Season year
- `event` (str): Grand Prix name
- `driver` (str): Driver code
- `current_lap` (int): Current lap number
- `total_laps` (int): Total race laps
- `position` (int): Current race position (1-20)
- `current_compound` (CompoundType): Current tyre compound
- `tyre_age` (int): Current tyre age in laps
- `gap_ahead` (float, optional): Gap to car ahead (seconds)
- `gap_behind` (float, optional): Gap to car behind (seconds)

**Returns:**
- Optimal pit lap
- Pit window (start/end)
- Recommended compound
- Expected stint length
- Undercut/overcut advantages
- Strategy type classification
- Confidence score
- Alternative strategies

**Example:**
```bash
curl "http://localhost:8001/api/v1/strategy/pit-optimization?year=2024&event=Monaco&driver=VER&current_lap=25&total_laps=78&position=1&current_compound=MEDIUM&tyre_age=10"
```

#### 9. Battle Forecast
**GET** `/api/v1/strategy/battle-forecast`

Forecast overtaking probability and battle outcome.

**Parameters:**
- `year` (int): Season year
- `event` (str): Grand Prix name
- `session` (SessionType): Session type
- `lap` (int): Current lap number
- `attacker` (str): Attacking driver code
- `defender` (str): Defending driver code
- `gap` (float): Current gap in seconds
- `drs_available` (bool): DRS available for attacker

**Returns:**
- Overtake probability
- Best overtaking zone
- Recommended strategy
- Speed advantage
- DRS impact
- Track difficulty
- Key factors
- Lap-by-lap forecast

**Example:**
```bash
curl "http://localhost:8001/api/v1/strategy/battle-forecast?year=2024&event=Monza&session=R&lap=25&attacker=VER&defender=LEC&gap=0.8&drs_available=true"
```

## Running the Server

### Start the server:
```bash
cd f1-race-strategy-simulator
uvicorn engines.main:app --port 8001 --reload
```

### Test all endpoints:
```bash
python3 api/test_apis.py
```

### View interactive API documentation:
```
http://localhost:8001/docs
```

## Session Types
- `FP1`, `FP2`, `FP3` - Free Practice
- `Q`, `Q1`, `Q2`, `Q3` - Qualifying
- `R` - Race
- `S` - Sprint
- `SS` - Sprint Shootout

## Tyre Compounds
- `SOFT` - Soft compound
- `MEDIUM` - Medium compound
- `HARD` - Hard compound
- `INTERMEDIATE` - Intermediate (wet)
- `WET` - Full wet

## Response Format
All endpoints return JSON with:
- Success (200): Data object matching response model
- Error (500): Error object with message, type, and details

## Architecture
The APIs leverage existing calculation engines:
- **ComparisonEngine**: Car and driver comparisons
- **PitStrategySimulator**: Pit strategy optimization
- **BattleForecast**: Battle outcome prediction
- **29 calculation modules**: Core F1 analytics

## Visualization API

### 🎨 Visualization Endpoints

All visualization endpoints support dual output formats:
- **format=json**: Interactive Plotly JSON charts (for frontend rendering)
- **format=png**: Static PNG images (for reports/sharing)

#### 1. Speed Trace Comparison
**GET** `/api/v1/visualizations/speed-trace`

Compare speed traces between two drivers on their fastest laps.

**Parameters:**
- `year` (int): Season year
- `event` (str): Event name (e.g., "Monaco")
- `session` (str): Session type (FP1, FP2, FP3, Q, R)
- `driver1` (str): First driver code
- `driver2` (str): Second driver code
- `format` (str): Output format ("json" or "png")

**Example:**
```bash
# Get interactive JSON chart
curl "http://localhost:8001/api/v1/visualizations/speed-trace?year=2024&event=Monaco&session=Q&driver1=VER&driver2=LEC&format=json"

# Download PNG image
curl "http://localhost:8001/api/v1/visualizations/speed-trace?year=2024&event=Monaco&session=Q&driver1=VER&driver2=LEC&format=png" --output speed_trace.png
```

#### 2. Throttle & Brake Analysis
**GET** `/api/v1/visualizations/throttle-brake`

3-panel analysis showing speed, throttle application (0-100%), and brake application.

**Parameters:** Same as speed trace

#### 3. Lap Time Distribution
**GET** `/api/v1/visualizations/lap-time-distribution`

Box plot showing lap time distribution for multiple drivers.

**Parameters:**
- `drivers` (str): Comma-separated driver codes (e.g., "VER,LEC,HAM")

#### 4. Sector Comparison
**GET** `/api/v1/visualizations/sector-comparison`

Bar chart comparing sector times between two drivers.

**Parameters:** Same as speed trace

#### 5. Tyre Degradation
**GET** `/api/v1/visualizations/tyre-degradation`

Lap time vs tyre age, showing degradation by compound.

**Parameters:**
- `year`, `event`, `session`, `driver`, `format`

#### 6. Gear Usage
**GET** `/api/v1/visualizations/gear-usage`

Visualize gear changes throughout a lap.

**Parameters:**
- `year`, `event`, `session`, `driver`, `format`

#### 7. Performance Radar
**GET** `/api/v1/visualizations/performance-radar`

Multi-metric radar chart comparing:
- Top Speed
- Consistency
- Braking Performance
- Cornering Speed
- Throttle Application

**Parameters:** Same as speed trace

#### 8. Health Check
**GET** `/api/v1/visualizations/health`

Check if visualization libraries (Plotly, Matplotlib) are installed.

**Example Response:**
```json
{
  "status": "ok",
  "libraries": {
    "plotly": true,
    "matplotlib": true
  },
  "capabilities": {
    "json_charts": true,
    "png_images": true
  }
}
```

---

### 💾 Cache Management Endpoints

#### 1. Cache Statistics
**GET** `/api/v1/cache/stats`

Get cache hit/miss statistics and performance metrics.

**Returns:**
```json
{
  "hits": 1247,
  "misses": 153,
  "total_requests": 1400,
  "hit_rate": 89.07,
  "memory_usage_mb": 124.5,
  "keys_count": 342,
  "uptime_seconds": 3600
}
```

#### 2. Cache Warming
**POST** `/api/v1/cache/warm`

Pre-load cache for specific event/session to improve response times.

**Parameters:**
- `year` (int): Season year
- `event` (str): Grand Prix name
- `session` (str): Session type (FP1, FP2, FP3, Q, R)

**Example:**
```bash
curl -X POST "http://localhost:8001/api/v1/cache/warm?year=2024&event=Monaco&session=R"
```

**Returns:**
```json
{
  "status": "success",
  "message": "Cache warmed for 2024 Monaco R",
  "cached_items": 45,
  "duration_seconds": 78.3
}
```

#### 3. Clear Cache
**POST** `/api/v1/cache/clear`

Clear all cache or specific patterns.

**Parameters (optional):**
- `pattern` (str): Redis key pattern to clear (e.g., "f1:session:2024:*")

**Example:**
```bash
# Clear all cache
curl -X POST "http://localhost:8001/api/v1/cache/clear"

# Clear specific pattern
curl -X POST "http://localhost:8001/api/v1/cache/clear?pattern=f1:session:2024:Monaco:*"
```

**Returns:**
```json
{
  "status": "success",
  "message": "Cache cleared",
  "keys_deleted": 342
}
```

#### 4. Cache Health Check
**GET** `/api/v1/cache/health`

Check Redis connection and cache system health.

**Returns:**
```json
{
  "status": "healthy",
  "redis_connected": true,
  "redis_version": "7.2.0",
  "ping_ms": 1.2,
  "memory_usage_mb": 124.5,
  "uptime_seconds": 3600
}
```

---

## Testing Results
✅ All 9 comparison/driver/strategy endpoints tested and working
✅ All response models validated
✅ Integration with calculation engines verified
✅ Error handling implemented
✅ Detailed car comparison with structured JSON format
✅ 8 visualization endpoints with dual format support
✅ 4 cache management endpoints operational
✅ Multi-tier caching with 99% performance improvement

## Recent Updates (v2.0)

### ✅ Redis Caching Implemented
- **4-tier cache architecture** - Session/Computed/API/Reference layers
- **Dynamic TTL strategy** - 5min (live) → 24h (completed) → 7d (historical)
- **99% performance boost** - 20-90s → 50-200ms on cache hits
- **Cache management endpoints** - Stats, warming, clearing, health checks
- **Connection pooling** - Up to 50 concurrent Redis connections

### 🔧 Bug Fixes
- **Visualization APIs** - Fixed 5+ endpoints
  - `lap-time-distribution`: Robust type handling for LapTime values (timedelta/float/string)
  - `gear-usage`: Changed `.loc[idxmin()]` → `.pick_fastest()` for proper Lap object retrieval
  - Applied same fixes to speed-trace, throttle-brake, sector-comparison
- **Port standardization** - Changed from 8000 → 8001
- **Timeout increases** - 30s → 120-180s for FastF1 data loading
- **Type handling** - Added float()/int() conversions for numpy/pandas types

## Next Steps
Potential enhancements:
- ~~Add caching for frequently requested data~~ ✅ **COMPLETED**
- Implement authentication/rate limiting
- Add WebSocket support for real-time updates
- Expand to include qualifying simulations
- Add race pace predictions
- Include weather impact analysis
- Add heatmap visualizations for track analysis
- Implement animated lap comparisons
