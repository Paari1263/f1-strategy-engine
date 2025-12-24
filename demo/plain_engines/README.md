# F1 Strategy Engine - Demo Scripts Parameter Guide

This directory contains demo implementation scripts for all 8 F1 strategy engines. Each script outputs plain JSON responses to demonstrate engine capabilities.

## 🏎️ Available Demo Scripts

1. **track_engine_impl.py** - Circuit characteristics analysis
2. **car_engine_impl.py** - Vehicle performance and telemetry
3. **tyre_engine_impl.py** - Tyre compound degradation analysis
4. **weather_engine_impl.py** - Weather conditions and impact
5. **traffic_engine_impl.py** - Race battles and gap analysis
6. **pit_engine_impl.py** - Pit stop strategy analysis
7. **safety_car_engine_impl.py** - Safety car periods and track status
8. **driver_engine_impl.py** - Driver performance and consistency

## 📋 Common Request Parameters

All engines share these core parameters:

### **year** (Required)
- **Type**: Integer
- **Range**: 2018-2025
- **Description**: F1 season year
- **Examples**: `2024`, `2023`, `2022`

### **gp** (Required)
- **Type**: String
- **Description**: Grand Prix name or round number
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
- **Note**: You can also use round numbers (e.g., `1` for first race, `2` for second, etc.)

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

## 🔧 Engine-Specific Parameters

### Car Engine (`car_engine_impl.py`)
```python
CarRequest(
    year=2024,
    gp="Bahrain",
    session="R",
    driver_number=1  # Optional - analyze specific driver
)
```
**Additional Parameters**:
- `driver_number` (Optional, Integer): Specific driver number
  - Examples: `1` (Verstappen), `11` (Perez), `16` (Leclerc), `55` (Sainz), `44` (Hamilton), `63` (Russell)
  - If `None`: Analyzes all drivers

### Driver Engine (`driver_engine_impl.py`)
```python
DriverRequest(
    year=2024,
    gp="Bahrain",
    session="R",
    driver_number=1  # Optional - focus on specific driver
)
```
**Additional Parameters**:
- `driver_number` (Optional, Integer): Specific driver to analyze
  - If `None`: Returns analysis for all drivers
  - Common driver numbers (2024):
    - `1` - Max Verstappen
    - `11` - Sergio Perez
    - `16` - Charles Leclerc
    - `55` - Carlos Sainz
    - `44` - Lewis Hamilton
    - `63` - George Russell
    - `4` - Lando Norris
    - `81` - Oscar Piastri
    - `14` - Fernando Alonso
    - `18` - Lance Stroll

### Tyre Engine (`tyre_engine_impl.py`)
```python
TyreRequest(
    year=2024,
    gp="Bahrain",
    session="R",
    driver_number=1  # Optional - specific driver's tyre usage
)
```
**Additional Parameters**:
- `driver_number` (Optional, Integer): Specific driver's tyre data
  - If `None`: Analyzes all drivers' tyre strategies

### Traffic Engine (`traffic_engine_impl.py`)
```python
TrafficRequest(
    year=2024,
    gp="Bahrain",
    session="R",
    focus_driver=1  # Optional - driver to focus gap analysis on
)
```
**Additional Parameters**:
- `focus_driver` (Optional, Integer): Driver number to center traffic analysis around
  - If `None`: General traffic and gap analysis for all drivers
  - Use case: Analyze battles around a specific driver

### Pit Engine (`pit_engine_impl.py`)
```python
PitRequest(
    year=2024,
    gp="Bahrain",
    session="R",  # Typically "R" for races
    driver_number=1  # Optional - specific driver's pit stops
)
```
**Additional Parameters**:
- `driver_number` (Optional, Integer): Specific driver's pit stop data
  - If `None`: Analyzes all pit stops in the session
- **Note**: Most meaningful for Race sessions (`"R"`)

### Weather Engine (`weather_engine_impl.py`)
```python
WeatherRequest(
    year=2024,
    gp="Bahrain",
    session="R"
)
```
**No Additional Parameters** - Weather analysis covers the entire session

### Safety Car Engine (`safety_car_engine_impl.py`)
```python
SafetyCarRequest(
    year=2024,
    gp="Bahrain",
    session="R"  # Typically "R" for races
)
```
**No Additional Parameters** - Safety car periods affect all drivers
- **Note**: Most relevant for Race sessions (`"R"`)

### Track Engine (`track_engine_impl.py`)
```python
TrackRequest(
    year=2024,
    gp="Bahrain",
    session="R"
)
```
**No Additional Parameters** - Track characteristics are session-wide

## 🎯 Usage Examples

### Running Individual Scripts
```bash
# From project root
cd demo/plain_engines

# Run any engine demo
python track_engine_impl.py
python car_engine_impl.py
python driver_engine_impl.py
# ... etc
```

### Modifying Parameters in Scripts
Each script contains 3 examples. You can modify the request parameters:

```python
# Example: Change to analyze Monaco 2023 Qualifying
request = TrackRequest(
    year=2023,
    gp="Monaco",
    session="Q"
)
```

```python
# Example: Focus on Hamilton's car performance
request = CarRequest(
    year=2024,
    gp="Silverstone",
    session="R",
    driver_number=44
)
```

## 📊 Output Format

All scripts output **plain JSON** using this format:
```python
result = await EngineService.analyze(request)
print(json.dumps(result.dict(), indent=2, default=str))
```

The JSON output includes all response fields from the respective engine's schema.

## 💡 Tips

1. **Season Availability**: Not all circuits are available in all years. The calendar changes between seasons.
2. **Session Types**: Sprint weekends have different session structures (FP1, SQ, S, Q, R instead of FP1/FP2/FP3/Q/R)
3. **Driver Numbers**: Driver numbers can change between seasons as drivers move teams
4. **Race Sessions**: For most realistic analysis, use `session="R"` for race data
5. **Qualifying**: Use `session="Q"` for single-lap pace analysis
6. **Practice**: Use `"FP1"`, `"FP2"`, `"FP3"` for practice session data

## 🔍 Finding Available Data

To check what data is available for a specific season:
- Visit [FastF1 documentation](https://docs.fastf1.dev/)
- Check the official F1 calendar for that year
- Use year >= 2018 for best data availability

## ⚠️ Common Issues

1. **Invalid GP Name**: Use official circuit names or aliases listed above
2. **Session Not Found**: Not all sessions exist for all races (e.g., no FP3 in Sprint weekends)
3. **Driver Not Found**: Driver may not have participated in that session
4. **Year Out of Range**: Data quality varies; 2018-2025 is the recommended range
