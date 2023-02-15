from pydantic import BaseModel, Extra

class MTModelConfig(BaseModel, extra=Extra.forbid):
    int_place_holder: int
    emsize: int
    nhid: int
    nlayers: int
    nhead: int
    src_lang_spacy_model_name: str
