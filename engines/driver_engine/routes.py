"""Driver Engine Routes - FastF1 Implementation"""
from fastapi import APIRouter, HTTPException
from engines.driver_engine.schemas import DriverRequest, DriverResponse
from engines.shared_services_fastf1 import DriverService
from shared.middleware import SessionNotAvailableError, DataNotFoundError
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/v1/engines/driver", tags=["Driver Engine"])

@router.post("/analyze", response_model=DriverResponse)
async def analyze_driver(request: DriverRequest) -> DriverResponse:
    """Analyze driver performance, consistency, and racecraft"""
    try:
        return await DriverService.analyze_driver_performance(request)
    except (SessionNotAvailableError, DataNotFoundError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Driver analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
