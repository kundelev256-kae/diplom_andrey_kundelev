# Импорт pytest — тестовый фреймворк с фикстурами, маркерами и параметризацией
import pytest
# Импорт инструментов мокирования: patch для подмены объектов, MagicMock для создания мок-объектов
from unittest.mock import patch, MagicMock
# Импорт тестируемого класса API-клиента
from api.api_client import ApiClient
# Импорт конфигурационных констант: базовый URL, эндпоинты, заголовки, таймауты
from api.api_config import BASE_URL, ENDPOINTS, HEADERS, TIMEOUT, MAX_RESPONSE_TIME


# Класс тестов для проверки формирования URL в ApiClient
class TestApiClientBuildUrl:
    """Тесты формирования URL в ApiClient."""

    # Тест: проверяет, что корневой путь "/" корректно склеивается с BASE_URL
    def test_relative_path_concatenation(self):
        # Создаём экземпляр API-клиента
        client = ApiClient()
        # Утверждение: путь "/" должен дать полный URL "https://itstep.by/"
        assert client._build_url("/") == "https://itstep.by/"

    # Тест: проверяет, что путь "/careers/" корректно склеивается с BASE_URL
    def test_relative_path_with_segment(self):
        # Создаём экземпляр API-клиента
        client = ApiClient()
        # Утверждение: путь "/careers/" должен дать "https://itstep.by/careers/"
        assert client._build_url("/careers/") == "https://itstep.by/careers/"

    # Тест: проверяет, что полный HTTP-URL возвращается без изменений
    def test_full_http_url_returned_as_is(self):
        # Создаём экземпляр API-клиента
        client = ApiClient()
        # Утверждение: полный HTTP-URL не модифицируется
        assert client._build_url("http://example.com") == "http://example.com"

    # Тест: проверяет, что полный HTTPS-URL возвращается без изменений
    def test_full_https_url_returned_as_is(self):
        # Создаём экземпляр API-клиента
        client = ApiClient()
        # Утверждение: полный HTTPS-URL не модифицируется
        assert client._build_url("https://2english.itstep.by/") == "https://2english.itstep.by/"

    # Тест: проверяет, что кастомный base_url используется вместо дефолтного
    def test_custom_base_url(self):
        # Создаём экземпляр API-клиента с кастомным base_url
        client = ApiClient(base_url="https://custom.api.com")
        # Утверждение: путь "/test" должен склеиться с кастомным base_url
        assert client._build_url("/test") == "https://custom.api.com/test"


# Класс тестов для проверки HTTP-методов ApiClient с мокированной сессией
class TestApiClientSession:
    """Тесты HTTP-методов ApiClient с мокированной сессией."""

    # Тест: проверяет, что при инициализации устанавливается правильный base_url
    def test_init_sets_base_url(self):
        # Создаём экземпляр API-клиента
        client = ApiClient()
        # Утверждение: base_url должен совпадать с константой из конфига
        assert client.base_url == BASE_URL

    # Тест: проверяет, что при инициализации создаётся объект сессии requests.Session
    def test_init_creates_session(self):
        # Создаём экземпляр API-клиента
        client = ApiClient()
        # Утверждение: сессия не должна быть None
        assert client.session is not None

    # Тест: проверяет, что при инициализации в сессию устанавливаются заголовки из конфига
    def test_init_sets_headers(self):
        # Создаём экземпляр API-клиента
        client = ApiClient()
        # Проходим по всем заголовкам из конфига
        for key, value in HEADERS.items():
            # Утверждение: каждый заголовок из конфига должен быть в сессии
            assert client.session.headers[key] == value

    # Декоратор patch: подменяем requests.Session на мок во время теста
    @patch("api.api_client.requests.Session")
    # Тест: проверяет, что метод get() вызывает session.get()
    def test_get_calls_session_get(self, mock_session_cls):
        # Создаём мок-объект сессии
        mock_session = MagicMock()
        # Настраиваем, чтобы при вызове requests.Session() возвращался наш мок
        mock_session_cls.return_value = mock_session

        # Создаём API-клиент (он использует мок вместо реальной сессии)
        client = ApiClient()
        # Вызываем метод get с путём "/"
        client.get("/")

        # Утверждение: session.get() был вызван ровно один раз
        mock_session.get.assert_called_once()
        # Получаем аргументы вызова session.get()
        call_args = mock_session.get.call_args
        # Утверждение: первый аргумент (URL) должен быть "https://itstep.by/"
        assert call_args[0][0] == "https://itstep.by/"

    # Декоратор patch: подменяем requests.Session на мок
    @patch("api.api_client.requests.Session")
    # Тест: проверяет, что по умолчанию используется таймаут из конфига
    def test_get_sets_default_timeout(self, mock_session_cls):
        # Создаём мок-объект сессии
        mock_session = MagicMock()
        # Настраиваем возврат мока при создании сессии
        mock_session_cls.return_value = mock_session

        # Создаём API-клиент
        client = ApiClient()
        # Вызываем get без указания таймаута
        client.get("/")

        # Получаем именованные аргументы вызова session.get()
        call_kwargs = mock_session.get.call_args[1]
        # Утверждение: таймаут должен совпадать с константой TIMEOUT из конфига
        assert call_kwargs["timeout"] == TIMEOUT

    # Декоратор patch: подменяем requests.Session на мок
    @patch("api.api_client.requests.Session")
    # Тест: проверяет, что кастомный таймаут переопределяет дефолтный
    def test_get_custom_timeout(self, mock_session_cls):
        # Создаём мок-объект сессии
        mock_session = MagicMock()
        # Настраиваем возврат мока
        mock_session_cls.return_value = mock_session

        # Создаём API-клиент
        client = ApiClient()
        # Вызываем get с кастомным таймаутом 5 секунд
        client.get("/", timeout=5)

        # Получаем именованные аргументы вызова
        call_kwargs = mock_session.get.call_args[1]
        # Утверждение: таймаут должен быть 5 (кастомный), а не дефолтный
        assert call_kwargs["timeout"] == 5

    # Декоратор patch: подменяем requests.Session на мок
    @patch("api.api_client.requests.Session")
    # Тест: проверяет, что метод post() вызывает session.post()
    def test_post_calls_session_post(self, mock_session_cls):
        # Создаём мок-объект сессии
        mock_session = MagicMock()
        # Настраиваем возврат мока
        mock_session_cls.return_value = mock_session

        # Создаём API-клиент
        client = ApiClient()
        # Вызываем post с данными формы
        client.post("/form", data={"key": "value"})

        # Утверждение: session.post() был вызван ровно один раз
        mock_session.post.assert_called_once()
        # Получаем аргументы вызова
        call_args = mock_session.post.call_args
        # Утверждение: URL должен быть "https://itstep.by/form"
        assert call_args[0][0] == "https://itstep.by/form"

    # Декоратор patch: подменяем requests.Session на мок
    @patch("api.api_client.requests.Session")
    # Тест: проверяет, что метод head() вызывает session.head()
    def test_head_calls_session_head(self, mock_session_cls):
        # Создаём мок-объект сессии
        mock_session = MagicMock()
        # Настраиваем возврат мока
        mock_session_cls.return_value = mock_session

        # Создаём API-клиент
        client = ApiClient()
        # Вызываем head с путём "/"
        client.head("/")

        # Утверждение: session.head() был вызван ровно один раз
        mock_session.head.assert_called_once()

    # Декоратор patch: подменяем requests.Session на мок
    @patch("api.api_client.requests.Session")
    # Тест: проверяет, что полный URL передаётся без модификации
    def test_get_with_full_url(self, mock_session_cls):
        # Создаём мок-объект сессии
        mock_session = MagicMock()
        # Настраиваем возврат мока
        mock_session_cls.return_value = mock_session

        # Создаём API-клиент
        client = ApiClient()
        # Вызываем get с полным внешним URL
        client.get("https://example.com/api")

        # Получаем аргументы вызова
        call_args = mock_session.get.call_args
        # Утверждение: URL не должен модифицироваться (передаётся как есть)
        assert call_args[0][0] == "https://example.com/api"

    # Декоратор patch: подменяем requests.Session на мок
    @patch("api.api_client.requests.Session")
    # Тест: проверяет, что get() возвращает объект ответа без модификации
    def test_get_returns_response(self, mock_session_cls):
        # Создаём мок-объект сессии
        mock_session = MagicMock()
        # Создаём мок-объект ответа
        mock_resp = MagicMock()
        # Настраиваем, чтобы session.get() возвращал мок-ответ
        mock_session.get.return_value = mock_resp
        # Настраиваем возврат мока сессии
        mock_session_cls.return_value = mock_session

        # Создаём API-клиент
        client = ApiClient()
        # Вызываем get и сохраняем результат
        result = client.get("/")

        # Утверждение: возвращённый объект должен быть тем же мок-ответом
        assert result is mock_resp


# Класс тестов для проверки позитивных POST-запросов с мокированной сессией
class TestApiClientPostPositive:
    """Позитивные тесты POST-метода ApiClient."""

    # Декоратор patch: подменяем requests.Session на мок
    @patch("api.api_client.requests.Session")
    # Тест: проверяет, что post() с JSON-данными вызывает session.post() с корректными аргументами
    def test_post_json_data(self, mock_session_cls):
        # Создаём мок-объект сессии
        mock_session = MagicMock()
        # Создаём мок-объект ответа с кодом 200
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        # Настраиваем, чтобы session.post() возвращал мок-ответ
        mock_session.post.return_value = mock_resp
        # Настраиваем возврат мока сессии
        mock_session_cls.return_value = mock_session

        # Создаём API-клиент
        client = ApiClient()
        # Формируем JSON-данные для отправки
        json_data = {"name": "Тест", "email": "test@example.com"}
        # Вызываем post с JSON-данными
        result = client.post("/contacts/", json=json_data)

        # Утверждение: session.post() был вызван ровно один раз
        mock_session.post.assert_called_once()
        # Получаем аргументы вызова
        call_args = mock_session.post.call_args
        # Утверждение: URL должен быть сформирован корректно
        assert call_args[0][0] == "https://itstep.by/contacts/"
        # Утверждение: JSON-данные должны быть переданы в вызов
        assert call_args[1]["json"] == json_data
        # Утверждение: результат должен быть мок-ответом
        assert result is mock_resp
        # Утверждение: статус-код ответа должен быть 200
        assert result.status_code == 200

    # Декоратор patch: подменяем requests.Session на мок
    @patch("api.api_client.requests.Session")
    # Тест: проверяет, что post() с form-data вызывает session.post() с data-параметром
    def test_post_form_data(self, mock_session_cls):
        # Создаём мок-объект сессии
        mock_session = MagicMock()
        # Создаём мок-объект ответа
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        # Настраиваем возврат мок-ответа
        mock_session.post.return_value = mock_resp
        # Настраиваем возврат мока сессии
        mock_session_cls.return_value = mock_session

        # Создаём API-клиент
        client = ApiClient()
        # Формируем данные формы
        form_data = {"name": "Иван", "phone": "+375291234567"}
        # Вызываем post с данными формы
        result = client.post("/kontakty/", data=form_data)

        # Утверждение: session.post() был вызван ровно один раз
        mock_session.post.assert_called_once()
        # Получаем аргументы вызова
        call_args = mock_session.post.call_args
        # Утверждение: data-параметр должен содержать переданные данные
        assert call_args[1]["data"] == form_data
        # Утверждение: результат должен быть мок-ответом
        assert result is mock_resp
        # Утверждение: статус-код ответа должен быть 200
        assert result.status_code == 200

    # Декоратор patch: подменяем requests.Session на мок
    @patch("api.api_client.requests.Session")
    # Тест: проверяет, что post() с файлами (multipart) корректно передаёт files-параметр
    def test_post_multipart_files(self, mock_session_cls):
        # Создаём мок-объект сессии
        mock_session = MagicMock()
        # Создаём мок-объект ответа
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        # Настраиваем возврат мок-ответа
        mock_session.post.return_value = mock_resp
        # Настраиваем возврат мока сессии
        mock_session_cls.return_value = mock_session

        # Создаём API-клиент
        client = ApiClient()
        # Формируем файл для загрузки (имя, содержимое, MIME-тип)
        files = {"file": ("test.txt", b"content", "text/plain")}
        # Формируем поля формы
        data = {"name": "Тест"}
        # Вызываем post с файлами и данными
        result = client.post("/kontakty/", data=data, files=files)

        # Утверждение: session.post() был вызван ровно один раз
        mock_session.post.assert_called_once()
        # Получаем аргументы вызова
        call_args = mock_session.post.call_args
        # Утверждение: files-параметр должен быть передан
        assert call_args[1]["files"] == files
        # Утверждение: data-параметр должен быть передан
        assert call_args[1]["data"] == data
        # Утверждение: результат должен быть мок-ответом
        assert result is mock_resp
        # Утверждение: статус-код ответа должен быть 200
        assert result.status_code == 200

    # Декоратор patch: подменяем requests.Session на мок
    @patch("api.api_client.requests.Session")
    # Тест: проверяет, что post() по умолчанию использует таймаут из конфига
    def test_post_default_timeout(self, mock_session_cls):
        # Создаём мок-объект сессии
        mock_session = MagicMock()
        # Создаём мок-объект ответа
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        # Настраиваем возврат мок-ответа
        mock_session.post.return_value = mock_resp
        # Настраиваем возврат мока сессии
        mock_session_cls.return_value = mock_session

        # Создаём API-клиент
        client = ApiClient()
        # Вызываем post без явного указания таймаута
        client.post("/", json={"key": "value"})

        # Получаем именованные аргументы вызова
        call_kwargs = mock_session.post.call_args[1]
        # Утверждение: таймаут должен совпадать с константой TIMEOUT из конфига
        assert call_kwargs["timeout"] == TIMEOUT

    # Декоратор patch: подменяем requests.Session на мок
    @patch("api.api_client.requests.Session")
    # Тест: проверяет, что post() с кастомным таймаутом переопределяет дефолтный
    def test_post_custom_timeout(self, mock_session_cls):
        # Создаём мок-объект сессии
        mock_session = MagicMock()
        # Создаём мок-объект ответа
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        # Настраиваем возврат мок-ответа
        mock_session.post.return_value = mock_resp
        # Настраиваем возврат мока сессии
        mock_session_cls.return_value = mock_session

        # Создаём API-клиент
        client = ApiClient()
        # Вызываем post с кастомным таймаутом 10 секунд
        client.post("/", json={"key": "value"}, timeout=10)

        # Получаем именованные аргументы вызова
        call_kwargs = mock_session.post.call_args[1]
        # Утверждение: таймаут должен быть 10 (кастомный)
        assert call_kwargs["timeout"] == 10

    # Декоратор patch: подменяем requests.Session на мок
    @patch("api.api_client.requests.Session")
    # Тест: проверяет, что post() с полным URL не модифицирует его
    def test_post_full_url(self, mock_session_cls):
        # Создаём мок-объект сессии
        mock_session = MagicMock()
        # Создаём мок-объект ответа
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        # Настраиваем возврат мок-ответа
        mock_session.post.return_value = mock_resp
        # Настраиваем возврат мока сессии
        mock_session_cls.return_value = mock_session

        # Создаём API-клиент
        client = ApiClient()
        # Вызываем post с полным внешним URL
        client.post("https://external.api.com/webhook", json={"event": "test"})

        # Получаем аргументы вызова
        call_args = mock_session.post.call_args
        # Утверждение: URL не должен модифицироваться (передаётся как есть)
        assert call_args[0][0] == "https://external.api.com/webhook"

    # Декоратор patch: подменяем requests.Session на мок
    @patch("api.api_client.requests.Session")
    # Тест: проверяет, что post() корректно передаёт кастомные заголовки
    def test_post_custom_headers(self, mock_session_cls):
        # Создаём мок-объект сессии
        mock_session = MagicMock()
        # Создаём мок-объект ответа
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        # Настраиваем возврат мок-ответа
        mock_session.post.return_value = mock_resp
        # Настраиваем возврат мока сессии
        mock_session_cls.return_value = mock_session

        # Создаём API-клиент
        client = ApiClient()
        # Формируем кастомные заголовки
        custom_headers = {"Content-Type": "application/json", "X-Custom": "value"}
        # Вызываем post с кастомными заголовками
        client.post("/", json={"key": "value"}, headers=custom_headers)

        # Получаем именованные аргументы вызова
        call_kwargs = mock_session.post.call_args[1]
        # Утверждение: кастомные заголовки должны быть переданы
        assert call_kwargs["headers"] == custom_headers


# Класс тестов для проверки конфигурации API
class TestApiConfig:
    """Тесты конфигурации API."""

    # Тест: проверяет, что BASE_URL является строкой
    def test_base_url_is_string(self):
        # Утверждение: BASE_URL должен быть строкой
        assert isinstance(BASE_URL, str)

    # Тест: проверяет, что BASE_URL использует HTTPS
    def test_base_url_is_https(self):
        # Утверждение: BASE_URL должен начинаться с "https://"
        assert BASE_URL.startswith("https://")

    # Тест: проверяет, что словарь ENDPOINTS не пустой
    def test_endpoints_not_empty(self):
        # Утверждение: количество эндпоинтов должно быть больше 0
        assert len(ENDPOINTS) > 0

    # Тест: проверяет, что в ENDPOINTS есть эндпоинт "main"
    def test_endpoints_has_main(self):
        # Утверждение: ключ "main" должен присутствовать в словаре
        assert "main" in ENDPOINTS

    # Тест: проверяет, что эндпоинт "main" указывает на корень сайта
    def test_main_endpoint_is_root(self):
        # Утверждение: значение эндпоинта "main" должно быть "/"
        assert ENDPOINTS["main"] == "/"

    # Тест: проверяет, что в заголовках есть User-Agent
    def test_headers_has_user_agent(self):
        # Утверждение: ключ "User-Agent" должен быть в HEADERS
        assert "User-Agent" in HEADERS

    # Тест: проверяет, что в заголовках есть Accept
    def test_headers_has_accept(self):
        # Утверждение: ключ "Accept" должен быть в HEADERS
        assert "Accept" in HEADERS

    # Тест: проверяет, что таймаут — положительное число
    def test_timeout_is_positive(self):
        # Утверждение: TIMEOUT должен быть больше 0
        assert TIMEOUT > 0

    # Тест: проверяет, что MAX_RESPONSE_TIME — положительное число
    def test_max_response_time_is_positive(self):
        # Утверждение: MAX_RESPONSE_TIME должен быть больше 0
        assert MAX_RESPONSE_TIME > 0

    # Тест: проверяет, что лимит времени отклика не превышает общий таймаут
    def test_max_response_time_less_than_timeout(self):
        # Утверждение: MAX_RESPONSE_TIME не должен превышать TIMEOUT
        assert MAX_RESPONSE_TIME <= TIMEOUT
