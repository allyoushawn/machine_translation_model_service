"""API router that includes all endpoints."""
from fastapi import APIRouter
from mt_model_service.api.endpoints import mt_service

api_router = APIRouter()
api_router.include_router(mt_service.router)