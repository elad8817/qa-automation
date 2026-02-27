import os
from dotenv import load_dotenv

load_dotenv()


def str_to_bool(value) -> bool:
    """
    Convert common string representations to bool.
    Accepts: true/false, 1/0, yes/no, y/n (case-insensitive).
    """
    if isinstance(value, bool):
        return value

    if value is None:
        raise ValueError("Boolean value cannot be None")

    s = str(value).strip().lower()
    if s in {"true", "1", "yes", "y", "on"}:
        return True
    if s in {"false", "0", "no", "n", "off"}:
        return False

    raise ValueError(f"Invalid boolean value: {value!r}. Use true/false, 1/0, yes/no.")


class Settings:
    def __init__(self, headless: bool = True):
        self.base_url = os.getenv("BASE_URL", "https://www.cnarios.com")
        self.api_base_url = os.getenv("API_BASE_URL", "https://httpbin.org")
        self.headless = headless


settings = Settings(headless=str_to_bool(os.getenv("HEADLESS", "true")))
