from page.base_page import WebPage
import os
from page.elements import WebElement
from selenium.webdriver.common.by import By


class MainPage(WebPage):

    def __init__(self, web_driver, url=''):
        if not url:
            url = os.getenv("MAIN") or 'https://itstep.by/'

        super().__init__(web_driver, url)

    # Cookies
    btn_access = WebElement(id="button-accept-cookies")

    # Навигация — десктопное меню (menu-panel)
    vacancies_link = WebElement(xpath="//a[contains(@href, 'careers')]")
    contacts_link = WebElement(xpath="//a[@href='https://itstep.by/kontakty/']")
    news_link = WebElement(xpath="//div[contains(@class,'menu-panel')]//a[@href='https://itstep.by/news/']")
    articles_link = WebElement(xpath="//a[@href='https://itstep.by/stati-i-publikaczii/']")
    english_link = WebElement(xpath="//div[contains(@class,'menu-panel')]//a[@href='https://2english.itstep.by/']")

    # Меню "IT ОБРАЗОВАНИЕ" — десктопное
    it_education_menu = WebElement(xpath="//div[contains(@class,'menu-panel')]//div[@class='menu']//a[contains(text(), 'IT ОБРАЗОВАНИЕ')]")

    # Курсы в выпадающем меню "IT ОБРАЗОВАНИЕ"
    qa_course_link = WebElement(xpath="//a[contains(@href, 'testirovanie-po-qa')]")
    python_course_link = WebElement(xpath="//a[contains(@href, 'razrabotka-po-na-python')]")
    java_course_link = WebElement(xpath="//a[contains(@href, 'razrabotka-po-na-java')]")
    ux_ui_course_link = WebElement(xpath="//a[contains(@href, 'ux-ui-dizajn')]")
    motion_design_link = WebElement(xpath="//a[contains(@href, 'motion-design')]")
    data_analyst_link = WebElement(xpath="//a[contains(@href, 'analitik-dannyh-v-it-data-analyst')]")
    pm_course_link = WebElement(xpath="//a[contains(@href, 'upravlenie-proektami-v-it-pm')]")
    devops_link = WebElement(xpath="//a[contains(@href, 'devops-engineer')]")
    it_start_link = WebElement(xpath="//a[contains(@href, 'it-start/')]")
    career_test_link = WebElement(xpath="//a[contains(@href, 'career-guidance-test')]")

    # Кнопка "УЗНАТЬ ПОДРОБНОСТИ" на слайдерах
    learn_more_btn = WebElement(xpath="//a[contains(@class, 'btn-info') and contains(@class, 'btn-styled')]")

    # Чат и форма обратной связи
    chat_button = WebElement(xpath="//*[contains(@class,'b24-widget-button')]")
    feedback_button = WebElement(xpath="//a[contains(@class,'b24-widget-button-crmform')]")
    name_input = WebElement(xpath="//input[@name='NAME']")
    phone_input = WebElement(xpath="//input[@name='PHONE']")
    email_input = WebElement(xpath="//input[@name='EMAIL']")
    message_input = WebElement(xpath="//textarea")

    # Программы для детей
    kids_7_8_link = WebElement(xpath="//a[contains(@href, 'kursy-dlya-detej-7-8-let')]")
    kids_9_11_link = WebElement(xpath="//a[contains(@href, 'kursy-dlya-detej-9-11-let')]")
    kids_12_13_link = WebElement(xpath="//a[contains(@href, 'kursy-dlya-detej-12-13-let')]")
    it_college_link = WebElement(xpath="//a[contains(@href, 'it-college.itstep.by')]")