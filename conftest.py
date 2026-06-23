# Импорт модуля os для работы с операционной системой (пути, файлы, переменные окружения)
import os
# Импорт модуля time для работы с функциями задержки (time.sleep)
import time
# Импорт модуля uuid для генерации уникальных идентификаторов (UUID) при сохранении скриншотов
import uuid
# Импорт библиотеки allure для интеграции с Allure Report — формирование отчётов и вложения скриншотов/логов
import allure
# Импорт pytest — основной фреймворк для запуска и управления тестами
import pytest
# Импорт класса webdriver из библиотеки Selenium для управления браузером
from selenium import webdriver
# Импорт класса Options из модуля настроек Chrome — конфигурация параметров запуска Chrome-драйвера
from selenium.webdriver.chrome.options import Options


# Хук pytest, выполняющийся первым (tryfirst=True) и оборачивающий (hookwrapper=True)
# для перехвата результатов выполнения каждого теста
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
# Функция-хук, вызываемая pytest после каждого этапа теста (setup/call/teardown)
def pytest_runtest_makereport(item, call):
    # yield передаёт управление следующему хуку в цепочке; outcome содержит результат
    outcome = yield
    # Получаем объект отчёта (rep) о текущем этапе выполнения теста
    rep = outcome.get_result()
    # Сохраняем отчёт как атрибут тестового элемента с динамическим именем:
    # rep_setup — для этапа setup, rep_call — для этапа call, rep_teardown — для teardown
    setattr(item, "rep_" + rep.when, rep)
    # Возвращаем отчёт, чтобы он был доступен другим хукам и фикстурам
    return rep


# Фикстура pytest, предоставляющая предварительно настроенные опции Chrome
@pytest.fixture
def chrome_options():
    # Создаём объект Options — контейнер для параметров запуска Chrome-драйвера
    options = Options()
    # Запуск браузера в режиме headless (без графического интерфейса) — подходит для CI/CD серверов
    options.add_argument("--headless")
    # Отключение ускорения отрисовки через GPU — предотвращает ошибки в контейнерах и CI-средах
    options.add_argument("--disable-gpu")
    # Отключение песочницы (sandbox) — требуется для запуска от имени root в Docker-контейнерах
    options.add_argument('--no-sandbox')
    # Отключение использования /dev/shm — предотвращает ошибки нехватки памяти в контейнерах с ограниченным tmpfs
    options.add_argument('--disable-dev-shm-usage')
    # Включение сбора всех логов браузера (console, network, performance и т.д.) через Google Chrome DevTools
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

    # Возвращаем готовый объект настроек Chrome — он будет подставлен в тесты при запросе этой фикстуры
    return options


# Основная фикстура web_browser — создаёт экземпляр браузера Chrome и управляет его жизненным циклом
@pytest.fixture
def web_browser(request):
    # Создаём новый объект Options для настройки Chrome-драйвера
    options = Options()
    # Отключение ускорения отрисовки через GPU — предотвращает графические ошибки в headless-режиме
    options.add_argument('--disable-gpu')
    # Отключение песочницы — необходимо для корректной работы в Docker-контейнерах
    options.add_argument('--no-sandbox')
    # Отключение использования /dev/shm — предотвращает проблемы с памятью в ограниченных средах
    options.add_argument('--disable-dev-shm-usage')
    # Включение сбора всех логов браузера для диагностики при падении тестов
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

    # Если в командной строке передан флаг --headless, добавляем аргумент запуска в headless-режиме
    if request.config.getoption("--headless"):
        # Новый синтаксис headless-режима в актуальных версиях Chrome (>= 109)
        options.add_argument("--headless=new")

    # Создаём экземпляр Chrome-драйвера с указанными настройками — запуск браузера
    browser = webdriver.Chrome(options=options)
    # Разворачиваем окно браузера на весь экран для корректного отображения элементов страницы
    browser.maximize_window()

    # yield передаёт управление тесту — браузер остаётся активным до завершения теста
    yield browser

    # Флаг для отслеживания статуса прохождения теста (успешно/неуспешно)
    failed = False
    # Проверяем, был ли этап call (выполнение тела теста) неуспешным
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        failed = True
    # Если этап call не провалился, проверяем этап setup (подготовка теста)
    elif hasattr(request.node, "rep_setup") and request.node.rep_setup.failed:
        failed = True

    # Если тест провалился — собираем диагностическую информацию
    if failed:
        try:
            # Получаем идентификатор воркера при параллельном запуске (для отладки в pytest-xdist)
            worker_id = request.config.getoption("rsyncdir", default="") or ""
            # Устанавливаем белый фон страницы для улучшения видимости контента на скриншоте
            browser.execute_script("document.body.style.background = 'white';")

            # Формируем уникальное имя файла скриншота с использованием UUID, чтобы избежать перезаписи
            screenshot_path = f'screenshots/{str(uuid.uuid4())}.png'
            # Сохраняем скриншот текущего состояния браузера в локальную файловую систему
            browser.save_screenshot(screenshot_path)

            # Прикрепляем скриншот в формате PNG к отчёту Allure — визуальное доказательство состояния страницы при ошибке
            allure.attach(
                browser.get_screenshot_as_png(),  # Получаем скриншот как бинарные данные PNG
                name=f"{request.function.__name__}_screenshot",  # Имя вложения = имя теста + суффикс
                attachment_type=allure.attachment_type.PNG  # Тип вложения для корректного отображения в отчёте
            )

            # Выводим текущий URL страницы в консоль — помогает определить, на каком шаге упал тест
            print('URL: ', browser.current_url)
            # Выводим заголовок для логов браузера
            print('Browser logs:')
            # Перебираем и печатаем каждую запись из логов браузера (ошибки JS, сетевые запросы и т.д.)
            for log in browser.get_log('browser'):
                print(log)

            # Объединяем все записи логов в одну строку через перенос строки для вложения в Allure
            logs = "\n".join([str(log) for log in browser.get_log('browser')])
            # Прикрепляем логи браузера как текстовое вложение в отчёт Allure — позволяет анализировать ошибки JS
            allure.attach(
                logs,  # Строка с логами браузера
                name=f"{request.function.__name__}_browser_logs",  # Имя вложения = имя теста + суффикс
                attachment_type=allure.attachment_type.TEXT  # Тип вложения — текст
            )

        # Перехватываем любые исключения при сборе отчётности, чтобы не потерять результаты теста из-за ошибки логирования
        except Exception as e:
            # Выводим сообщение об ошибке в консоль — позволяет увидеть проблему при формировании отчёта
            print(f"Ошибка при создании отчетности: {e}")

    # Задержка 2 секунды перед закрытием браузера — даёт время завершиться фоновым процессам и анимациям на странице
    time.sleep(2)
    # Закрываем браузер и освобождаем ресурсы (процесс chromedriver)
    browser.quit()


def pytest_configure(config):
    config.option.alluredir = "allure-results"
    config.option.clean_alluredir = True


# Хук pytest для добавления пользовательских командных опций через консоль
def pytest_addoption(parser):
    # Опция --browser: выбор браузера для запуска тестов (по умолчанию chrome), может быть расширена на firefox и др.
    parser.addoption("--browser", default="chrome", help="Browser to run tests (chrome, firefox)")
    # Опция --headless: флаг для запуска браузера в безголовом режиме (без GUI), полезно для CI/CD
    parser.addoption("--headless", action="store_true", default=False, help="Run tests in headless mode")


# Вспомогательная функция для извлечения и форматирования docstring тест-кейса
def get_test_case_docstring(item):
    """ Эта функция получает строку документа из тестового примера и форматирует ее
        отображая эту строку в документации вместо имени тестового примера в отчетах.
    """

    # Инициализируем пустую строку для формирования полного имени теста
    full_name = ''

    # Проверяем, есть ли у тестовой функции docstring (строка документации)
    if item._obj.__doc__:
        # Удаляем лишние пробелы из строки документа: берём всё до первой точки, убираем пробелы по краям
        name = str(item._obj.__doc__.split('.')[0]).strip()
        # Убираем множественные пробелы между словами, оставляя один пробел
        full_name = ' '.join(name.split())

        # Генерируем список параметров для параметризованных тестовых случаев (с декоратором @pytest.mark.parametrize)
        if hasattr(item, 'callspec'):
            # Получаем словарь параметров теста (например, {'url': 'http://...', 'user': 'admin'})
            params = item.callspec.params

            # Сортируем ключи параметров по алфавиту для стабильного порядка отображения
            res_keys = sorted([k for k in params])
            # Создаём список строк вида 'key_"value"' для каждого параметра
            res = ['{0}_"{1}"'.format(k, params[k]) for k in res_keys]
            # Добавляем параметры к имени теста в формате: 'Название теста Parameters key1_"val1", key2_"val2"'
            full_name += ' Parameters ' + str(', '.join(res))
            # Убираем двоеточия из имени теста, чтобы избежать конфликтов с форматом отчёта
            full_name = full_name.replace(':', '')

    # Возвращаем сформированное полное имя теста с параметрами (или пустую строку, если docstring нет)
    return full_name


# Хук pytest, вызываемый при сборе каждого тест-кейса — изменяет отображаемое имя теста
def pytest_itemcollected(item):
    """ Эта функция изменяет имена тестовых случаев «на лету».
        во время выполнения тест-кейсов.
    """

    # Если у тестовой функции есть docstring, заменяем стандартный идентификатор теста на docstring
    if item._obj.__doc__:
        # Переопределяем _nodeid — внутренний идентификатор теста, отображаемый в отчётах и при запуске
        item._nodeid = get_test_case_docstring(item)


# Хук pytest, вызываемый после завершения сбора всех тестов — используется для вывода списка тестов
def pytest_collection_finish(session):
    """ Эта функция изменяет имена тестовых случаев «на лету»
        когда мы используем параметр --collect-only для pytest
        (чтобы получить полный список всех существующих тестовых случаев).
    """

    # Проверяем, был ли pytest запущен с флагом --collect-only (только сбор тестов без выполнения)
    if session.config.option.collectonly is True:
        # Перебираем все собранные тестовые элементы
        for item in session.items:
            # Если в тестовом примере есть строка документа, нам нужно изменить ее имя на
            # эту строку документа для отображения удобочитаемых отчетов и для
            # автоматически импортировать тестовые случаи в систему управления тестированием.
            if item._obj.__doc__:
                # Получаем отформатированное имя теста на основе docstring
                full_name = get_test_case_docstring(item)
                # Выводим имя теста в консоль — позволяет получить читаемый список всех тестов
                print(full_name)

        # Завершаем работу pytest сразу после вывода списка тестов — дальнейшее выполнение не требуется
        pytest.exit('Done!')
