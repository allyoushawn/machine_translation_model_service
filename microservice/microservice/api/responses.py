from pydantic import BaseModel, Extra
from microservice.api.payloads import SentimentAnalysisPayload


class Result(BaseModel, extra=Extra.forbid):
    word_num: int
    sentiment_score: float


class SentimentAnalysisResponse(BaseModel, extra=Extra.forbid):
    request: SentimentAnalysisPayload
    response: Result
