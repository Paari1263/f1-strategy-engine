"""Pit Engine Routes - FastF1 Implementation"""
from fastapi import APIRouter, HTTPException
from engines.pit_engine.schemas import PitRequest, PitResponse
from engines.shared_services_fastf1 import PitService
from shared.middleware import SessionNotAvailableError, DataNotFoundError
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/v1/engines/pit", tags=["Pit Engine"])

@router.post("/analyze", response_model=PitResponse)
async def analyze_pit_stops(request: PitRequest) -> PitResponse:
    """Analyze pit stop performance and strategy"""
    try:
        return await PitService.analyze_pit_stops(request)
    except (SessionNotAvailableError, DataNotFoundError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Pit analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
