"""
F1 Race Strategy Simulator - Main Application (FastF1 Implementation)
Hosts all microservice engines on a single port (8001)

Available Engines:
- Track Engine:      /v1/engines/track/*
- Car Engine:        /v1/engines/car/*
- Tyre Engine:       /v1/engines/tyre/*
- Weather Engine:    /v1/engines/weather/*
- Traffic Engine:    /v1/engines/traffic/*
- Pit Engine:        /v1/engines/pit/*
- Safety Car Engine: /v1/engines/safetycar/*
- Driver Engine:     /v1/engines/driver/*

Start the server:
    uvicorn engines.main:app --port 8001 --reload

API Documentation:
    http://localhost:8001/docs

Data Source: FastF1 Python Library (2018-2025 historical data)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import logging
import fastf1
from datetime import datetime, timedelta

# Import error handlers
from shared.middleware.error_handler import register_error_handlers
from shared.config.settings import settings
from shared.clients.fastf1_client import FastF1Client

# Import cache management
from cache import get_cache_manager, get_redis_client

# Import all engine routers
from engines.track_engine.routes import router as track_router
from engines.car_engine.routes import router as car_router
from engines.tyre_engine.routes import router as tyre_router
from engines.weather_engine.routes import router as weather_router
from engines.traffic_engine.routes import router as traffic_router
from engines.pit_engine.routes import router as pit_router
from engines.safetycar_engine.routes import router as safetycar_router
from engines.driver_engine.routes import router as driver_router

# Import new API routers (calculation_engines-based)
from api.comparison_router import router as comparison_router
from api.driver_router import router as driver_insights_router
from api.strategy_router import router as strategy_router
from api.visualization_router import router as visualization_router

# Create main application
app = FastAPI(
    title="F1 Race Strategy Simulator",
    description="Comprehensive F1 race strategy analysis using FastF1 library with high-resolution telemetry",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastF1 on startup
@app.on_event("startup")
async def startup_event():
    """Initialize FastF1 client, Redis cache, and warm cache"""
    logger.info("Initializing F1 Race Strategy Simulator...")
    
    # Initialize Redis connection
    try:
        redis_client = get_redis_client()
        redis_stats = redis_client.get_stats()
        if redis_stats.get('connected'):
            logger.info(f"✓ Redis connected: v{redis_stats.get('version', 'unknown')}")
            logger.info(f"  Cache hit rate: {redis_stats.get('hit_rate', 0)}%")
            logger.info(f"  Total keys: {redis_stats.get('total_keys', 0)}")
        else:
            logger.warning("⚠ Redis not connected - caching disabled")
    except Exception as e:
        logger.error(f"✗ Failed to connect to Redis: {e}")
        logger.warning("⚠ Application will run without caching")
    
    # Initialize FastF1 client
    logger.info("Initializing FastF1 client...")
    try:
        client = FastF1Client(cache_dir=settings.fastf1_cache_dir)
        logger.info(f"✓ FastF1 initialized with cache at: {settings.fastf1_cache_dir}")
        logger.info(f"  FastF1 cache enabled: {settings.fastf1_cache_enabled}")
        logger.info(f"  Ergast support: {settings.fastf1_ergast_support}")
    except Exception as e:
        logger.error(f"✗ Failed to initialize FastF1: {e}")
        raise
    
    # Warm cache with current season data
    logger.info("Warming cache with reference data...")
    try:
        await warm_cache_on_startup()
        logger.info("✓ Cache warming completed")
    except Exception as e:
        logger.warning(f"⚠ Cache warming failed (non-critical): {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down F1 Race Strategy Simulator...")
    
    # Close Redis connection
    try:
        redis_client = get_redis_client()
        redis_client.close()
        logger.info("✓ Redis connection closed")
    except Exception as e:
        logger.error(f"Error closing Redis: {e}")

# Register error handlers
register_error_handlers(app)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all engine routers
app.include_router(track_router, tags=["Track Engine"])
app.include_router(car_router, tags=["Car Engine"])
app.include_router(tyre_router, tags=["Tyre Engine"])
app.include_router(weather_router, tags=["Weather Engine"])
app.include_router(traffic_router, tags=["Traffic Engine"])
app.include_router(pit_router, tags=["Pit Engine"])
app.include_router(safetycar_router, tags=["Safety Car Engine"])
app.include_router(driver_router, tags=["Driver Engine"])

# Include new API routers (calculation_engines-based GET APIs)
app.include_router(comparison_router, tags=["Comparison API"])
app.include_router(driver_insights_router, tags=["Driver Insights API"])
app.include_router(strategy_router, tags=["Strategy API"])
app.include_router(visualization_router, tags=["Visualization API"])


# ===== FASTF1 UTILITY ENDPOINTS =====

@app.get("/v1/schedule/{year}", tags=["FastF1 Utilities"])
async def get_season_schedule(year: int):
    """
    Get F1 season schedule for a specific year
    
    Returns all Grand Prix events with dates and locations
    """
    try:
        schedule = fastf1.get_event_schedule(year)
        events = []
        for idx, event in schedule.iterrows():
            events.append({
                "round": int(event.get('RoundNumber', idx + 1)),
                "gp_name": event.get('EventName', 'Unknown'),
                "location": event.get('Location', 'Unknown'),
                "country": event.get('Country', 'Unknown'),
                "event_date": str(event.get('EventDate', '')),
                "session_types": ["FP1", "FP2", "FP3", "Q", "R"]
            })
        return {
            "year": year,
            "total_events": len(events),
            "events": events
        }
    except Exception as e:
        logger.error(f"Failed to fetch schedule: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/event/{year}/{gp}", tags=["FastF1 Utilities"])
async def get_event_info(year: int, gp: str):
    """
    Get detailed information about a specific Grand Prix event
    
    Returns event details and available sessions
    """
    try:
        event = fastf1.get_event(year, gp)
        return {
            "year": year,
            "gp_name": event.get('EventName', gp),
            "location": event.get('Location', 'Unknown'),
            "country": event.get('Country', 'Unknown'),
            "event_date": str(event.get('EventDate', '')),
            "sessions": {
                "practice_1": "FP1",
                "practice_2": "FP2",
                "practice_3": "FP3" if year >= 2021 else "Sprint Qualifying",
                "qualifying": "Q",
                "race": "R"
            }
        }
    except Exception as e:
        logger.error(f"Failed to fetch event info: {e}")
        raise HTTPException(status_code=404, detail=f"Event not found: {year} {gp}")


# ===== CACHE MANAGEMENT ENDPOINTS =====

@app.get("/v1/cache/stats", tags=["Cache Management"])
async def get_cache_stats():
    """
    Get comprehensive cache statistics
    
    Returns metrics including hit rate, memory usage, and layer counts
    """
    try:
        cache_manager = get_cache_manager()
        stats = cache_manager.get_cache_stats()
        return {
            "status": "connected" if stats.get('connected') else "disconnected",
            "redis_version": stats.get('version'),
            "uptime_seconds": stats.get('uptime_seconds'),
            "total_keys": stats.get('total_keys'),
            "used_memory": stats.get('used_memory'),
            "hit_rate_percent": stats.get('hit_rate'),
            "layer_counts": stats.get('layer_counts', {}),
            "pool_size": stats.get('pool_size')
        }
    except Exception as e:
        logger.error(f"Failed to get cache stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/cache/invalidate/{layer}", tags=["Cache Management"])
async def invalidate_cache_layer(layer: str):
    """
    Invalidate entire cache layer
    
    Layers: session, computed, api, reference
    """
    try:
        cache_manager = get_cache_manager()
        count = cache_manager.invalidate_layer(layer)
        return {
            "layer": layer,
            "keys_deleted": count,
            "message": f"Invalidated {count} keys in {layer} layer"
        }
    except Exception as e:
        logger.error(f"Failed to invalidate cache layer: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/cache/invalidate/session/{year}/{event}", tags=["Cache Management"])
async def invalidate_session_cache(year: int, event: str, session_type: Optional[str] = None):
    """
    Invalidate cache for specific session
    
    Clears all data related to the specified session
    """
    try:
        cache_manager = get_cache_manager()
        count = cache_manager.invalidate_session(year, event, session_type)
        return {
            "year": year,
            "event": event,
            "session_type": session_type or "all",
            "keys_deleted": count,
            "message": f"Invalidated {count} cache entries"
        }
    except Exception as e:
        logger.error(f"Failed to invalidate session cache: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/v1/cache/flush", tags=["Cache Management"])
async def flush_all_cache():
    """
    **WARNING**: Flush ALL cache entries
    
    This will delete all cached data. Use with caution!
    """
    try:
        cache_manager = get_cache_manager()
        success = cache_manager.invalidate_all()
        if success:
            return {
                "message": "All cache entries flushed successfully",
                "warning": "Cache is now empty - performance may be slower until warmed"
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to flush cache")
    except Exception as e:
        logger.error(f"Failed to flush cache: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== CACHE WARMING UTILITY =====

async def warm_cache_on_startup():
    """
    Pre-populate cache with frequently accessed reference data
    
    Warms cache with:
    - Current season schedule
    - Recent event schedules
    """
    try:
        from shared.clients.fastf1_client import get_client
        
        cache_manager = get_cache_manager()
        client = get_client()
        current_year = datetime.now().year
        
        warming_tasks = []
        
        # Warm current season schedule
        warming_tasks.append({
            'name': f'season_schedule_{current_year}',
            'function': lambda: client.get_schedule(current_year, use_cache=True),
            'key': cache_manager.keys.season_schedule(current_year),
            'ttl': 604800  # 7 days
        })
        
        # Warm previous season schedule (if early in year)
        if datetime.now().month <= 3:
            warming_tasks.append({
                'name': f'season_schedule_{current_year - 1}',
                'function': lambda: client.get_schedule(current_year - 1, use_cache=True),
                'key': cache_manager.keys.season_schedule(current_year - 1),
                'ttl': 604800
        })
        
        # Execute warming
        stats = cache_manager.warm_cache(warming_tasks)
        
        logger.info(
            f"Cache warmed: {stats['success']}/{stats['total']} tasks completed"
        )
        
        if stats['errors']:
            for error in stats['errors']:
                logger.warning(f"Cache warming error: {error}")
        
        return stats
        
    except Exception as e:
        logger.error(f"Cache warming failed: {e}")
        raise


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - provides information about available engines and FastF1 capabilities
    """
    return {
        "application": "F1 Race Strategy Simulator",
        "version": "2.0.0",
        "data_source": "FastF1 Python Library",
        "capabilities": {
            "historical_data": "2018-2025 seasons",
            "telemetry_resolution": "~200Hz (high-resolution)",
            "weather_tracking": "8-parameter lap-by-lap monitoring",
            "track_status": "Safety car, VSC, red flag periods",
            "tyre_compounds": "Full stint and degradation analysis"
        },
        "engines": {
            "track": {
                "endpoint": "/v1/engines/track/analyze",
                "description": "Track characteristics with sector analysis, DRS zones, elevation",
                "input": {"year": 2024, "gp": "Bahrain", "session": "R"}
            },
            "car": {
                "endpoint": "/v1/engines/car/analyze",
                "description": "High-res telemetry: throttle, brake, RPM, gear, DRS",
                "input": {"year": 2024, "gp": "Bahrain", "session": "R", "driver_number": 1}
            },
            "tyre": {
                "endpoint": "/v1/engines/tyre/analyze",
                "description": "Compound degradation curves, thermal windows, cliff detection",
                "input": {"year": 2024, "gp": "Bahrain", "session": "R"}
            },
            "weather": {
                "endpoint": "/v1/engines/weather/analyze",
                "description": "Lap-by-lap weather evolution and performance impact",
                "input": {"year": 2024, "gp": "Bahrain", "session": "R"}
            },
            "traffic": {
                "endpoint": "/v1/engines/traffic/analyze",
                "description": "Gap evolution, overtaking patterns, DRS trains",
                "input": {"year": 2024, "gp": "Bahrain", "session": "R", "focus_driver": 1}
            },
            "pit": {
                "endpoint": "/v1/engines/pit/analyze",
                "description": "Exact pit durations, team comparisons, strategy analysis",
                "input": {"year": 2024, "gp": "Bahrain", "session": "R"}
            },
            "safetycar": {
                "endpoint": "/v1/engines/safetycar/analyze",
                "description": "Track status timeline, SC/VSC periods, strategic impact",
                "input": {"year": 2024, "gp": "Bahrain", "session": "R"}
            },
            "driver": {
                "endpoint": "/v1/engines/driver/analyze",
                "description": "Consistency, racecraft, tyre management, historical stats",
                "input": {"year": 2024, "gp": "Bahrain", "session": "R", "driver_number": 1}
            }
        },
        "utilities": {
            "schedule": {
                "endpoint": "/v1/schedule/{year}",
                "description": "Get full season schedule",
                "example": "/v1/schedule/2024"
            },
            "event_info": {
                "endpoint": "/v1/event/{year}/{gp}",
                "description": "Get event details",
                "example": "/v1/event/2024/Bahrain"
            }
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "session_types": {
            "FP1": "Free Practice 1",
            "FP2": "Free Practice 2",
            "FP3": "Free Practice 3",
            "Q": "Qualifying",
            "S": "Sprint",
            "R": "Race"
        }
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint with FastF1 status
    """
    try:
        # Test FastF1 availability
        fastf1_version = fastf1.__version__
        cache_status = "enabled" if settings.fastf1_cache_enabled else "disabled"
        
        return {
            "status": "healthy",
            "version": "2.0.0",
            "engines_loaded": 8,
            "fastf1": {
                "version": fastf1_version,
                "cache": cache_status,
                "cache_dir": settings.fastf1_cache_dir,
                "ergast_support": settings.fastf1_ergast_support
            },
            "data_coverage": {
                "years": "2018-2025",
                "telemetry_hz": "~200",
                "weather_params": 8
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "degraded",
            "error": str(e)
        }
