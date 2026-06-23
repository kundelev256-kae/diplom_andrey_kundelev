import allure
import requests

from api.api_config import BASE_URL, HEADERS, TIMEOUT


class ApiClient:

    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    @allure.step("GET {path}")
    def get(self, path, **kwargs):
        url = self._build_url(path)
        kwargs.setdefault("timeout", TIMEOUT)
        return self.session.get(url, **kwargs)

    @allure.step("POST {path}")
    def post(self, path, **kwargs):
        url = self._build_url(path)
        kwargs.setdefault("timeout", TIMEOUT)
        return self.session.post(url, **kwargs)

    @allure.step("HEAD {path}")
    def head(self, path, **kwargs):
        url = self._build_url(path)
        kwargs.setdefault("timeout", TIMEOUT)
        return self.session.head(url, **kwargs)

    def _build_url(self, path):
        if path.startswith("http"):
            return path
        return f"{self.base_url}{path}"
