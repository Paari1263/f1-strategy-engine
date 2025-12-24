"""Safety Car Engine Routes - FastF1 Implementation"""
from fastapi import APIRouter, HTTPException
from engines.safetycar_engine.schemas import SafetyCarRequest, SafetyCarResponse
from engines.shared_services_fastf1 import SafetyCarService
from shared.middleware import SessionNotAvailableError, DataNotFoundError
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/v1/engines/safetycar", tags=["Safety Car Engine"])

@router.post("/analyze", response_model=SafetyCarResponse)
async def analyze_safety_car(request: SafetyCarRequest) -> SafetyCarResponse:
    """Analyze safety car periods and strategic impact"""
    try:
        return await SafetyCarService.analyze_safety_car(request)
    except (SessionNotAvailableError, DataNotFoundError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Safety car analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
