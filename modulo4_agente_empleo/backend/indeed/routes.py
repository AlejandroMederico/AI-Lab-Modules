from fastapi import APIRouter, HTTPException
from backend.indeed.schemas import SearchRequest, SearchResponse
from backend.indeed.service import IndeedService
from backend.logger.logger import logger

router = APIRouter(prefix="/indeed", tags=["indeed"])


@router.post("/search", response_model=SearchResponse)
async def search_jobs(request: SearchRequest):
    logger.info(f"Búsqueda de empleos iniciada con parámetros: {request.dict()}")
    try:
        return await IndeedService.search_jobs(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ping")
async def ping():
    logger.info("Petición de ping recibida")
    return {"status": "healthy"}
