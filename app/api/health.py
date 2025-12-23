"""
Health check API endpoints.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.config import get_settings
from app.models.responses import HealthResponse, ErrorResponse

settings = get_settings()
router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check del Servicio",
    description="Endpoint de health check para verificar el estado del servicio de atribución. Retorna información básica sobre el estado, nombre y versión del servicio. Usado para monitoreo automático y verificación de deployment.",
    responses={
        200: {
            "description": "Servicio funcionando correctamente",
            "content": {
                "application/json": {
                    "example": {
                        "status": "ok",
                        "service": "market-ads-attribution-msa",
                        "version": "1.0.0"
                    }
                }
            }
        },
        500: {
            "description": "Error interno del servidor",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Error interno del servidor: Conexión a base de datos fallida"
                    }
                }
            }
        }
    }
)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="ok", 
        service=settings.app_name,
        version=settings.app_version
    )