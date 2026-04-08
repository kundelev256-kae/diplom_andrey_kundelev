import allure
from selenium.webdriver.common.devtools.v143 import page

from locators.locators_main import Main
from conftest import web_browser




def test_main_chat(web_browser):#фикстура
    page = Main(web_browser)
    # page.btn_access.click(3)
    # page.btn_main.click(3)
    # page.btn_chat.click(3)


data = [
    (page.btn_games, 'Кнопка игры')
    (page.btn_news, 'Кнопка новости')
    (page.btn_faq, 'Кнопка faq')

    ]

for btn, text in data:
    with allure, text in data:
        with allure.step(f'Проверка кликабельности {text}')
            assert btn.is_clickable(), f'некликабельная {text}'


