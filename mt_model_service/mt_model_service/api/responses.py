from pydantic import BaseModel, Extra
from mt_model_service.api.payloads import MachineTranslationPayload


class Result(BaseModel, extra=Extra.forbid):
    word_num: int
    translated_text: str


class MachineTranslationResponse(BaseModel, extra=Extra.forbid):
    request: MachineTranslationPayload
    response: Result
