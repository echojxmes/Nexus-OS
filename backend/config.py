import json
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "config.json"

_config_cache = None

def load_config():
    global _config_cache
    if _config_cache is None:
        with open(CONFIG_PATH, "r") as f:
            _config_cache = json.load(f)
    return _config_cache

def reload_config():
    global _config_cache
    _config_cache = None
    return load_config()

def is_simulation() -> bool:
    return load_config().get("simulation", True)