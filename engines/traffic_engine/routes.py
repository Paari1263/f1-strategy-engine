"""Traffic Engine Routes - FastF1 Implementation"""
from fastapi import APIRouter, HTTPException
from engines.traffic_engine.schemas import TrafficRequest, TrafficResponse
from engines.shared_services_fastf1 import TrafficService
from shared.middleware import SessionNotAvailableError, DataNotFoundError
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/v1/engines/traffic", tags=["Traffic Engine"])

@router.post("/analyze", response_model=TrafficResponse)
async def analyze_traffic(request: TrafficRequest) -> TrafficResponse:
    """Analyze traffic patterns, gaps, and overtaking opportunities"""
    try:
        return await TrafficService.analyze_traffic(request)
    except (SessionNotAvailableError, DataNotFoundError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Traffic analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
