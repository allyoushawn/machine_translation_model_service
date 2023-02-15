import pytest
from sentiment_analysis_model_service.model.sentiment_model import SentimentAnalyzer
from typing import Generator
from sentiment_analysis_model_service.config.config_models import SentimentModelConfig


@pytest.fixture(scope="module")
def sentiment_analyzer() -> Generator[SentimentAnalyzer, None, None]:
    config = {
        "int_place_holder": 1
    }
    sentiment_analyzer: SentimentAnalyzer = SentimentAnalyzer(SentimentModelConfig.parse_obj(config))
    yield sentiment_analyzer

@pytest.mark.parametrize("text, valence, word_num", [("I am happy.", 1, 3), ("I am so sad.", -1, 4)])
def test_model(sentiment_analyzer: SentimentAnalyzer, text: str, valence: int, word_num: int) -> None:
    pred_score = sentiment_analyzer.get_sentiment_score(text)
    pred_word_num = sentiment_analyzer.get_word_num(text)
    if valence > 0:
        assert pred_score > 0
    elif valence < 0:
        assert pred_score < 0
    else:
        assert pred_score == 0

    assert pred_word_num == word_num
