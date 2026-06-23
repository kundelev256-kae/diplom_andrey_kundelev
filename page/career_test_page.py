import os
from page.base_page import WebPage
from page.elements import WebElement


class CareerTestPage(WebPage):

    def __init__(self, web_driver, url=''):
        if not url:
            url = os.getenv("MAIN") or 'https://itstep.by/career-guidance-test/'
        super().__init__(web_driver, url)

    # Кнопка "Пройти тест"
    start_test_btn = WebElement(xpath="//a[contains(@class,'btn') and contains(text(),'пройти тест')]")

    # Поля формы (после нажатия "Пройти тест" появляется форма)
    first_name_input = WebElement(xpath="//input[@name='first_name' or @name='name' or @placeholder='* Ваше имя']")
    last_name_input = WebElement(xpath="//input[@name='last_name' or @name='surname' or @placeholder='* Ваша фамилия']")
    email_input = WebElement(xpath="//input[@name='email' or @type='email' or @placeholder='* Ваш e-mail']")
    phone_input = WebElement(xpath="//input[@name='phone' or @type='tel' or @placeholder='* Телефон']")
    submit_btn = WebElement(xpath="//button[@type='submit' or contains(text(),'Отправить') or contains(text(),'Готово')]")
