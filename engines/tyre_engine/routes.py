"""Tyre Engine Routes - FastF1 Implementation"""
from fastapi import APIRouter, HTTPException
from engines.tyre_engine.schemas import TyreRequest, TyreResponse
from engines.shared_services_fastf1 import TyreService
from shared.middleware import SessionNotAvailableError, DataNotFoundError
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/v1/engines/tyre", tags=["Tyre Engine"])

@router.post("/analyze", response_model=TyreResponse)
async def analyze_tyres(request: TyreRequest) -> TyreResponse:
    """Analyze tyre compound performance and degradation"""
    try:
        return await TyreService.analyze_tyre_performance(request)
    except (SessionNotAvailableError, DataNotFoundError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Tyre analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
