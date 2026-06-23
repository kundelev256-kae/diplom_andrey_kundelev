# Импорт базового класса WebPage из модуля base_page — родительский класс для всех страниц
from page.base_page import WebPage
# Импорт модуля os для работы с переменными окружения (получение URL из env)
import os
# Импорт класса WebElement — кастомный элемент страницы для работы с локаторами
from page.elements import WebElement
# Импорт By из Selenium — используется для определения стратегии поиска элементов
from selenium.webdriver.common.by import By


# Класс MainPage — локаторы и элементы главной страницы сайта itstep.by
class MainPage(WebPage):

    # Конструктор MainPage: принимает веб-драйвер и необязательный URL
    def __init__(self, web_driver, url=''):
        # Если URL не передан, берём его из переменной окружения MAIN или используем значение по умолчанию
        if not url:
            url = os.getenv("MAIN") or 'https://itstep.by/'

        # Вызов конструктора родительского класса WebPage с драйвером и URL
        super().__init__(web_driver, url)

    # Кнопка принятия куки (cookies-уведомление) — ищется по ID кнопки
    btn_access = WebElement(id="button-accept-cookies")

    # === Навигация — десктопное меню (menu-panel) ===

    # Ссылка на страницу вакансий (раздел "Карьера") — ищется по атрибуту href
    vacancies_link = WebElement(xpath="//a[contains(@href, 'careers')]")
    # Ссылка на страницу контактов — прямой URL
    contacts_link = WebElement(xpath="//a[@href='https://itstep.by/kontakty/']")
    # Ссылка на новостную страницу — вложена внутри div с классом menu-panel
    news_link = WebElement(xpath="//div[contains(@class,'menu-panel')]//a[@href='https://itstep.by/news/']")
    # Ссылка на раздел статей и публикаций
    articles_link = WebElement(xpath="//a[@href='https://itstep.by/stati-i-publikaczii/']")
    # Ссылка на раздел изучения английского языка — вложенная в меню
    english_link = WebElement(xpath="//div[contains(@class,'menu-panel')]//a[@href='https://2english.itstep.by/']")

    # === Меню "IT ОБРАЗОВАНИЕ" — десктопное ===

    # Заголовок/ссылка меню "IT ОБРАЗОВАНИЕ" — вложенная в панель меню, ищется по тексту
    it_education_menu = WebElement(xpath="//div[contains(@class,'menu-panel')]//div[@class='menu']//a[contains(text(), 'IT ОБРАЗОВАНИЕ')]")

    # === Курсы в выпадающем меню "IT ОБРАЗОВАНИЕ" ===

    # Ссылка на курс тестирования QA — ищется по части URL в href
    qa_course_link = WebElement(xpath="//a[contains(@href, 'testirovanie-po-qa')]")
    # Ссылка на курс разработки на Python
    python_course_link = WebElement(xpath="//a[contains(@href, 'razrabotka-po-na-python')]")
    # Ссылка на курс разработки на Java
    java_course_link = WebElement(xpath="//a[contains(@href, 'razrabotka-po-na-java')]")
    # Ссылка на курс UX/UI дизайна
    ux_ui_course_link = WebElement(xpath="//a[contains(@href, 'ux-ui-dizajn')]")
    # Ссылка на курс Motion Design
    motion_design_link = WebElement(xpath="//a[contains(@href, 'motion-design')]")
    # Ссылка на курс анализа данных (Data Analyst)
    data_analyst_link = WebElement(xpath="//a[contains(@href, 'analitik-dannyh-v-it-data-analyst')]")
    # Ссылка на курс управления проектами (PM)
    pm_course_link = WebElement(xpath="//a[contains(@href, 'upravlenie-proektami-v-it-pm')]")
    # Ссылка на курс DevOps Engineer
    devops_link = WebElement(xpath="//a[contains(@href, 'devops-engineer')]")
    # Ссылка на курс IT Start (введение в IT)
    it_start_link = WebElement(xpath="//a[contains(@href, 'it-start/')]")
    # Ссылка на тест по профориентации (career guidance test)
    career_test_link = WebElement(xpath="//a[contains(@href, 'career-guidance-test')]")

    # Кнопка "УЗНАТЬ ПОДРОБНОСТИ" на слайдерах — ищется по комбинации CSS-классов btn-info и btn-styled
    learn_more_btn = WebElement(xpath="//a[contains(@class, 'btn-info') and contains(@class, 'btn-styled')]")

    # === Чат и форма обратной связи ===

    # Кнопка всплывающего виджета чата (Bitrix24) — ищется по классу виджета
    chat_button = WebElement(xpath="//*[contains(@class,'b24-widget-button')]")
    # Кнопка формы обратной связи CRM (Bitrix24) — отдельная кнопка от основного чата
    feedback_button = WebElement(xpath="//a[contains(@class,'b24-widget-button-crmform')]")
    # Поле ввода имени в форме обратной связи — атрибут name='NAME'
    name_input = WebElement(xpath="//input[@name='NAME']")
    # Поле ввода телефона в форме обратной связи — атрибут name='PHONE'
    phone_input = WebElement(xpath="//input[@name='PHONE']")
    # Поле ввода email в форме обратной связи — атрибут name='EMAIL'
    email_input = WebElement(xpath="//input[@name='EMAIL']")
    # Поле ввода сообщения (textarea) — общее для всех форм
    message_input = WebElement(xpath="//textarea")

    # === Программы для детей ===

    # Ссылка на курс для детей 7-8 лет — ищется по части URL
    kids_7_8_link = WebElement(xpath="//a[contains(@href, 'kursy-dlya-detej-7-8-let')]")
    # Ссылка на курс для детей 9-11 лет
    kids_9_11_link = WebElement(xpath="//a[contains(@href, 'kursy-dlya-detej-9-11-let')]")
    # Ссылка на курс для детей 12-13 лет
    kids_12_13_link = WebElement(xpath="//a[contains(@href, 'kursy-dlya-detej-12-13-let')]")
    # Ссылка на IT-колледж — ищется по домену в href
    it_college_link = WebElement(xpath="//a[contains(@href, 'it-college.itstep.by')]")
