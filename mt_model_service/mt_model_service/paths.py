import os
from pathlib import Path

_ROOT_DIR = Path(os.path.abspath(__file__)).parent
CONFIG_DIR = _ROOT_DIR / "config"
SERVICE_CONFIG_PATH = CONFIG_DIR / "service_config.json"
RESOURCE_DIR = _ROOT_DIR / "resource"
MODEL_PATH = RESOURCE_DIR / "model.cpu.pt"
SRC_VOCAB_PATH = RESOURCE_DIR / "src.vocab"
TGT_VOCAB_PATH = RESOURCE_DIR / "tgt.vocab"
