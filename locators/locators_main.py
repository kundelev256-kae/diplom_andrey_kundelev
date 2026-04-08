from page.base_page import WebPage
import os

from page.elements import WebElement

class Main(WebPage):

    def __init__(self, web_driver, url=''):
        if not url:
            url = os.genetv("MAIN") or 'https://itstep.by//'

        super().__init__(web_driver, url)

        btn_access = WebElement(id="button-accept-cookies")
        # btn_main = WebElement(id="uw-main-button")
        # btn_chat = WebElement(id="uw-button-chat")
        # btn_message = WebElement(name="message")
        # btn_message_submit = WebElement(id="uw-message-submit-button")