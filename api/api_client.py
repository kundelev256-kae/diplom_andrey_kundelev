import allure # Импорт библиотеки Allure для интеграции с системой отчётов о тестировании
import requests # Импорт библиотеки requests для выполнения HTTP-запросов

from api.api_config import BASE_URL, HEADERS, TIMEOUT # Импорт констант конфигурации API: базовый URL, заголовки и таймаут


class ApiClient: # Клиент для взаимодействия с REST API, инкапсулирующий логику HTTP-запросов

    def __init__(self, base_url=BASE_URL): # Конструктор: принимает базовый URL API (по умолчанию из конфига)
        self.base_url = base_url # Сохранение базового URL для последующего построения полных адресов
        self.session = requests.Session() # Создание сессии requests для переиспользования соединений и общих заголовков
        self.session.headers.update(HEADERS) # Установка стандартных HTTP-заголовков (User-Agent, Accept и др.) для всех запросов сессии

    @allure.step("GET {path}") # Декоратор Allure: автоматически добавляет шаг в отчёт при вызове метода GET
    def get(self, path, **kwargs): # Метод для выполнения HTTP GET-запроса по указанному пути
        url = self._build_url(path) # Формирование полного URL из относительного пути
        kwargs.setdefault("timeout", TIMEOUT) # Установка таймаута по умолчанию, если он не передан вызывающим кодом
        return self.session.get(url, **kwargs) # Выполнение GET-запроса через сессию с возвратом объекта Response

    @allure.step("POST {path}") # Декоратор Allure: автоматически добавляет шаг в отчёт при вызове метода POST
    def post(self, path, **kwargs): # Метод для выполнения HTTP POST-запроса по указанному пути
        url = self._build_url(path) # Формирование полного URL из относительного пути
        kwargs.setdefault("timeout", TIMEOUT) # Установка таймаута по умолчанию, если он не передан вызывающим кодом
        return self.session.post(url, **kwargs) # Выполнение POST-запроса через сессию с возвратом объекта Response

    @allure.step("HEAD {path}") # Декоратор Allure: автоматически добавляет шаг в отчёт при вызове метода HEAD
    def head(self, path, **kwargs): # Метод для выполнения HTTP HEAD-запроса (получение только заголовков ответа)
        url = self._build_url(path) # Формирование полного URL из относительного пути
        kwargs.setdefault("timeout", TIMEOUT) # Установка таймаута по умолчанию, если он не передан вызывающим кодом
        return self.session.head(url, **kwargs) # Выполнение HEAD-запроса через сессию с возвратом объекта Response

    def _build_url(self, path): # Приватный метод: формирует полный URL из базового URL и относительного пути
        if path.startswith("http"): # Если путь уже является полным URL (начинается с http/https)
            return path # Возврат полного URL как есть, без дополнительной обработки
        return f"{self.base_url}{path}" # Конкатенация базового URL с относительным путём для формирования итогового адреса
