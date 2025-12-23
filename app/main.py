"""
Market Ads Attribution MSA - Main application module.
Following XTRIM 2.0 standards.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.api import health_router, redirect_router

# Configurar logging
logger = logging.getLogger("uvicorn.error")
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info(f"{settings.app_name} v{settings.app_version} ready on port {settings.api_port}")
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {settings.app_name}")


# Create FastAPI application
app = FastAPI(
    title="Market Ads Attribution MSA",
    description="Microservicio para orquestar la atribución inicial de campañas publicitarias de Meta Ads. Recibe clics desde anuncios, valida parámetros usando templates configurables desde MongoDB, registra el ClickEvent en sec-session-identity-msa y redirige al usuario a WhatsApp con mensaje limpio para trazabilidad posterior.",
    version=settings.app_version,

    servers=[
        {
            "url": "https://capi-dev.xtrim.com.ec",
            "description": "Ambiente de Desarrollo"
        },
        {
            "url": "https://capi.xtrim.com.ec", 
            "description": "Producción"
        },
        {
            "url": f"http://localhost:{settings.api_port}",
            "description": "Desarrollo Local"
        }
    ],
    lifespan=lifespan,
    docs_url=f"{settings.api_prefix}/ui",
    redoc_url=f"{settings.api_prefix}/redoc",
    openapi_url=f"{settings.api_prefix}/openapi.json"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Manejador global de errores
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Maneja errores inesperados de forma consistente"""
    logger.error(f"Error inesperado en {request.url}: {str(exc)}", extra={
        "url": str(request.url),
        "method": request.method,
        "error": str(exc)
    })
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"},
    )

# Include Routers with tags
app.include_router(health_router, prefix=settings.api_prefix, tags=["health"])
app.include_router(redirect_router, prefix=settings.api_prefix, tags=["redirect"])


@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint."""
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.app_env == "development",
        log_level=settings.log_level.lower()
    )