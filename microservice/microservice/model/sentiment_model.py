from afinn import Afinn
from microservice.config.config_models import SentimentModelConfig
from typing import Any, Dict, List


class SentimentAnalyzer:

    def __init__(self, config: SentimentModelConfig) -> None:
        self.scorer = Afinn()
        self.config = config


    def get_sentiment_score(self, text: str) -> float:
        """

        :param text:
        :return: sentiment analysis score of the given text
        """
        score = self.scorer.score(text)
        if type(score) is not float:
            raise Exception("Error returned type from Afinn")
        return score

    def get_word_num(self, text: str) -> int:
        return len(self.scorer.split(text))

if __name__ == "__main__":
    config = SentimentModelConfig.parse_obj({"int_place_holder": 1})
    sentiment_analyzer = SentimentAnalyzer(config)
    text = "This is really good."
    score = sentiment_analyzer.get_sentiment_score(text)
    print(f"text: {text}")
    print(f"score: {score}")
    word_num = sentiment_analyzer.get_word_num(text)
    print(f"word num: {word_num}")
    print(f"config int: {sentiment_analyzer.config.int_place_holder}")
