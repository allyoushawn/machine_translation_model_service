import pytest
from fastapi.testclient import TestClient
from microservice.entrypoint import application
from typing import Generator

@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    client: TestClient = TestClient(application)
    client.testing = True
    yield client