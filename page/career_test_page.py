# Импорт модуля os для доступа к переменным окружения (получение URL из env)
import os
# Импорт базового класса WebPage — родительский класс для всех страниц проекта
from page.base_page import WebPage
# Импорт класса WebElement — кастомный элемент для работы с XPath/ID-локаторами
from page.elements import WebElement


# Класс CareerTestPage — локаторы страницы теста по профориентации
class CareerTestPage(WebPage):

    # Конструктор: принимает веб-драйвер Selenium и необязательный URL страницы
    def __init__(self, web_driver, url=''):
        # Если URL не передан явно, берём из переменной окружения MAIN или используем дефолтный
        if not url:
            url = os.getenv("MAIN") or 'https://itstep.by/career-guidance-test/'
        # Инициализация родительского класса WebPage с драйвером и URL
        super().__init__(web_driver, url)

    # Кнопка запуска теста — ищется по CSS-классу btn и тексту "пройти тест" внутри тега a
    start_test_btn = WebElement(xpath="//a[contains(@class,'btn') and contains(text(),'пройти тест')]")

    # === Поля формы (появляются после нажатия кнопки "Пройти тест") ===

    # Поле ввода имени — универсальный локатор: ищет по атрибуту name (first_name или name) или по placeholder
    first_name_input = WebElement(xpath="//input[@name='first_name' or @name='name' or @placeholder='* Ваше имя']")
    # Поле ввода фамилии — ищет по name (last_name/surname) или placeholder
    last_name_input = WebElement(xpath="//input[@name='last_name' or @name='surname' or @placeholder='* Ваша фамилия']")
    # Поле ввода email — ищет по name, типу input (email) или placeholder
    email_input = WebElement(xpath="//input[@name='email' or @type='email' or @placeholder='* Ваш e-mail']")
    # Поле ввода телефона — ищет по name, типу input (tel) или placeholder
    phone_input = WebElement(xpath="//input[@name='phone' or @type='tel' or @placeholder='* Телефон']")
    # Кнопка отправки формы — ищет по типу button (submit) или тексту "Отправить"/"Готово"
    submit_btn = WebElement(xpath="//button[@type='submit' or contains(text(),'Отправить') or contains(text(),'Готово')]")
