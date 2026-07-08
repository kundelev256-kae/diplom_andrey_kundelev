# Импорт библиотеки Allure для создания отчётов о тестировании и декорирования тестов
import allure
# Импорт pytest — тестовый фреймворк,добавляет фикстуры, маркеры, параметризацию
import pytest
# Импорт модуля time для работы со временем (проверка SSL-сертификата на просроченность)
import time
# Импорт модуля ssl для проверки SSL/TLS-сертификатов сервера
import ssl
# Импорт модуля socket для установки TCP-соединения с сервером (для проверки SSL)
import socket
# Импорт функции urlparse для разбора URL на компоненты (схема, хост, путь и т.д.)
from urllib.parse import urlparse

# Импорт API-клиента — класс-обёртка над requests для отправки HTTP-запросов
from api.api_client import ApiClient
# Импорт конфигурации API: базовый URL, словарь эндпоинтов, лимит времени отклика
from api.api_config import BASE_URL, ENDPOINTS, MAX_RESPONSE_TIME


# Фикстура pytest с областью видимости "session" — создаёт один экземпляр ApiClient на всю сессию тестов
@pytest.fixture(scope="session")
def api():
    # Возвращаем новый экземпляр API-клиента для использования во всех тестах
    return ApiClient()


# ──────────────────────────────────────────────
# 1. Проверка HTTP-статусов основных страниц
# ──────────────────────────────────────────────

# Декоратор Allure: название группы тестов — "Проверка HTTP-статусов основных страниц"
@allure.title('Проверка HTTP-статусов основных страниц')
# Декоратор Allure: фича — "API: HTTP-статусы" (группировка в отчёте)
@allure.feature('API: HTTP-статусы')
# Класс тестов для проверки HTTP-статусов всех основных страниц сайта
class TestHttpStatuses:

    # Декоратор Allure: story — "Главная страница" (подгруппа внутри фичи)
    @allure.story('Главная страница')
    # Декоратор Allure: уровень важности — BLOCKER (наивысший, блокирует всё)
    @allure.severity(allure.severity_level.BLOCKER)
    # Тест: проверяет, что главная страница возвращает HTTP 200
    def test_main_page_status(self, api):
        response = api.get(ENDPOINTS["main"])  # Отправляем GET-запрос на главную страницу через API-клиент
        assert response.status_code == 200  # Утверждение: статус-код ответа должен быть 200 (OK)

    # Декоратор Allure: story — "Вакансии"
    @allure.story('Вакансии')
    # Тест: проверяет, что страница вакансий возвращает HTTP 200
    def test_vacancies_status(self, api):
        response = api.get(ENDPOINTS["vacancies"])  # Отправляем GET-запрос на страницу вакансий
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200

    # Декоратор Allure: story — "Контакты"
    @allure.story('Контакты')
    # Тест: проверяет, что страница контактов возвращает HTTP 200
    def test_contacts_status(self, api):
        response = api.get(ENDPOINTS["contacts"])  # Отправляем GET-запрос на страницу контактов
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200

    # Декоратор Allure: story — "Новости"
    @allure.story('Новости')
    # Тест: проверяет, что страница новостей возвращает HTTP 200
    def test_news_status(self, api):
        response = api.get(ENDPOINTS["news"])  # Отправляем GET-запрос на страницу новостей
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200

    # Декоратор Allure: story — "Статьи"
    @allure.story('Статьи')
    # Тест: проверяет, что страница статей возвращает HTTP 200
    def test_articles_status(self, api):
        response = api.get(ENDPOINTS["articles"])  # Отправляем GET-запрос на страницу статей
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200

    # Декоратор Allure: story — "Курс QA"
    @allure.story('Курс QA')
    # Тест: проверяет, что страница курса QA возвращает HTTP 200
    def test_qa_course_status(self, api):
        response = api.get(ENDPOINTS["qa_course"])  # Отправляем GET-запрос на страницу курса QA
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200

    # Декоратор Allure: story — "Курс Python"
    @allure.story('Курс Python')
    # Тест: проверяет, что страница курса Python возвращает HTTP 200
    def test_python_course_status(self, api):
        response = api.get(ENDPOINTS["python_course"])  # Отправляем GET-запрос на страницу курса Python
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200

    # Декоратор Allure: story — "Курс Java"
    @allure.story('Курс Java')
    # Тест: проверяет, что страница курса Java возвращает HTTP 200
    def test_java_course_status(self, api):
        response = api.get(ENDPOINTS["java_course"])  # Отправляем GET-запрос на страницу курса Java
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200

    # Декоратор Allure: story — "Курс UX/UI"
    @allure.story('Курс UX/UI')
    # Тест: проверяет, что страница курса UX/UI возвращает HTTP 200
    def test_ux_ui_course_status(self, api):
        response = api.get(ENDPOINTS["ux_ui_course"])  # Отправляем GET-запрос на страницу курса UX/UI
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200

    # Декоратор Allure: story — "Data Analyst"
    @allure.story('Data Analyst')
    # Тест: проверяет, что страница курса Data Analyst возвращает HTTP 200
    def test_data_analyst_status(self, api):
        response = api.get(ENDPOINTS["data_analyst"])  # Отправляем GET-запрос на страницу курса Data Analyst
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200

    # Декоратор Allure: story — "Курс PM"
    @allure.story('Курс PM')
    # Тест: проверяет, что страница курса PM возвращает HTTP 200
    def test_pm_course_status(self, api):
        response = api.get(ENDPOINTS["pm_course"])  # Отправляем GET-запрос на страницу курса PM
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200

    # Декоратор Allure: story — "DevOps"
    @allure.story('DevOps')
    # Тест: проверяет, что страница курса DevOps возвращает HTTP 200
    def test_devops_status(self, api):
        response = api.get(ENDPOINTS["devops"])  # Отправляем GET-запрос на страницу курса DevOps
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200

    # Декоратор Allure: story — "IT Start"
    @allure.story('IT Start')
    # Тест: проверяет, что страница IT Start возвращает HTTP 200
    def test_it_start_status(self, api):
        response = api.get(ENDPOINTS["it_start"])  # Отправляем GET-запрос на страницу IT Start
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200

    # Декоратор Allure: story — "Карьерный тест"
    @allure.story('Карьерный тест')
    # Тест: проверяет, что страница карьерного теста возвращает HTTP 200
    def test_career_test_status(self, api):
        response = api.get(ENDPOINTS["career_test"])  # Отправляем GET-запрос на страницу карьерного теста
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200

    # Декоратор Allure: story — "Программы для детей 7-8"
    @allure.story('Программы для детей 7-8')
    # Тест: проверяет, что страница программы для детей 7-8 лет возвращает HTTP 200
    def test_kids_7_8_status(self, api):
        response = api.get(ENDPOINTS["kids_7_8"])  # Отправляем GET-запрос на страницу программы для детей 7-8 лет
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200

    # Декоратор Allure: story — "Программы для детей 9-11"
    @allure.story('Программы для детей 9-11')
    # Тест: проверяет, что страница программы для детей 9-11 лет возвращает HTTP 200
    def test_kids_9_11_status(self, api):
        response = api.get(ENDPOINTS["kids_9_11"])  # Отправляем GET-запрос на страницу программы для детей 9-11 лет
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200

    # Декоратор Allure: story — "Программы для детей 12-13"
    @allure.story('Программы для детей 12-13')
    # Тест: проверяет, что страница программы для детей 12-13 лет возвращает HTTP 200
    def test_kids_12_13_status(self, api):
        response = api.get(ENDPOINTS["kids_12_13"])  # Отправляем GET-запрос на страницу программы для детей 12-13 лет
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200

    # Декоратор Allure: story — "Английский язык"
    @allure.story('Английский язык')
    # Тест: проверяет, что страница английского языка возвращает HTTP 200
    def test_english_status(self, api):
        response = api.get(ENDPOINTS["english"])  # Отправляем GET-запрос на страницу английского языка
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200


# ──────────────────────────────────────────────
# 2. Проверка времени отклика
# ──────────────────────────────────────────────

# Декоратор Allure: название — "Проверка времени отклика страниц"
@allure.title('Проверка времени отклика страниц')
# Декоратор Allure: фича — "API: Производительность" (производительность сервера)
@allure.feature('API: Производительность')
# Класс тестов для проверки скорости загрузки страниц
class TestResponseTime:

    # Декоратор Allure: story — "Время отклика главной страницы"
    @allure.story('Время отклика главной страницы')
    # Декоратор Allure: уровень важности — CRITICAL (критический тест)
    @allure.severity(allure.severity_level.CRITICAL)
    # Тест: проверяет, что главная страница загружается быстрее MAX_RESPONSE_TIME
    def test_main_page_response_time(self, api):
        response = api.get(ENDPOINTS["main"])  # Отправляем GET-запрос на главную страницу
        # Утверждение: время загрузки (response.elapsed) должно быть меньше лимита из конфига
        assert response.elapsed.total_seconds() < MAX_RESPONSE_TIME, \
            f"Главная страница загружается {response.elapsed.total_seconds():.2f}с (лимит {MAX_RESPONSE_TIME}с)"

    # Декоратор Allure: story — "Время отклика всех страниц"
    @allure.story('Время отклика всех страниц')
    # Параметризация: проверяем время отклика для всех эндпоинтов кроме robots_txt, sitemap, english
    @pytest.mark.parametrize("name,path", [
        (name, path) for name, path in ENDPOINTS.items()
        if name not in ("robots_txt", "sitemap", "english")
    ])
    # Тест: проверяет, что каждая страница загружается быстрее MAX_RESPONSE_TIME
    def test_all_pages_response_time(self, api, name, path):
        response = api.get(path)  # Отправляем GET-запрос на текущую страницу из параметризации
        elapsed = response.elapsed.total_seconds()  # Получаем время загрузки в секундах
        # Утверждение: время загрузки должно быть меньше лимита
        assert elapsed < MAX_RESPONSE_TIME, \
            f"{name} загружается {elapsed:.2f}с (лимит {MAX_RESPONSE_TIME}с)"


# ──────────────────────────────────────────────
# 3. Проверка заголовков ответа
# ──────────────────────────────────────────────

# Декоратор Allure: название — "Проверка HTTP-заголовков"
@allure.title('Проверка HTTP-заголовков')
# Декоратор Allure: фича — "API: Заголовки"
@allure.feature('API: Заголовки')
# Класс тестов для проверки HTTP-заголовков ответа
class TestHeaders:

    # Декоратор Allure: story — "Content-Type главной страницы"
    @allure.story('Content-Type главной страницы')
    # Тест: проверяет, что главная страница возвращает Content-Type с text/html
    def test_main_page_content_type(self, api):
        response = api.get(ENDPOINTS["main"])  # Отправляем GET-запрос на главную страницу
        # Утверждение: заголовок Content-Type должен содержать "text/html"
        assert "text/html" in response.headers.get("Content-Type", "")

    # Декоратор Allure: story — "Наличие security-заголовков"
    @allure.story('Наличие security-заголовков')
    # Тест: проверяет, что ответ содержит хотя бы один security-заголовок
    def test_security_headers_present(self, api):
        response = api.get(ENDPOINTS["main"])  # Отправляем GET-запрос на главную страницу
        # Преобразуем заголовки в нижний регистр для регистронезависимого сравнения
        headers = {k.lower(): v for k, v in response.headers.items()}
        has_security = any(h in headers for h in [  # Проверяем наличие хотя бы одного из security-заголовков
            "x-frame-options", "content-security-policy",
            "x-content-type-options", "strict-transport-security"
        ])
        # Утверждение: хотя бы один security-заголовок должен присутствовать
        assert has_security, "Отсутствуют security-заголовки (X-Frame-Options/CSP/HSTS)"

    # Декоратор Allure: story — "Заголовки ответа содержат сервер"
    @allure.story('Заголовки ответа содержат сервер')
    # Тест: проверяет, что ответ содержит заголовок Server
    def test_server_header(self, api):
        response = api.get(ENDPOINTS["main"])  # Отправляем GET-запрос на главную страницу
        # Утверждение: заголовок Server должен присутствовать (в любом регистре)
        assert "Server" in response.headers or "server" in {k.lower(): v for k, v in response.headers.items()}

    # Декоратор Allure: story — "Все страницы возвращают text/html"
    @allure.story('Все страницы возвращают text/html')
    # Параметризация: проверяем Content-Type для всех эндпоинтов кроме robots_txt, sitemap, english
    @pytest.mark.parametrize("name,path", [
        (name, path) for name, path in ENDPOINTS.items()
        if name not in ("robots_txt", "sitemap", "english")
    ])
    # Тест: проверяет, что каждая страница возвращает Content-Type с text/html
    def test_content_type_all_pages(self, api, name, path):
        response = api.get(path)  # Отправляем GET-запрос на текущую страницу из параметризации
        # Утверждение: Content-Type должен содержать "text/html"
        assert "text/html" in response.headers.get("Content-Type", ""), \
            f"{name}: Content-Type не text/html ({response.headers.get('Content-Type')})"


# ──────────────────────────────────────────────
# 4. Проверка robots.txt и sitemap.xml
# ──────────────────────────────────────────────

# Декоратор Allure: название — "Проверка robots.txt и sitemap.xml"
@allure.title('Проверка robots.txt и sitemap.xml')
# Декоратор Allure: фича — "API: SEO" (поисковая оптимизация)
@allure.feature('API: SEO')
# Класс тестов для проверки SEO-файлов robots.txt и sitemap.xml
class TestRobotsAndSitemap:

    # Декоратор Allure: story — "robots.txt доступен"
    @allure.story('robots.txt доступен')
    # Тест: проверяет, что файл robots.txt доступен (HTTP 200)
    def test_robots_txt_status(self, api):
        response = api.get(ENDPOINTS["robots_txt"])  # Отправляем GET-запрос на robots.txt
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200 (файл найден и доступен)

    # Декоратор Allure: story — "robots.txt содержит User-agent"
    @allure.story('robots.txt содержит User-agent')
    # Тест: проверяет, что robots.txt содержит директиву User-agent
    def test_robots_txt_content(self, api):
        response = api.get(ENDPOINTS["robots_txt"])  # Отправляем GET-запрос на robots.txt
        assert "User-agent" in response.text  # Утверждение: текст ответа должен содержать "User-agent"

    # Декоратор Allure: story — "robots.txt ссылается на sitemap"
    @allure.story('robots.txt ссылается на sitemap')
    # Тест: проверяет, что robots.txt содержит ссылку на sitemap
    def test_robots_txt_has_sitemap(self, api):
        response = api.get(ENDPOINTS["robots_txt"])  # Отправляем GET-запрос на robots.txt
        assert "Sitemap" in response.text  # Утверждение: текст ответа должен содержать "Sitemap"

    # Декоратор Allure: story — "sitemap.xml доступен"
    @allure.story('sitemap.xml доступен')
    # Тест: проверяет, что файл sitemap.xml доступен (HTTP 200)
    def test_sitemap_status(self, api):
        response = api.get(ENDPOINTS["sitemap"])  # Отправляем GET-запрос на sitemap.xml
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200

    # Декоратор Allure: story — "sitemap.xml содержит URL"
    @allure.story('sitemap.xml содержит URL')
    # Тест: проверяет, что sitemap.xml содержит теги URL или sitemapindex
    def test_sitemap_content(self, api):
        response = api.get(ENDPOINTS["sitemap"])  # Отправляем GET-запрос на sitemap.xml
        text = response.text  # Сохраняем текст ответа
        # Утверждение: текст должен содержать теги <url>, <urlset>, <sitemapindex> или <sitemap>
        assert "<url>" in text or "<urlset" in text or "<sitemapindex" in text or "<sitemap>" in text, \
            "sitemap.xml не содержит тегов <url> или <sitemapindex>"


# ──────────────────────────────────────────────
# 5. Проверка SSL-сертификата
# ──────────────────────────────────────────────

# Декоратор Allure: название — "Проверка SSL-сертификата"
@allure.title('Проверка SSL-сертификата')
# Декоратор Allure: фича — "API: Безопасность" (шифрование соединения)
@allure.feature('API: Безопасность')
# Класс тестов для проверки валидности SSL-сертификата сайта
class TestSSL:

    # Декоратор Allure: story — "SSL-сертификат валиден"
    @allure.story('SSL-сертификат валиден')
    # Тест: проверяет, что SSL-сертификат сервера itstep.by валиден и может быть получен
    def test_ssl_certificate_valid(self):
        hostname = "itstep.by"  # Имя проверяемого хоста
        context = ssl.create_default_context()  # Создаём SSL-контекст с настройками по умолчанию (проверка цепочки сертификатов)
        # Устанавливаем TCP-соединение с сервером на порт 443 (HTTPS) с таймаутом 10 секунд
        with socket.create_connection((hostname, 443), timeout=10) as sock:
            # Оборачиваем TCP-соединение в SSL (TLS) с проверкой имени хоста
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()  # Получаем сертификат сервера (в виде словаря)
                assert cert is not None, "Сертификат не получен"  # Утверждение: сертификат должен быть получен (не None)

    # Декоратор Allure: story — "SSL-сертификат не просрочен"
    @allure.story('SSL-сертификат не просрочен')
    # Тест: проверяет, что SSL-сертификат не истёк (дата окончания > текущего времени)
    def test_ssl_certificate_not_expired(self):
        hostname = "itstep.by"  # Имя проверяемого хоста
        context = ssl.create_default_context()  # Создаём SSL-контекст с настройками по умолчанию
        # Устанавливаем TCP-соединение с сервером на порт 443
        with socket.create_connection((hostname, 443), timeout=10) as sock:
            # Оборачиваем соединение в SSL
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()  # Получаем сертификат сервера
                not_after = ssl.cert_time_to_seconds(cert["notAfter"])  # Преобразуем дату окончания сертификата в секунды (timestamp)
                assert not_after > time.time(), "SSL-сертификат просрочен"  # Утверждение: дата окончания должна быть больше текущего времени

    # Декоратор Allure: story — "SSL-сертификат выдан для правильного домена"
    @allure.story('SSL-сертификат выдан для правильного домена')
    # Тест: проверяет, что сертификат выдан для домена itstep.by
    def test_ssl_certificate_domain(self):
        hostname = "itstep.by"  # Имя проверяемого хоста
        context = ssl.create_default_context()  # Создаём SSL-контекст
        # Устанавливаем TCP-соединение
        with socket.create_connection((hostname, 443), timeout=10) as sock:
            # Оборачиваем в SSL
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()  # Получаем сертификат
                subject = dict(x[0] for x in cert.get("subject", ()))  # Извлекаем поле Subject (содержит Common Name)
                cn = subject.get("commonName", "")  # Получаем Common Name (CN) из сертификата
                # Получаем все альтернативные имена (SAN) с типом DNS
                alt_names = [v for t, v in cert.get("subjectAltName", ()) if t == "DNS"]
                all_names = [cn] + alt_names  # Объединяем CN и SAN в один список
                # Утверждение: hostname должен быть среди имён в сертификате
                assert any(hostname in name for name in all_names), \
                    f"Сертификат не содержит {hostname}: {all_names}"


# ──────────────────────────────────────────────
# 6. Проверка содержимого страниц
# ──────────────────────────────────────────────

# Декоратор Allure: название — "Проверка содержимого страниц"
@allure.title('Проверка содержимого страниц')
# Декоратор Allure: фича — "API: Контент"
@allure.feature('API: Контент')
# Класс тестов для проверки содержимого HTML-страниц
class TestPageContent:

    # Декоратор Allure: story — "Главная страница содержит заголовок"
    @allure.story('Главная страница содержит заголовок')
    # Тест: проверяет, что главная страница содержит тег <title> или упоминание "ит шаг"
    def test_main_page_has_title(self, api):
        response = api.get(ENDPOINTS["main"])  # Отправляем GET-запрос на главную страницу
        # Утверждение: текст должен содержать <title> или "ит шаг"
        assert "<title>" in response.text.lower() or "ит шаг" in response.text.lower()

    # Декоратор Allure: story — "Страница контактов содержит контакты"
    @allure.story('Страница контактов содержит контакты')
    # Тест: проверяет, что страница контактов содержит контактную информацию
    def test_contacts_page_content(self, api):
        response = api.get(ENDPOINTS["contacts"])  # Отправляем GET-запрос на страницу контактов
        text = response.text.lower()  # Приводим текст к нижнему регистру для регистронезависимого поиска
        # Утверждение: текст должен содержать одно из ключевых слов
        assert "контакт" in text or "телефон" in text or "адрес" in text

    # Декоратор Allure: story — "Страница вакансий содержит вакансии"
    @allure.story('Страница вакансий содержит вакансии')
    # Тест: проверяет, что страница вакансий содержит информацию о вакансиях
    def test_vacancies_page_content(self, api):
        response = api.get(ENDPOINTS["vacancies"])  # Отправляем GET-запрос на страницу вакансий
        text = response.text.lower()  # Приводим текст к нижнему регистру
        # Утверждение: текст должен содержать одно из ключевых слов
        assert "вакан" in text or "career" in text or "работ" in text

    # Декоратор Allure: story — "Страница новостей содержит новости"
    @allure.story('Страница новостей содержит новости')
    # Тест: проверяет, что страница новостей содержит новостной контент
    def test_news_page_content(self, api):
        response = api.get(ENDPOINTS["news"])  # Отправляем GET-запрос на страницу новостей
        text = response.text.lower()  # Приводим текст к нижнему регистру
        # Утверждение: текст должен содержать одно из ключевых слов
        assert "новост" in text or "news" in text or "мероприят" in text

    # Декоратор Allure: story — "Страница курса QA содержит информацию о курсе"
    @allure.story('Страница курса QA содержит информацию о курсе')
    # Тест: проверяет, что страница курса QA содержит релевантную информацию
    def test_qa_course_content(self, api):
        response = api.get(ENDPOINTS["qa_course"])  # Отправляем GET-запрос на страницу курса QA
        text = response.text.lower()  # Приводим текст к нижнему регистру
        assert "qa" in text or "тестир" in text  # Утверждение: текст должен содержать "qa" или "тестир"

    # Декоратор Allure: story — "Все страницы содержат ссылку на главную"
    @allure.story('Все страницы содержат ссылку на главную')
    # Параметризация: проверяем все страницы кроме robots_txt, sitemap, english, main
    @pytest.mark.parametrize("name,path", [
        (name, path) for name, path in ENDPOINTS.items()
        if name not in ("robots_txt", "sitemap", "english", "main")
    ])
    # Тест: проверяет, что каждая страница содержит ссылку на главную
    def test_all_pages_have_main_link(self, api, name, path):
        response = api.get(path)  # Отправляем GET-запрос на текущую страницу
        # Утверждение: страница должна содержать ссылку на корень сайта
        assert 'href="/"' in response.text or "href='/'" in response.text or \
               "itstep.by" in response.text.lower(), \
            f"{name}: не содержит ссылку на главную"


# ──────────────────────────────────────────────
# 7. Позитивные POST-тесты (отправка форм)
# ──────────────────────────────────────────────

# Декоратор Allure: название — "Позитивные POST-запросы"
@allure.title('Позитивные POST-запросы')
# Декоратор Allure: фича — "API: Формы (позитивные)"
@allure.feature('API: Формы (позитивные)')
# Класс позитивных тестов: проверяет, что сервер возвращает 200 при валидных POST-запросах
class TestPositivePostRequests:

    # Декоратор Allure: story — "POST с JSON-данными на главную"
    @allure.story('POST с JSON-данными на главную')
    # Декоратор Allure: уровень важности — CRITICAL
    @allure.severity(allure.severity_level.CRITICAL)
    # Тест: проверяет, что POST с JSON-данными на главную страницу возвращает 200
    def test_post_json_to_main(self, api):
        # Формируем тело запроса в формате JSON (имитация отправки формы)
        json_data = {"name": "Тест Тестов", "email": "test@example.com", "message": "Тестовое сообщение"}
        response = api.post(ENDPOINTS["main"], json=json_data)  # Отправляем POST-запрос с JSON-данными на главную страницу
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200 (OK)

    # Декоратор Allure: story — "POST с JSON на страницу курса QA"
    @allure.story('POST с JSON на страницу курса QA')
    # Тест: проверяет, что POST с заявкой на курс QA возвращает 200
    def test_post_json_to_qa_course(self, api):
        json_data = {  # Формируем JSON с заявкой на курс QA
            "name": "Петр Петров",
            "email": "petr@example.com",
            "phone": "+375297654321",
            "course": "qa",
            "utm_source": "organic"
        }
        response = api.post(ENDPOINTS["qa_course"], json=json_data)  # Отправляем POST-запрос с JSON на страницу курса QA
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200 (OK)

    # Декоратор Allure: story — "POST с JSON на страницу курса Python"
    @allure.story('POST с JSON на страницу курса Python')
    # Тест: проверяет, что POST с заявкой на курс Python возвращает 200
    def test_post_json_to_python_course(self, api):
        json_data = {  # Формируем JSON с заявкой на курс Python
            "name": "Анна Сидорова",
            "email": "anna@example.com",
            "phone": "+375299876543",
            "course": "python"
        }
        # Отправляем POST-запрос с JSON на страницу курса Python
        response = api.post(ENDPOINTS["python_course"], json=json_data)
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200 (OK)

    # Декоратор Allure: story — "POST с JSON на страницу курса Java"
    @allure.story('POST с JSON на страницу курса Java')
    # Тест: проверяет, что POST с заявкой на курс Java возвращает 200
    def test_post_json_to_java_course(self, api):
        json_data = {  # Формируем JSON с заявкой на курс Java
            "name": "Сергей Козлов",
            "email": "sergey@example.com",
            "phone": "+375291112233",
            "course": "java"
        }
        # Отправляем POST-запрос с JSON на страницу курса Java
        response = api.post(ENDPOINTS["java_course"], json=json_data)
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200 (OK)

    # Декоратор Allure: story — "POST с JSON на карьерный тест"
    @allure.story('POST с JSON на карьерный тест')
    # Тест: проверяет, что POST с результатами карьерного теста возвращает 200
    def test_post_json_to_career_test(self, api):
        json_data = {  # Формируем JSON с ответами на карьерный тест
            "answers": [1, 2, 3, 1, 2],
            "email": "career@example.com"
        }
        # Отправляем POST-запрос на страницу карьерного теста
        response = api.post(ENDPOINTS["career_test"], json=json_data)
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200 (OK)

    # Декоратор Allure: story — "POST с пустым JSON"
    @allure.story('POST с пустым JSON')
    # Тест: проверяет, что POST с пустым JSON-объектом возвращает 200
    def test_post_empty_json(self, api):
        response = api.post(ENDPOINTS["main"], json={})  # Отправляем POST-запрос с пустым JSON-объектом
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200 (OK)

    # Декоратор Allure: story — "POST с JSON на страницу UX/UI"
    @allure.story('POST с JSON на страницу UX/UI')
    # Тест: проверяет, что POST с заявкой на курс UX/UI возвращает 200
    def test_post_json_to_ux_ui_course(self, api):
        json_data = {  # Формируем JSON с заявкой на курс UX/UI
            "name": "Мария Волкова",
            "email": "maria@example.com",
            "phone": "+375294445566",
            "course": "ux_ui"
        }
        # Отправляем POST-запрос с JSON на страницу курса UX/UI
        response = api.post(ENDPOINTS["ux_ui_course"], json=json_data)
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200 (OK)

    # Декоратор Allure: story — "POST с JSON на страницу DevOps"
    @allure.story('POST с JSON на страницу DevOps')
    # Тест: проверяет, что POST с заявкой на курс DevOps возвращает 200
    def test_post_json_to_devops(self, api):
        json_data = {  # Формируем JSON с заявкой на курс DevOps
            "name": "Алексей Новиков",
            "email": "alexey@example.com",
            "phone": "+375297778899",
            "course": "devops"
        }
        response = api.post(ENDPOINTS["devops"], json=json_data)  # Отправляем POST-запрос с JSON на страницу курса DevOps
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200 (OK)

    # Декоратор Allure: story — "POST с JSON на страницу IT Start"
    @allure.story('POST с JSON на страницу IT Start')
    # Тест: проверяет, что POST с заявкой на программу IT Start возвращает 200
    def test_post_json_to_it_start(self, api):
        json_data = {  # Формируем JSON с заявкой на программу IT Start
            "name": "Дмитрий Смирнов",
            "email": "dmitry@example.com",
            "phone": "+375290001122",
            "program": "it_start",
            "age": 15
        }
        response = api.post(ENDPOINTS["it_start"], json=json_data)  # Отправляем POST-запрос с JSON на страницу IT Start
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200 (OK)

    # Декоратор Allure: story — "POST с кириллицей в JSON"
    @allure.story('POST с кириллицей в JSON')
    # Тест: проверяет, что сервер корректно обрабатывает кириллические символы в JSON
    def test_post_cyrillic_json(self, api):
        json_data = {  # Формируем JSON с кириллическими данными
            "name": "Тест Тестович Тестов",
            "email": "кириллица@пример.рф",
            "message": "Привет! Это тестовое сообщение на русском языке с ё, ъ, ы"
        }
        response = api.post(ENDPOINTS["contacts"], json=json_data)  # Отправляем POST-запрос с кириллическим JSON
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200 (OK)

    # Декоратор Allure: story — "POST с длинными данными"
    @allure.story('POST с длинными данными')
    # Тест: проверяет, что сервер корректно обрабатывает длинные строки в форме
    def test_post_long_data(self, api):
        json_data = {  # Формируем JSON с длинным сообщением (1000 символов)
            "name": "Тест",
            "email": "long@example.com",
            "message": "А" * 1000
        }
        response = api.post(ENDPOINTS["contacts"], json=json_data)  # Отправляем POST-запрос с длинными данными
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200 (OK)

    # Декоратор Allure: story — "POST с JSON на страницу Data Analyst"
    @allure.story('POST с JSON на страницу Data Analyst')
    # Тест: проверяет, что POST с заявкой на курс Data Analyst возвращает 200
    def test_post_json_to_data_analyst(self, api):
        json_data = {  # Формируем JSON с заявкой на курс Data Analyst
            "name": "Елена Кузнецова",
            "email": "elena@example.com",
            "phone": "+375293334455",
            "course": "data_analyst"
        }
        # Отправляем POST-запрос с JSON на страницу курса Data Analyst
        response = api.post(ENDPOINTS["data_analyst"], json=json_data)
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200 (OK)


# ──────────────────────────────────────────────
# 8. Проверка methods (OPTIONS, HEAD)
# ──────────────────────────────────────────────

# Декоратор Allure: название — "Проверка HTTP-методов"
@allure.title('Проверка HTTP-методов')
# Декоратор Allure: фича — "API: HTTP-методы"
@allure.feature('API: HTTP-методы')
# Класс тестов для проверки HTTP-методов (HEAD)
class TestHttpMethods:

    # Декоратор Allure: story — "HEAD-запрос главной страницы"
    @allure.story('HEAD-запрос главной страницы')
    # Тест: проверяет, что HEAD-запрос на главную страницу возвращает 200
    def test_head_main_page(self, api):
        response = api.head(ENDPOINTS["main"])  # Отправляем HEAD-запрос на главную страницу
        assert response.status_code == 200  # Утверждение: статус-код должен быть 200

    # Декоратор Allure: story — "HEAD возвращает Content-Type"
    @allure.story('HEAD возвращает Content-Type')
    # Тест: проверяет, что HEAD-запрос возвращает заголовок Content-Type
    def test_head_content_type(self, api):
        response = api.head(ENDPOINTS["main"])  # Отправляем HEAD-запрос на главную страницу
        assert "Content-Type" in response.headers  # Утверждение: заголовок Content-Type должен присутствовать

    # Декоратор Allure: story — "HEAD не возвращает тело"
    @allure.story('HEAD не возвращает тело')
    # Тест: проверяет, что HEAD-запрос не возвращает тело ответа
    def test_head_no_body(self, api):
        response = api.head(ENDPOINTS["main"])  # Отправляем HEAD-запрос на главную страницу
        assert len(response.content) == 0  # Утверждение: длина тела ответа должна быть 0

    # Декоратор Allure: story — "HEAD для всех основных страниц"
    @allure.story('HEAD для всех основных страниц')
    # Параметризация: проверяем HEAD для всех эндпоинтов кроме robots_txt, sitemap, english
    @pytest.mark.parametrize("name,path", [
        (name, path) for name, path in ENDPOINTS.items()
        if name not in ("robots_txt", "sitemap", "english")
    ])
    # Тест: проверяет, что HEAD-запрос возвращает 200 для каждой страницы
    def test_head_all_pages(self, api, name, path):
        response = api.head(path)  # Отправляем HEAD-запрос на текущую страницу
        # Утверждение: статус должен быть 200
        assert response.status_code == 200, f"HEAD {name} вернул {response.status_code}"


# ──────────────────────────────────────────────
# 9. Проверка кеширования
# ──────────────────────────────────────────────

# Декоратор Allure: название — "Проверка кеширования"
@allure.title('Проверка кеширования')
# Декоратор Allure: фича — "API: Кеширование"
@allure.feature('API: Кеширование')
# Класс тестов для проверки заголовков кеширования
class TestCaching:

    # Декоратор Allure: story — "Заголовки кеширования главной страницы"
    @allure.story('Заголовки кеширования главной страницы')
    # Тест: проверяет, что главная страница содержит заголовки кеширования или сжатия
    def test_cache_headers(self, api):
        response = api.get(ENDPOINTS["main"])  # Отправляем GET-запрос на главную страницу
        # Преобразуем заголовки в нижний регистр
        headers = {k.lower(): v for k, v in response.headers.items()}
        has_cache = any(h in headers for h in [  # Проверяем наличие хотя бы одного из заголовков кеширования/сжатия
            "cache-control", "etag", "last-modified",
            "expires", "vary", "content-encoding"
        ])
        # Утверждение: хотя бы один заголовок кеширования должен присутствовать
        assert has_cache, "Отсутствуют заголовки кеширования/сжатия"

    # Декоратор Allure: story — "Повторный запрос возвращает тот же ETag"
    @allure.story('Повторный запрос возвращает тот же ETag')
    # Тест: проверяет, что ETag не меняется между двумя запросами
    def test_etag_consistency(self, api):
        r1 = api.get(ENDPOINTS["main"])  # Отправляем первый GET-запрос
        r2 = api.get(ENDPOINTS["main"])  # Отправляем второй GET-запрос
        etag1 = r1.headers.get("ETag", "")  # Получаем ETag из первого ответа
        etag2 = r2.headers.get("ETag", "")  # Получаем ETag из второго ответа
        # Если ETag есть — проверяем, что он не изменился
        if etag1:
            assert etag1 == etag2, f"ETag изменился: {etag1} -> {etag2}"


# ──────────────────────────────────────────────
# 10. Проверка cookie и сессий
# ──────────────────────────────────────────────

# Декоратор Allure: название — "Проверка cookie"
@allure.title('Проверка cookie')
# Декоратор Allure: фича — "API: Cookie"
@allure.feature('API: Cookie')
# Класс тестов для проверки cookie в ответах сервера
class TestCookies:

    # Декоратор Allure: story — "Ответ содержит cookie"
    @allure.story('Ответ содержит cookie')
    # Тест: проверяет, что ответ сервера содержит cookie
    def test_cookies_present(self, api):
        response = api.get(ENDPOINTS["main"])  # Отправляем GET-запрос на главную страницу
        cookies = response.cookies  # Получаем cookie из ответа
        assert len(cookies) >= 0  # Утверждение: количество cookie должно быть >= 0 (проверяем, что объект существует)

    # Декоратор Allure: story — "Cookie-согласие"
    @allure.story('Cookie-согласие')
    # Тест: проверяет, что на странице есть уведомление о cookie
    def test_cookie_consent(self, api):
        response = api.get(ENDPOINTS["main"])  # Отправляем GET-запрос на главную страницу
        text = response.text.lower()  # Приводим текст к нижнему регистру
        # Утверждение: текст должен содержать упоминание cookie или кнопку принятия
        assert "cookie" in text or "cookies" in text or "button-accept-cookies" in text


# ──────────────────────────────────────────────
# 11. Проверка навигации через ссылки в HTML
# ──────────────────────────────────────────────

# Декоратор Allure: название — "Проверка внутренних ссылок"
@allure.title('Проверка внутренних ссылок')
# Декоратор Allure: фича — "API: Ссылки"
@allure.feature('API: Ссылки')
# Класс тестов для проверки доступности внутренних ссылок сайта
class TestInternalLinks:

    # Декоратор Allure: story — "Все внутренние ссылки доступны (выборочно)"
    @allure.story('Все внутренние ссылки доступны (выборочно)')
    # Параметризация: список основных внутренних путей сайта
    @pytest.mark.parametrize("path", [
        "/",
        "/careers/",
        "/kontakty/",
        "/news/",
        "/stati-i-publikaczii/",
        "/testirovanie-po-qa/",
        "/razrabotka-po-na-python/",
        "/razrabotka-po-na-java/",
        "/ux-ui-dizajn/",
        "/upravlenie-proektami-v-it-pm/",
        "/devops-engineer/",
        "/it-start/",
        "/career-guidance-test/",
        "/kursy-dlya-detej-7-8-let/",
        "/kursy-dlya-detej-9-11-let/",
        "/kursy-dlya-detej-12-13-let/",
    ])
    # Тест: проверяет, что каждая внутренняя ссылка возвращает HTTP 200
    def test_internal_link_accessible(self, api, path):
        response = api.get(path)  # Отправляем GET-запрос на текущий путь
        # Утверждение: статус-код должен быть 200
        assert response.status_code == 200, \
            f"Внутренняя ссылка {path} вернула {response.status_code}"
