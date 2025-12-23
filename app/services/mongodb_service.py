"""
MongoDB service for template management.
"""

import logging
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import get_settings

logger = logging.getLogger("uvicorn.error")
settings = get_settings()

# Cliente MongoDB
mongo_client = AsyncIOMotorClient(settings.mongodb_url)
mongo_db = mongo_client[settings.mongodb_database]
mongo_collection = mongo_db[settings.mongodb_collection]

# Cache del template (se actualiza cada 5 minutos)
_template_cache = None
_cache_timestamp = 0


async def get_session_template() -> dict:
    """Obtiene el template de sesión desde MongoDB con cache"""
    global _template_cache, _cache_timestamp
    
    import time
    current_time = time.time()
    
    # Usar cache si es válido (5 minutos)
    if _template_cache and (current_time - _cache_timestamp) < 300:
        return _template_cache
    
    try:
        # Buscar el template específico directamente
        template = await mongo_collection.find_one(
            {"_id": "session.meta.ads.v1", "active": True}
        )
        
        if not template:
            # Buscar cualquier template de meta como fallback
            template = await mongo_collection.find_one({"source": "meta", "active": True})
            if not template:
                template = _get_fallback_template()
        
        # Actualizar cache
        _template_cache = template
        _cache_timestamp = current_time
        
        return template
        
    except Exception as e:
        # Si hay error pero tenemos cache, usarlo
        if _template_cache:
            return _template_cache
        
        logger.warning(f"MongoDB fallback: {type(e).__name__}")
        return _get_fallback_template()


def _get_fallback_template() -> dict:
    """Template fallback hardcodeado"""
    return {
        "_id": "fallback",
        "tenant": "xtrim",
        "channel": "ads", 
        "source": "meta",
        "defaults": {
            "business": {"brand": "xtrim"},
            "consent": {"ad_personalization": True},
            "context": {"device": "mobile"}
        },
        "mapping": {
            "context.click_signals": {
                "fbclid": "$query.fbclid",
                "campaign_id": "$query.campaign_id",
                "adset_id": "$query.adset_id",
                "ad_id": "$query.ad_id",
                "placement": "$query.placement",
                "utm_source": "$query.utm_source",
                "utm_medium": "$query.utm_medium",
                "utm_campaign": "$query.utm_campaign",
                "utm_content": "$query.utm_content"
            }
        },
        "require": ["campaign_id", "adset_id", "ad_id"]
    }