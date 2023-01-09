from typing import Dict, Any
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import  InferringRouter
from microservice.model.sentiment_model import  SentimentAnalyzer
from microservice.config.config_models import SentimentModelConfig

from microservice.api.payloads import SentimentAnalysisPayload
from microservice.api.responses import SentimentAnalysisResponse
from microservice import paths

router = InferringRouter()
@cbv(router)
class SentimentService:
    sentiment_analyzer = SentimentAnalyzer(
        SentimentModelConfig.parse_file(paths.SERVICE_CONFIG_PATH)
    )
    @router.post("/sentiment_analysis", response_model=SentimentAnalysisResponse)
    def handle_sentiment_analysis_inference_request(self, payload: SentimentAnalysisPayload) -> Dict[str, Any]:
        score = self.sentiment_analyzer.get_sentiment_score(payload.text)
        word_num = self.sentiment_analyzer.get_word_num(payload.text)
        results = {"sentiment_score": score, "word_num": word_num}
        return {"request": payload, "response": results}
