import time
import requests #для HTTP-запросов (используется в методе validate_html для проверки HTML через W3C validator).

from termcolor import colored #colored — функция для окрашивания текста в консоли (используется для вывода сообщений об ошибках в красном цвете).
from selenium.webdriver.common.by import By #способ локализации элементов (по ID, XPATH, CLASS_NAME и т.д.).
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC #EC — предсказуемые условия (например, element_to_be_clickable, presence_of_element_located).


class WebPage(object): #базовый класс для всех страниц сайта в POM.
    _web_driver = None #приватный атрибут для хранения экземпляра Selenium WebDriver (инициализируется в __init__).

    def __init__(self, web_driver, url=''): #Сохраняет драйвер в _web_driver, Сразу вызывает get(url) — открывает страницу.

        self._web_driver = web_driver #web_driver — экземпляр WebDriver (например, webdriver.Chrome()
        self.get(url) #URL страницы (по умолчанию пустой).

    def __setattr__(self, name, value): #Магический метод __setattr__ вызывается при любой попытке присвоить значение атрибуту
        #Это позволяет писать в тесте:page.username = "tom"  # автоматически найдёт элемент и впишет текст
        if not name.startswith('_'): #Если атрибут не начинается с _ (то есть публичный):
            self.__getattribute__(name)._set_value(self._web_driver, value) #Получает этот атрибут через __getattribute__.
        else:
            super(WebPage, self).__setattr__(name, value) #Использует стандартное присваивание через super().

    def __getattribute__(self, item): #Магический метод __getattribute__
        attr = object.__getattribute__(self, item) #Переопределяет доступ к атрибутам.

        if not item.startswith('_') and not callable(attr): #если атрибут публичный и не является методом (callable),
            attr._web_driver = self._web_driver #добавляет к нему _web_driver и _page — ссылки на драйвер и страницу
            attr._page = self #Это нужно для объектов-локаторов из elements.py, чтобы они могли работать с драйвером.

        return attr

    def get(self, url):
        self._web_driver.get(url) #Открывает URL через driver.get(url)
        self.wait_page_loaded() #Ожидает загрузки страницы через wait_page_loaded()

    def go_back(self):
        self._web_driver.back() #Возвращается на предыдущую страницу (как кнопка "Назад" в браузере).
        self.wait_page_loaded() #Ожидает загрузки

    def refresh(self):
        self._web_driver.refresh() #Перезагружает текущую страницу.
        self.wait_page_loaded() #Ожидает загрузки

    def screenshot(self, file_name='screenshot.png'): #Сохраняет скриншот страницы в файл
        self._web_driver.save_screenshot(file_name) #По умолчанию — screenshot.png

    def scroll_down(self, offset=0):
        """ Прокрутите страницу вниз. """

        if offset: #Если указан offset — скролл на конкретную позицию
            self._web_driver.execute_script('window.scrollTo(0, {0});'.format(offset))
        else: #Если offset=0 — скролл в самый конец страницы
            self._web_driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

    def scroll_up(self, offset=0): #аналогично, но вверх
        """ Прокрутить страницу вверх. """

        if offset:
            self._web_driver.execute_script('window.scrollTo(0, -{0});'.format(offset))
        else:
            self._web_driver.execute_script('window.scrollTo(0, -document.body.scrollHeight);')

    def switch_to_iframe(self, iframe): #Переключает контекст на iframe (по имени или объекту)
        """ Переключитесь на iframe по его имени. """
        self._web_driver.switch_to.frame(iframe)

    def get_cookies(self): #Возвращает все cookie текущей сессии.
        """ Этот метод выводит все доступные файлы cookie для текущей сессии. """
        return self._web_driver.get_cookies()

    def add_cookie(self, name, value): #Добавляет cookie с именем name и значением value
        """ Этот метод помогает настроить файл cookie для сессии. """
        return self._web_driver.add_cookie(name=name, value=value)

    def switch_to_alert_accept(self): #Метод принимает (подтверждает) модальное окно alert/confirm/prompt в браузере — то есть нажимает кнопку "OK"
        """ Deprecated use switch_to_alert. """
        # self._web_driver - Экземпляр Selenium WebDriver (браузер).switch_to Объект для переключения контекста (вкладки, iframe, alert)
        #.alert Возвращает объект Alert — представление модального окна
        #Это переключает контекст браузера на модальное окно. Без этого нельзя работать с alert.
        #.accept() Нажимает кнопку "OK" (подтверждает),.dismiss() Нажимает кнопку "Cancel" (отклоняет)
        #accept() закрывает алерт и продолжает выполнение теста.
        #Типы модальных окон в JavaScript: alert("Сообщение"),confirm("OK или Отмена?"),prompt("Введите текст:")
        self._web_driver.switch_to.alert.accept()

    def switch_to_window(self, window=0): #Переключается на вкладку по индексу (0 — первая)
        """ Переключитесь на вкладку по его индексу. """
        self._web_driver.switch_to.window(self._web_driver.window_handles[window])

    def switch_out_iframe(self): #Возвращает контекст из iframe в основное содержимое.
        """ Отменить фокус iframe. """
        self._web_driver.switch_to.default_content()

    def validate_html(self, url):#проверяет код веб-страниц на соответствие официальным стандартам интернета
        """Функция для проверки валидации HTML страницы"""
        validator_url = 'https://validator.w3.org/nu/?out=json'
        headers = {'Content-Type': 'text/html; charset=utf-8'}
        data = requests.get(url).text #Получает HTML страницы через requests.get(url).
        response = requests.post(validator_url, headers=headers, data=data.encode('utf-8'))
        results = response.json()
        return results #Возвращает JSON с результатами проверки валидности HTML

    def get_current_url(self):
        """ Возвращает URL текущего браузера. """
        return self._web_driver.current_url

    def execute_script(self, script):
        """ Возвращает JS скрипт. """
        return self._web_driver.execute_script(script)

    def get_page_source(self):
        """ Возвращает тело текущей страницы. """

        source = ''
        try:
            source = self._web_driver.page_source
        except:
            print(colored('Can not get page source', 'red'))

        return source

    def check_js_errors(self, ignore_list=None):
        """ Эта функция проверяет ошибки JS на странице. """

        ignore_list = ignore_list or []

        logs = self._web_driver.get_log('browser') #Получает логи браузера ('browser').

        for log_message in logs:
            if log_message['level'] != 'WARNING': #Если уровень не 'WARNING' — игнорирует.
                ignore = False
                for issue in ignore_list: #Если сообщение содержит что-то из ignore_list — игнорирует.
                    if issue in log_message['message']:
                        ignore = True
                        break
                #Иначе — assert с ошибкой JS.
                assert ignore, 'JS error "{0}" on the page!'.format(log_message)
    #Это самый сложный метод — ожидает полной загрузки страницы через несколько проверок
    #timeout = 60 — максимальное время ожидания(сек).
    #check_js_complete = True — проверить document.readyState == 'complete'.
    #check_page_changes = False — убедиться, что HTML не меняется.
    #check_images = False — проверить загрузку изображений.
    #wait_for_element = None — ожидать появления элемента.
    #wait_for_xpath_to_disappear = '' — ожидать исчезновения XPATH.
    #sleep_time = 2 — начальная задержка.
    def wait_page_loaded(self, timeout=60, check_js_complete=True,
                         check_page_changes=False, check_images=False,
                         wait_for_element=None,
                         wait_for_xpath_to_disappear='',
                         sleep_time=2):
        """ Эта функция ждет, пока страница не будет полностью загружена.
            Мы используем много разных способов определить, загружена страница или нет.:
            1) Проверить статус JS
            2) Проверить модификацию в исходном коде страницы
            3) Убедитесь, что все изображения загружены полностью
               (Примечание: по умолчанию эта проверка отключена)
            4) Убедиться, что ожидаемые элементы, представленные на странице
        """

        page_loaded = False
        double_check = False
        k = 0

        if sleep_time:
            time.sleep(sleep_time) #Начальная задержка time.sleep(sleep_time)

        # Получить исходный код страницы для отслеживания изменений в HTML:
        source = ''
        try:
            source = self._web_driver.page_source #апоминает исходный HTML
        except:
            pass

        # Подождать, пока страница загрузится (и прокрутить ее, чтобы убедиться, что все объекты будут загружены):
        while not page_loaded:
            time.sleep(0.5)
            k += 1

            if check_js_complete:
                # Прокрутить вниз и подождите, пока страница загрузится:
                try:
                    self._web_driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    page_loaded = self._web_driver.execute_script("return document.readyState == 'complete';")
                except Exception as e:
                    pass

            if page_loaded and check_page_changes:
                # Проверьть не изменился ли источник страницы
                new_source = ''
                try:
                    new_source = self._web_driver.page_source
                except:
                    pass

                page_loaded = new_source == source
                source = new_source

            # Подождить когда какой-то элемент исчезнет:
            if page_loaded and wait_for_xpath_to_disappear:
                bad_element = None

                try:
                    bad_element = WebDriverWait(self._web_driver, 0.1).until(
                        EC.presence_of_element_located((By.XPATH, wait_for_xpath_to_disappear))
                    )
                except:
                    pass  # Игнорировать ошибки тайм-аута

                page_loaded = not bad_element

            if page_loaded and wait_for_element:
                try:
                    page_loaded = WebDriverWait(self._web_driver, 0.1).until(
                        EC.element_to_be_clickable(wait_for_element._locator)
                    )
                except:
                    pass  # Игнорировать ошибки тайм-аута

            assert k < timeout, 'The page loaded more than {0} seconds!'.format(timeout)

            # Проверить два раза, что страница полностью загружена:
            if page_loaded and not double_check:
                page_loaded = False
                double_check = True

        # Поднимать вверх (скролл):
        self._web_driver.execute_script('window.scrollTo(document.body.scrollHeight, 0);')