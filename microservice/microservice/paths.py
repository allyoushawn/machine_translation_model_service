import os
from pathlib import Path

_ROOT_DIR = Path(os.path.abspath(__file__)).parent
CONFIG_DIR = _ROOT_DIR / "config"
SERVICE_CONFIG_PATH = CONFIG_DIR / "service_config.json"
