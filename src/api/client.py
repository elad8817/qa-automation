import requests

class ApiClient:
    def __init__(self, base_url: str, timeout: int = 20):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def get(self, path: str, **kwargs):
        url = f"{self.base_url}/{path.lstrip('/')}"
        return self.session.get(url, timeout=self.timeout, **kwargs)

    def post(self, path: str, json=None, **kwargs):
        url = f"{self.base_url}/{path.lstrip('/')}"
        return self.session.post(url, json=json, timeout=self.timeout, **kwargs)
