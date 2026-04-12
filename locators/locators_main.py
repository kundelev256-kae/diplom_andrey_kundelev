from page.base_page import WebPage
import os
from page.elements import WebElement
from selenium.webdriver.common.by import By


class MainPage(WebPage):

    def __init__(self, web_driver, url=''):
        if not url:
            url = os.getenv("MAIN") or 'https://itstep.by/'

        super().__init__(web_driver, url)

    btn_access = WebElement(id="button-accept-cookies")

    # Кнопка "IT ОБРАЗОВАНИЕ"
    vacancies_link = WebElement(xpath="//a[contains(@href, 'careers')]")

    # для теста с чатом и заполнением формы
    chat_button = WebElement(xpath="//*[contains(@class,'b24-widget-button')]")

    feedback_button = WebElement(xpath="//a[contains(@class,'b24-widget-button-crmform')]")

    name_input = WebElement(xpath="//input[@name='NAME']")
    phone_input = WebElement(xpath="//input[@name='PHONE']")
    email_input = WebElement(xpath="//input[@name='EMAIL']")
    message_input = WebElement(xpath="//textarea")


        # btn_access = WebElement(id="button-accept-cookies")
        # btn_main = WebElement(id="uw-main-button")
        # btn_chat = WebElement(id="uw-button-chat")
        # btn_message = WebElement(name="message")
        # btn_message_submit = WebElement(id="uw-message-submit-button")