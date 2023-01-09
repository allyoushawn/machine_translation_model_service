"""API router that includes all endpoints."""
from fastapi import APIRouter
from microservice.api.endpoints import sentiment_service

api_router = APIRouter()
api_router.include_router(sentiment_service.router)