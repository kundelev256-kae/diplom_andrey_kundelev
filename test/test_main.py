import allure
import time

from locators.locators_main import MainPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.title('Проверка кнопки "Вакансии"')
@allure.feature('Навигация')
def test_go_to_vacancies(web_browser):
    page = MainPage(web_browser)

    with allure.step('Принять cookies'):
        if page.btn_access.is_presented():
            page.btn_access.click()

    with allure.step('Перейти по ссылке "Вакансии"'):
        element = page.vacancies_link.find()
        web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        WebDriverWait(web_browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'careers')]")))
        web_browser.execute_script("arguments[0].click();", element)
        time.sleep(3)

    with allure.step('Проверить URL содержит "careers"'):
        assert "careers" in page.get_current_url()


@allure.title('Проверка кнопки "Контакты"')
@allure.feature('Навигация')
def test_go_to_contacts(web_browser):
    page = MainPage(web_browser)

    with allure.step('Принять cookies'):
        if page.btn_access.is_presented():
            page.btn_access.click()

    with allure.step('Перейти по ссылке "Контакты"'):
        element = page.contacts_link.find()
        web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        web_browser.execute_script("arguments[0].click();", element)
        time.sleep(3)

    with allure.step('Проверить URL содержит "kontakty"'):
        assert "kontakty" in page.get_current_url()


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


@allure.title('Проверка перехода на курс "Тестирование ПО (QA)"')
@allure.feature('Меню IT ОБРАЗОВАНИЕ')
def test_go_to_qa_course(web_browser):
    page = MainPage(web_browser)

    with allure.step('Принять cookies'):
        if page.btn_access.is_presented():
            page.btn_access.click()

    with allure.step('Открыть меню "IT ОБРАЗОВАНИЕ"'):
        element = page.it_education_menu.find()
        web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        web_browser.execute_script("arguments[0].click();", element)
        time.sleep(2)

    with allure.step('Кликнуть по курсу "Тестирование ПО (QA)"'):
        qa = page.qa_course_link.find()
        web_browser.execute_script("arguments[0].click();", qa)
        time.sleep(3)

    with allure.step('Проверить URL содержит "testirovanie-po-qa"'):
        assert "testirovanie-po-qa" in page.get_current_url()


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


@allure.title('Проверка кнопки "Обратная связь" (чат)')
@allure.feature('Форма обратной связи')
def test_feedback_form(web_browser):
    page = MainPage(web_browser)

    with allure.step('Принять cookies'):
        if page.btn_access.is_presented():
            page.btn_access.click()

    with allure.step('Проверить наличие виджета чата в DOM'):
        page.wait_page_loaded()
        time.sleep(8)
        chat = page.chat_button.find()
        assert chat is not None, "Виджет чата не найден в DOM"

    with allure.step('Кликнуть по виджету чата через JS'):
        web_browser.execute_script("arguments[0].click();", chat)
        time.sleep(8)

    with allure.step('Проверить появление элементов чата'):
        chat_panel = WebDriverWait(web_browser, 15).until(
            EC.presence_of_element_located((By.XPATH,
                "//*[contains(@class,'b24-widget')] | "
                "//*[contains(@class,'bitrix24')]"
            ))
        )
        assert chat_panel is not None, "Панель чата не появилась после клика"


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


@allure.title('Проверка заголовка страницы')
@allure.feature('Главная страница')
def test_page_title(web_browser):
    page = MainPage(web_browser)

    with allure.step('Принять cookies'):
        if page.btn_access.is_presented():
            page.btn_access.click()

    with allure.step('Проверить заголовок страницы'):
        title = web_browser.title
        assert "IT" in title or "ШАГ" in title or "itstep" in title.lower(), \
            f"Заголовок страницы не содержит ожидаемый текст: {title}"


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
