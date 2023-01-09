from fastapi import FastAPI

def build_base_api() -> FastAPI:
    application = FastAPI()
    return application