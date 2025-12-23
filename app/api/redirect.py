"""
Redirect API endpoints for Meta Ads attribution.
"""

import logging
from fastapi import APIRouter, Request, Query
from fastapi.responses import RedirectResponse
from typing import Optional

from app.utils.validation import detect_source_and_normalize
from app.services.session_service import register_click_event
from app.services.whatsapp_service import generate_whatsapp_url
from app.models.responses import ErrorResponse, ValidationErrorResponse

logger = logging.getLogger("uvicorn.error")
router = APIRouter()


@router.get(
    "/w/redirect",
    response_class=RedirectResponse,
    summary="Redirección de Meta Ads a WhatsApp",
    description="Endpoint principal para procesar clics desde anuncios de Meta Ads y redirigir a WhatsApp. Valida parámetros según templates MongoDB, registra el ClickEvent en sec-session-identity-msa para trazabilidad y redirige con HTTP 302 a WhatsApp con mensaje limpio.",
    responses={
        302: {
            "description": "Redirección exitosa a WhatsApp",
            "headers": {
                "Location": {
                    "description": "URL de WhatsApp con mensaje y token REF",
                    "schema": {
                        "type": "string",
                        "example": "https://wa.me/593968600400?text=Hola%20quiero%20más%20información"
                    }
                }
            }
        },
        400: {
            "description": "Parámetros faltantes o inválidos",
            "content": {
                "application/json": {
                    "examples": {
                        "missing_fbclid": {
                            "summary": "fbclid faltante",
                            "description": "El parámetro fbclid es obligatorio para Meta Ads",
                            "value": {"detail": "Missing or invalid fbclid parameter"}
                        },
                        "invalid_campaign_id": {
                            "summary": "campaign_id inválido",
                            "description": "El campaign_id debe ser numérico",
                            "value": {"detail": "Invalid required parameter: campaign_id"}
                        },
                        "missing_required": {
                            "summary": "Parámetro requerido faltante",
                            "description": "Falta un parámetro requerido según template MongoDB",
                            "value": {"detail": "Missing required parameter: adset_id"}
                        }
                    }
                }
            }
        },
        500: {
            "description": "Error interno del servidor",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Error interno del servidor: Conexión a MongoDB fallida"
                    }
                }
            }
        }
    }
)
async def redirect_handler(
    request: Request,
    fbclid: str = Query(
        ..., 
        description="Facebook Click ID generado por Meta Ads (siempre obligatorio)",
        example="IwAR1234567890abcdef",
        min_length=5,
        max_length=500
    ),
    campaign_id: str = Query(
        ..., 
        description="ID numérico de la campaña publicitaria en Meta Ads",
        example="1234567890",
        pattern="^[0-9]+$"
    ),
    adset_id: str = Query(
        ..., 
        description="ID numérico del conjunto de anuncios (adset) en Meta Ads",
        example="9876543210",
        pattern="^[0-9]+$"
    ),
    ad_id: str = Query(
        ..., 
        description="ID numérico del anuncio específico en Meta Ads",
        example="5555666677",
        pattern="^[0-9]+$"
    ),
    placement: Optional[str] = Query(
        None, 
        description="Ubicación donde se mostró el anuncio (feed, stories, etc.)",
        example="feed",
        max_length=100
    ),
    utm_source: Optional[str] = Query(
        None, 
        description="Fuente de tráfico para tracking UTM",
        example="facebook",
        max_length=200
    ),
    utm_medium: Optional[str] = Query(
        None, 
        description="Medio de tráfico para tracking UTM",
        example="cpc",
        max_length=200
    ),
    utm_campaign: Optional[str] = Query(
        None, 
        description="Nombre de campaña para tracking UTM",
        example="promo_internet_2024",
        max_length=200
    ),
    utm_term: Optional[str] = Query(
        None, 
        description="Término o palabra clave para tracking UTM",
        example="internet_fibra",
        max_length=200
    ),
    utm_content: Optional[str] = Query(
        None, 
        description="Contenido específico del anuncio para tracking UTM",
        example="banner_promocional",
        max_length=200
    )
):
    """Endpoint principal de redirección desde anuncios de Meta"""
    
    # Obtener parámetros de query
    params = dict(request.query_params)
    
    logger.info("Procesando redirect de Meta Ads")
    
    # Normalizar parámetros al formato canónico usando template dinámico
    canonical_payload = await detect_source_and_normalize(params)
    
    # Registrar ClickEvent en sec-session-identity-msa
    uid = await register_click_event(canonical_payload)
    
    # Generar URL de WhatsApp limpia
    whatsapp_url = generate_whatsapp_url()
    
    logger.info("Redirect exitoso a WhatsApp")
    
    # Redirección HTTP 302
    return RedirectResponse(url=whatsapp_url, status_code=302)