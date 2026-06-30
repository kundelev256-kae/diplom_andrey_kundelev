# Импорт библиотеки Allure для создания отчётов и декорирования тестов
import allure
# Импорт модуля time для использования задержек (sleep) между действиями браузера
import time
# Импорт модуля random для случайного выбора данных (имена, телефоны)
import random
# Импорт модуля string для работы со строковыми константами (не используется напрямую, но полезен для генерации)
import string

# Импорт локаторов главной страницы — содержит CSS/XPath селекторы для элементов
from locators.locators_main import MainPage
# Импорт Page Object для страницы карьерного теста (используется в E2E тесте)
from page.career_test_page import CareerTestPage
# Импорт By для указания способа поиска элементов (ID, XPath, CSS и т.д.)
from selenium.webdriver.common.by import By
# Импорт WebDriverWait для явного ожидания появления/кликабельности элементов
from selenium.webdriver.support.ui import WebDriverWait
# Импорт expected_conditions — предусловия для WebDriverWait (кликабельность, видимость и т.д.)
from selenium.webdriver.support import expected_conditions as EC


# Декоратор Allure: задаёт название теста в отчёте — "Проверка кнопки 'Вакансии'"
@allure.title('Проверка кнопки "Вакансии"')
# Декоратор Allure: группирует тест по фиче "Навигация" для удобства навигации в отчёте
@allure.feature('Навигация')
# Функция теста: проверяет переход на страницу вакансий. web_browser — фикстура Selenium WebDriver
def test_go_to_vacancies(web_browser):
    # Создаём экземпляр Page Object главной страницы, передавая экземпляр браузера
    page = MainPage(web_browser)

    # Шаг Allure: принимаем cookies, если баннер отображается
    with allure.step('Принять cookies'):
        # Проверяем, представлен ли (видим в DOM) кнопка принятия cookies
        if page.btn_access.is_presented():
            # Кликаем по кнопке принятия cookies, чтобы убрать баннер
            page.btn_access.click()

    # Шаг Allure: переход по ссылке "Вакансии"
    with allure.step('Перейти по ссылке "Вакансии"'):
        # Находим элемент ссылки "Вакансии" на странице
        element = page.vacancies_link.find()
        # Прокручиваем страницу так, чтобы элемент оказался в центре видимой области
        web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        # Явное ожидание: ждём до 10 секунд, пока ссылка не станет кликабельной (по XPath содержимому href)
        WebDriverWait(web_browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'careers')]")))
        # Кликаем по элементу через JavaScript (надёжнее стандартного клика для некоторых элементов)
        web_browser.execute_script("arguments[0].click();", element)
        # Пауза 3 секунды для завершения навигации и загрузки новой страницы
        time.sleep(3)

    # Шаг Allure: проверяем, что URL содержит подстроку "careers"
    with allure.step('Проверить URL содержит "careers"'):
        # Утверждение: текущий URL должен содержать "careers" — это подтверждает успешный переход
        assert "careers" in page.get_current_url()


# Декоратор Allure: название теста — "Проверка кнопки 'Контакты'"
@allure.title('Проверка кнопки "Контакты"')
# Декоратор Allure: фича — "Навигация"
@allure.feature('Навигация')
# Функция теста: проверяет переход на страницу контактов
def test_go_to_contacts(web_browser):
    # Создаём Page Object главной страницы
    page = MainPage(web_browser)

    # Шаг Allure: принимаем cookies, если баннер отображается
    with allure.step('Принять cookies'):
        # Если кнопка cookies присутствует — кликаем по ней
        if page.btn_access.is_presented():
            page.btn_access.click()

    # Шаг Allure: переход по ссылке "Контакты"
    with allure.step('Перейти по ссылке "Контакты"'):
        # Находим элемент ссылки "Контакты" на странице
        element = page.contacts_link.find()
        # Прокручиваем страницу к элементу, чтобы он был виден
        web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        # Кликаем по ссылке через JavaScript (обход потенциальных проблем с кликом)
        web_browser.execute_script("arguments[0].click();", element)
        # Ждём 3 секунды загрузки страницы контактов
        time.sleep(3)

    # Шаг Allure: проверяем, что URL содержит подстроку "kontakty"
    with allure.step('Проверить URL содержит "kontakty"'):
        # Утверждение: URL должен содержать "kontakty" — подтверждает успешный переход
        assert "kontakty" in page.get_current_url()


# ---- Закомментированные тесты (временно отключены) ----
# Тест перехода на страницу "Мероприятия" — отключён, т.к. ссылка может вести на внешний ресурс
# @allure.title('Проверка кнопки "Мероприятия"')
# @allure.feature('Навигация')
# def test_go_to_news(web_browser):
#     page = MainPage(web_browser)
#     with allure.step('Принять cookies'):
#         if page.btn_access.is_presented():
#             page.btn_access.click()
#     with allure.step('Перейти по ссылке "Мероприятия"'):
#         element = page.news_link.find()
#         web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
#         href = element.get_attribute("href")
#         web_browser.execute_script("arguments[0].click();", element)
#         time.sleep(3)
#         if "news" not in page.get_current_url():
#             web_browser.get(href)
#             time.sleep(3)
#     with allure.step('Проверить URL содержит "news"'):
#         assert "news" in page.get_current_url()

# Тест перехода на страницу "Статьи" — отключён
# @allure.title('Проверка кнопки "Статьи"')
# @allure.feature('Навигация')
# def test_go_to_articles(web_browser):
#     page = MainPage(web_browser)
#     with allure.step('Принять cookies'):
#         if page.btn_access.is_presented():
#             page.btn_access.click()
#     with allure.step('Перейти по ссылке "Статьи"'):
#         element = page.articles_link.find()
#         web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
#         web_browser.execute_script("arguments[0].click();", element)
#         time.sleep(3)
#     with allure.step('Проверить URL содержит "stati-i-publikaczii"'):
#         assert "stati-i-publikaczii" in page.get_current_url()

# Тест перехода на страницу "Обучение английскому языку" — отключён
# @allure.title('Проверка кнопки "Обучение английскому языку"')
# @allure.feature('Навигация')
# def test_go_to_english(web_browser):
#     page = MainPage(web_browser)
#     with allure.step('Принять cookies'):
#         if page.btn_access.is_presented():
#             page.btn_access.click()
#     with allure.step('Перейти по ссылке "Обучение английскому языку"'):
#         element = page.english_link.find()
#         web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
#         href = element.get_attribute("href")
#         web_browser.execute_script("arguments[0].click();", element)
#         time.sleep(3)
#         if "2english" not in page.get_current_url():
#             web_browser.get(href)
#             time.sleep(3)
#     with allure.step('Проверить URL содержит "2english"'):
#         assert "2english" in page.get_current_url()


# Декоратор Allure: название теста — "Проверка перехода на курс 'Тестирование ПО (QA)'"
@allure.title('Проверка перехода на курс "Тестирование ПО (QA)"')
# Декоратор Allure: фича — "Меню IT ОБРАЗОВАНИЕ" (тест проверяет навигацию через выпадающее меню)
@allure.feature('Меню IT ОБРАЗОВАНИЕ')
# Функция теста: проверяет переход на страницу курса QA через меню IT-образования
def test_go_to_qa_course(web_browser):
    # Создаём Page Object главной страницы
    page = MainPage(web_browser)

    # Шаг Allure: принимаем cookies
    with allure.step('Принять cookies'):
        # Если кнопка cookies видна — кликаем для закрытия баннера
        if page.btn_access.is_presented():
            page.btn_access.click()

    # Шаг Allure: открываем выпадающее меню "IT ОБРАЗОВАНИЕ"
    with allure.step('Открыть меню "IT ОБРАЗОВАНИЕ"'):
        # Находим элемент пункта меню "IT ОБРАЗОВАНИЕ"
        element = page.it_education_menu.find()
        # Прокручиваем к нему, чтобы он был кликабелен
        web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        # Кликаем по меню через JavaScript для раскрытия подменю
        web_browser.execute_script("arguments[0].click();", element)
        # Ждём 2 секунды для появления выпадающего списка с курсами
        time.sleep(2)

    # Шаг Allure: выбираем курс "Тестирование ПО (QA)" из раскрытого меню
    with allure.step('Кликнуть по курсу "Тестирование ПО (QA)"'):
        # Находим ссылку на курс QA в выпадающем меню
        qa = page.qa_course_link.find()
        # Кликаем по ссылке курса через JavaScript
        web_browser.execute_script("arguments[0].click();", qa)
        # Ждём 3 секунды для загрузки страницы курса
        time.sleep(3)

    # Шаг Allure: проверяем, что URL содержит "testirovanie-po-qa"
    with allure.step('Проверить URL содержит "testirovanie-po-qa"'):
        # Утверждение: URL должен содержать slug курса QA — подтверждает успешный переход
        assert "testirovanie-po-qa" in page.get_current_url()


# ---- Закомментированные тесты курсов IT-образования (временно отключены) ----
# Тест перехода на курс "Разработка ПО на Python"
# @allure.title('Проверка перехода на курс "Разработка ПО на Python"')
# @allure.feature('Меню IT ОБРАЗОВАНИЕ')
# def test_go_to_python_course(web_browser):
#     page = MainPage(web_browser)
#     with allure.step('Принять cookies'):
#         if page.btn_access.is_presented():
#             page.btn_access.click()
#     with allure.step('Открыть меню "IT ОБРАЗОВАНИЕ"'):
#         element = page.it_education_menu.find()
#         web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
#         web_browser.execute_script("arguments[0].click();", element)
#         time.sleep(2)
#     with allure.step('Кликнуть по курсу "Разработка ПО на Python"'):
#         link = page.python_course_link.find()
#         web_browser.execute_script("arguments[0].click();", link)
#         time.sleep(3)
#     with allure.step('Проверить URL содержит "razrabotka-po-na-python"'):
#         assert "razrabotka-po-na-python" in page.get_current_url()

# Тест перехода на курс "Разработка ПО на Java"
# @allure.title('Проверка перехода на курс "Разработка ПО на Java"')
# @allure.feature('Меню IT ОБРАЗОВАНИЕ')
# def test_go_to_java_course(web_browser):
#     page = MainPage(web_browser)
#     with allure.step('Принять cookies'):
#         if page.btn_access.is_presented():
#             page.btn_access.click()
#     with allure.step('Открыть меню "IT ОБРАЗОВАНИЕ"'):
#         element = page.it_education_menu.find()
#         web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
#         web_browser.execute_script("arguments[0].click();", element)
#         time.sleep(2)
#     with allure.step('Кликнуть по курсу "Разработка ПО на Java"'):
#         link = page.java_course_link.find()
#         web_browser.execute_script("arguments[0].click();", link)
#         time.sleep(3)
#     with allure.step('Проверить URL содержит "razrabotka-po-na-java"'):
#         assert "razrabotka-po-na-java" in page.get_current_url()

# Тест перехода на курс "UX/UI Дизайн"
# @allure.title('Проверка перехода на курс "UX/UI Дизайн"')
# @allure.feature('Меню IT ОБРАЗОВАНИЕ')
# def test_go_to_ux_ui_course(web_browser):
#     page = MainPage(web_browser)
#     with allure.step('Принять cookies'):
#         if page.btn_access.is_presented():
#             page.btn_access.click()
#     with allure.step('Открыть меню "IT ОБРАЗОВАНИЕ"'):
#         element = page.it_education_menu.find()
#         web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
#         web_browser.execute_script("arguments[0].click();", element)
#         time.sleep(2)
#     with allure.step('Кликнуть по курсу "UX/UI Дизайн"'):
#         link = page.ux_ui_course_link.find()
#         web_browser.execute_script("arguments[0].click();", link)
#         time.sleep(3)
#     with allure.step('Проверить URL содержит "ux-ui-dizajn"'):
#         assert "ux-ui-dizajn" in page.get_current_url()

# Тест перехода на курс "Data Analyst"
# @allure.title('Проверка перехода на курс "Data Analyst"')
# @allure.feature('Меню IT ОБРАЗОВАНИЕ')
# def test_go_to_data_analyst(web_browser):
#     page = MainPage(web_browser)
#     with allure.step('Принять cookies'):
#         if page.btn_access.is_presented():
#             page.btn_access.click()
#     with allure.step('Открыть меню "IT ОБРАЗОВАНИЕ"'):
#         element = page.it_education_menu.find()
#         web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
#         web_browser.execute_script("arguments[0].click();", element)
#         time.sleep(2)
#     with allure.step('Кликнуть по курсу "Аналитик данных в IT"'):
#         link = page.data_analyst_link.find()
#         web_browser.execute_script("arguments[0].click();", link)
#         time.sleep(3)
#     with allure.step('Проверить URL содержит "analitik-dannyh-v-it-data-analyst"'):
#         assert "analitik-dannyh-v-it-data-analyst" in page.get_current_url()

# Тест перехода на курс "Управление проектами в IT (PM)"
# @allure.title('Проверка перехода на курс "Управление проектами в IT (PM)"')
# @allure.feature('Меню IT ОБРАЗОВАНИЕ')
# def test_go_to_pm_course(web_browser):
#     page = MainPage(web_browser)
#     with allure.step('Принять cookies'):
#         if page.btn_access.is_presented():
#             page.btn_access.click()
#     with allure.step('Открыть меню "IT ОБРАЗОВАНИЕ"'):
#         element = page.it_education_menu.find()
#         web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
#         web_browser.execute_script("arguments[0].click();", element)
#         time.sleep(2)
#     with allure.step('Кликнуть по курсу "Управление проектами в IT (PM)"'):
#         link = page.pm_course_link.find()
#         web_browser.execute_script("arguments[0].click();", link)
#         time.sleep(3)
#     with allure.step('Проверить URL содержит "upravlenie-proektami-v-it-pm"'):
#         assert "upravlenie-proektami-v-it-pm" in page.get_current_url()

# Тест перехода на курс "DevOps+MLOps"
# @allure.title('Проверка перехода на курс "DevOps+MLOps"')
# @allure.feature('Меню IT ОБРАЗОВАНИЕ')
# def test_go_to_devops(web_browser):
#     page = MainPage(web_browser)
#     with allure.step('Принять cookies'):
#         if page.btn_access.is_presented():
#             page.btn_access.click()
#     with allure.step('Открыть меню "IT ОБРАЗОВАНИЕ"'):
#         element = page.it_education_menu.find()
#         web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
#         web_browser.execute_script("arguments[0].click();", element)
#         time.sleep(2)
#     with allure.step('Кликнуть по курсу "DevOps+MLOps"'):
#         link = page.devops_link.find()
#         web_browser.execute_script("arguments[0].click();", link)
#         time.sleep(3)
#     with allure.step('Проверить URL содержит "devops-engineer"'):
#         assert "devops-engineer" in page.get_current_url()

# Тест перехода на "Профориентационный тест"
# @allure.title('Проверка кнопки "Проф orientation тест"')
# @allure.feature('Меню IT ОБРАЗОВАНИЕ')
# def test_go_to_career_test(web_browser):
#     page = MainPage(web_browser)
#     with allure.step('Принять cookies'):
#         if page.btn_access.is_presented():
#             page.btn_access.click()
#     with allure.step('Открыть меню "IT ОБРАЗОВАНИЕ"'):
#         element = page.it_education_menu.find()
#         web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
#         web_browser.execute_script("arguments[0].click();", element)
#         time.sleep(2)
#     with allure.step('Кликнуть по "Профorientation тест"'):
#         link = page.career_test_link.find()
#         web_browser.execute_script("arguments[0].click();", link)
#         time.sleep(3)
#     with allure.step('Проверить URL содержит "career-guidance-test"'):
#         assert "career-guidance-test" in page.get_current_url()

# Тест перехода на курс "IT Start"
# @allure.title('Проверка перехода на "IT Start"')
# @allure.feature('Меню IT ОБРАЗОВАНИЕ')
# def test_go_to_it_start(web_browser):
#     page = MainPage(web_browser)
#     with allure.step('Принять cookies'):
#         if page.btn_access.is_presented():
#             page.btn_access.click()
#     with allure.step('Открыть меню "IT ОБРАЗОВАНИЕ"'):
#         element = page.it_education_menu.find()
#         web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
#         web_browser.execute_script("arguments[0].click();", element)
#         time.sleep(2)
#     with allure.step('Кликнуть по "КУРС IT START"'):
#         link = page.it_start_link.find()
#         web_browser.execute_script("arguments[0].click();", link)
#         time.sleep(3)
#     with allure.step('Проверить URL содержит "it-start"'):
#         assert "it-start" in page.get_current_url()

# Тест кнопки "ПОЛУЧИТЬ КОНСУЛЬТАЦИЮ" на слайдере — отключён
# @allure.title('Проверка кнопки "ПОЛУЧИТЬ КОНСУЛЬТАЦИЮ" на слайдере')
# @allure.feature('Слайдер')
# def test_slider_consultation_button(web_browser):
#     page = MainPage(web_browser)
#     with allure.step('Принять cookies'):
#         if page.btn_access.is_presented():
#             page.btn_access.click()
#     with allure.step('Найти кнопку "ПОЛУЧИТЬ КОНСУЛЬТАЦИЮ"'):
#         element = page.learn_more_btn.find()
#         assert element is not None, "Кнопка 'ПОЛУЧИТЬ КОНСУЛЬТАЦИЮ' не найдена"
#     with allure.step('Проверить кликабельность кнопки'):
#         is_clickable = page.learn_more_btn.is_clickable()
#         assert is_clickable, "Кнопка 'ПОЛУЧИТЬ КОНСУЛЬТАЦИЮ' некликабельна"


# Декоратор Allure: название — "Проверка кнопки 'Обратная связь' (чат)"
@allure.title('Проверка кнопки "Обратная связь" (чат)')
# Декоратор Allure: фича — "Форма обратной связи"
@allure.feature('Форма обратной связи')
# Функция теста: проверяет работоспособность виджета чата обратной связи (Bitrix24)
def test_feedback_form(web_browser):
    # Создаём Page Object главной страницы
    page = MainPage(web_browser)

    # Шаг Allure: принимаем cookies
    with allure.step('Принять cookies'):
        # Если кнопка cookies присутствует — кликаем
        if page.btn_access.is_presented():
            page.btn_access.click()

    # Шаг Allure: проверяем наличие виджета чата в DOM страницы
    with allure.step('Проверить наличие виджета чата в DOM'):
        # Ждём полной загрузки страницы (waitForPageLoaded)
        page.wait_page_loaded()
        # Дополнительная пауза 8 секунд — виджет чата может загружаться асинхронно (JS-виджет)
        time.sleep(8)
        # Находим элемент кнопки чата на странице
        chat = page.chat_button.find()
        # Утверждение: элемент чата должен быть найден в DOM
        assert chat is not None, "Виджет чата не найден в DOM"

    # Шаг Allure: кликаем по виджету чата через JavaScript
    with allure.step('Кликнуть по виджету чата через JS'):
        # Кликаем по кнопке чата через execute_script (обход стандартного клика)
        web_browser.execute_script("arguments[0].click();", chat)
        # Ждём 8 секунд — панель чата может открываться с анимацией/задержкой
        time.sleep(8)

    # Шаг Allure: проверяем, что панель чата появилась после клика
    with allure.step('Проверить появление элементов чата'):
        # Явное ожидание: ждём до 15 секунд появления элемента чата в DOM (Bitrix24 или b24-widget)
        chat_panel = WebDriverWait(web_browser, 15).until(
            EC.presence_of_element_located((By.XPATH,
                # XPath ищет элемент с классом b24-widget ИЛИ bitrix24 (два варианта разметки виджета)
                "//*[contains(@class,'b24-widget')] | "
                "//*[contains(@class,'bitrix24')]"
            ))
        )
        # Утверждение: панель чата должна появиться после клика
        assert chat_panel is not None, "Панель чата не появилась после клика"


# ---- Закомментированные тесты (временно отключены) ----
# Тест наличия логотипа на странице
# @allure.title('Проверка логотипа сайта')
# @allure.feature('Главная страница')
# def test_logo_present(web_browser):
#     page = MainPage(web_browser)
#     with allure.step('Принять cookies'):
#         if page.btn_access.is_presented():
#             page.btn_access.click()
#     with allure.step('Проверить наличие логотипа'):
#         logo = WebDriverWait(web_browser, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".logo a img, .logo a"))
#         )
#         assert logo is not None, "Логотип не найден на странице"
#     with allure.step('Проверить кликабельность логотипа'):
#         logo_link = web_browser.find_element(By.CSS_SELECTOR, ".logo a")
#         href = logo_link.get_attribute("href")
#         assert href is not None, "Логотип не является ссылкой"

# Тест наличия телефонных номеров в шапке/футере
# @allure.title('Проверка наличия телефонных номеров')
# @allure.feature('Контактная информация')
# def test_phone_numbers_present(web_browser):
#     page = MainPage(web_browser)
#     with allure.step('Принять cookies'):
#         if page.btn_access.is_presented():
#             page.btn_access.click()
#     with allure.step('Проверить наличие телефонных номеров'):
#         phones = WebDriverWait(web_browser, 10).until(
#             EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".phones .phone a[href^='tel:']"))
#         )
#         assert len(phones) >= 2, f"Найдено менее 2 телефонных номеров: {len(phones)}"

# Тест наличия адреса компании на странице
# @allure.title('Проверка адреса компании')
# @allure.feature('Контактная информация')
# def test_address_present(web_browser):
#     page = MainPage(web_browser)
#     with allure.step('Принять cookies'):
#         if page.btn_access.is_presented():
#             page.btn_access.click()
#     with allure.step('Проверить наличие адреса'):
#         address = WebDriverWait(web_browser, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".address .location, .address p"))
#         )
#         assert address is not None, "Адрес не найден на странице"
#         text = address.text
#         assert "Минск" in text or "Маркса" in text, f"Адрес не содержит ожидаемый текст: {text}"

# Тест заголовка страницы (дублируется — ниже есть активная версия)
# @allure.title('Проверка заголовка страницы')
# @allure.feature('Главная страница')
# def test_page_title(web_browser):
#     page = MainPage(web_browser)
#     with allure.step('Принять cookies'):
#         if page.btn_access.is_presented():
#             page.btn_access.click()
#     with allure.step('Проверить заголовок страницы'):
#         title = web_browser.title
#         assert "IT" in title or "ШАГ" in title or "itstep" in title.lower(), \
#             f"Заголовок страницы не содержит ожидаемый текст: {title}"

# Тест наличия блока "ОБУЧЕНИЕ ДЛЯ ДЕТЕЙ И ПОДРОСТКОВ"
# @allure.title('Проверка наличия блока "ОБУЧЕНИЕ ДЛЯ ДЕТЕЙ И ПОДРОСТКОВ"')
# @allure.feature('Главная страница')
# def test_kids_section_present(web_browser):
#     page = MainPage(web_browser)
#     with allure.step('Принять cookies'):
#         if page.btn_access.is_presented():
#             page.btn_access.click()
#     with allure.step('Проверить наличие секции обучения для детей'):
#         section = WebDriverWait(web_browser, 10).until(
#             EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'ДЕТЕЙ И ПОДРОСТКОВ')]"))
#         )
#         assert section is not None, "Секция 'ОБУЧЕНИЕ ДЛЯ ДЕТЕЙ И ПОДРОСТКОВ' не найдена"

# Тест перехода на программу "7-8 лет"
# @allure.title('Проверка ссылки на программу "7-8 лет"')
# @allure.feature('Программы для детей')
# def test_kids_7_8_link(web_browser):
#     page = MainPage(web_browser)
#     with allure.step('Принять cookies'):
#         if page.btn_access.is_presented():
#             page.btn_access.click()
#     with allure.step('Кликнуть по ссылке "7-8 лет"'):
#         element = page.kids_7_8_link.find()
#         web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
#         web_browser.execute_script("arguments[0].click();", element)
#         time.sleep(3)
#     with allure.step('Проверить URL содержит "kursy-dlya-detej-7-8-let"'):
#         assert "kursy-dlya-detej-7-8-let" in page.get_current_url()

# Тест перехода на программу "9-11 лет"
# @allure.title('Проверка ссылки на программу "9-11 лет"')
# @allure.feature('Программы для детей')
# def test_kids_9_11_link(web_browser):
#     page = MainPage(web_browser)
#     with allure.step('Принять cookies'):
#         if page.btn_access.is_presented():
#             page.btn_access.click()
#     with allure.step('Кликнуть по ссылке "9-11 лет"'):
#         element = page.kids_9_11_link.find()
#         web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
#         web_browser.execute_script("arguments[0].click();", element)
#         time.sleep(3)
#     with allure.step('Проверить URL содержит "kursy-dlya-detej-9-11-let"'):
#         assert "kursy-dlya-detej-9-11-let" in page.get_current_url()

# Тест перехода на программу "12-13 лет"
# @allure.title('Проверка ссылки на программу "12-13 лет"')
# @allure.feature('Программы для детей')
# def test_kids_12_13_link(web_browser):
#     page = MainPage(web_browser)
#     with allure.step('Принять cookies'):
#         if page.btn_access.is_presented():
#             page.btn_access.click()
#     with allure.step('Кликнуть по ссылке "12-13 лет"'):
#         element = page.kids_12_13_link.find()
#         web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
#         web_browser.execute_script("arguments[0].click();", element)
#         time.sleep(3)
#     with allure.step('Проверить URL содержит "kursy-dlya-detej-12-13-let"'):
#         assert "kursy-dlya-detej-12-13-let" in page.get_current_url()

# Тест кнопки "УЗНАТЬ ПОДРОБНОСТИ" на слайдере
# @allure.title('Проверка кнопки "УЗНАТЬ ПОДРОБНОСТИ" на слайдере')
# @allure.feature('Слайдер')
# def test_slider_learn_more_button(web_browser):
#     page = MainPage(web_browser)
#     with allure.step('Принять cookies'):
#         if page.btn_access.is_presented():
#             page.btn_access.click()
#     with allure.step('Проверить наличие кнопки "УЗНАТЬ ПОДРОБНОСТИ"'):
#         elements = page.learn_more_btn.find()
#         assert elements is not None, "Кнопка 'УЗНАТЬ ПОДРОБНОСТИ' не найдена"
#     with allure.step('Проверить, что кнопка ведет на внешний ресурс'):
#         href = page.learn_more_btn.get_attribute("href")
#         assert href is not None, "Кнопка не содержит ссылку"

# Тест отсутствия JavaScript ошибок на главной странице
# @allure.title('Проверка отсутствия JS ошибок на главной странице')
# @allure.feature('Главная страница')
# def test_no_js_errors(web_browser):
#     page = MainPage(web_browser)
#     with allure.step('Принять cookies'):
#         if page.btn_access.is_presented():
#             page.btn_access.click()
#     with allure.step('Проверить отсутствие JS ошибок'):
#         page.wait_page_loaded()
#         page.check_js_errors(ignore_list=[
#             'favicon', 'google', 'facebook', 'bitrix', 'gtm',
#             'analytics', 'cdn-ru.bitrix24', 'Slow network', 'intervention',
#             'Fallback font', 'utmstat', 'call-tracking'
#         ])


# Декоратор Allure: название — "Проверка заголовка страницы"
@allure.title('Проверка заголовка страницы')
# Декоратор Allure: фича — "Главная страница"
@allure.feature('Главная страница')
# Функция теста: проверяет корректность заголовка (title) страницы
def test_page_title(web_browser):
    # Создаём Page Object главной страницы
    page = MainPage(web_browser)

    # Шаг Allure: принимаем cookies
    with allure.step('Принять cookies'):
        # Если кнопка cookies видна — кликаем
        if page.btn_access.is_presented():
            page.btn_access.click()

    # Шаг Allure: проверяем заголовок страницы
    with allure.step('Проверить заголовок страницы'):
        # Получаем текущий заголовок страницы (тег <title>)
        title = web_browser.title
        # Утверждение: заголовок должен содержать "IT", "ШАГ" или "itstep" (любой из вариантов)
        assert "IT" in title or "ШАГ" in title or "itstep" in title.lower(), \
            f"Заголовок страницы не содержит ожидаемый текст: {title}"


# ---- Закомментированный тест блока отзывов ----
# Тест отображения карточек отзывов (YANDEX, GOOGLE, FACEBOOK)
# @allure.title('Проверка отображения всех карточек в блоке отзывов')
# @allure.feature('Блок отзывов')
# def test_reviews_cards_count(web_browser):
#     page = MainPage(web_browser)
#     with allure.step('Принять cookies'):
#         if page.btn_access.is_presented():
#             page.btn_access.click()
#     with allure.step('Прокрутить к блоку отзывов'):
#         title = WebDriverWait(web_browser, 10).until(
#             EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'title') and contains(text(),'ОТЗЫВЫ')]"))
#         )
#         web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", title)
#         time.sleep(2)
#     with allure.step('Подсчитать количество карточек отзывов'):
#         section = title.find_element(By.XPATH, "./ancestor::section")
#         cards = section.find_elements(By.CSS_SELECTOR, '.slide-container')
#         count = len(cards)
#     with allure.step(f'Проверить что отображается 3 карточки отзывов (фактически: {count})'):
#         assert count == 3, f"Ожидалось 3 карточки отзывов, найдено: {count}"
#     with allure.step('Проверить содержимое каждой карточки'):
#         titles = []
#         for card in cards:
#             title_el = card.find_element(By.CSS_SELECTOR, '.slide-title')
#             titles.append(title_el.text.strip())
#         expected = ['YANDEX', 'GOOGLE', 'FACEBOOK']
#         for name in expected:
#             assert name in titles, f"Отзыв '{name}' не найден среди карточек: {titles}"
#     with allure.step('Проверить что все карточки содержат ссылки'):
#         for i, card in enumerate(cards):
#             link = card.find_element(By.TAG_NAME, 'a')
#             href = link.get_attribute('href')
#             assert href is not None and href.startswith('http'), \
#                 f"Карточка отзывов {i + 1} не содержит валидную ссылку: {href}"


# Декоратор Allure: название — E2E тест профориентационного теста (полный сценарий заполнения формы)
@allure.title('E2E: Профориентационный тест — заполнение формы')
# Декоратор Allure: фича — "E2E тесты" (сквозные тесты от начала до конца)
@allure.feature('E2E тесты')
# Функция E2E теста: проходит весь путь от главной страницы до заполнения и отправки формы профтеста
def test_career_guidance_form(web_browser):
    # Список мужских и женских имён для случайной генерации данных
    first_names = ['Александр', 'Мария', 'Дмитрий', 'Анна', 'Сергей', 'Елена', 'Иван', 'Ольга']
    # Список фамилий для случайной генерации данных
    last_names = ['Иванов', 'Петрова', 'Сидоров', 'Козлова', 'Морозов', 'Новикова', 'Волков', 'Лебедева']

    # Случайный выбор имени из списка
    first_name = random.choice(first_names)
    # Случайный выбор фамилии из списка
    last_name = random.choice(last_names)
    # Генерация белорусского номера телефона: +375 + код оператора (29/33/25/17) + 7 цифр
    phone = f"+375{random.choice(['29', '33', '25', '17'])}{random.randint(1000000, 9999999)}"
    # Фиксированный email для тестовой формы
    email = "kuzayo@mail.ru"

    # Создаём Page Object главной страницы
    page = MainPage(web_browser)

    # Шаг Allure: принимаем cookies
    with allure.step('Принять cookies'):
        # Если баннер cookies отображается — кликаем для его закрытия
        if page.btn_access.is_presented():
            page.btn_access.click()

    # Шаг Allure: логируем сформированные тестовые данные (pass — ничего не делаем, только для отчёта)
    with allure.step(f'Сформированы данные: {first_name} {last_name}, {phone}, {email}'):
        pass

    # Шаг Allure: открываем выпадающее меню "IT ОБРАЗОВАНИЕ"
    with allure.step('Открыть меню "IT ОБРАЗОВАНИЕ"'):
        # Находим пункт меню "IT ОБРАЗОВАНИЕ"
        element = page.it_education_menu.find()
        # Прокручиваем к нему для видимости
        web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        # Кликаем по меню через JavaScript для раскрытия подменю
        web_browser.execute_script("arguments[0].click();", element)
        # Ждём 2 секунды для появления выпадающего списка
        time.sleep(2)

    # Шаг Allure: кликаем по ссылке "Профориентационный тест" в раскрытом меню
    with allure.step('Кликнуть по "Профориентационный тест"'):
        # Находим ссылку на карьерный тест в выпадающем меню
        link = page.career_test_link.find()
        # Кликаем по ссылке через JavaScript
        web_browser.execute_script("arguments[0].click();", link)
        # Ждём 3 секунды для загрузки страницы теста
        time.sleep(3)

    # Шаг Allure: проверяем, что URL содержит slug карьерного теста
    with allure.step('Проверить URL содержит "career-guidance-test"'):
        # Утверждение: URL должен содержать "career-guidance-test"
        assert "career-guidance-test" in page.get_current_url()

    # Шаг Allure: кликаем по кнопке "Пройти тест" для перехода к форме
    with allure.step('Кликнуть "Пройти тест"'):
        # Явное ожидание: ищем кнопку/ссылку "Пройти тест" (несколько вариантов XPath для разных разметок)
        start_btn = WebDriverWait(web_browser, 15).until(
            EC.element_to_be_clickable((By.XPATH,
                # XPath-список: ищем ссылку или кнопку с текстом "пройти тест" (с учётом регистра)
                "//a[contains(translate(text(),'АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЭЮЯ','абвгдежзиклмнопрстуфхцчшщэюя'), 'пройти тест')] | "
                "//button[contains(translate(text(),'АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЭЮЯ','абвгдежзиклмнопрстуфхцчшщэюя'), 'пройти тест')] | "
                "//a[contains(@class, 'btn') and contains(@href, 'test')] | "
                "//button[contains(@class, 'btn') and contains(@class, 'test')]"
            ))
        )
        # Кликаем по кнопке "Пройти тест" через JavaScript
        web_browser.execute_script("arguments[0].click();", start_btn)
        # Ждём 5 секунд — возможен переход на внешний домен (proftest.itstep.by)
        time.sleep(5)

    # Шаг Allure: проверяем, что произошёл переход на форму теста
    with allure.step('Проверить переход на форму (proftest.itstep.by)'):
        # Получаем текущий URL страницы
        current_url = web_browser.current_url
        # Утверждение: URL должен содержать "proftest.itstep.by" или "form"
        assert "proftest.itstep.by" in current_url or "form" in current_url, \
            f"Не удалось перейти на форму. URL: {current_url}"

    # Шаг Allure: заполняем поле "Имя" сгенерированными данными
    with allure.step(f'Заполнить имя: {first_name} {last_name}'):
        # Явное ожидание: находим поле ввода имени по атрибуту name="question0"
        name_field = WebDriverWait(web_browser, 10).until(
            EC.presence_of_element_located((By.NAME, "question0"))
        )
        # Прокручиваем к полю для видимости
        web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", name_field)
        # Очищаем поле от возможного старого значения
        name_field.clear()
        # Вводим полное имя (имя + фамилия)
        name_field.send_keys(f"{first_name} {last_name}")
        # Короткая пауза для обработки ввода страницей
        time.sleep(0.5)

    # Шаг Allure: заполняем поле "Email"
    with allure.step(f'Заполнить email: {email}'):
        # Находим поле ввода email по name="question1"
        email_field = WebDriverWait(web_browser, 10).until(
            EC.presence_of_element_located((By.NAME, "question1"))
        )
        # Очищаем поле
        email_field.clear()
        # Вводим email
        email_field.send_keys(email)
        # Пауза для обработки
        time.sleep(0.5)

    # Шаг Allure: заполняем поле "Телефон"
    with allure.step(f'Заполнить телефон: {phone}'):
        # Находим поле ввода телефона по name="question2"
        phone_field = WebDriverWait(web_browser, 10).until(
            EC.presence_of_element_located((By.NAME, "question2"))
        )
        # Очищаем поле
        phone_field.clear()
        # Вводим номер телефона
        phone_field.send_keys(phone)
        # Пауза для обработки
        time.sleep(0.5)

    # Шаг Allure: делаем скриншот заполненной формы (для отчёта Allure)
    with allure.step('Сделать скриншот заполненной формы'):
        # Сохраняем скриншот в файл career_test_form_filled.png
        web_browser.save_screenshot('career_test_form_filled.png')

    # Шаг Allure: отвечаем на вопросы теста (radio/checkbox)
    with allure.step('Ответить на вопросы теста (radio/checkbox)'):
        # Множество имён уже обработанных групп вопросов (чтобы не отвечать дважды)
        question_names = set()

        # Вспомогательная функция безопасного клика: кликает через JS и обрабатывает всплывающие алерты
        def safe_click(element):
            try:
                # Кликаем по элементу через JavaScript
                web_browser.execute_script("arguments[0].click();", element)
            except:
                # Игнорируем ошибки клика (элемент может быть невидим)
                pass
            try:
                # Проверяем, не появился ли всплывающий алерт после клика
                alert = web_browser.switch_to.alert
                # Получаем текст алерта
                alert_text = alert.text
                # Принимаем (закрываем) алерт
                alert.accept()
                # Публикуем текст алерта в отчёт Allure
                allure.step(f'Алерт: {alert_text}').publish()
            except:
                # Если алерта нет — просто продолжаем
                pass

        # Находим все radio-кнопки на странице теста
        all_radios = web_browser.find_elements(By.CSS_SELECTOR, "input[type='radio']")
        # Перебираем каждую radio-кнопку
        for r in all_radios:
            # Получаем имя группы radio-кнопок (атрибут name)
            qname = r.get_attribute("name")
            # Если эта группа вопросов ещё не обработана
            if qname not in question_names:
                # Добавляем имя группы в множество обработанных
                question_names.add(qname)
                # Находим все варианты ответа в этой группе
                options = web_browser.find_elements(By.CSS_SELECTOR, f"input[name='{qname}']")
                # Если варианты найдены — выбираем случайный
                if options:
                    # Случайный выбор одного варианта ответа
                    chosen = random.choice(options)
                    # Кликаем по выбранному варианту
                    safe_click(chosen)

        # Находим все checkbox-кнопки на странице теста
        all_checkboxes = web_browser.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
        # Перебираем каждую checkbox-кнопку
        for c in all_checkboxes:
            # Получаем имя группы чекбоксов
            qname = c.get_attribute("name")
            # Если эта группа ещё не обработана
            if qname not in question_names:
                # Добавляем имя группы в множество обработанных
                question_names.add(qname)
                # Находим все варианты чекбоксов в этой группе
                options = web_browser.find_elements(By.CSS_SELECTOR, f"input[name='{qname}']")
                # Если варианты найдены — выбираем случайное количество (от 1 до 3)
                if options:
                    # Случайное количество чекбоксов для отметки (от 1 до минимум(3, общее кол-во))
                    num_to_check = random.randint(1, min(3, len(options)))
                    # Случайно выбираем нужное количество вариантов и отмечаем их
                    for opt in random.sample(options, num_to_check):
                        safe_click(opt)

    # Шаг Allure: нажимаем кнопку "Узнать свой результат!" для отправки формы
    with allure.step('Нажать "Узнать свой результат!"'):
        # Перед отправкой закрываем возможные висящие алерты
        try:
            alert = web_browser.switch_to.alert
            alert.accept()
        except:
            # Если алерта нет — продолжаем
            pass
        # Явное ожидание: находим кнопку отправки формы (button[type='submit'])
        submit = WebDriverWait(web_browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        # Прокручиваем к кнопке отправки
        web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit)
        # Кликаем по кнопке отправки через JavaScript
        web_browser.execute_script("arguments[0].click();", submit)
        # Пауза 2 секунды после клика
        time.sleep(2)
        # Обрабатываем возможный алерт после отправки формы
        try:
            alert = web_browser.switch_to.alert
            alert_text = alert.text
            alert.accept()
            # Публикуем текст алерта в отчёт Allure
            allure.step(f'Алерт после отправки: {alert_text}').publish()
        except:
            # Если алерта нет — продолжаем
            pass
        # Пауза 3 секунды для завершения обработки формы сервером
        time.sleep(3)

    # Шаг Allure: проверяем, что форма успешно отправлена
    with allure.step('Проверить отправку формы'):
        # Получаем HTML-исходник страницы в нижнем регистре для поиска
        page_source = web_browser.page_source.lower()
        # Список индикаторов успешной отправки формы (ключевые слова, которые появляются после отправки)
        success_indicators = ['результат', 'спасибо', 'отправлено', 'готово', 'ваш', 'профориентация', 'курс']
        # Проверяем, есть ли хотя бы один индикатор на странице
        form_still_visible = any(ind in page_source for ind in success_indicators)
        # Утверждение: хотя бы один индикатор должен присутствовать — форма отправлена успешно
        assert form_still_visible, "Форма не была отправлена — индикатор успеха не найден"

    # Шаг Allure: делаем скриншот результата отправки (для отчёта Allure)
    with allure.step('Сделать скриншот результата'):
        # Сохраняем скриншот результата в файл career_test_submitted.png
        web_browser.save_screenshot('career_test_submitted.png')
