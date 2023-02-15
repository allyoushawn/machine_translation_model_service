import pytest
from fastapi.testclient import TestClient
from sentiment_analysis_model_service.entrypoint import application
from typing import Generator

@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    client: TestClient = TestClient(application)
    client.testing = True
    yield client