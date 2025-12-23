"""
Configuration module for market-ads-attribution-msa.
Manages all environment variables and application settings following XTRIM standards.
"""

import os
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Application settings loaded from environment variables.
    All configuration follows XTRIM 2.0 standards.
    """

    def __init__(self):
        # Application Configuration
        self.app_name = os.getenv("APP_NAME", "market-ads-attribution-msa")
        self.app_version = os.getenv("APP_VERSION", "1.0.0")
        self.app_env = os.getenv("APP_ENV", "development")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

        # API Configuration
        self.api_host = os.getenv("API_HOST", "0.0.0.0")
        self.api_port = int(os.getenv("PORT", "2217"))
        self.api_prefix = os.getenv("API_PREFIX", "/market-ads-attribution-api/v1")

        # WhatsApp Configuration
        self.whatsapp_number = os.getenv("WHATSAPP_NUMBER", "593968600400")
        self.whatsapp_message_template = os.getenv(
            "WHATSAPP_MESSAGE_TEMPLATE", 
            "Hola quiero más información"
        )

        # Session Service Configuration (sec-session-identity-msa)
        self.caching_service_url = os.getenv(
            "CACHING_SERVICE_URL", 
            "https://prehaproxy.xtrim.tv:2001/sec-session-identity-api/v1"
        )

        # MongoDB Configuration
        self.mongodb_url = os.getenv(
            "MONGODB_URL", 
            "mongodb://localhost:27017/"
        )
        self.mongodb_database = os.getenv("MONGODB_DATABASE", "templates_db")
        self.mongodb_collection = os.getenv("MONGODB_COLLECTION", "session_templates")


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Returns:
        Settings: Application settings singleton.
    """
    return Settings()