"""API router that includes all endpoints."""
from fastapi import APIRouter
from sentiment_analysis_model_service.api.endpoints import sentiment_service

api_router = APIRouter()
api_router.include_router(sentiment_service.router)