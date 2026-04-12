from locators.locators_main import MainPage
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_go_to_vacancies(web_browser):
    page = MainPage(web_browser)

    # ✅ принять cookies
    if page.btn_access.is_presented():
        page.btn_access.click()



    # ✅ клик по вакансии
    element = page.vacancies_link.find()
    web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    WebDriverWait(web_browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='https://itstep.by/careers/']")))
    web_browser.execute_script("arguments[0].click();", element)

    time.sleep(3)

    # ✅ проверка
    assert "careers" in page.get_current_url()





def test_feedback_form(web_browser):
    page = MainPage(web_browser)

    if page.btn_access.is_presented():
        page.btn_access.click()

    # открыть чат
    page.wait_page_loaded()
    import time
    time.sleep(5)
    element = page.chat_button.find()
    web_browser.execute_script("arguments[0].click();", element)

    # нажать "Обратная связь"
    chat = WebDriverWait(web_browser, 15).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'b24-widget-button')]"))
    )
    web_browser.execute_script("arguments[0].click();", chat)

    feedback = WebDriverWait(web_browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Обратная связь')]"))
    )
    web_browser.execute_script("arguments[0].click();", feedback)

    # заполнить форму
    time.sleep(2)
    page.name_input.send_keys("Test User")
    page.phone_input.send_keys("+375291234567")
    page.email_input.send_keys("test@test.com")
    page.message_input.send_keys("Автотест")

    # проверки
    assert page.name_input.get_attribute("value") == "Test User"
    assert page.email_input.get_attribute("value") == "test@test.com"


# import allure
#
#
# from locators.locators_main import MainPage
#
#
#
# def test_go_to_qa_course(web_driver):
#     page = MainPage(web_driver)
#
#     # Кликаем по "IT ОБРАЗОВАНИЕ"
#     page.it_education_menu.click()
#
#     # Кликаем по "Тестирование ПО (QA)"
#     page.qa_course_link.click()
#
#     # Проверка
#     current_url = page.get_current_url()
#     assert "testirovanie-po-qa" in current_url
#


# def test_main_chat(web_browser):#фикстура
#     page = Main(web_browser)
#     # page.btn_access.click(3)
#     # page.btn_main.click(3)
#     # page.btn_chat.click(3)
#
#
# data = [
#     (page.btn_games, 'Кнопка игры')
#     (page.btn_news, 'Кнопка новости')
#     (page.btn_faq, 'Кнопка faq')
#
#     ]
#
# for btn, text in data:
#     with allure, text in data:
#         with allure.step(f'Проверка кликабельности {text}')
#             assert btn.is_clickable(), f'некликабельная {text}'
#

