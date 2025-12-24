# F1 Strategy Engine - API Demo Scripts Parameter Guide

This directory contains demo implementation scripts for all F1 Strategy Engine APIs. Each script demonstrates how to use the APIs with real examples and outputs complete JSON responses.

## 📂 Directory Structure

```
demo/apis/
├── comparison/          # Car vs Car and Driver vs Driver comparisons
├── driver/             # Individual driver performance insights
├── strategy/           # Race strategy optimization
├── visualization/      # Interactive charts and visualizations
└── README.md          # This file
```

## 🔧 Common Request Parameters

These parameters are used across most or all API endpoints:

### **year** (Required)
- **Type**: Integer
- **Range**: 2018-2025
- **Description**: F1 season year
- **Examples**: `2024`, `2023`, `2022`

### **event** / **gp** (Required)
- **Type**: String
- **Description**: Grand Prix name or circuit name
- **Valid Values**:
  - `"Bahrain"`
  - `"Saudi Arabia"` / `"Jeddah"`
  - `"Australia"` / `"Melbourne"`
  - `"Azerbaijan"` / `"Baku"`
  - `"Miami"`
  - `"Monaco"`
  - `"Spain"` / `"Barcelona"` / `"Catalunya"`
  - `"Canada"` / `"Montreal"`
  - `"Austria"` / `"Spielberg"`
  - `"Great Britain"` / `"Silverstone"`
  - `"Hungary"` / `"Hungaroring"`
  - `"Belgium"` / `"Spa"`
  - `"Netherlands"` / `"Zandvoort"`
  - `"Italy"` / `"Monza"`
  - `"Singapore"`
  - `"Japan"` / `"Suzuka"`
  - `"Qatar"` / `"Losail"`
  - `"United States"` / `"Austin"` / `"COTA"`
  - `"Mexico"` / `"Mexico City"`
  - `"Brazil"` / `"Sao Paulo"` / `"Interlagos"`
  - `"Las Vegas"`
  - `"Abu Dhabi"` / `"Yas Marina"`

### **session** (Required)
- **Type**: String
- **Description**: Session type identifier
- **Valid Values**:
  - `"FP1"` - Free Practice 1
  - `"FP2"` - Free Practice 2
  - `"FP3"` - Free Practice 3
  - `"Q"` - Qualifying
  - `"SQ"` - Sprint Qualifying
  - `"S"` - Sprint Race
  - `"R"` - Race (Main Grand Prix)

### **driver** / **driver1** / **driver2** (Required for driver-specific endpoints)
- **Type**: String (3-letter driver code)
- **Description**: Driver identifier code
- **Valid Values** (2024 Season):
  - `"VER"` - Max Verstappen
  - `"PER"` - Sergio Perez
  - `"LEC"` - Charles Leclerc
  - `"SAI"` - Carlos Sainz
  - `"HAM"` - Lewis Hamilton
  - `"RUS"` - George Russell
  - `"NOR"` - Lando Norris
  - `"PIA"` - Oscar Piastri
  - `"ALO"` - Fernando Alonso
  - `"STR"` - Lance Stroll
  - `"TSU"` - Yuki Tsunoda
  - `"RIC"` - Daniel Ricciardo
  - `"GAS"` - Pierre Gasly
  - `"OCO"` - Esteban Ocon
  - `"ALB"` - Alexander Albon
  - `"SAR"` - Logan Sargeant
  - `"MAG"` - Kevin Magnussen
  - `"HUL"` - Nico Hulkenberg
  - `"BOT"` - Valtteri Bottas
  - `"ZHO"` - Zhou Guanyu

---

## 📊 API Category-Specific Parameters

## 1. Comparison APIs (`/demo/apis/comparison/`)

### Car Performance Comparison
**Endpoint**: `/api/v1/compare/cars/performance`

**Script**: `car_performance_impl.py`

**Parameters**:
- `year` (required): Season year
- `event` (required): Grand Prix name
- `session` (required): Session type
- `driver1` (required): First driver code
- `driver2` (required): Second driver code

**Example**:
```python
params = {
    'year': 2024,
    'event': 'Bahrain',
    'session': 'R',
    'driver1': 'VER',
    'driver2': 'LEC'
}
```

---

### Detailed Car Performance Comparison
**Endpoint**: `/api/v1/compare/cars/performance/detailed`

**Script**: `car_performance_detailed_impl.py`

**Parameters**: Same as Car Performance Comparison
- Provides detailed breakdown: power, aero, drag, grip, ERS, reliability, thermal, setup profiles

---

### Car Tyre Performance Comparison
**Endpoint**: `/api/v1/compare/cars/tyre-performance`

**Script**: `car_tyre_performance_impl.py`

**Parameters**:
- `year` (required): Season year
- `event` (required): Grand Prix name
- `session` (required): Session type
- `driver1` (required): First driver code
- `driver2` (required): Second driver code
- `compound` (required): Tyre compound to analyze

**Compound Values**:
- `"SOFT"` - Red-walled soft compound
- `"MEDIUM"` - Yellow-walled medium compound
- `"HARD"` - White-walled hard compound
- `"INTERMEDIATE"` - Green-walled intermediate (wet)
- `"WET"` - Blue-walled full wet

**Example**:
```python
params = {
    'year': 2024,
    'event': 'Monaco',
    'session': 'R',
    'driver1': 'LEC',
    'driver2': 'SAI',
    'compound': 'SOFT'
}
```

---

### Driver Pace Comparison
**Endpoint**: `/api/v1/compare/drivers/pace`

**Script**: `drivers_pace_impl.py`

**Parameters**:
- `year` (required): Season year
- `event` (required): Grand Prix name
- `session` (required): Session type
- `driver1` (required): First driver code
- `driver2` (required): Second driver code
- `fuel_corrected` (optional): Apply fuel weight correction

**fuel_corrected Values**:
- `true` - Apply fuel correction (shows true pace)
- `false` - Raw lap times (default)

**Example**:
```python
params = {
    'year': 2023,
    'event': 'Silverstone',
    'session': 'R',
    'driver1': 'HAM',
    'driver2': 'RUS',
    'fuel_corrected': True
}
```

---

### Driver Consistency Comparison
**Endpoint**: `/api/v1/compare/drivers/consistency`

**Script**: `drivers_consistency_impl.py`

**Parameters**: Same as Driver Pace Comparison (without fuel_corrected)
- Analyzes lap time variation, outliers, clean lap percentage

---

## 2. Driver Insights APIs (`/demo/apis/driver/`)

### Driver Performance Profile
**Endpoint**: `/api/v1/driver/performance-profile`

**Script**: `driver_performance_profile_impl.py`

**Parameters**:
- `year` (required): Season year
- `event` (required): Grand Prix name
- `session` (required): Session type
- `driver` (required): Driver code

**Returns**:
- Pace metrics (fastest lap, median, average)
- Consistency metrics (std deviation, outliers)
- Tyre management rating
- Car performance ratings
- Strengths and weaknesses
- Overall rating

**Example**:
```python
params = {
    'year': 2024,
    'event': 'Bahrain',
    'session': 'R',
    'driver': 'VER'
}
```

---

### Driver Stint Analysis
**Endpoint**: `/api/v1/driver/stint-analysis`

**Script**: `driver_stint_analysis_impl.py`

**Parameters**:
- `year` (required): Season year
- `event` (required): Grand Prix name
- `session` (required): Session type (typically `"R"`)
- `driver` (required): Driver code
- `stint` (required): Stint number (1-based)

**stint Values**:
- `1` - First stint
- `2` - Second stint
- `3` - Third stint
- etc.

**Example**:
```python
params = {
    'year': 2023,
    'event': 'Monaco',
    'session': 'R',
    'driver': 'LEC',
    'stint': 2
}
```

---

## 3. Strategy APIs (`/demo/apis/strategy/`)

### Pit Stop Optimization
**Endpoint**: `/api/v1/strategy/pit-optimization`

**Script**: `pit_optimization_impl.py`

**Parameters**:
- `year` (required): Season year
- `event` (required): Grand Prix name
- `driver` (required): Driver code
- `current_lap` (required): Current lap number (≥1)
- `total_laps` (required): Total race laps (≥1)
- `current_compound` (required): Current tyre compound
- `tyre_age` (required): Current tyre age in laps (≥0)
- `position` (required): Current race position (1-20)
- `gap_ahead` (optional): Gap to car ahead in seconds
- `gap_behind` (optional): Gap to car behind in seconds

**current_compound Values**:
- `"SOFT"`, `"MEDIUM"`, `"HARD"`, `"INTERMEDIATE"`, `"WET"`

**Example**:
```python
params = {
    'year': 2024,
    'event': 'Bahrain',
    'driver': 'VER',
    'current_lap': 15,
    'total_laps': 57,
    'current_compound': 'MEDIUM',
    'tyre_age': 14,
    'position': 1,
    'gap_behind': 3.2
}
```

---

### Battle Forecast
**Endpoint**: `/api/v1/strategy/battle-forecast`

**Script**: `battle_forecast_impl.py`

**Parameters**:
- `year` (required): Season year
- `event` (required): Grand Prix name
- `session` (required): Session type (typically `"R"`)
- `lap` (required): Current lap number (≥1)
- `attacker` (required): Attacking driver code
- `defender` (required): Defending driver code
- `gap` (required): Current gap in seconds (≥0)
- `drs_available` (optional): DRS available for attacker

**drs_available Values**:
- `true` - DRS is available
- `false` - No DRS (default)

**Example**:
```python
params = {
    'year': 2023,
    'event': 'Monza',
    'session': 'R',
    'lap': 35,
    'attacker': 'VER',
    'defender': 'LEC',
    'gap': 0.8,
    'drs_available': True
}
```

---

## 4. Visualization APIs (`/demo/apis/visualization/`)

### Speed Trace Comparison
**Endpoint**: `/api/v1/visualizations/speed-trace`

**Parameters**:
- `year` (required): Season year
- `event` (required): Grand Prix name
- `session` (required): Session type
- `driver1` (required): First driver code
- `driver2` (required): Second driver code
- `format` (optional): Output format

---

### Throttle & Brake Analysis
**Endpoint**: `/api/v1/visualizations/throttle-brake`

**Parameters**: Same as Speed Trace

---

### Lap Time Distribution
**Endpoint**: `/api/v1/visualizations/lap-time-distribution`

**Parameters**:
- `year` (required): Season year
- `event` (required): Grand Prix name
- `session` (required): Session type
- `drivers` (required): Comma-separated driver codes
- `format` (optional): Output format

**drivers Format**:
- Multiple drivers separated by commas: `"VER,LEC,HAM,ALO,SAI"`

---

### Sector Comparison
**Endpoint**: `/api/v1/visualizations/sector-comparison`

**Parameters**: Same as Speed Trace

---

### Tyre Degradation
**Endpoint**: `/api/v1/visualizations/tyre-degradation`

**Parameters**:
- `year` (required): Season year
- `event` (required): Grand Prix name
- `session` (required): Session type (typically `"R"`)
- `driver` (required): Driver code
- `format` (optional): Output format

---

### Gear Usage
**Endpoint**: `/api/v1/visualizations/gear-usage`

**Parameters**: Same as Tyre Degradation

---

### Performance Radar
**Endpoint**: `/api/v1/visualizations/performance-radar`

**Parameters**: Same as Speed Trace

---

### format Parameter (All Visualization APIs)
**Values**:
- `"json"` - Interactive Plotly chart data (default)
- `"png"` - Static PNG image

---

## 💡 Usage Tips

### 1. **Season Availability**
Not all circuits are available in all years. The F1 calendar changes between seasons.
- Use years 2018-2025 for best data availability
- Check the official F1 calendar for specific year/event combinations

### 2. **Session Types**
- Sprint weekends have different structure: FP1, SQ, S, Q, R (no FP2/FP3)
- Regular weekends: FP1, FP2, FP3, Q, R
- For race strategy analysis, use `session="R"`
- For qualifying pace, use `session="Q"`

### 3. **Driver Codes**
- Driver codes can change between seasons as drivers move teams
- Use 3-letter abbreviations (all uppercase)
- Check current season driver lineup for accurate codes

### 4. **Tyre Compounds**
- Not all compounds are available at every race
- Pirelli selects 3 dry compounds per race weekend
- Wet compounds (INTERMEDIATE, WET) used in rain conditions

### 5. **Gap Parameters**
- Gaps are measured in seconds
- `null` or omitted means no car ahead/behind
- Use floating-point values: `2.5`, `0.8`, `12.3`

### 6. **Position Parameter**
- Valid range: 1-20 (maximum grid size)
- Position 1 = Leading the race
- Position 20 = Last place

### 7. **Lap Numbers**
- 1-based indexing (first lap = lap 1)
- `current_lap` must be ≤ `total_laps`
- Race length varies by circuit (typically 50-70 laps)

### 8. **Stint Numbers**
- 1-based indexing (first stint = 1)
- Most races have 1-3 stints per driver
- Stint changes occur at pit stops

---

## 🚀 Running the Demos

### Python Scripts (Comparison, Driver, Strategy)
```bash
# Navigate to the specific demo directory
cd demo/apis/comparison
# or
cd demo/apis/driver
# or
cd demo/apis/strategy

# Run any demo script
python car_performance_impl.py
python driver_performance_profile_impl.py
python pit_optimization_impl.py
```

### Jupyter Notebook (Visualization)
```bash
# Navigate to visualization directory
cd demo/apis/visualization

# Open Jupyter
jupyter notebook visualization_apis_impl.ipynb
# or use VS Code's notebook interface
```

---

## 📖 API Documentation

For complete API documentation with interactive testing:
- **Main API Server**: `http://localhost:8000/docs`
- **Visualization Server**: `http://localhost:8001/docs` (if separate)

---

## ⚠️ Common Issues

### 1. **Invalid GP Name**
- **Error**: Event not found
- **Solution**: Use official circuit names or aliases listed above

### 2. **Session Not Found**
- **Error**: Session does not exist
- **Solution**: Check if session exists for that race (e.g., no FP3 in Sprint weekends)

### 3. **Driver Not Found**
- **Error**: Driver did not participate
- **Solution**: Verify driver participated in that session/year

### 4. **Year Out of Range**
- **Error**: Data not available
- **Solution**: Use years 2018-2025 for best data quality

### 5. **Connection Error**
- **Error**: Could not connect to server
- **Solution**: Ensure API server is running on correct port (8000 or 8001)

### 6. **Timeout**
- **Error**: Request timed out
- **Solution**: Increase timeout value or check server performance

---

## 📝 Example Workflows

### Complete Race Analysis
```python
# 1. Compare cars
GET /api/v1/compare/cars/performance
# 2. Analyze tyre strategy
GET /api/v1/compare/cars/tyre-performance
# 3. Get driver profile
GET /api/v1/driver/performance-profile
# 4. Optimize pit strategy
GET /api/v1/strategy/pit-optimization
# 5. Visualize results
GET /api/v1/visualizations/speed-trace
```

### Driver vs Driver Deep Dive
```python
# 1. Overall performance
GET /api/v1/compare/cars/performance/detailed
# 2. Pace comparison
GET /api/v1/compare/drivers/pace?fuel_corrected=true
# 3. Consistency analysis
GET /api/v1/compare/drivers/consistency
# 4. Visual comparison
GET /api/v1/visualizations/performance-radar
```

---

## 🔍 Finding Available Data

To check what data is available:
1. Visit [FastF1 Documentation](https://docs.fastf1.dev/)
2. Check official F1 calendar for the year
3. Use the API's error messages as guidance
4. Start with well-known races (Monaco, Monza, Silverstone)

---

## 📚 Additional Resources

- **F1 Strategy Engine Documentation**: See main project README
- **FastF1 Library**: https://docs.fastf1.dev/
- **Plotly Charts**: https://plotly.com/python/
- **F1 Official**: https://www.formula1.com/

---

**Last Updated**: December 2025  
**API Version**: 1.0  
**Supported Seasons**: 2018-2025
