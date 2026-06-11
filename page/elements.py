#!/usr/bin/python3
# -*- encoding=utf8 -*-

import time
from termcolor import colored

from selenium.webdriver import ActionChains #имитирует сложные действия пользователя(перетаскивание, правый клик)
from selenium.webdriver.support.ui import WebDriverWait #явные ожидания
from selenium.webdriver.support import expected_conditions as EC #условия ожидания (element_to_be_clickable, presence_of_element_located и т.д.).
from selenium.webdriver.common.keys import Keys #спец. клавиши (например, Keys.DOWN, Keys.ENTER)


class WebElement(object): #базовый класс для одного элемента страницы
    _locator = ('', '') #локатор в формате (BY, value), например ('xpath', '//input[@id="username"]')
    _web_driver = None # ссылка на WebDriver (заполняется из base_page.py)
    _page = None #ссылка на страницу (из base_page.py)
    _timeout = 10 #время ожидания по умолчанию
    _wait_after_click = False  # ждать ли загрузки страницы после клика.
    # параметры timeout=10 — время ожидания, wait_after_click=False — ждать ли после клика, **kwargs — произвольные локаторы (например, xpath='...', id='...').
    def __init__(self, timeout=10, wait_after_click=False, **kwargs):
        self._timeout = timeout
        self._wait_after_click = wait_after_click

        for attr in kwargs: #Преобразует имя атрибута (например, xpath) в формат 'xpath'
            self._locator = (str(attr).replace('_', ' '), str(kwargs.get(attr))) #Сохраняет в _locator = ('xpath', 'value').

    def find(self, timeout=10): #Ожидает появления элемента в DOM.
        """ Найти элемент на странице. """

        element = None

        try: #Использует EC.presence_of_element_located(self._locator)
            element = WebDriverWait(self._web_driver, timeout).until(
                EC.presence_of_element_located(self._locator)
            )
        except: #Если не найдено — выводит красное сообщение.
            print(colored('Element not found on the page!', 'red'))

        return element ##Использует EC.presence_of_element_located(self._locator)

    def wait_to_be_clickable(self, timeout=10, check_visibility=True):
        """ Подождать пока элемент будет готов к клику. """

        element = None

        try:
            element = WebDriverWait(self._web_driver, timeout).until(
                EC.element_to_be_clickable(self._locator)
            )
        except:
            print(colored('Element not clickable!', 'red'))

        if check_visibility: #Если check_visibility=True — вызывает wait_until_not_visible() (ожидает исчезновения)
            self.wait_until_not_visible()

        return element #Возвращает элемент или None.

    def is_clickable(self): #Быстрая проверка кликабельности (timeout=0.1).
        """ Проверка, готов ли элемент к клику или нет. """

        element = self.wait_to_be_clickable(timeout=0.1)
        return element is not None #Возвращает True/False.

    def is_presented(self):
        """ Проверка, что элемент представлен на странице. """

        element = self.find(timeout=0.1)
        return element is not None #Возвращает True/False.

    def is_visible(self):
        """ Проверка, виден ли элемент или нет. """

        element = self.find(timeout=0.1)

        if element:
            return element.is_displayed() #element.is_displayed() — Selenium метод

        return False #True/False

    def wait_until_not_visible(self, timeout=10): #Имя метода неочевидное: он ожидает видимости элемента (не исчезновения!)

        element = None

        try:
            element = WebDriverWait(self._web_driver, timeout).until(
                EC.visibility_of_element_located(self._locator)
            ) #Использует EC.visibility_of_element_located()
        except:
            print(colored('Element not visible!', 'red'))

        if element: #Если элемент найден:
            js = ('return (!(arguments[0].offsetParent === null) && '
                  '!(window.getComputedStyle(arguments[0]) === "none") &&'
                  'arguments[0].offsetWidth > 0 && arguments[0].offsetHeight > 0'
                  ');')
            visibility = self._web_driver.execute_script(js, element) #Выполняет JS-проверку видимости (offsetParent, offsetWidth, offsetHeight)
            iteration = 0

            while not visibility and iteration < 10: #В цикле (до 10 итераций) повторяет проверку с задержкой 0.5 сек
                time.sleep(0.5)

                iteration += 1

                visibility = self._web_driver.execute_script(js, element)
                print('Element {0} visibility: {1}'.format(self._locator, visibility)) #Выводит лог видимости.

        return element #Возвращает элемент.

    def send_keys(self, keys, wait=2):
        """ Написать текст. """

        keys = keys.replace('\n', '\ue007') #Заменяет \n на спец. символ \ue007 (Enter).

        element = self.find()  #Находит элемент.

        if element: #Если найден:
            element.click() #кликает
            element.clear() #очищает поле
            element.send_keys(keys) #вводит текст
            time.sleep(wait) #задержка 2 сек
        else:
            msg = 'Element with locator {0} not found'
            raise AttributeError(msg.format(self._locator)) #Если не найден — AttributeError

    def get_text(self):
        """ Взять текст. """

        element = self.find()
        text = ''

        try:
            text = str(element.text)
        except Exception as e:
            print('Error: {0}'.format(e)) #Если ошибка — выводит сообщение.

        return text #Возвращает текст элемента (element.text).

    def get_attribute(self, attr_name):
        """ Взять атрибут. """

        element = self.find()

        if element:
            return element.get_attribute(attr_name) #Возвращает атрибут элемента (например, value, class, href).

    def _set_value(self, web_driver, value, clear=True): #Используется через __setattr__ из base_page.py
        """ Установить значение для элемента ввода. """

        element = self.find()

        if clear:
            element.clear()

        element.send_keys(value) #Очищает поле (если clear=True) и вводит значение.

    def click(self, hold_seconds=0, x_offset=1, y_offset=1): #Ожидает кликабельности.
        """ Подождать и нажать на элемент. """

        element = self.wait_to_be_clickable()

        if element: #Если найден:
            action = ActionChains(self._web_driver) #ActionChains — создаёт цепочку действий
            action.move_to_element_with_offset(element, x_offset, y_offset). \
                pause(hold_seconds).click(on_element=element).perform() #move_to_element_with_offset() — перемещает к элементу с offset, perform() — выполняет цепочку.
        else:
            msg = 'Element with locator {0} not found'
            raise AttributeError(msg.format(self._locator)) #Если не найден — AttributeError.

        if self._wait_after_click: #Если _wait_after_click=True — ожидает загрузки страницы после клика.
            self._page.wait_page_loaded()

    def right_mouse_click(self, x_offset=0, y_offset=0, hold_seconds=0):
        """ Нажать на элемент правой кнопкой мыши. """

        element = self.wait_to_be_clickable()

        if element:
            action = ActionChains(self._web_driver)
            action.move_to_element_with_offset(element, x_offset, y_offset). \
                pause(hold_seconds).context_click(on_element=element).perform() #Аналогично click(), но использует context_click().
        else:
            msg = 'Element with locator {0} not found'
            raise AttributeError(msg.format(self._locator))

    def highlight_and_make_screenshot(self, file_name='element.png'):
        """ Выделите элемент и сделайте снимок экрана всей страницы.. """

        element = self.find()

        # Прокрутите страницу до элемента:
        self._web_driver.execute_script("arguments[0].scrollIntoView();", element) #Скроллит к элементу.

        # Добавьте красную рамку к стилю (border='3px solid red'):
        self._web_driver.execute_script("arguments[0].style.border='3px solid red'", element)

        # Сделать скрин страницы:
        self._web_driver.save_screenshot(file_name)

    def scroll_to_element(self):
        """ Прокрутка к элементу. """

        element = self.find()

        # Прокрутите страницу до элемента:
        # Вариант №1 для перехода к элементу: #Вариант 1 (закомментирован): scrollIntoView() через JS.
        # self._web_driver.execute_script("arguments[0].scrollIntoView();", element)

        # Вариант №2 для перехода к элементу:
        try:
            element.send_keys(Keys.DOWN) #send_keys(Keys.DOWN) — отправляет клавишу DOWN.
        except Exception as e: #Если ошибка — игнорирует.
            pass  # Просто проигнорим ошибку, если мы не можем отправить ключи элементу

    def delete(self):
        """ Удалить элемент. """

        element = self.find()

        # Удаляет элемент из DOM через JS (element.remove()).
        self._web_driver.execute_script("arguments[0].remove();", element)


class ManyWebElements(WebElement): #Дочерний класс для нахождения нескольких элементов (например, список <li>).
    # Переопределяет методы для работы с списком.
    def __getitem__(self, item): #Позволяет обращаться по индексу:
        """ Получить список элементов и попытаться вернуть требуемый элемент. """

        elements = self.find()
        return elements[item]

    def find(self, timeout=10): #Находит все элементы по локатору.
        """ Найти элемент на странице. """

        elements = []

        try:
            elements = WebDriverWait(self._web_driver, timeout).until(
                EC.presence_of_all_elements_located(self._locator)
            )
        except:
            print(colored('Elements not found on the page!', 'red'))

        return elements #Возвращает список элементов.

    def _set_value(self, web_driver, value): #Не применимо для списка — поднимает NotImplemented.

        """ Примечание: данное действие неприменимо для списка элементов. """
        raise NotImplemented('This action is not applicable for the list of elements')

    def click(self, hold_seconds=0, x_offset=0, y_offset=0): #Также не применимо для списка.
        """ Примечание: данное действие неприменимо для списка элементов. """
        raise NotImplemented('This action is not applicable for the list of elements')

    def count(self): #Возвращает количество найденных элементов.
        """ Сумма элементов. """

        elements = self.find()
        return len(elements) #Возвращает количество найденных элементов.

    def get_text(self):#Метод get_text() для класса ManyWebElements:
        """ Взять текст элементов. """

        elements = self.find() #self.find() — переопределённый метод из ManyWebElements.
        result = [] #Находит все элементы по локатору (список).

        for element in elements: #Для каждого элемента извлекает его текстовое содержимое.
            text = ''

            try: #Selenium свойство — возвращает текстовое содержимое элемента (включая всех потомков)
                text = str(element.text) #Преобразует в строку (на всякий случай, хотя element.text уже строка)
            except Exception as e: #Если ошибка (например, элемент удалён из DOM) — выводит сообщение и оставляет text = ''
                print('Error: {0}'.format(e))

            result.append(text)

        return result #Возвращает список строк (один текст на каждый элемент).

    def get_attribute(self, attr_name): #Возвращает список атрибутов всех элементов.
        """ Взять атрибут элементов. """

        results = []
        elements = self.find()

        for element in elements:
            results.append(element.get_attribute(attr_name))

        return results

    def highlight_and_make_screenshot(self, file_name='element.png'):
        """ Выделите элементы и сделайте скриншот всей страницы.. """

        elements = self.find()

        for element in elements:
            # Прокрутите страницу до элемента:
            self._web_driver.execute_script("arguments[0].scrollIntoView();", element)

            # Добавьте красную рамку к стилю:
            self._web_driver.execute_script("arguments[0].style.border='3px solid red'", element)

        # Сделать скрин страницы:
        self._web_driver.save_screenshot(file_name)
