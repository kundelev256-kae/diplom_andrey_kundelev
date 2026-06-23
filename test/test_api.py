import allure
import pytest
import time
import ssl
import socket
from urllib.parse import urlparse

from api.api_client import ApiClient
from api.api_config import BASE_URL, ENDPOINTS, MAX_RESPONSE_TIME


@pytest.fixture(scope="session")
def api():
    return ApiClient()


# ──────────────────────────────────────────────
# 1. Проверка HTTP-статусов основных страниц
# ──────────────────────────────────────────────

@allure.title('Проверка HTTP-статусов основных страниц')
@allure.feature('API: HTTP-статусы')
class TestHttpStatuses:

    @allure.story('Главная страница')
    @allure.severity(allure.severity_level.BLOCKER)
    def test_main_page_status(self, api):
        response = api.get(ENDPOINTS["main"])
        assert response.status_code == 200

    # @allure.story('Вакансии')
    # def test_vacancies_status(self, api):
    #     response = api.get(ENDPOINTS["vacancies"])
    #     assert response.status_code == 200
    #
    # @allure.story('Контакты')
    # def test_contacts_status(self, api):
    #     response = api.get(ENDPOINTS["contacts"])
    #     assert response.status_code == 200
    #
    # @allure.story('Новости')
    # def test_news_status(self, api):
    #     response = api.get(ENDPOINTS["news"])
    #     assert response.status_code == 200
    #
    # @allure.story('Статьи')
    # def test_articles_status(self, api):
    #     response = api.get(ENDPOINTS["articles"])
    #     assert response.status_code == 200
    #
    # @allure.story('Курс QA')
    # def test_qa_course_status(self, api):
    #     response = api.get(ENDPOINTS["qa_course"])
    #     assert response.status_code == 200
    #
    # @allure.story('Курс Python')
    # def test_python_course_status(self, api):
    #     response = api.get(ENDPOINTS["python_course"])
    #     assert response.status_code == 200
    #
    # @allure.story('Курс Java')
    # def test_java_course_status(self, api):
    #     response = api.get(ENDPOINTS["java_course"])
    #     assert response.status_code == 200
    #
    # @allure.story('Курс UX/UI')
    # def test_ux_ui_course_status(self, api):
    #     response = api.get(ENDPOINTS["ux_ui_course"])
    #     assert response.status_code == 200
    #
    # @allure.story('Data Analyst')
    # def test_data_analyst_status(self, api):
    #     response = api.get(ENDPOINTS["data_analyst"])
    #     assert response.status_code == 200
    #
    # @allure.story('Курс PM')
    # def test_pm_course_status(self, api):
    #     response = api.get(ENDPOINTS["pm_course"])
    #     assert response.status_code == 200
    #
    # @allure.story('DevOps')
    # def test_devops_status(self, api):
    #     response = api.get(ENDPOINTS["devops"])
    #     assert response.status_code == 200
    #
    # @allure.story('IT Start')
    # def test_it_start_status(self, api):
    #     response = api.get(ENDPOINTS["it_start"])
    #     assert response.status_code == 200
    #
    # @allure.story('Карьерный тест')
    # def test_career_test_status(self, api):
    #     response = api.get(ENDPOINTS["career_test"])
    #     assert response.status_code == 200
    #
    # @allure.story('Программы для детей 7-8')
    # def test_kids_7_8_status(self, api):
    #     response = api.get(ENDPOINTS["kids_7_8"])
    #     assert response.status_code == 200
    #
    # @allure.story('Программы для детей 9-11')
    # def test_kids_9_11_status(self, api):
    #     response = api.get(ENDPOINTS["kids_9_11"])
    #     assert response.status_code == 200
    #
    # @allure.story('Программы для детей 12-13')
    # def test_kids_12_13_status(self, api):
    #     response = api.get(ENDPOINTS["kids_12_13"])
    #     assert response.status_code == 200
    #
    # @allure.story('Английский язык')
    # def test_english_status(self, api):
    #     response = api.get(ENDPOINTS["english"])
    #     assert response.status_code == 200


# ──────────────────────────────────────────────
# 2. Проверка времени отклика
# ──────────────────────────────────────────────

@allure.title('Проверка времени отклика страниц')
@allure.feature('API: Производительность')
class TestResponseTime:

    @allure.story('Время отклика главной страницы')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_main_page_response_time(self, api):
        response = api.get(ENDPOINTS["main"])
        assert response.elapsed.total_seconds() < MAX_RESPONSE_TIME, \
            f"Главная страница загружается {response.elapsed.total_seconds():.2f}с (лимит {MAX_RESPONSE_TIME}с)"

    # @allure.story('Время отклика всех страниц')
    # @pytest.mark.parametrize("name,path", [
    #     (name, path) for name, path in ENDPOINTS.items()
    #     if name not in ("robots_txt", "sitemap", "english")
    # ])
    # def test_all_pages_response_time(self, api, name, path):
    #     response = api.get(path)
    #     elapsed = response.elapsed.total_seconds()
    #     assert elapsed < MAX_RESPONSE_TIME, \
    #         f"{name} загружается {elapsed:.2f}с (лимит {MAX_RESPONSE_TIME}с)"


# ──────────────────────────────────────────────
# 3. Проверка заголовков ответа
# ──────────────────────────────────────────────

# @allure.title('Проверка HTTP-заголовков')
# @allure.feature('API: Заголовки')
# class TestHeaders:
#
#     @allure.story('Content-Type главной страницы')
#     def test_main_page_content_type(self, api):
#         response = api.get(ENDPOINTS["main"])
#         assert "text/html" in response.headers.get("Content-Type", "")
#
#     @allure.story('Наличие security-заголовков')
#     def test_security_headers_present(self, api):
#         response = api.get(ENDPOINTS["main"])
#         headers = {k.lower(): v for k, v in response.headers.items()}
#         has_security = any(h in headers for h in [
#             "x-frame-options", "content-security-policy",
#             "x-content-type-options", "strict-transport-security"
#         ])
#         assert has_security, "Отсутствуют security-заголовки (X-Frame-Options/CSP/HSTS)"
#
#     @allure.story('Заголовки ответа содержат сервер')
#     def test_server_header(self, api):
#         response = api.get(ENDPOINTS["main"])
#         assert "Server" in response.headers or "server" in {k.lower() for k in response.headers}
#
#     @allure.story('Все страницы возвращают text/html')
#     @pytest.mark.parametrize("name,path", [
#         (name, path) for name, path in ENDPOINTS.items()
#         if name not in ("robots_txt", "sitemap", "english")
#     ])
#     def test_content_type_all_pages(self, api, name, path):
#         response = api.get(path)
#         assert "text/html" in response.headers.get("Content-Type", ""), \
#             f"{name}: Content-Type не text/html ({response.headers.get('Content-Type')})"


# ──────────────────────────────────────────────
# 4. Проверка редиректов
# ──────────────────────────────────────────────

@allure.title('Проверка редиректов')
@allure.feature('API: Редиректы')
class TestRedirects:

    @allure.story('HTTP->HTTPS редирект')
    def test_http_to_https_redirect(self, api):
        response = api.get("http://itstep.by/", allow_redirects=False)
        assert response.status_code in (301, 302, 307, 308), \
            f"Ожидался редирект, получен {response.status_code}"
        location = response.headers.get("Location", "")
        assert "https" in location, f"Редирект не на HTTPS: {location}"

    # @allure.story('Редирект с trailing slash')
    # def test_redirect_trailing_slash(self, api):
    #     response = api.get("https://itstep.by/kontakty", allow_redirects=False)
    #     assert response.status_code in (301, 302, 307, 308, 200), \
    #         f"Неожиданный статус: {response.status_code}"
    #
    # @allure.story('Нет циклических редиректов')
    # def test_no_redirect_loop(self, api):
    #     response = api.get(ENDPOINTS["main"])
    #     assert len(response.history) < 10, \
    #         f"Обнаружено {len(response.history)} редиректов — возможен цикл"


# ──────────────────────────────────────────────
# 5. Проверка robots.txt и sitemap.xml
# ──────────────────────────────────────────────

@allure.title('Проверка robots.txt и sitemap.xml')
@allure.feature('API: SEO')
class TestRobotsAndSitemap:

    @allure.story('robots.txt доступен')
    def test_robots_txt_status(self, api):
        response = api.get(ENDPOINTS["robots_txt"])
        assert response.status_code == 200

    # @allure.story('robots.txt содержит User-agent')
    # def test_robots_txt_content(self, api):
    #     response = api.get(ENDPOINTS["robots_txt"])
    #     assert "User-agent" in response.text
    #
    # @allure.story('robots.txt ссылается на sitemap')
    # def test_robots_txt_has_sitemap(self, api):
    #     response = api.get(ENDPOINTS["robots_txt"])
    #     assert "Sitemap" in response.text
    #
    # @allure.story('sitemap.xml доступен')
    # def test_sitemap_status(self, api):
    #     response = api.get(ENDPOINTS["sitemap"])
    #     assert response.status_code == 200
    #
    # @allure.story('sitemap.xml содержит URL')
    # def test_sitemap_content(self, api):
    #     response = api.get(ENDPOINTS["sitemap"])
    #     text = response.text
    #     assert "<url>" in text or "<urlset" in text or "<sitemapindex" in text or "<sitemap>" in text, \
    #         "sitemap.xml не содержит тегов <url> или <sitemapindex>"


# ──────────────────────────────────────────────
# 6. Проверка SSL-сертификата
# ──────────────────────────────────────────────

@allure.title('Проверка SSL-сертификата')
@allure.feature('API: Безопасность')
class TestSSL:

    @allure.story('SSL-сертификат валиден')
    def test_ssl_certificate_valid(self):
        hostname = "itstep.by"
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                assert cert is not None, "Сертификат не получен"

    # @allure.story('SSL-сертификат не просрочен')
    # def test_ssl_certificate_not_expired(self):
    #     hostname = "itstep.by"
    #     context = ssl.create_default_context()
    #     with socket.create_connection((hostname, 443), timeout=10) as sock:
    #         with context.wrap_socket(sock, server_hostname=hostname) as ssock:
    #             cert = ssock.getpeercert()
    #             not_after = ssl.cert_time_to_seconds(cert["notAfter"])
    #             assert not_after > time.time(), "SSL-сертификат просрочен"
    #
    # @allure.story('SSL-сертификат выдан для правильного домена')
    # def test_ssl_certificate_domain(self):
    #     hostname = "itstep.by"
    #     context = ssl.create_default_context()
    #     with socket.create_connection((hostname, 443), timeout=10) as sock:
    #         with context.wrap_socket(sock, server_hostname=hostname) as ssock:
    #             cert = ssock.getpeercert()
    #             subject = dict(x[0] for x in cert.get("subject", ()))
    #             cn = subject.get("commonName", "")
    #             alt_names = [v for t, v in cert.get("subjectAltName", ()) if t == "DNS"]
    #             all_names = [cn] + alt_names
    #             assert any(hostname in name for name in all_names), \
    #                 f"Сертификат не содержит {hostname}: {all_names}"


# ──────────────────────────────────────────────
# 7. Проверка содержимого страниц
# ──────────────────────────────────────────────

# @allure.title('Проверка содержимого страниц')
# @allure.feature('API: Контент')
# class TestPageContent:
#
#     @allure.story('Главная страница содержит заголовок')
#     def test_main_page_has_title(self, api):
#         response = api.get(ENDPOINTS["main"])
#         assert "<title>" in response.text.lower() or "ит шаг" in response.text.lower()
#
#     @allure.story('Страница контактов содержит контакты')
#     def test_contacts_page_content(self, api):
#         response = api.get(ENDPOINTS["contacts"])
#         text = response.text.lower()
#         assert "контакт" in text or "телефон" in text or "адрес" in text
#
#     @allure.story('Страница вакансий содержит вакансии')
#     def test_vacancies_page_content(self, api):
#         response = api.get(ENDPOINTS["vacancies"])
#         text = response.text.lower()
#         assert "вакан" in text or "career" in text or "работ" in text
#
#     @allure.story('Страница новостей содержит новости')
#     def test_news_page_content(self, api):
#         response = api.get(ENDPOINTS["news"])
#         text = response.text.lower()
#         assert "новост" in text or "news" in text or "мероприят" in text
#
#     @allure.story('Страница курса QA содержит информацию о курсе')
#     def test_qa_course_content(self, api):
#         response = api.get(ENDPOINTS["qa_course"])
#         text = response.text.lower()
#         assert "qa" in text or "тестир" in text or "qa" in text
#
#     @allure.story('Все страницы содержат ссылку на главную')
#     @pytest.mark.parametrize("name,path", [
#         (name, path) for name, path in ENDPOINTS.items()
#         if name not in ("robots_txt", "sitemap", "english", "main")
#     ])
#     def test_all_pages_have_main_link(self, api, name, path):
#         response = api.get(path)
#         assert 'href="/"' in response.text or "href='/'" in response.text or \
#                "itstep.by" in response.text.lower(), \
#             f"{name}: не содержит ссылку на главную"


# ──────────────────────────────────────────────
# 8. Проверка POST-запросов (форма обратной связи)
# ──────────────────────────────────────────────

# @allure.title('Проверка POST-запросов')
# @allure.feature('API: Формы')
# class TestPostRequests:
#
#     @allure.story('POST на несуществующий endpoint')
#     def test_post_nonexistent_endpoint(self, api):
#         response = api.post("/nonexistent-endpoint-12345/")
#         assert response.status_code in (404, 405, 301, 302), \
#             f"Неожиданный статус: {response.status_code}"
#
#     @allure.story('POST без данных')
#     def test_post_empty(self, api):
#         response = api.post(ENDPOINTS["contacts"])
#         assert response.status_code in (200, 301, 302, 405), \
#             f"Неожиданный статус: {response.status_code}"


# ──────────────────────────────────────────────
# 9. Проверка methods (OPTIONS, HEAD)
# ──────────────────────────────────────────────

# @allure.title('Проверка HTTP-методов')
# @allure.feature('API: HTTP-методы')
# class TestHttpMethods:
#
#     @allure.story('HEAD-запрос главной страницы')
#     def test_head_main_page(self, api):
#         response = api.head(ENDPOINTS["main"])
#         assert response.status_code == 200
#
#     @allure.story('HEAD возвращает Content-Type')
#     def test_head_content_type(self, api):
#         response = api.head(ENDPOINTS["main"])
#         assert "Content-Type" in response.headers
#
#     @allure.story('HEAD не возвращает тело')
#     def test_head_no_body(self, api):
#         response = api.head(ENDPOINTS["main"])
#         assert len(response.content) == 0
#
#     @allure.story('HEAD для всех основных страниц')
#     @pytest.mark.parametrize("name,path", [
#         (name, path) for name, path in ENDPOINTS.items()
#         if name not in ("robots_txt", "sitemap", "english")
#     ])
#     def test_head_all_pages(self, api, name, path):
#         response = api.head(path)
#         assert response.status_code == 200, f"HEAD {name} вернул {response.status_code}"


# ──────────────────────────────────────────────
# 10. Проверка кеширования
# ──────────────────────────────────────────────

# @allure.title('Проверка кеширования')
# @allure.feature('API: Кеширование')
# class TestCaching:
#
#     @allure.story('Заголовки кеширования главной страницы')
#     def test_cache_headers(self, api):
#         response = api.get(ENDPOINTS["main"])
#         headers = {k.lower(): v for k, v in response.headers.items()}
#         has_cache = any(h in headers for h in [
#             "cache-control", "etag", "last-modified",
#             "expires", "vary", "content-encoding"
#         ])
#         assert has_cache, "Отсутствуют заголовки кеширования/сжатия"
#
#     @allure.story('Повторный запрос возвращает тот же ETag')
#     def test_etag_consistency(self, api):
#         r1 = api.get(ENDPOINTS["main"])
#         r2 = api.get(ENDPOINTS["main"])
#         etag1 = r1.headers.get("ETag", "")
#         etag2 = r2.headers.get("ETag", "")
#         if etag1:
#             assert etag1 == etag2, f"ETag изменился: {etag1} -> {etag2}"


# ──────────────────────────────────────────────
# 11. Проверка cookie и сессий
# ──────────────────────────────────────────────

# @allure.title('Проверка cookie')
# @allure.feature('API: Cookie')
# class TestCookies:
#
#     @allure.story('Ответ содержит cookie')
#     def test_cookies_present(self, api):
#         response = api.get(ENDPOINTS["main"])
#         cookies = response.cookies
#         assert len(cookies) >= 0
#
#     @allure.story('Cookie-согласие')
#     def test_cookie_consent(self, api):
#         response = api.get(ENDPOINTS["main"])
#         text = response.text.lower()
#         assert "cookie" in text or "cookies" in text or "button-accept-cookies" in text


# ──────────────────────────────────────────────
# 12. Проверка навигации через ссылки в HTML
# ──────────────────────────────────────────────

# @allure.title('Проверка внутренних ссылок')
# @allure.feature('API: Ссылки')
# class TestInternalLinks:
#
#     @allure.story('Все внутренние ссылки доступны (выборочно)')
#     @pytest.mark.parametrize("path", [
#         "/",
#         "/careers/",
#         "/kontakty/",
#         "/news/",
#         "/stati-i-publikaczii/",
#         "/testirovanie-po-qa/",
#         "/razrabotka-po-na-python/",
#         "/razrabotka-po-na-java/",
#         "/ux-ui-dizajn/",
#         "/upravlenie-proektami-v-it-pm/",
#         "/devops-engineer/",
#         "/it-start/",
#         "/career-guidance-test/",
#         "/kursy-dlya-detej-7-8-let/",
#         "/kursy-dlya-detej-9-11-let/",
#         "/kursy-dlya-detej-12-13-let/",
#     ])
#     def test_internal_link_accessible(self, api, path):
#         response = api.get(path)
#         assert response.status_code == 200, \
#             f"Внутренняя ссылка {path} вернула {response.status_code}"
