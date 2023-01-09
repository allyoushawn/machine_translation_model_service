from base_microservice.application import api as base_api
from microservice.api import api as sentiment_analysis_api
from fastapi import FastAPI
import uvicorn

def build_service() -> FastAPI:
    application: FastAPI = base_api.build_base_api()
    application.include_router((sentiment_analysis_api.api_router))
    return application

application: FastAPI = build_service()

if __name__ == "__main__":
    uvicorn.run(application, host="0.0.0.0")