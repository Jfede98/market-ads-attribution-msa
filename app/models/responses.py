"""
Response models for API documentation.
"""

from pydantic import BaseModel
from typing import Optional


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    service: str
    version: str


class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str


class ValidationErrorResponse(BaseModel):
    """Validation error response model"""
    detail: str
    error_code: Optional[str] = None