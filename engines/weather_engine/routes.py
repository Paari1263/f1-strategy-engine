"""Weather Engine Routes - FastF1 Implementation"""
from fastapi import APIRouter, HTTPException
from engines.weather_engine.schemas import WeatherRequest, WeatherResponse
from engines.shared_services_fastf1 import WeatherService
from shared.middleware import SessionNotAvailableError, DataNotFoundError
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/v1/engines/weather", tags=["Weather Engine"])

@router.post("/analyze", response_model=WeatherResponse)
async def analyze_weather(request: WeatherRequest) -> WeatherResponse:
    """Analyze weather conditions and impact on performance"""
    try:
        return await WeatherService.analyze_weather(request)
    except (SessionNotAvailableError, DataNotFoundError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Weather analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
