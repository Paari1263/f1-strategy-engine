"""Car Engine Routes - FastF1 Implementation"""
from fastapi import APIRouter, HTTPException
from engines.car_engine.schemas import CarRequest, CarResponse
from engines.car_engine.service import CarService
from shared.middleware import SessionNotAvailableError, DataNotFoundError
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/v1/engines/car", tags=["Car Engine"])

@router.post("/analyze", response_model=CarResponse)
async def analyze_car(request: CarRequest) -> CarResponse:
    """Analyze car performance using high-resolution telemetry"""
    try:
        return await CarService.analyze_car_performance(request)
    except (SessionNotAvailableError, DataNotFoundError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Car analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
