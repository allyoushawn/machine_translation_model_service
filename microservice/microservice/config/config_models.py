from pydantic import BaseModel, Extra

class SentimentModelConfig(BaseModel, extra=Extra.forbid):
    int_place_holder: int