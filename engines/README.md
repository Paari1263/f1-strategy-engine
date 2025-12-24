# Engine Services (Microservices)

## 🔧 Overview

The **Engine Services** provide domain-specific REST API endpoints following a microservice architecture pattern. Each engine handles a specific aspect of F1 race analysis and strategy.

---

## 📁 Structure

```
engines/
├── main.py                    # FastAPI application entry point
├── track_engine/              # Track characteristics & analysis
├── car_engine/                # Car performance metrics
├── tyre_engine/               # Tyre management & degradation
├── weather_engine/            # Weather impact analysis
├── traffic_engine/            # Traffic & overtaking
├── pit_engine/                # Pit stop strategy
├── safetycar_engine/          # Safety car scenarios
└── driver_engine/             # Driver-specific performance
```

---

## 🌐 Main Application

### `main.py`

**Purpose:** FastAPI application hosting all microservice engines on a single port (8001)

**Key Features:**
- Hosts 8 engine services + 4 API groups
- Swagger UI documentation at `/docs`
- ReDoc documentation at `/redoc`
- CORS enabled for cross-origin requests
- Global error handling middleware
- FastF1 client initialization on startup

**Start Server:**
```bash
uvicorn engines.main:app --port 8001 --reload
```

**API Documentation:**
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

---

## 🏎️ Individual Engine Services

### 1. Track Engine

**Path:** `track_engine/`  
**Prefix:** `/v1/engines/track`

**Purpose:** Track characteristics, grip evolution, sector analysis

**Endpoints:**
- `GET /characteristics` - Track layout and characteristics
- `GET /grip-evolution` - Grip progression across sessions
- `GET /sector-analysis` - Detailed sector breakdown
- `GET /corners` - Corner-by-corner analysis
- `GET /straights` - Straight sections and DRS zones

**Example:**
```bash
curl "http://localhost:8001/v1/engines/track/characteristics?track=Monaco"
```

**Use Cases:**
- Setup optimization
- Track familiarization
- Grip evolution prediction
- Overtaking zone identification

---

### 2. Car Engine

**Path:** `car_engine/`  
**Prefix:** `/v1/engines/car`

**Purpose:** Car performance analysis, setup, aerodynamics

**Endpoints:**
- `GET /performance` - Overall car performance metrics
- `GET /power-unit` - Power unit analysis
- `GET /aerodynamics` - Aero efficiency and downforce
- `GET /setup` - Current setup parameters
- `GET /comparison` - Car-to-car comparison

**Example:**
```bash
curl "http://localhost:8001/v1/engines/car/performance?year=2024&event=Monaco&driver=VER&session=Q"
```

**Use Cases:**
- Car development tracking
- Setup analysis
- Performance benchmarking
- Aero balance assessment

---

### 3. Tyre Engine

**Path:** `tyre_engine/`  
**Prefix:** `/v1/engines/tyre`

**Purpose:** Tyre compound selection, degradation, temperature management

**Endpoints:**
- `GET /degradation` - Degradation curves and predictions
- `GET /compound-performance` - Compound comparison
- `GET /thermal-analysis` - Temperature management
- `GET /life-prediction` - Stint length estimation
- `GET /allocation` - Available tyre sets

**Example:**
```bash
curl "http://localhost:8001/v1/engines/tyre/degradation?year=2024&event=Monaco&driver=VER&compound=SOFT"
```

**Use Cases:**
- Pit strategy planning
- Compound selection
- Stint length optimization
- Temperature management

---

### 4. Weather Engine

**Path:** `weather_engine/`  
**Prefix:** `/v1/engines/weather`

**Purpose:** Weather impact analysis, rain strategy, temperature effects

**Endpoints:**
- `GET /current` - Current weather conditions
- `GET /forecast` - Weather forecast
- `GET /impact` - Performance impact analysis
- `GET /grip-evolution` - Wet-to-dry grip changes
- `GET /crossover-point` - Tyre crossover prediction

**Example:**
```bash
curl "http://localhost:8001/v1/engines/weather/impact?year=2024&event=Silverstone&session=R"
```

**Use Cases:**
- Rain strategy decisions
- Tyre crossover timing
- Temperature impact assessment
- Risk evaluation

---

### 5. Traffic Engine

**Path:** `traffic_engine/`  
**Prefix:** `/v1/engines/traffic`

**Purpose:** Traffic analysis, overtaking opportunities, gap management

**Endpoints:**
- `GET /density` - Track traffic density
- `GET /overtake-opportunities` - Passing zones
- `GET /gap-analysis` - Time gaps between cars
- `GET /drs-zones` - DRS effectiveness
- `GET /backmarker-impact` - Lapped car effect

**Example:**
```bash
curl "http://localhost:8001/v1/engines/traffic/overtake-opportunities?year=2024&event=Monaco&session=R&lap=45"
```

**Use Cases:**
- Overtaking strategy
- Gap management
- DRS zone optimization
- Traffic avoidance

---

### 6. Pit Engine

**Path:** `pit_engine/`  
**Prefix:** `/v1/engines/pit`

**Purpose:** Pit stop timing, strategy optimization, pit loss calculation

**Endpoints:**
- `GET /strategy` - Optimal pit strategy
- `GET /window` - Pit window calculation
- `GET /loss` - Pit stop time loss
- `GET /undercut-overcut` - Tactical advantage
- `GET /traffic-clear` - Clean air windows

**Example:**
```bash
curl "http://localhost:8001/v1/engines/pit/strategy?current_lap=20&total_laps=78&compound=MEDIUM&tyre_age=19"
```

**Use Cases:**
- Pit stop timing
- Undercut/overcut decisions
- Strategy optimization
- Tyre compound selection

---

### 7. Safety Car Engine

**Path:** `safetycar_engine/`  
**Prefix:** `/v1/engines/safetycar`

**Purpose:** Safety car probability, strategy adaptation, gap neutralization

**Endpoints:**
- `GET /probability` - SC deployment likelihood
- `GET /impact` - Impact on race strategy
- `GET /window` - Pit stop opportunity
- `GET /gap-neutralization` - Position changes
- `GET /strategy-adaptation` - Updated strategy

**Example:**
```bash
curl "http://localhost:8001/v1/engines/safetycar/probability?year=2024&event=Monaco&lap=30"
```

**Use Cases:**
- Risk assessment
- Strategy flexibility
- Pit stop opportunism
- Position prediction

---

### 8. Driver Engine

**Path:** `driver_engine/`  
**Prefix:** `/v1/engines/driver`

**Purpose:** Driver-specific performance, consistency, racecraft

**Endpoints:**
- `GET /performance` - Overall driver performance
- `GET /consistency` - Lap-to-lap variation
- `GET /racecraft` - Wheel-to-wheel ability
- `GET /pressure-performance` - Performance under pressure
- `GET /track-adaptation` - Track-specific skills

**Example:**
```bash
curl "http://localhost:8001/v1/engines/driver/performance?year=2024&event=Monaco&driver=VER&session=Q"
```

**Use Cases:**
- Driver assessment
- Team orders decisions
- Contract negotiations
- Coaching priorities

---

## 🏗️ Engine Architecture Pattern

Each engine follows a consistent structure:

```
engine_name/
├── __init__.py
├── routes.py              # FastAPI endpoints
├── models.py              # Request/response schemas
├── services.py            # Business logic
└── calculations.py        # Domain-specific calculations
```

### Example: Track Engine Structure

```python
# routes.py
from fastapi import APIRouter, Query
from .models import TrackCharacteristicsResponse
from .services import TrackService

router = APIRouter(prefix="/v1/engines/track")
service = TrackService()

@router.get("/characteristics", response_model=TrackCharacteristicsResponse)
async def get_track_characteristics(track: str = Query(...)):
    return service.get_characteristics(track)
```

```python
# models.py
from pydantic import BaseModel

class TrackCharacteristicsResponse(BaseModel):
    name: str
    length_meters: float
    corners: int
    straights: int
    drs_zones: int
```

```python
# services.py
class TrackService:
    def get_characteristics(self, track: str):
        # Business logic
        return {...}
```

---

## 🔗 Integration with API Layer

The engines layer works alongside the API layer:

```
Port 8001 (FastAPI)
  │
  ├─> Engine Services (8 engines)
  │     ├─> /v1/engines/track/*
  │     ├─> /v1/engines/car/*
  │     └─> ... (6 more engines)
  │
  └─> API Groups (4 groups)
        ├─> /api/v1/compare/*        (Comparison API)
        ├─> /api/v1/drivers/*        (Driver Insights API)
        ├─> /api/v1/strategy/*       (Strategy API)
        └─> /api/v1/visualizations/* (Visualization API)
```

**Difference:**
- **Engines** = Lower-level, domain-specific services
- **API Groups** = Higher-level, aggregated analysis

---

## 🚀 Usage Examples

### Single Engine Request

```python
import requests

# Get track characteristics
response = requests.get(
    "http://localhost:8001/v1/engines/track/characteristics",
    params={"track": "Monaco"}
)

track_data = response.json()
print(f"Track: {track_data['name']}")
print(f"Corners: {track_data['corners']}")
```

### Multi-Engine Analysis

```python
# Combine multiple engines for comprehensive analysis
import requests

BASE = "http://localhost:8001/v1/engines"

# Get track info
track = requests.get(f"{BASE}/track/characteristics", 
                     params={"track": "Monaco"}).json()

# Get car performance
car = requests.get(f"{BASE}/car/performance", params={
    "year": 2024, "event": "Monaco", "driver": "VER", "session": "Q"
}).json()

# Get tyre degradation
tyre = requests.get(f"{BASE}/tyre/degradation", params={
    "year": 2024, "event": "Monaco", "driver": "VER", "compound": "SOFT"
}).json()

# Analyze
print(f"Track: {track['name']} - {track['corners']} corners")
print(f"Car top speed: {car['max_speed']} km/h")
print(f"Tyre deg rate: {tyre['degradation_rate']} s/lap")
```

---

## 🎨 Advanced Features

### Error Handling

All engines use consistent error responses:

```python
# 400 Bad Request
{
    "detail": "Invalid track name",
    "status_code": 400
}

# 404 Not Found
{
    "detail": "Session data not available",
    "status_code": 404
}

# 500 Internal Server Error
{
    "detail": "Failed to process telemetry data",
    "status_code": 500
}
```

### Middleware

The main app includes:
- **CORS Middleware** - Cross-origin support
- **Error Handler Middleware** - Global exception handling
- **Logging Middleware** - Request/response logging

### Startup/Shutdown Events

```python
@app.on_event("startup")
async def startup_event():
    """Initialize FastF1 client and cache"""
    client = FastF1Client(cache_dir=settings.fastf1_cache_dir)
    logger.info("FastF1 initialized")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down...")
```

---

## 🧪 Testing

### Engine Tests

Each engine has its own test suite:

```bash
# Test specific engine
pytest engines/track_engine/test/

# Test all engines
pytest engines/

# Integration tests
pytest tests/test_integration.py
```

### Example Test

```python
from fastapi.testclient import TestClient
from engines.main import app

client = TestClient(app)

def test_track_characteristics():
    response = client.get(
        "/v1/engines/track/characteristics",
        params={"track": "Monaco"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'Monaco'
    assert data['corners'] > 0
```

---

## ⚡ Performance

### Optimization Strategies:
- **FastF1 Caching** - Session data cached permanently
- **Async Endpoints** - Non-blocking I/O operations
- **Connection Pooling** - Efficient HTTP client usage
- **Response Compression** - GZIP for large responses

### Benchmarks:
| Engine | Avg Response Time | Max Response Time |
|--------|------------------|-------------------|
| Track Engine | 50-100ms | 200ms |
| Car Engine | 100-300ms | 1s |
| Tyre Engine | 80-150ms | 500ms |
| Weather Engine | 60-120ms | 300ms |
| Traffic Engine | 100-200ms | 800ms |
| Pit Engine | 200-500ms | 2s |
| Safety Car Engine | 50-100ms | 300ms |
| Driver Engine | 100-250ms | 1s |

---

## 🎯 Real-World Scenarios

### Scenario 1: Qualifying Preparation

```python
# Get track characteristics
track = get("/v1/engines/track/characteristics?track=Monaco")

# Analyze car setup
car = get("/v1/engines/car/setup?year=2024&event=Monaco&session=FP3")

# Check tyre allocation
tyres = get("/v1/engines/tyre/allocation?year=2024&event=Monaco")

# Recommendation
if car['downforce'] == 'high' and tyres['soft_sets'] >= 2:
    print("Ready for qualifying - high downforce Monaco setup")
```

### Scenario 2: Race Strategy

```python
# Check weather
weather = get("/v1/engines/weather/forecast?event=Silverstone")

# Calculate pit window
pit = get("/v1/engines/pit/window?lap=20&total=52&compound=MEDIUM")

# Check traffic
traffic = get("/v1/engines/traffic/density?lap=22")

# Decision
if weather['rain_risk'] < 0.2 and traffic['density'] == 'low':
    print(f"Pit on lap {pit['optimal_lap']}")
```

### Scenario 3: Safety Car Adaptation

```python
# Safety car deployed
sc = get("/v1/engines/safetycar/impact?lap=30")

# Pit opportunity
pit = get("/v1/engines/pit/strategy?safety_car=true")

# Gap analysis
traffic = get("/v1/engines/traffic/gap-analysis?lap=30")

# Strategy
if sc['pit_window_open'] and pit['advantage'] > 5:
    print("Box box box - free pit stop")
```

---

## 🎓 Summary

The **Engine Services** provide domain-specific microservices:

✅ **8 Specialized Engines** - Track, Car, Tyre, Weather, Traffic, Pit, Safety Car, Driver  
✅ **REST API Endpoints** - FastAPI with OpenAPI documentation  
✅ **Consistent Architecture** - Standardized structure across engines  
✅ **Production Ready** - Error handling, logging, testing  
✅ **High Performance** - Cached data, async operations  
✅ **Composable** - Combine engines for comprehensive analysis  

Each engine focuses on a specific domain, following microservice principles while being hosted on a single port for simplicity.

---

## 📚 Related Documentation

- [API Examples](../API_EXAMPLES.md) - API usage with examples
- [Architecture](../ARCHITECTURE.md) - System design overview
- [Main README](../README.md) - Project overview
