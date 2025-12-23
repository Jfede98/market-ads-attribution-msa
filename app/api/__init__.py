from .health import router as health_router
from .redirect import router as redirect_router

__all__ = ["health_router", "redirect_router"]