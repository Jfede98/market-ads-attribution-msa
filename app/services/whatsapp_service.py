"""
WhatsApp service for redirect generation.
"""

from urllib.parse import quote
from app.config import get_settings

settings = get_settings()


def generate_whatsapp_url() -> str:
    """Genera URL de WhatsApp limpia sin parámetros adicionales"""
    encoded_message = quote(settings.whatsapp_message_template)
    
    return f"https://wa.me/{settings.whatsapp_number}?text={encoded_message}"