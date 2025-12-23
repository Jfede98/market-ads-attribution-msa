"""
Validation utilities for parameters.
"""

import re
import logging
from fastapi import HTTPException
from app.services.mongodb_service import get_session_template

logger = logging.getLogger("uvicorn.error")

# Pre-compilar regex para mejor rendimiento
_FBCLID_PATTERN = re.compile(r'^[a-zA-Z0-9._-]+$')
_PLACEMENT_PATTERN = re.compile(r'^[a-zA-Z0-9\s._-]+$')


def _validate_fbclid(value: str) -> bool:
    """Valida formato de fbclid"""
    return _FBCLID_PATTERN.match(value) and 5 <= len(value) <= 500


def _validate_numeric_id(value: str) -> bool:
    """Valida IDs numéricos (campaign_id, adset_id, ad_id)"""
    return value.isdigit()


def _validate_placement(value: str) -> bool:
    """Valida formato de placement"""
    return _PLACEMENT_PATTERN.match(value) and len(value) <= 100


def _validate_utm_param(value: str) -> bool:
    """Valida parámetros UTM"""
    return len(value) <= 200


def validate_param(param_name: str, value: str) -> bool:
    """Valida formato de parámetros"""
    if not value or not value.strip():
        return False
        
    value = value.strip()
    
    # Mapeo de validadores por tipo de parámetro
    validators = {
        "fbclid": _validate_fbclid,
        "campaign_id": _validate_numeric_id,
        "adset_id": _validate_numeric_id,
        "ad_id": _validate_numeric_id,
        "placement": _validate_placement
    }
    
    # Usar validador específico si existe
    if param_name in validators:
        return validators[param_name](value)
    
    # Validar parámetros UTM
    if param_name.startswith("utm_"):
        return _validate_utm_param(value)
            
    return True


async def detect_source_and_normalize(params: dict) -> dict:
    """Detecta la fuente (Meta) y normaliza parámetros usando template dinámico"""
    
    # Obtener template desde MongoDB
    template = await get_session_template()
    
    # Validar parámetros requeridos según template
    required_params = template.get("require", [])
    
    for param in required_params:
        if param not in params:
            raise HTTPException(status_code=400, detail=f"Missing required parameter: {param}")
        if not validate_param(param, params[param]):
            raise HTTPException(status_code=400, detail=f"Invalid required parameter: {param}")
    
    # Validar fbclid (siempre obligatorio para Meta)
    fbclid = params.get("fbclid", "")
    if not fbclid or not validate_param("fbclid", fbclid):
        raise HTTPException(status_code=400, detail="Missing or invalid fbclid parameter")
    
    # Construir payload usando template
    payload = {"channel": template.get("channel", "ads")}
    
    # Aplicar defaults del template
    if "defaults" in template:
        defaults = template["defaults"]
        if "consent" in defaults:
            payload["consent"] = defaults["consent"]
    
    # Aplicar mapping dinámico para context
    if "mapping" in template:
        context = {}
        
        # Agregar defaults de context si existen
        if "defaults" in template and "context" in template["defaults"]:
            context.update(template["defaults"]["context"])
        
        for target_path, mapping_rules in template["mapping"].items():
            if target_path == "context.click_signals":
                click_signals = {}
                for field, source in mapping_rules.items():
                    if source.startswith("$query."):
                        param_name = source.replace("$query.", "")
                        if param_name in params and validate_param(param_name, params[param_name]):
                            click_signals[field] = params[param_name].strip()
                
                context["click_signals"] = click_signals
        
        payload["context"] = context
    
    return payload