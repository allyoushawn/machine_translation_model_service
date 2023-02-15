from typing import Dict, Any
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from mt_model_service.model.mt_model import MTModel
from mt_model_service.config.config_models import MTModelConfig

from mt_model_service.api.payloads import MachineTranslationPayload
from mt_model_service.api.responses import MachineTranslationResponse
from mt_model_service import paths

router = InferringRouter()
@cbv(router)
class MTService:
    mt_model = MTModel(
        MTModelConfig.parse_file(paths.SERVICE_CONFIG_PATH)
    )
    @router.post("/machine_translation", response_model=MachineTranslationResponse)
    def handle_machine_translation_inference_request(self, payload: MachineTranslationPayload) -> Dict[str, Any]:
        translated_text = self.mt_model.get_translated_text(payload.text)
        word_num = MTModel.get_word_num(payload.text)
        results = {"translated_text": translated_text, "word_num": word_num}
        return {"request": payload, "response": results}
