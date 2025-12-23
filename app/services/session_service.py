"""
Session service integration with sec-session-identity-msa.
"""

import logging
import uuid
import httpx
from app.config import get_settings

logger = logging.getLogger("uvicorn.error")
settings = get_settings()

# Cliente HTTP reutilizable con connection pooling
_http_client = None

def get_http_client():
    global _http_client
    if _http_client is None:
        _http_client = httpx.AsyncClient(
            timeout=5.0,
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
        )
    return _http_client


async def register_click_event(payload: dict) -> str:
    """Registra ClickEvent en sec-session-identity-msa y retorna uid"""
    client = get_http_client()
    try:
        transaction_id = str(uuid.uuid4())
        
        response = await client.post(
            f"{settings.caching_service_url}/session",
            json=payload,
            headers={
                "Content-Type": "application/json",
                "X-External-Transaction-Id": transaction_id,
                "X-Channel": payload.get("channel", "ads")
            }
        )
        
        response.raise_for_status()
        result = response.json()
        logger.info("ClickEvent registrado exitosamente")
        return result["uid"]
    except Exception as e:
        # Fallback rápido con log mínimo de error
        logger.warning(f"Session service fallback: {type(e).__name__}")
        return str(uuid.uuid4())