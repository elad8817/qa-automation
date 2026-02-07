import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

def _get_bool(name: str, default: bool = False) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "y", "on")

@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("BASE_URL", "https://the-internet.herokuapp.com")
    api_base_url: str = os.getenv("API_BASE_URL", "https://httpbin.org")
    headless: bool = _get_bool("HEADLESS", True)

settings = Settings()
