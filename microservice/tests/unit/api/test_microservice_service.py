import pytest
from typing import Generator, Dict, Any
from microservice.api.payloads import SentimentAnalysisPayload
from fastapi.testclient import TestClient
import json


@pytest.fixture(scope="module")
def microservice_hostname() -> Generator[str, None, None]:
    yield "http://0.0.0.0/sentiment_analysis"


@pytest.fixture(scope="module")
def valid_payload() -> Generator[SentimentAnalysisPayload, None, None]:
    payload = {
        "text": "I am happy today."
    }
    yield SentimentAnalysisPayload(**payload)


@pytest.fixture(scope="module")
def expected_response() -> Generator[Dict[str, Any], None, None]:
    yield {
        "word_num": 4,
        "sentiment_score": 3.0
    }


def test_service_correctness(client: TestClient, microservice_hostname: str,
                             valid_payload: SentimentAnalysisPayload,
                             expected_response: Dict[str, Any]) -> None:
    service_response = client.post(microservice_hostname, data=valid_payload.json())
    assert service_response.status_code == 200
    expected_response_sorted = json.dumps(expected_response, sort_keys=True)
    service_response_sorted = json.dumps(service_response.json()["response"], sort_keys=True)
    assert expected_response_sorted == service_response_sorted

def test_extra_key_in_payload(client: TestClient, microservice_hostname: str,
                             valid_payload: SentimentAnalysisPayload) -> None:
    invalid_payload = valid_payload.dict()
    invalid_payload["extra_key"] = "extra_key"
    service_response = client.post(microservice_hostname, data=json.dumps(invalid_payload))
    assert service_response.status_code == 422

def test_missing_key_in_payload(client: TestClient, microservice_hostname: str,
                              valid_payload: SentimentAnalysisPayload) -> None:
    invalid_payload = valid_payload.dict(exclude={"text"})
    service_response = client.post(microservice_hostname, data=json.dumps(invalid_payload))
    assert service_response.status_code == 422
