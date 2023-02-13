from typing import Dict, Any
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import  InferringRouter
from sentiment_analysis_model_service.model.sentiment_model import  SentimentAnalyzer
from sentiment_analysis_model_service.config.config_models import SentimentModelConfig

from sentiment_analysis_model_service.api.payloads import SentimentAnalysisPayload
from sentiment_analysis_model_service.api.responses import SentimentAnalysisResponse
from sentiment_analysis_model_service import paths

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
