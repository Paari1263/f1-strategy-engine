# API Examples & Usage Guide

## 🚀 Getting Started

### Start the Servers
```bash
# Main API Server (Port 8000)
cd /path/to/f1-race-strategy-simulator
source venv/bin/activate
uvicorn api.main:app --port 8000 --reload

# Or Engines Server (Port 8001)
uvicorn engines.main:app --port 8001 --reload
```

### Access Documentation
- **Main API Swagger UI:** http://localhost:8000/docs
- **Main API ReDoc:** http://localhost:8000/redoc
- **Engines Swagger UI:** http://localhost:8001/docs
- **Engines ReDoc:** http://localhost:8001/redoc

---

## 📋 Table of Contents

1. [Comparison API](#comparison-api) - 5 endpoints
2. [Driver Insights API](#driver-insights-api) - 2 endpoints
3. [Strategy API](#strategy-api) - 2 endpoints
4. [Visualization API](#visualization-api) - 7 endpoints
5. [Quick Test Suite](#quick-test-suite)

---

## 1️⃣ Comparison API (5 Endpoints)

### 🏎️ Car Performance Comparison (Standard)

**Endpoint:** `GET /api/v1/compare/cars/performance`

**Purpose:** Compare overall car performance between two drivers

**Example Requests:**

```bash
# Monaco Qualifying - Verstappen vs Leclerc
curl "http://localhost:8000/api/v1/compare/cars/performance?year=2024&event=Monaco&session=Q&driver1=VER&driver2=LEC"

# Silverstone Race - Hamilton vs Russell
curl "http://localhost:8000/api/v1/compare/cars/performance?year=2024&event=Silverstone&session=R&driver1=HAM&driver2=RUS"
```

---

### 🔬 Car Performance Comparison (Detailed)

**Endpoint:** `GET /api/v1/compare/cars/performance/detailed`

**Purpose:** Detailed car analysis with power, aero, drag, grip, ERS, thermal profiles

**Example:**
```bash
curl "http://localhost:8000/api/v1/compare/cars/performance/detailed?year=2024&event=Bahrain&session=R&driver1=VER&driver2=PER"
```

---

### 🛞 Tyre Performance Comparison

**Endpoint:** `GET /api/v1/compare/cars/tyre-performance`

**Purpose:** Compare tyre management and degradation

**Parameters:** year, event, session, driver1, driver2, **compound**

**Example:**
```bash
curl "http://localhost:8000/api/v1/compare/cars/tyre-performance?year=2024&event=Monaco&session=R&driver1=LEC&driver2=SAI&compound=SOFT"
```

---

### ⏱️ Driver Pace Comparison

**Endpoint:** `GET /api/v1/compare/drivers/pace`

**Purpose:** Compare lap time performance between drivers

**Parameters:** year, event, session, driver1, driver2, fuel_corrected (optional)

**Example:**
```bash
# With fuel correction
curl "http://localhost:8000/api/v1/compare/drivers/pace?year=2023&event=Silverstone&session=R&driver1=HAM&driver2=RUS&fuel_corrected=true"
```

---

### 📊 Driver Consistency Comparison

**Endpoint:** `GET /api/v1/compare/drivers/consistency`

**Purpose:** Compare consistency metrics and lap time variation

**Example:**
```bash
curl "http://localhost:8000/api/v1/compare/drivers/consistency?year=2024&event=Monaco&session=R&driver1=VER&driver2=PER"
```

---

**Query Parameters:**

| Parameter | Type | Required | Description | Valid Values | Example |
|-----------|------|----------|-------------|--------------|---------|
| `year` | integer | ✅ Yes | F1 season year | 2018-2025 | `2024` |
| `event` | string | ✅ Yes | Grand Prix name | See [GP Events](#popular-grand-prix-events) | `"Monaco"` |
| `session` | string | ✅ Yes | Session type | `FP1`, `FP2`, `FP3`, `Q`, `S`, `R` | `"Q"` |
| `driver1` | string | ✅ Yes | First driver code | 3-letter code (see below) | `"VER"` |
| `driver2` | string | ✅ Yes | Second driver code | 3-letter code (see below) | `"LEC"` |

**Session Type Details:**
- `FP1` - Free Practice 1 (Friday morning)
- `FP2` - Free Practice 2 (Friday afternoon)
- `FP3` - Free Practice 3 (Saturday morning)
- `Q` - Qualifying (Saturday afternoon)
- `S` - Sprint (Sprint race format weekends)
- `R` - Race (Sunday, main event)

**Driver Codes:**
```
2024 Season Drivers:
VER - Max Verstappen (Red Bull)          LEC - Charles Leclerc (Ferrari)
PER - Sergio Perez (Red Bull)            SAI - Carlos Sainz (Ferrari)
HAM - Lewis Hamilton (Mercedes)          RUS - George Russell (Mercedes)
NOR - Lando Norris (McLaren)             PIA - Oscar Piastri (McLaren)
ALO - Fernando Alonso (Aston Martin)     STR - Lance Stroll (Aston Martin)
GAS - Pierre Gasly (Alpine)              OCO - Esteban Ocon (Alpine)
HUL - Nico Hulkenberg (Haas)             MAG - Kevin Magnussen (Haas)
TSU - Yuki Tsunoda (AlphaTauri)          RIC - Daniel Ricciardo (AlphaTauri)
BOT - Valtteri Bottas (Alfa Romeo)       ZHO - Zhou Guanyu (Alfa Romeo)
ALB - Alexander Albon (Williams)         SAR - Logan Sargeant (Williams)
LAW - Liam Lawson (Reserve/Sub)          DEV - Nyck de Vries (Reserve/Sub)
```

**Response Example:**
```json
{
  "driver1": "VER",
  "driver2": "LEC",
  "fastest_lap1": "1:12.345",
  "fastest_lap2": "1:12.567",
  "delta_seconds": -0.222,
  "winner": "VER",
  "power_delta_percent": 1.5,
  "drag_penalty_percent": -2.3,
  "mechanical_grip_delta_percent": 0.8,
  "metadata": {
    "year": 2024,
    "event": "Monaco",
    "session": "Q"
  }
}
```

---

### 🏎️ Compare Cars (Detailed)

**Endpoint:** `GET /api/v1/compare/cars/performance/detailed`

**Purpose:** Get comprehensive performance analysis with structured JSON

**Example Requests:**

```bash
# Monaco Qualifying - Full Analysis
curl "http://localhost:8001/api/v1/compare/cars/performance/detailed?year=2024&event=Monaco&session=Q&driver1=VER&driver2=LEC"

# Bahrain Race - Race Pace Comparison
curl "http://localhost:8001/api/v1/compare/cars/performance/detailed?year=2024&event=Bahrain&session=R&driver1=VER&driver2=PER"

# Singapore Night Race
curl "http://localhost:8001/api/v1/compare/cars/performance/detailed?year=2024&event=Singapore&session=Q&driver1=NOR&driver2=PIA"
```

**Query Parameters:**

| Parameter | Type | Required | Description | Valid Values | Example |
|-----------|------|----------|-------------|--------------|---------|
| `year` | integer | ✅ Yes | F1 season year | 2018-2025 | `2024` |
| `event` | string | ✅ Yes | Grand Prix name | See [GP Events](#popular-grand-prix-events) | `"Monaco"` |
| `session` | string | ✅ Yes | Session type | `FP1`, `FP2`, `FP3`, `Q`, `S`, `R` | `"Q"` |
| `driver1` | string | ✅ Yes | First driver code | 3-letter code | `"VER"` |
| `driver2` | string | ✅ Yes | Second driver code | 3-letter code | `"LEC"` |

**Response Structure:**
```json
{
  "car1": {
    "metadata": {
      "team": "Red Bull Racing",
      "car": "RB20",
      "session_key": 9472,
      "track": "Monaco",
      "driver": "VER"
    },
    "performance_profile": {
      "powerDelta": 1.5,
      "aeroDelta": -0.8,
      "dragPenalty": -2.3,
      "mechanicalGripDelta": 0.8
    },
    "tyre_interaction": {
      "tyreEnergyLoad": {
        "soft": 85,
        "medium": 78,
        "hard": 72
      },
      "fuelWeightSensitivity": 0.035
    },
    "aero_behavior": {
      "downforceSensitivity": 7.2,
      "dirtyAirAmplification": 1.25
    },
    "thermal_profile": {
      "coolingSensitivity": {
        "engine": 0.8,
        "brakes": 0.9
      }
    },
    "ers_profile": {
      "ersEfficiency": 92
    },
    "reliability_profile": {
      "reliabilityStress": 65,
      "pushFailureRisk": 0.08
    },
    "setup_profile": {
      "kerbCompliance": 75,
      "setupFlexibility": 8
    },
    "session_bias": {
      "qualifyingRaceBias": {
        "qualifyingBias": 0.6,
        "raceBias": 0.4
      }
    }
  },
  "car2": { /* same structure */ },
  "delta_analysis": {
    "powerDelta": 0.3,
    "aeroDelta": -0.5,
    "mechanicalGripDelta": 0.2,
    /* ... more deltas */
  },
  "overall_advantage": "VER"
}
```

---

### 👤 Compare Drivers

**Endpoint:** `GET /api/v1/compare/drivers`

**Purpose:** Analyze driver performance and characteristics

**Example Requests:**

```bash
# Verstappen vs Hamilton - Battle Analysis
curl "http://localhost:8001/api/v1/compare/drivers?year=2024&event=Monaco&session=Q&driver1=VER&driver2=HAM"

# Norris vs Piastri - Teammate Comparison
curl "http://localhost:8001/api/v1/compare/drivers?year=2024&event=Silverstone&session=R&driver1=NOR&driver2=PIA"

# Alonso vs Stroll - Experience Gap
curl "http://localhost:8001/api/v1/compare/drivers?year=2024&event=Bahrain&session=Q&driver1=ALO&driver2=STR"
```

**Query Parameters:**

| Parameter | Type | Required | Description | Valid Values | Example |
|-----------|------|----------|-------------|--------------|---------|
| `year` | integer | ✅ Yes | F1 season year | 2018-2025 | `2024` |
| `event` | string | ✅ Yes | Grand Prix name | See [GP Events](#popular-grand-prix-events) | `"Monaco"` |
| `session` | string | ✅ Yes | Session type | `FP1`, `FP2`, `FP3`, `Q`, `S`, `R` | `"Q"` |
| `driver1` | string | ✅ Yes | First driver code | 3-letter code | `"VER"` |
| `driver2` | string | ✅ Yes | Second driver code | 3-letter code | `"HAM"` |

**Response Example:**
```json
{
  "driver1": {
    "name": "VER",
    "consistency_score": 99.2,
    "error_risk_percent": 3.5,
    "racecraft_score": 88,
    "pressure_index": 95,
    "fastest_lap": "1:12.345"
  },
  "driver2": {
    "name": "HAM",
    "consistency_score": 98.8,
    "error_risk_percent": 4.2,
    "racecraft_score": 92,
    "pressure_index": 93,
    "fastest_lap": "1:12.456"
  },
  "delta_analysis": {
    "lap_time_delta": -0.111,
    "consistency_delta": 0.4,
    "racecraft_delta": -4,
    "winner": "VER"
  }
}
```

---

## 2️⃣ Driver Insights API (2 Endpoints)

### 👤 Driver Performance Profile

**Endpoint:** `GET /api/v1/insights/driver/performance`

**Purpose:** Comprehensive driver performance analysis including pace, consistency, and tire management

**Example Requests:**

```bash
# Verstappen - Bahrain Race Performance
curl "http://localhost:8000/api/v1/insights/driver/performance?year=2024&event=Bahrain&session=R&driver=VER"

# Hamilton - Silverstone Race Analysis
curl "http://localhost:8000/api/v1/insights/driver/performance?year=2024&event=Silverstone&session=R&driver=HAM"

# Leclerc - Monaco Qualifying
curl "http://localhost:8000/api/v1/insights/driver/performance?year=2024&event=Monaco&session=Q&driver=LEC"
```

**Query Parameters:**

| Parameter | Type | Required | Description | Valid Values | Example |
|-----------|------|----------|-------------|--------------|---------|
| `year` | integer | ✅ Yes | F1 season year | 2018-2025 | `2024` |
| `event` | string | ✅ Yes | Grand Prix name | See [GP Events](#popular-grand-prix-events) | `"Bahrain"` |
| `session` | string | ✅ Yes | Session type | `FP1`, `FP2`, `FP3`, `Q`, `S`, `R` | `"R"` |
| `driver` | string | ✅ Yes | Driver code | 3-letter code | `"VER"` |

**Response Example:**
```json
{
  "driver": "VER",
  "fastest_lap": "1:32.456",
  "average_lap_time": "1:33.245",
  "consistency_score": 99.2,
  "pace_rating": 98.5,
  "tire_management_score": 95.8,
  "sector_performance": {
    "sector1_avg": "28.456",
    "sector2_avg": "35.123",
    "sector3_avg": "29.666"
  },
  "metadata": {
    "year": 2024,
    "event": "Bahrain",
    "session": "R"
  }
}
```

---

### 🏁 Driver Stint Analysis

**Endpoint:** `GET /api/v1/insights/driver/stint-analysis`

**Purpose:** Detailed stint-by-stint performance breakdown for race sessions

**Example Requests:**

```bash
# Leclerc - Monaco Race Stint Analysis
curl "http://localhost:8000/api/v1/insights/driver/stint-analysis?year=2024&event=Monaco&session=R&driver=LEC"

# Hamilton - Silverstone Multi-Stint Analysis
curl "http://localhost:8000/api/v1/insights/driver/stint-analysis?year=2024&event=Silverstone&session=R&driver=HAM"

# Verstappen - Bahrain Race Stints
curl "http://localhost:8000/api/v1/insights/driver/stint-analysis?year=2024&event=Bahrain&session=R&driver=VER"
```

**Query Parameters:**

| Parameter | Type | Required | Description | Valid Values | Example |
|-----------|------|----------|-------------|--------------|---------|
| `year` | integer | ✅ Yes | F1 season year | 2018-2025 | `2024` |
| `event` | string | ✅ Yes | Grand Prix name | See [GP Events](#popular-grand-prix-events) | `"Monaco"` |
| `session` | string | ✅ Yes | Session type (usually R for stints) | `R` (Race) | `"R"` |
| `driver` | string | ✅ Yes | Driver code | 3-letter code | `"LEC"` |

**Response Example:**
```json
{
  "driver": "LEC",
  "total_stints": 2,
  "stints": [
    {
      "stint_number": 1,
      "compound": "SOFT",
      "start_lap": 1,
      "end_lap": 28,
      "total_laps": 28,
      "average_lap_time": "1:14.567",
      "degradation_rate": 0.045,
      "tire_life_used_percent": 95
    },
    {
      "stint_number": 2,
      "compound": "HARD",
      "start_lap": 29,
      "end_lap": 78,
      "total_laps": 50,
      "average_lap_time": "1:15.123",
      "degradation_rate": 0.028,
      "tire_life_used_percent": 88
    }
  ],
  "pit_stops": 1,
  "total_pit_time": "25.3s",
  "metadata": {
    "year": 2024,
    "event": "Monaco",
    "session": "R"
  }
}
```

---

## 3️⃣ Strategy API (2 Endpoints)

### ⛽ Pit Stop Optimization

**Endpoint:** `GET /api/v1/drivers/head-to-head`

**Purpose:** Direct driver comparison with battle prediction

**Example Requests:**

```bash
# Verstappen vs Leclerc - Championship Battle
curl "http://localhost:8001/api/v1/drivers/head-to-head?year=2024&event=Monaco&session=Q&driver1=VER&driver2=LEC"

# Norris vs Piastri - Teammate Rivalry
curl "http://localhost:8001/api/v1/drivers/head-to-head?year=2024&event=Silverstone&session=R&driver1=NOR&driver2=PIA"

# Hamilton vs Russell - Mercedes Showdown
curl "http://localhost:8001/api/v1/drivers/head-to-head?year=2024&event=Spa&session=Q&driver1=HAM&driver2=RUS"
```

**Query Parameters:**

| Parameter | Type | Required | Description | Valid Values | Example |
|-----------|------|----------|-------------|--------------|---------|
| `year` | integer | ✅ Yes | F1 season year | 2018-2025 | `2024` |
| `event` | string | ✅ Yes | Grand Prix name | See [GP Events](#popular-grand-prix-events) | `"Monaco"` |
| `session` | string | ✅ Yes | Session type | `FP1`, `FP2`, `FP3`, `Q`, `S`, `R` | `"Q"` |
| `driver1` | string | ✅ Yes | First driver code | 3-letter code | `"VER"` |
| `driver2` | string | ✅ Yes | Second driver code | 3-letter code | `"LEC"` |

**Response Example:**
```json
{
  "driver1": "VER",
  "driver2": "LEC",
  "pace_advantage_seconds": 0.15,
  "consistency_comparison": {
    "driver1_score": 99.2,
    "driver2_score": 98.5,
    "delta": 0.7
  },
  "racecraft_comparison": {
    "driver1_score": 88,
    "driver2_score": 85,
    "delta": 3
  },
  "battle_prediction": {
    "overtake_probability": 0.68,
    "winner_prediction": "VER",
    "confidence": 0.85
  },
  "lap_time_delta": -0.15,
  "metadata": {
    "year": 2024,
    "event": "Monaco",
    "session": "Q"
  }
}
```

---

## 3️⃣ Strategy API (2 Endpoints)

### ⛽ Pit Stop Optimization

**Endpoint:** `GET /api/v1/strategy/pit-optimization`

**Purpose:** Optimal pit stop timing and strategy recommendations

**Example Requests:**

```bash
# Leclerc - Monza Race Strategy
curl "http://localhost:8000/api/v1/strategy/pit-optimization?year=2024&event=Monza&session=R&driver=LEC"

# Verstappen - Monaco Strategy
curl "http://localhost:8000/api/v1/strategy/pit-optimization?year=2024&event=Monaco&session=R&driver=VER"

# Hamilton - Silverstone Pit Windows
curl "http://localhost:8000/api/v1/strategy/pit-optimization?year=2024&event=Silverstone&session=R&driver=HAM"
```

**Query Parameters:**

| Parameter | Type | Required | Description | Valid Values | Example |
|-----------|------|----------|-------------|--------------|---------|
| `year` | integer | ✅ Yes | F1 season year | 2018-2025 | `2024` |
| `event` | string | ✅ Yes | Grand Prix name | See [GP Events](#popular-grand-prix-events) | `"Monza"` |
| `session` | string | ✅ Yes | Session type (usually R for strategy) | `R` (Race) | `"R"` |
| `driver` | string | ✅ Yes | Driver code | 3-letter code | `"LEC"` |

**Response Example:**
```json
{
  "driver": "LEC",
  "optimal_strategy": "One-stop",
  "recommended_pit_lap": 35,
  "pit_window": {
    "earliest": 30,
    "optimal": 35,
    "latest": 42
  },
  "tyre_compounds": {
    "stint1": "SOFT",
    "stint2": "HARD"
  },
  "estimated_time_loss": "24.5s",
  "alternative_strategies": [
    {
      "strategy": "Two-stop",
      "pit_laps": [22, 44],
      "compounds": ["SOFT", "MEDIUM"],
      "estimated_time_loss": "48.8s"
    }
  ],
  "undercut_opportunity": true,
  "overcut_advantage_seconds": 1.2,
  "metadata": {
    "year": 2024,
    "event": "Monza",
    "session": "R"
  }
}
```

---

### ⚔️ Battle Forecast

**Endpoint:** `GET /api/v1/strategy/battle-forecast`

**Purpose:** Predict race outcome and battles between two drivers

**Example Requests:**

```bash
# Hamilton vs Russell - Mercedes Battle
curl "http://localhost:8000/api/v1/strategy/battle-forecast?year=2024&event=Silverstone&session=R&driver1=HAM&driver2=RUS"

# Verstappen vs Leclerc - Championship Fight
curl "http://localhost:8000/api/v1/strategy/battle-forecast?year=2024&event=Monaco&session=R&driver1=VER&driver2=LEC"

# Norris vs Piastri - Teammate Battle
curl "http://localhost:8000/api/v1/strategy/battle-forecast?year=2024&event=Monza&session=R&driver1=NOR&driver2=PIA"
```

**Query Parameters:**

| Parameter | Type | Required | Description | Valid Values | Example |
|-----------|------|----------|-------------|--------------|---------|
| `year` | integer | ✅ Yes | F1 season year | 2018-2025 | `2024` |
| `event` | string | ✅ Yes | Grand Prix name | See [GP Events](#popular-grand-prix-events) | `"Silverstone"` |
| `session` | string | ✅ Yes | Session type (usually R for battles) | `R` (Race) | `"R"` |
| `driver1` | string | ✅ Yes | First driver code | 3-letter code | `"HAM"` |
| `driver2` | string | ✅ Yes | Second driver code | 3-letter code | `"RUS"` |

**Response Example:**
```json
{
  "driver1": "HAM",
  "driver2": "RUS",
  "battle_prediction": {
    "winner": "HAM",
    "confidence": 0.72,
    "predicted_gap_seconds": 3.5
  },
  "overtake_probability": {
    "driver1_overtakes_driver2": 0.65,
    "driver2_overtakes_driver1": 0.35
  },
  "pace_comparison": {
    "driver1_avg_lap": "1:28.456",
    "driver2_avg_lap": "1:28.623",
    "delta_seconds": -0.167
  },
  "key_factors": [
    "Driver 1 has superior race pace",
    "DRS zones favor overtaking",
    "Tire strategy advantage for Driver 1"
  ],
  "metadata": {
    "year": 2024,
    "event": "Silverstone",
    "session": "R"
  }
}
```
```

**Query Parameters:**

| Parameter | Type | Required | Description | Valid Values | Example |
|-----------|------|----------|-------------|--------------|---------|
| `current_lap` | integer | ✅ Yes | Current lap number | 1 to `total_laps` | `15` |
| `total_laps` | integer | ✅ Yes | Total race distance | Circuit-specific (44-78 laps) | `78` |
| `current_compound` | string | ✅ Yes | Current tyre compound | `SOFT`, `MEDIUM`, `HARD`, `INTERMEDIATE`, `WET` | `"MEDIUM"` |
| `track` | string | ✅ Yes | Track/circuit name | See [GP Events](#popular-grand-prix-events) | `"Monaco"` |
| `year` | integer | ✅ Yes | F1 season year | 2018-2025 | `2024` |
| `current_tyre_age` | integer | ❌ No | Laps on current tyres | 0 to `current_lap` | `14` |
| `target_position` | integer | ❌ No | Desired finishing position | 1-20 | `5` |

**Response Example:**
```json
{
  "strategies": [
    {
      "name": "Conservative 1-Stop",
      "pit_laps": [45],
      "compounds": ["HARD"],
      "total_time_seconds": 6780.5,
      "risk_level": "low",
      "advantages": ["Predictable", "Safe"],
      "disadvantages": ["Slower pace"]
    },
    {
      "name": "Aggressive 2-Stop",
      "pit_laps": [25, 38],
      "compounds": ["SOFT", "SOFT"],
      "total_time_seconds": 6775.2,
      "risk_level": "high",
      "advantages": ["Faster pace", "Undercut potential"],
      "disadvantages": ["Traffic risk", "Time loss"]
    },
    {
      "name": "Balanced 1-Stop",
      "pit_laps": [35],
      "compounds": ["MEDIUM"],
      "total_time_seconds": 6778.0,
      "risk_level": "medium",
      "advantages": ["Flexible", "Balanced"],
      "disadvantages": ["Requires precision"]
    }
  ],
  "recommended": "Balanced 1-Stop",
  "metadata": {
    "track": "Monaco",
    "total_laps": 78
  }
}
```

---

### ⚡ Live Strategy Adjustment

**Endpoint:** `GET /api/v1/strategy/live-adjustment`

**Purpose:** Real-time strategy updates during race

**Example Requests:**

```bash
# Safety Car deployed - recalculate
curl "http://localhost:8001/api/v1/strategy/live-adjustment?current_lap=25&total_laps=58&current_compound=MEDIUM&tyre_age=24&event=safety_car&track=Silverstone&year=2024"

# Rain starting - change strategy
curl "http://localhost:8001/api/v1/strategy/live-adjustment?current_lap=18&total_laps=53&current_compound=SOFT&tyre_age=17&event=rain_start&track=Spa&year=2024"

# Competitor pits - react
curl "http://localhost:8001/api/v1/strategy/live-adjustment?current_lap=32&total_laps=71&current_compound=HARD&tyre_age=31&event=competitor_pit&track=Bahrain&year=2024"
```

**Query Parameters:**

| Parameter | Type | Required | Description | Valid Values | Example |
|-----------|------|----------|-------------|--------------|---------|
| `current_lap` | integer | ✅ Yes | Current lap number | 1 to `total_laps` | `25` |
| `total_laps` | integer | ✅ Yes | Total race distance | Circuit-specific (44-78 laps) | `58` |
| `current_compound` | string | ✅ Yes | Current tyre compound | `SOFT`, `MEDIUM`, `HARD`, `INTERMEDIATE`, `WET` | `"MEDIUM"` |
| `tyre_age` | integer | ✅ Yes | Laps on current tyres | 0 to `current_lap` | `24` |
| `event` | string | ✅ Yes | Race event trigger | See event types below | `"safety_car"` |
| `track` | string | ✅ Yes | Track/circuit name | See [GP Events](#popular-grand-prix-events) | `"Silverstone"` |
| `year` | integer | ✅ Yes | F1 season year | 2018-2025 | `2024` |
| `gap_ahead` | float | ❌ No | Gap to car ahead (seconds) | Any positive float | `2.5` |
| `gap_behind` | float | ❌ No | Gap to car behind (seconds) | Any positive float | `3.8` |
| `current_position` | integer | ❌ No | Current race position | 1-20 | `3` |

**Event Types:**

| Event Type | Description | Typical Action |
|------------|-------------|----------------|
| `safety_car` | Safety car deployed | Consider free pit stop |
| `vsc` | Virtual safety car | Evaluate pit opportunity |
| `rain_start` | Rain beginning | Switch to wet tyres |
| `rain_stop` | Track drying | Plan crossover to slicks |
| `competitor_pit` | Rival pits | React with undercut/overcut |
| `damage` | Car damage sustained | Conservative strategy |
| `red_flag` | Red flag/race stopped | Free tyre change opportunity |
| `drs_enabled` | DRS enabled | Adjust attack/defend strategy |

**Response Example:**
```json
{
  "original_strategy": {
    "pit_lap": 42,
    "compound": "MEDIUM"
  },
  "adjusted_strategy": {
    "pit_lap": 26,
    "compound": "HARD",
    "reason": "Safety car window - free pit stop"
  },
  "time_gain_seconds": 22.5,
  "track_position_change": "+2 positions",
  "risk_assessment": "low",
  "alternative_option": {
    "action": "Stay out",
    "reasoning": "Extend to next safety car",
    "risk": "medium"
  },
  "metadata": {
    "event": "safety_car",
    "current_lap": 25
  }
}
```

---

## 4️⃣ Visualization API (7 Endpoints)

### 📈 Speed Trace Comparison

**Endpoint:** `GET /api/v1/visualizations/speed-trace`

**Purpose:** Visualize speed profiles for two drivers

**Example Requests:**

```bash
# JSON format (interactive Plotly chart)
curl "http://localhost:8001/api/v1/visualizations/speed-trace?year=2024&event=Monaco&session=Q&driver1=VER&driver2=LEC&format=json"

# PNG format (static image)
curl "http://localhost:8001/api/v1/visualizations/speed-trace?year=2024&event=Monaco&session=Q&driver1=VER&driver2=LEC&format=png" --output speed_trace.png

# Monza top speed comparison
curl "http://localhost:8001/api/v1/visualizations/speed-trace?year=2024&event=Monza&session=Q&driver1=NOR&driver2=PIA&format=png" -o monza_speed.png
```

**Query Parameters:**

| Parameter | Type | Required | Description | Valid Values | Example |
|-----------|------|----------|-------------|--------------|---------|
| `year` | integer | ✅ Yes | F1 season year | 2018-2025 | `2024` |
| `event` | string | ✅ Yes | Grand Prix name | See [GP Events](#popular-grand-prix-events) | `"Monaco"` |
| `session` | string | ✅ Yes | Session type | `FP1`, `FP2`, `FP3`, `Q`, `S`, `R` | `"Q"` |
| `driver1` | string | ✅ Yes | First driver code | 3-letter code | `"VER"` |
| `driver2` | string | ✅ Yes | Second driver code | 3-letter code | `"LEC"` |
| `format` | string | ❌ No | Output format | `json`, `png` (default: `json`) | `"json"` |
| `lap_number` | integer | ❌ No | Specific lap to analyze | Valid lap number | `5` |

**Format Details:**
- `json` - Returns Plotly JSON for frontend rendering (interactive charts)
  - Response: `{"plotly_json": "{...}", "type": "plotly"}`
  - Use in web apps with Plotly.js
  - Enables zoom, pan, hover tooltips
  
- `png` - Returns PNG image file (static charts)
  - Content-Type: `image/png`
  - Resolution: 150 DPI (1200x800px)
  - Save with: `curl ... --output file.png`

**JSON Response:**
```json
{
  "plotly_json": "{\"data\": [...], \"layout\": {...}}",
  "type": "plotly"
}
```

**PNG Response:**
- Content-Type: `image/png`
- Binary image data (150 DPI)

---

### 🎚️ Throttle & Brake Analysis

**Endpoint:** `GET /api/v1/visualizations/throttle-brake`

**Purpose:** 3-panel view of speed, throttle, and brake application

**Example Requests:**

```bash
# Monaco corner analysis
curl "http://localhost:8001/api/v1/visualizations/throttle-brake?year=2024&event=Monaco&session=Q&driver1=VER&driver2=LEC&format=json"

# Silverstone braking zones
curl "http://localhost:8001/api/v1/visualizations/throttle-brake?year=2024&event=Silverstone&session=Q&driver1=HAM&driver2=RUS&format=png" -o throttle_brake.png
```

**Query Parameters:**

| Parameter | Type | Required | Description | Valid Values | Example |
|-----------|------|----------|-------------|--------------|---------|
| `year` | integer | ✅ Yes | F1 season year | 2018-2025 | `2024` |
| `event` | string | ✅ Yes | Grand Prix name | See [GP Events](#popular-grand-prix-events) | `"Monaco"` |
| `session` | string | ✅ Yes | Session type | `FP1`, `FP2`, `FP3`, `Q`, `S`, `R` | `"Q"` |
| `driver1` | string | ✅ Yes | First driver code | 3-letter code | `"VER"` |
| `driver2` | string | ✅ Yes | Second driver code | 3-letter code | `"LEC"` |
| `format` | string | ❌ No | Output format | `json`, `png` (default: `json`) | `"json"` |

**Chart Output:** 3-panel stacked chart showing:
1. **Speed (km/h)** - Speed comparison over lap distance
2. **Throttle (%)** - Throttle application (0-100%)
3. **Brake** - Braking zones (boolean on/off)

---

### 📦 Lap Time Distribution

**Endpoint:** `GET /api/v1/visualizations/lap-time-distribution`

**Purpose:** Box plot showing consistency for multiple drivers

**Example Requests:**

```bash
# Compare 3 drivers
curl "http://localhost:8001/api/v1/visualizations/lap-time-distribution?year=2024&event=Monaco&session=Q&drivers=VER,LEC,HAM&format=json"

# Full top 5 comparison
curl "http://localhost:8001/api/v1/visualizations/lap-time-distribution?year=2024&event=Silverstone&session=R&drivers=VER,NOR,LEC,PIA,HAM&format=png" -o lap_distribution.png

# Teammate comparison
curl "http://localhost:8001/api/v1/visualizations/lap-time-distribution?year=2024&event=Monza&session=Q&drivers=NOR,PIA&format=json"
```

**Query Parameters:**

| Parameter | Type | Required | Description | Valid Values | Example |
|-----------|------|----------|-------------|--------------|---------|
| `year` | integer | ✅ Yes | F1 season year | 2018-2025 | `2024` |
| `event` | string | ✅ Yes | Grand Prix name | See [GP Events](#popular-grand-prix-events) | `"Monaco"` |
| `session` | string | ✅ Yes | Session type | `FP1`, `FP2`, `FP3`, `Q`, `S`, `R` | `"Q"` |
| `drivers` | string | ✅ Yes | Comma-separated driver codes | 2-10 drivers (e.g., `"VER,LEC,HAM"`) | `"VER,LEC,HAM"` |
| `format` | string | ❌ No | Output format | `json`, `png` (default: `json`) | `"json"` |

**Chart Output:** Box plot showing:
- Median lap time (center line)
- 25th-75th percentile range (box)
- Min/max lap times (whiskers)
- Outliers (individual points)
- Color-coded by driver

---

### 📊 Sector Comparison

**Endpoint:** `GET /api/v1/visualizations/sector-comparison`

**Purpose:** Bar chart comparing sector times

**Example Requests:**

```bash
# Monaco sector analysis
curl "http://localhost:8001/api/v1/visualizations/sector-comparison?year=2024&event=Monaco&session=Q&driver1=VER&driver2=LEC&format=json"

# Spa sector comparison
curl "http://localhost:8001/api/v1/visualizations/sector-comparison?year=2024&event=Spa&session=Q&driver1=HAM&driver2=RUS&format=png" -o sectors.png

# Qualifying sector breakdown
curl "http://localhost:8001/api/v1/visualizations/sector-comparison?year=2024&event=Silverstone&session=Q&driver1=NOR&driver2=PIA&format=json"
```

**Query Parameters:**

| Parameter | Type | Required | Description | Valid Values | Example |
|-----------|------|----------|-------------|--------------|---------|
| `year` | integer | ✅ Yes | F1 season year | 2018-2025 | `2024` |
| `event` | string | ✅ Yes | Grand Prix name | See [GP Events](#popular-grand-prix-events) | `"Monaco"` |
| `session` | string | ✅ Yes | Session type | `FP1`, `FP2`, `FP3`, `Q`, `S`, `R` | `"Q"` |
| `driver1` | string | ✅ Yes | First driver code | 3-letter code | `"VER"` |
| `driver2` | string | ✅ Yes | Second driver code | 3-letter code | `"LEC"` |
| `format` | string | ❌ No | Output format | `json`, `png` (default: `json`) | `"json"` |

**Chart Output:** Grouped bar chart showing:
- Sector 1, Sector 2, Sector 3 times (seconds)
- Side-by-side comparison for both drivers
- Color-coded by driver
- Total lap time included

---

### 🛞 Tyre Degradation

**Endpoint:** `GET /api/v1/visualizations/tyre-degradation`

**Purpose:** Lap time vs tyre age by compound

**Example Requests:**

```bash
# Verstappen's race degradation
curl "http://localhost:8001/api/v1/visualizations/tyre-degradation?year=2024&event=Monaco&session=R&driver=VER&format=json"

# Hamilton's stint analysis
curl "http://localhost:8001/api/v1/visualizations/tyre-degradation?year=2024&event=Silverstone&session=R&driver=HAM&format=png" -o tyre_deg.png

# Multi-stint degradation
curl "http://localhost:8001/api/v1/visualizations/tyre-degradation?year=2024&event=Spa&session=R&driver=LEC&format=json"
```

**Query Parameters:**

| Parameter | Type | Required | Description | Valid Values | Example |
|-----------|------|----------|-------------|--------------|---------|
| `year` | integer | ✅ Yes | F1 season year | 2018-2025 | `2024` |
| `event` | string | ✅ Yes | Grand Prix name | See [GP Events](#popular-grand-prix-events) | `"Monaco"` |
| `session` | string | ✅ Yes | Session type (usually R for degradation) | `R` (Race) | `"R"` |
| `driver` | string | ✅ Yes | Driver code | 3-letter code | `"VER"` |
| `format` | string | ❌ No | Output format | `json`, `png` (default: `json`) | `"json"` |

**Chart Output:** Scatter plot with trend lines showing:
- Lap time (seconds) vs Tyre age (laps)
- Color-coded by compound (SOFT/MEDIUM/HARD)
- Linear regression trend for each stint
- Pit stop markers (vertical lines)
- Degradation rate displayed (s/lap)

---

### ⚙️ Gear Usage

**Endpoint:** `GET /api/v1/visualizations/gear-usage`

**Purpose:** Visualize gear changes throughout lap

**Example Requests:**

```bash
# Monaco low-speed circuit
curl "http://localhost:8001/api/v1/visualizations/gear-usage?year=2024&event=Monaco&session=Q&driver=VER&format=json"

# Monza high-speed analysis
curl "http://localhost:8001/api/v1/visualizations/gear-usage?year=2024&event=Monza&session=Q&driver=NOR&format=png" -o gears.png

# Spa mixed-speed circuit
curl "http://localhost:8001/api/v1/visualizations/gear-usage?year=2024&event=Spa&session=Q&driver=HAM&format=json"
```

**Query Parameters:**

| Parameter | Type | Required | Description | Valid Values | Example |
|-----------|------|----------|-------------|--------------|---------|
| `year` | integer | ✅ Yes | F1 season year | 2018-2025 | `2024` |
| `event` | string | ✅ Yes | Grand Prix name | See [GP Events](#popular-grand-prix-events) | `"Monaco"` |
| `session` | string | ✅ Yes | Session type | `FP1`, `FP2`, `FP3`, `Q`, `S`, `R` | `"Q"` |
| `driver` | string | ✅ Yes | Driver code | 3-letter code | `"VER"` |
| `format` | string | ❌ No | Output format | `json`, `png` (default: `json`) | `"json"` |

**Chart Output:** Gear vs Distance plot showing:
- Gear number (1-8) vs Lap distance (meters)
- Color-coded by gear
- Corner locations marked
- Gear shift points highlighted
- Useful for setup analysis and driver comparison

---

### 🎯 Performance Radar

**Endpoint:** `GET /api/v1/visualizations/performance-radar`

**Purpose:** Multi-metric radar chart (5 metrics)

**Metrics:**
- Top Speed (km/h)
- Consistency Score (0-100)
- Braking Performance (0-100)
- Cornering Speed Average (km/h)
- Throttle Application (0-100%)

**Example Requests:**

```bash
# Verstappen vs Leclerc overall performance
curl "http://localhost:8001/api/v1/visualizations/performance-radar?year=2024&event=Monaco&session=Q&driver1=VER&driver2=LEC&format=json"

# Norris vs Piastri teammate comparison
curl "http://localhost:8001/api/v1/visualizations/performance-radar?year=2024&event=Silverstone&session=R&driver1=NOR&driver2=PIA&format=png" -o radar.png

# Hamilton vs Russell Mercedes comparison
curl "http://localhost:8001/api/v1/visualizations/performance-radar?year=2024&event=Spa&session=Q&driver1=HAM&driver2=RUS&format=json"
```

**Query Parameters:**

| Parameter | Type | Required | Description | Valid Values | Example |
|-----------|------|----------|-------------|--------------|---------|
| `year` | integer | ✅ Yes | F1 season year | 2018-2025 | `2024` |
| `event` | string | ✅ Yes | Grand Prix name | See [GP Events](#popular-grand-prix-events) | `"Monaco"` |
| `session` | string | ✅ Yes | Session type | `FP1`, `FP2`, `FP3`, `Q`, `S`, `R` | `"Q"` |
| `driver1` | string | ✅ Yes | First driver code | 3-letter code | `"VER"` |
| `driver2` | string | ✅ Yes | Second driver code | 3-letter code | `"LEC"` |
| `format` | string | ❌ No | Output format | `json`, `png` (default: `json`) | `"json"` |

**Chart Output:** Radar/spider chart showing:
- 5 performance metrics normalized (0-100)
- Overlaid comparison of both drivers
- Filled areas for visual comparison
- Legend with driver names
- Ideal for at-a-glance performance overview

---

### ✅ Health Check

**Endpoint:** `GET /api/v1/visualizations/health`

**Purpose:** Check visualization library availability

**Example Request:**

```bash
curl "http://localhost:8001/api/v1/visualizations/health"
```

**Response:**
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

## 🧪 Quick Test Suite

### Run All Comparison Tests
```bash
# Test all comparison endpoints (Port 8000)
curl "http://localhost:8000/api/v1/compare/cars/performance?year=2024&event=Monaco&session=Q&driver1=VER&driver2=LEC"
curl "http://localhost:8000/api/v1/compare/cars/performance/detailed?year=2024&event=Monaco&session=Q&driver1=VER&driver2=LEC"
curl "http://localhost:8000/api/v1/compare/cars/tyre-performance?year=2024&event=Monaco&session=R&driver1=VER&driver2=LEC&compound=SOFT"
curl "http://localhost:8000/api/v1/compare/drivers/pace?year=2024&event=Monaco&session=Q&driver1=VER&driver2=LEC"
curl "http://localhost:8000/api/v1/compare/drivers/consistency?year=2024&event=Monaco&session=R&driver1=VER&driver2=LEC"
```

### Run All Driver Insights Tests
```bash
# Test driver insights endpoints (Port 8000)
curl "http://localhost:8000/api/v1/insights/driver/performance?year=2024&event=Monaco&session=R&driver=VER"
curl "http://localhost:8000/api/v1/insights/driver/stint-analysis?year=2024&event=Monaco&session=R&driver=LEC"
```

### Run All Strategy Tests
```bash
# Test strategy endpoints (Port 8000)
curl "http://localhost:8000/api/v1/strategy/pit-optimization?year=2024&event=Monaco&session=R&driver=LEC"
curl "http://localhost:8000/api/v1/strategy/battle-forecast?year=2024&event=Silverstone&session=R&driver1=HAM&driver2=RUS"
```

### Run All Visualization Tests
```bash
# Test visualization endpoints (Port 8001)
curl "http://localhost:8001/api/v1/visualizations/health"
curl "http://localhost:8001/api/v1/visualizations/speed-trace?year=2024&event=Monaco&session=Q&driver1=VER&driver2=LEC&format=json" | jq '.type'
curl "http://localhost:8001/api/v1/visualizations/performance-radar?year=2024&event=Monaco&session=Q&driver1=VER&driver2=LEC&format=json" | jq '.type'
```

---

## � Query Parameters Glossary

### Complete Parameter Reference

This section provides a comprehensive reference for all query parameters used across all API endpoints.

#### Core Race Parameters

| Parameter | Type | Required | Used In | Description | Valid Values | Example |
|-----------|------|----------|---------|-------------|--------------|---------|
| `year` | integer | ✅ | All endpoints | F1 season year | 2018-2025 | `2024` |
| `event` | string | ✅ | All data endpoints | Grand Prix name | See [GP Events](#popular-grand-prix-events) | `"Monaco"` |
| `session` | string | ✅ | All data endpoints | Session type | `FP1`, `FP2`, `FP3`, `Q`, `S`, `R` | `"Q"` |
| `driver` | string | ✅ | Single-driver endpoints | Driver code | 3-letter code | `"VER"` |
| `driver1` | string | ✅ | Comparison endpoints | First driver code | 3-letter code | `"VER"` |
| `driver2` | string | ✅ | Comparison endpoints | Second driver code | 3-letter code | `"LEC"` |
| `drivers` | string | ✅ | Multi-driver endpoints | Comma-separated driver codes | 2-10 drivers | `"VER,LEC,HAM"` |

#### Visualization Parameters

| Parameter | Type | Required | Used In | Description | Valid Values | Example |
|-----------|------|----------|---------|-------------|--------------|---------|
| `format` | string | ❌ | All visualization endpoints | Output format | `json`, `png` (default: `json`) | `"json"` |
| `lap_number` | integer | ❌ | Visualization endpoints | Specific lap to analyze | Valid lap number | `5` |

**Format Details:**
- `json` - Returns Plotly JSON for frontend rendering (interactive)
  - Response: `{"plotly_json": "{...}", "type": "plotly"}`
  - Use in web apps with Plotly.js
  - Enables zoom, pan, hover tooltips
  
- `png` - Returns PNG image file (static)
  - Content-Type: `image/png`
  - Resolution: 150 DPI (1200x800px)
  - Save with: `curl ... --output file.png`

---

### Session Type Reference

| Code | Name | Day | Time | Purpose |
|------|------|-----|------|---------|
| `FP1` | Free Practice 1 | Friday | Morning | Initial car setup, track familiarization |
| `FP2` | Free Practice 2 | Friday | Afternoon | Race simulation, tyre testing |
| `FP3` | Free Practice 3 | Saturday | Morning | Final setup adjustments before qualifying |
| `Q` | Qualifying | Saturday | Afternoon | Grid position determination (Q1/Q2/Q3) |
| `S` | Sprint | Saturday | Afternoon | Short race (Sprint weekend format only) |
| `R` | Race | Sunday | Afternoon | Main event (full race distance) |

**Best Session for Analysis:**
- **Speed Analysis:** Qualifying (`Q`) - maximum attack, clean air
- **Consistency:** Race (`R`) - long runs, traffic
- **Degradation:** Race (`R`) - multiple stints
- **Racecraft:** Race (`R`) - wheel-to-wheel battles
- **Setup Evolution:** FP1→FP2→FP3→Q - track progression

---

### Tyre Compound Reference

| Compound | Code | Grip Level | Degradation | Typical Stint Length | Use Case |
|----------|------|-----------|-------------|---------------------|----------|
| **C5 (Soft)** | `SOFT` | Highest | Fastest | 10-20 laps | Qualifying, short stints |
| **C3-C4 (Medium)** | `MEDIUM` | Medium | Medium | 20-35 laps | Balanced race strategy |
| **C1-C2 (Hard)** | `HARD` | Lowest | Slowest | 30-50 laps | Long stints, one-stop |
| **Intermediate** | `INTERMEDIATE` | Wet | Variable | N/A | Light rain, drying track |
| **Wet** | `WET` | Wet | Variable | N/A | Heavy rain |

**Strategy Notes:**
- **Monaco:** Usually SOFT → MEDIUM (1-stop)
- **Monza:** SOFT → SOFT or MEDIUM → HARD (1-stop)
- **Silverstone:** MEDIUM → HARD or SOFT → MEDIUM → HARD (1 or 2-stop)
- **Spa:** MEDIUM → MEDIUM or SOFT → HARD (1-stop)

---

### Driver Code Reference (2024 Season)

| Code | Driver Name | Team | Number |
|------|-------------|------|--------|
| `VER` | Max Verstappen | Red Bull Racing | 1 |
| `PER` | Sergio Perez | Red Bull Racing | 11 |
| `LEC` | Charles Leclerc | Ferrari | 16 |
| `SAI` | Carlos Sainz | Ferrari | 55 |
| `HAM` | Lewis Hamilton | Mercedes | 44 |
| `RUS` | George Russell | Mercedes | 63 |
| `NOR` | Lando Norris | McLaren | 4 |
| `PIA` | Oscar Piastri | McLaren | 81 |
| `ALO` | Fernando Alonso | Aston Martin | 14 |
| `STR` | Lance Stroll | Aston Martin | 18 |
| `GAS` | Pierre Gasly | Alpine | 10 |
| `OCO` | Esteban Ocon | Alpine | 31 |
| `HUL` | Nico Hulkenberg | Haas | 27 |
| `MAG` | Kevin Magnussen | Haas | 20 |
| `TSU` | Yuki Tsunoda | AlphaTauri | 22 |
| `RIC` | Daniel Ricciardo | AlphaTauri | 3 |
| `BOT` | Valtteri Bottas | Alfa Romeo | 77 |
| `ZHO` | Zhou Guanyu | Alfa Romeo | 24 |
| `ALB` | Alexander Albon | Williams | 23 |
| `SAR` | Logan Sargeant | Williams | 2 |
| `LAW` | Liam Lawson | Reserve/Sub | - |
| `DEV` | Nyck de Vries | Reserve/Sub | - |

---

### Race Distance Reference (Lap Counts)

| Circuit | Event Name | Typical Laps | Distance (km) |
|---------|------------|--------------|---------------|
| Monaco | Monaco | 78 | 260.5 |
| Spa | Belgian GP | 44 | 308.1 |
| Monza | Italian GP | 53 | 306.7 |
| Silverstone | British GP | 52 | 306.2 |
| Bahrain | Bahrain GP | 57 | 308.2 |
| Jeddah | Saudi Arabian GP | 50 | 308.5 |
| Melbourne | Australian GP | 58 | 306.1 |
| Suzuka | Japanese GP | 53 | 307.5 |
| Austin | United States GP | 56 | 308.4 |
| Mexico City | Mexican GP | 71 | 305.4 |
| Brazil | São Paulo GP | 71 | 305.9 |
| Las Vegas | Las Vegas GP | 50 | 309.9 |
| Abu Dhabi | Abu Dhabi GP | 58 | 307.6 |

**Note:** Race distances vary slightly year-to-year based on track modifications.

---

## �📚 Popular Grand Prix Events

### 2024 Season Events
```
"Bahrain"      - Season opener, high speed
"Jeddah"       - Street circuit, Saudi Arabia
"Melbourne"    - Albert Park, Australia
"Imola"        - Emilia Romagna GP, Italy
"Miami"        - Street circuit, USA
"Monaco"       - Legendary street circuit
"Barcelona"    - Catalunya, Spain
"Montreal"     - Circuit Gilles Villeneuve, Canada
"Silverstone"  - British GP, high-speed corners
"Austria"      - Red Bull Ring, short lap
"Spa"          - Belgian GP, longest circuit
"Monza"        - Italian GP, fastest track
"Singapore"    - Night race, street circuit
"Suzuka"       - Japanese GP, figure-8 layout
"Austin"       - Circuit of the Americas, USA
"Mexico"       - High altitude, unique challenges
"Brazil"       - Interlagos, counter-clockwise
"Las Vegas"    - Night race, Nevada Strip
"Qatar"        - Lusail, middle-east
"Abu Dhabi"    - Season finale, Yas Marina
```

---

## 🎓 Response Format Notes

### JSON Responses
- All endpoints return valid JSON
- Include metadata (year, event, session)
- Timestamps in ISO 8601 format
- Decimal precision: 2-3 places

### Error Responses
```json
{
  "detail": "Session not found",
  "status_code": 404
}
```

### HTTP Status Codes
- `200 OK` - Success
- `400 Bad Request` - Invalid parameters
- `404 Not Found` - Session/driver not found
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Library missing (visualizations)

---

## 💡 Pro Tips

### 1. Use Qualifying for Clean Comparisons
Qualifying sessions have:
- Clean air (no traffic)
- Maximum push (representative pace)
- Consistent conditions

### 2. Use Race for Strategy Analysis
Race sessions provide:
- Degradation data
- Traffic impact
- Multiple stints

### 3. Cache Results Locally
FastF1 caches data, but API calls can still take 1-3 seconds. Cache responses for repeated queries.

### 4. Combine Endpoints
```bash
# Get full analysis
curl "http://localhost:8001/api/v1/compare/cars/performance/detailed?..."
curl "http://localhost:8001/api/v1/visualizations/speed-trace?..."
curl "http://localhost:8001/api/v1/visualizations/performance-radar?..."
```

### 5. Use Python for Automation
```python
import requests

BASE_URL = "http://localhost:8001"

# Get comparison
response = requests.get(f"{BASE_URL}/api/v1/compare/cars", params={
    "year": 2024,
    "event": "Monaco",
    "session": "Q",
    "driver1": "VER",
    "driver2": "LEC"
})

data = response.json()
print(f"Winner: {data['winner']}")
print(f"Delta: {data['delta_seconds']}s")
```

---

## 🎉 Ready to Explore!

All 17 endpoints are production-ready with comprehensive test coverage. Explore the Swagger UI at http://localhost:8001/docs for interactive testing and detailed schema documentation.
