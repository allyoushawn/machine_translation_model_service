from pydantic import BaseModel, Extra
from typing import Any, Dict, List


class MachineTranslationPayload(BaseModel, extra=Extra.forbid):
    text: str

    def get_payload_for_response(self) -> Dict[str, Any]:
        return self.dict()
