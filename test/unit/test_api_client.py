import pytest
from unittest.mock import patch, MagicMock
from api.api_client import ApiClient
from api.api_config import BASE_URL, ENDPOINTS, HEADERS, TIMEOUT, MAX_RESPONSE_TIME


class TestApiClientBuildUrl:
    """Тесты формирования URL в ApiClient."""

    def test_relative_path_concatenation(self):
        client = ApiClient()
        assert client._build_url("/") == "https://itstep.by/"

    def test_relative_path_with_segment(self):
        client = ApiClient()
        assert client._build_url("/careers/") == "https://itstep.by/careers/"

    def test_full_http_url_returned_as_is(self):
        client = ApiClient()
        assert client._build_url("http://example.com") == "http://example.com"

    def test_full_https_url_returned_as_is(self):
        client = ApiClient()
        assert client._build_url("https://2english.itstep.by/") == "https://2english.itstep.by/"

    def test_custom_base_url(self):
        client = ApiClient(base_url="https://custom.api.com")
        assert client._build_url("/test") == "https://custom.api.com/test"


class TestApiClientSession:
    """Тесты HTTP-методов ApiClient с мокированной сессией."""

    def test_init_sets_base_url(self):
        client = ApiClient()
        assert client.base_url == BASE_URL

    def test_init_creates_session(self):
        client = ApiClient()
        assert client.session is not None

    def test_init_sets_headers(self):
        client = ApiClient()
        for key, value in HEADERS.items():
            assert client.session.headers[key] == value

    @patch("api.api_client.requests.Session")
    def test_get_calls_session_get(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session

        client = ApiClient()
        client.get("/")

        mock_session.get.assert_called_once()
        call_args = mock_session.get.call_args
        assert call_args[0][0] == "https://itstep.by/"

    @patch("api.api_client.requests.Session")
    def test_get_sets_default_timeout(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session

        client = ApiClient()
        client.get("/")

        call_kwargs = mock_session.get.call_args[1]
        assert call_kwargs["timeout"] == TIMEOUT

    @patch("api.api_client.requests.Session")
    def test_get_custom_timeout(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session

        client = ApiClient()
        client.get("/", timeout=5)

        call_kwargs = mock_session.get.call_args[1]
        assert call_kwargs["timeout"] == 5

    @patch("api.api_client.requests.Session")
    def test_post_calls_session_post(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session

        client = ApiClient()
        client.post("/form", data={"key": "value"})

        mock_session.post.assert_called_once()
        call_args = mock_session.post.call_args
        assert call_args[0][0] == "https://itstep.by/form"

    @patch("api.api_client.requests.Session")
    def test_head_calls_session_head(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session

        client = ApiClient()
        client.head("/")

        mock_session.head.assert_called_once()

    @patch("api.api_client.requests.Session")
    def test_get_with_full_url(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session

        client = ApiClient()
        client.get("https://example.com/api")

        call_args = mock_session.get.call_args
        assert call_args[0][0] == "https://example.com/api"

    @patch("api.api_client.requests.Session")
    def test_get_returns_response(self, mock_session_cls):
        mock_session = MagicMock()
        mock_resp = MagicMock()
        mock_session.get.return_value = mock_resp
        mock_session_cls.return_value = mock_session

        client = ApiClient()
        result = client.get("/")

        assert result is mock_resp


class TestApiConfig:
    """Тесты конфигурации API."""

    def test_base_url_is_string(self):
        assert isinstance(BASE_URL, str)

    def test_base_url_is_https(self):
        assert BASE_URL.startswith("https://")

    def test_endpoints_not_empty(self):
        assert len(ENDPOINTS) > 0

    def test_endpoints_has_main(self):
        assert "main" in ENDPOINTS

    def test_main_endpoint_is_root(self):
        assert ENDPOINTS["main"] == "/"

    def test_headers_has_user_agent(self):
        assert "User-Agent" in HEADERS

    def test_headers_has_accept(self):
        assert "Accept" in HEADERS

    def test_timeout_is_positive(self):
        assert TIMEOUT > 0

    def test_max_response_time_is_positive(self):
        assert MAX_RESPONSE_TIME > 0

    def test_max_response_time_less_than_timeout(self):
        assert MAX_RESPONSE_TIME <= TIMEOUT
