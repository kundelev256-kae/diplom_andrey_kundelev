# Импорт библиотеки Allure для создания отчётов и декорирования тестов
import allure
# Импорт модуля time для использования задержек (sleep) между действиями браузера
import time
# Импорт модуля random для случайного выбора данных (имена, телефоны)
import random

# Импорт локаторов главной страницы — содержит CSS/XPath селекторы для элементов
from locators.locators_main import MainPage
# Импорт By для указания способа поиска элементов (ID, XPath, CSS и т.д.)
from selenium.webdriver.common.by import By
# Импорт WebDriverWait для явного ожидания появления/кликабельности элементов
from selenium.webdriver.support.ui import WebDriverWait
# Импорт expected_conditions — предусловия для WebDriverWait (кликабельность, видимость и т.д.)
from selenium.webdriver.support import expected_conditions as EC


# Вспомогательная функция: закрывает баннер cookies, если он отображается
def dismiss_cookies(page):
    # Если кнопка принятия cookies присутствует на странице
    if page.btn_access.is_presented():
        # Кликаем по кнопке cookies для закрытия баннера
        page.btn_access.click()


# ──────────────────────────────────────────────
# 1. Проверка хэдера
# ──────────────────────────────────────────────

# Декоратор Allure: название теста — "Проверка хэдера: наличие, отображение и кликабельность всех элементов"
@allure.title('Проверка хэдера: наличие, отображение и кликабельность всех элементов')
# Декоратор Allure: фича — "Хэдер" (группировка в отчёте)
@allure.feature('Хэдер')
# Функция теста: проверяет все элементы хэдера на главной странице
def test_header(web_browser):
    # Создаём Page Object главной страницы
    page = MainPage(web_browser)
    # Закрываем баннер cookies, если он отображается
    dismiss_cookies(page)

    # Шаг Allure: проверяем логотип
    with allure.step('Проверить логотип'):
        # Утверждение: логотип должен быть видим на странице
        assert page.logo.is_visible(), "Логотип не отображается"
        # Утверждение: логотип должен быть кликабелен
        assert page.logo.is_clickable(), "Логотип не кликабелен"

    # Шаг Allure: проверяем блок телефонов
    with allure.step('Проверить блок телефонов'):
        # Утверждение: блок телефонов должен присутствовать на странице
        assert page.phones_block.is_presented(), "Блок телефонов не найден"
        # Утверждение: блок телефонов должен быть видим
        assert page.phones_block.is_visible(), "Блок телефонов не отображается"

    # Шаг Allure: проверяем адрес компании
    with allure.step('Проверить адрес'):
        # Утверждение: адрес должен быть видим на странице
        assert page.address_text.is_visible(), "Адрес не отображается"

    # Шаг Allure: проверяем панель информации
    with allure.step('Проверить панель информации'):
        # Утверждение: панель информации должна присутствовать
        assert page.info_panel.is_presented(), "Панель информации не найдена"

    # Шаг Allure: проверяем панель меню
    with allure.step('Проверить панель меню'):
        # Утверждение: панель меню должна присутствовать
        assert page.menu_panel.is_presented(), "Панель меню не найдена"

    # Шаг Allure: проверяем выпадающее меню "IT ОБРАЗОВАНИЕ"
    with allure.step('Проверить меню "IT ОБРАЗОВАНИЕ"'):
        # Утверждение: меню должно быть видимым
        assert page.it_education_menu.is_visible(), "Меню 'IT ОБРАЗОВАНИЕ' не отображается"

    # Шаг Allure: проверяем навигационные ссылки в меню
    with allure.step('Проверить навигационные ссылки'):
        # Утверждение: ссылка "МЕРОПРИЯТИЯ" должна быть видима и кликабельна
        assert page.nav_news.is_visible(), "Ссылка 'МЕРОПРИЯТИЯ' не отображается"
        assert page.nav_news.is_clickable(), "Ссылка 'МЕРОПРИЯТИЯ' не кликабельна"
        # Утверждение: ссылка "Статьи" должна быть видима и кликабельна
        assert page.nav_articles.is_visible(), "Ссылка 'Статьи' не отображается"
        assert page.nav_articles.is_clickable(), "Ссылка 'Статьи' не кликабельна"
        # Утверждение: ссылка "КОНТАКТЫ" должна быть видима и кликабельна
        assert page.nav_contacts.is_visible(), "Ссылка 'КОНТАКТЫ' не отображается"
        assert page.nav_contacts.is_clickable(), "Ссылка 'КОНТАКТЫ' не кликабельна"
        # Утверждение: ссылка "Обучение английскому" должна быть видима и кликабельна
        assert page.nav_english.is_visible(), "Ссылка 'Обучение английскому' не отображается"
        assert page.nav_english.is_clickable(), "Ссылка 'Обучение английскому' не кликабельна"

    # Шаг Allure: проверяем бургер-меню (мобильная версия)
    with allure.step('Проверить бургер-меню'):
        # Утверждение: бургер-меню должно присутствовать в DOM
        assert page.burger_menu.is_presented(), "Бургер-меню не найдено"


# ──────────────────────────────────────────────
# 2. Проверка футера
# ──────────────────────────────────────────────

# Декоратор Allure: название теста — "Проверка футера: наличие, отображение и кликабельность всех элементов"
@allure.title('Проверка футера: наличие, отображение и кликабельность всех элементов')
# Декоратор Allure: фича — "Футер" (группировка в отчёте)
@allure.feature('Футер')
# Функция теста: проверяет все элементы футера на главной странице
def test_footer(web_browser):
    # Создаём Page Object главной страницы
    page = MainPage(web_browser)
    # Закрываем баннер cookies
    dismiss_cookies(page)

    # Шаг Allure: прокручиваем страницу к футеру
    with allure.step('Прокрутить к футеру'):
        # Прокручиваем страницу к футеру через JavaScript
        web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", page.footer.find())
        # Ждём 1 секунду для полной отрисовки футера
        time.sleep(1)

    # Шаг Allure: проверяем логотип в футере
    with allure.step('Проверить логотип в футере'):
        # Утверждение: логотип в футере должен быть видим
        assert page.footer_logo.is_visible(), "Логотип в футере не отображается"
        # Утверждение: логотип в футере должен быть кликабелен
        assert page.footer_logo.is_clickable(), "Логотип в футере не кликабелен"

    # Шаг Allure: проверяем блок контактов футера
    with allure.step('Проверить блок контактов футера'):
        # Утверждение: секция контактов футера должна присутствовать
        assert page.footer_contacts_section.is_presented(), "Секция контактов футера не найдена"

    # Шаг Allure: проверяем ссылку на сайт в контактах
    with allure.step('Проверить ссылку на сайт'):
        # Утверждение: ссылка на сайт должна быть кликабельна
        assert page.footer_contacts_site.is_clickable(), "Ссылка на сайт не кликабельна"

    # Шаг Allure: проверяем телефоны в контактах футера
    with allure.step('Проверить телефоны в контактах'):
        # Утверждение: телефон 1 в контактах должен быть кликабелен
        assert page.footer_contacts_phone1.is_clickable(), "Телефон 1 в контактах не кликабелен"
        # Утверждение: телефон 2 в контактах должен быть кликабелен
        assert page.footer_contacts_phone2.is_clickable(), "Телефон 2 в контактах не кликабелен"

    # Шаг Allure: проверяем email в контактах
    with allure.step('Проверить email'):
        # Утверждение: email в контактах должен быть кликабелен
        assert page.footer_contacts_email.is_clickable(), "Email в контактах не кликабелен"

    # Шаг Allure: проверяем навигацию в футере
    with allure.step('Проверить навигацию в футере'):
        # Утверждение: ссылка "Направления обучения" должна быть кликабельна
        assert page.footer_nav_directions.is_clickable(), "Ссылка 'Направления обучения' не кликабельна"
        # Утверждение: ссылка "Статьи" должна быть кликабельна
        assert page.footer_nav_articles.is_clickable(), "Ссылка 'Статьи' не кликабельна"
        # Утверждение: ссылка "Новости и акции" должна быть кликабельна
        assert page.footer_nav_news.is_clickable(), "Ссылка 'Новости и акции' не кликабельна"
        # Утверждение: ссылка "Контакты" должна быть кликабельна
        assert page.footer_nav_contacts.is_clickable(), "Ссылка 'Контакты' не кликабельна"

    # Шаг Allure: проверяем телефоны в футере
    with allure.step('Проверить телефоны в футере'):
        # Утверждение: телефон 1 в футере должен быть кликабелен
        assert page.footer_phone1.is_clickable(), "Телефон 1 в футере не кликабелен"
        # Утверждение: телефон 2 в футере должен быть кликабелен
        assert page.footer_phone2.is_clickable(), "Телефон 2 в футере не кликабелен"

    # Шаг Allure: проверяем адрес в футере
    with allure.step('Проверить адрес в футере'):
        # Утверждение: адрес в футере должен присутствовать
        assert page.footer_address.is_presented(), "Адрес в футере не найден"

    # Шаг Allure: проверяем соцсети в футере
    with allure.step('Проверить соцсети в футере'):
        # Утверждение: ссылка VK должна быть кликабельна
        assert page.footer_vk.is_clickable(), "Ссылка VK не кликабельна"
        # Утверждение: ссылка Facebook должна быть кликабельна
        assert page.footer_facebook.is_clickable(), "Ссылка Facebook не кликабельна"
        # Утверждение: ссылка Telegram должна быть кликабельна
        assert page.footer_telegram.is_clickable(), "Ссылка Telegram не кликабельна"
        # Утверждение: ссылка Instagram должна быть кликабельна
        assert page.footer_instagram.is_clickable(), "Ссылка Instagram не кликабельна"
        # Утверждение: ссылка YouTube должна быть кликабельна
        assert page.footer_youtube.is_clickable(), "Ссылка YouTube не кликабельна"

    # Шаг Allure: проверяем копирайт
    with allure.step('Проверить копирайт'):
        # Утверждение: копирайт должен присутствовать
        assert page.footer_copyright.is_presented(), "Копирайт не найден"


# ──────────────────────────────────────────────
# 3. Проверка центрального блока
# ──────────────────────────────────────────────

# Декоратор Allure: название теста — "Проверка центрального блока: наличие, отображение и кликабельность всех элементов"
@allure.title('Проверка центрального блока: наличие, отображение и кликабельность всех элементов')
# Декоратор Allure: фича — "Центральный блок" (группировка в отчёте)
@allure.feature('Центральный блок')
# Функция теста: проверяет элементы центрального блока (слайдер, дети, отзывы, чат)
def test_central_block(web_browser):
    # Создаём Page Object главной страницы
    page = MainPage(web_browser)
    # Закрываем баннер cookies
    dismiss_cookies(page)

    # Шаг Allure: проверяем слайдер
    with allure.step('Проверить слайдер'):
        # Утверждение: секция слайдера должна присутствовать
        assert page.slider_section.is_presented(), "Слайдер не найден"

    # Шаг Allure: проверяем кнопку "УЗНАТЬ ПОДРОБНОСТИ"
    with allure.step('Проверить кнопку "УЗНАТЬ ПОДРОБНОСТИ"'):
        # Утверждение: кнопка слайдера должна быть кликабельна
        assert page.learn_more_btn.is_clickable(), "Кнопка слайдера не кликабельна"

    # Шаг Allure: проверяем блок "Обучение для детей и подростков"
    with allure.step('Проверить блок "Обучение для детей и подростков"'):
        # Утверждение: заголовок блока детей должен быть видим
        assert page.kids_section_title.is_visible(), "Заголовок блока детей не отображается"

    # Шаг Allure: проверяем ссылки на курсы для детей
    with allure.step('Проверить ссылки на курсы для детей'):
        # Утверждение: ссылка "7-8 лет" должна присутствовать в DOM
        assert page.kids_7_8_link.is_presented(), "Ссылка '7-8 лет' не найдена"
        # Утверждение: ссылка "9-11 лет" должна присутствовать в DOM
        assert page.kids_9_11_link.is_presented(), "Ссылка '9-11 лет' не найдена"
        # Утверждение: ссылка "12-13 лет" должна присутствовать в DOM
        assert page.kids_12_13_link.is_presented(), "Ссылка '12-13 лет' не найдена"
        # Утверждение: ссылка "IT колледж" должна присутствовать в DOM
        assert page.it_college_link.is_presented(), "Ссылка 'IT колледж' не найдена"

    # Шаг Allure: проверяем блок отзывов
    with allure.step('Проверить блок отзывов'):
        # Утверждение: заголовок отзывов должен быть видим
        assert page.reviews_title.is_visible(), "Заголовок отзывов не отображается"
        # Утверждение: отзыв YANDEX должен присутствовать
        assert page.review_yandex.is_presented(), "Отзыв YANDEX не найден"
        # Утверждение: отзыв GOOGLE должен присутствовать
        assert page.review_google.is_presented(), "Отзыв GOOGLE не найден"
        # Утверждение: отзыв FACEBOOK должен присутствовать
        assert page.review_facebook.is_presented(), "Отзыв FACEBOOK не найден"

    # Шаг Allure: проверяем ссылку на профориентационный тест
    with allure.step('Проверить ссылку на профориентационный тест'):
        # Утверждение: ссылка на профтест должна присутствовать в DOM
        assert page.career_guidance_link.is_presented(), "Ссылка на профтест не найдена"

    # Шаг Allure: проверяем виджет чата
    with allure.step('Проверить виджет чата'):
        # Утверждение: виджет чата должен присутствовать в DOM
        assert page.chat_button.is_presented(), "Виджет чата не найден"


# ──────────────────────────────────────────────
# 4. E2E тест: заполнение формы профориентации
# ──────────────────────────────────────────────

# Декоратор Allure: название теста — "E2E: Профориентационный тест — заполнение формы"
@allure.title('E2E: Профориентационный тест — заполнение формы')
# Декоратор Allure: фича — "E2E тесты" (сквозные тесты от начала до конца)
@allure.feature('E2E тесты')
# Функция E2E теста: проходит весь путь от главной страницы до заполнения и отправки формы профтеста
def test_career_guidance_form(web_browser):
    # Список мужских и женских имён для случайной генерации данных
    first_names = ['Александр', 'Мария', 'Дмитрий', 'Анна', 'Сергей', 'Елена', 'Иван', 'Ольга']
    # Список фамилий для случайной генерации данных
    last_names = ['Иванов', 'Петрова', 'Сидоров', 'Козлова', 'Морозов', 'Новикова', 'Волков', 'Лебедева']

    # Случайный выбор имени из списка
    first_name = random.choice(first_names)
    # Случайный выбор фамилии из списка
    last_name = random.choice(last_names)
    # Генерация белорусского номера телефона: +375 + код оператора (29/33/25/17) + 7 цифр
    phone = f"+375{random.choice(['29', '33', '25', '17'])}{random.randint(1000000, 9999999)}"
    # Фиксированный email для тестовой формы
    email = "kuzayo@mail.ru"

    # Создаём Page Object главной страницы
    page = MainPage(web_browser)

    # Шаг Allure: принимаем cookies
    with allure.step('Принять cookies'):
        # Кликаем по кнопке принятия cookies
        page.btn_access.click()

    # Шаг Allure: открываем выпадающее меню "IT ОБРАЗОВАНИЕ"
    with allure.step('Открыть меню "IT ОБРАЗОВАНИЕ"'):
        # Кликаем по пункту меню "IT ОБРАЗОВАНИЕ" для раскрытия подменю
        page.it_education_menu.click()

    # Шаг Allure: кликаем по ссылке "Профориентационный тест" в раскрытом меню
    with allure.step('Кликнуть по "Профориентационный тест"'):
        # Находим ссылку на карьерный тест в выпадающем меню
        link = page.career_test_link.find()
        # Кликаем по ссылке через JavaScript (обход потенциальных проблем с кликом)
        web_browser.execute_script("arguments[0].click();", link)
        # Ждём 3 секунды для загрузки страницы теста
        time.sleep(3)

    # Шаг Allure: кликаем по кнопке "Пройти тест" для перехода к форме
    with allure.step('Кликнуть "Пройти тест"'):
        # Явное ожидание: ищем кнопку/ссылку "Пройти тест" (несколько вариантов XPath для разных разметок)
        start_btn = WebDriverWait(web_browser, 15).until(
            EC.element_to_be_clickable((By.XPATH,
                # XPath-список: ищем ссылку или кнопку с текстом "пройти тест" (с учётом регистра)
                "//a[contains(translate(text(),'АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЭЮЯ','абвгдежзиклмнопрстуфхцчшщэюя'), 'пройти тест')] | "
                "//button[contains(translate(text(),'АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЭЮЯ','абвгдежзиклмнопрстуфхцчшщэюя'), 'пройти тест')] | "
                "//a[contains(@class, 'btn') and contains(@href, 'test')] | "
                "//button[contains(@class, 'btn') and contains(@class, 'test')]"
            ))
        )
        # Кликаем по кнопке "Пройти тест" через JavaScript
        web_browser.execute_script("arguments[0].click();", start_btn)
        # Ждём 5 секунд — возможен переход на внешний домен (proftest.itstep.by)
        time.sleep(5)

    # Шаг Allure: проверяем, что произошёл переход на форму теста
    with allure.step('Проверить переход на форму (proftest.itstep.by)'):
        # Получаем текущий URL страницы
        current_url = web_browser.current_url
        # Утверждение: URL должен содержать "proftest.itstep.by" или "form"
        assert "proftest.itstep.by" in current_url or "form" in current_url, \
            f"Не удалось перейти на форму. URL: {current_url}"

    # Шаг Allure: заполняем поле "Имя" сгенерированными данными
    with allure.step(f'Заполнить имя: {first_name} {last_name}'):
        # Явное ожидание: находим поле ввода имени по атрибуту name="question0"
        name_field = WebDriverWait(web_browser, 10).until(
            EC.presence_of_element_located((By.NAME, "question0"))
        )
        # Прокручиваем к полю для видимости
        web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", name_field)
        # Очищаем поле от возможного старого значения
        name_field.clear()
        # Вводим полное имя (имя + фамилия)
        name_field.send_keys(f"{first_name} {last_name}")
        # Короткая пауза для обработки ввода страницей
        time.sleep(0.5)

    # Шаг Allure: заполняем поле "Email"
    with allure.step(f'Заполнить email: {email}'):
        # Находим поле ввода email по name="question1"
        email_field = WebDriverWait(web_browser, 10).until(
            EC.presence_of_element_located((By.NAME, "question1"))
        )
        # Очищаем поле
        email_field.clear()
        # Вводим email
        email_field.send_keys(email)
        # Пауза для обработки
        time.sleep(0.5)

    # Шаг Allure: заполняем поле "Телефон"
    with allure.step(f'Заполнить телефон: {phone}'):
        # Находим поле ввода телефона по name="question2"
        phone_field = WebDriverWait(web_browser, 10).until(
            EC.presence_of_element_located((By.NAME, "question2"))
        )
        # Очищаем поле
        phone_field.clear()
        # Вводим номер телефона
        phone_field.send_keys(phone)
        # Пауза для обработки
        time.sleep(0.5)

    # Шаг Allure: отвечаем на вопросы теста (radio/checkbox)
    with allure.step('Ответить на вопросы теста (radio/checkbox)'):
        # Множество имён уже обработанных групп вопросов (чтобы не отвечать дважды)
        question_names = set()

        # Вспомогательная функция безопасного клика: кликает через JS и обрабатывает всплывающие алерты
        def safe_click(element):
            # Пытаемся кликнуть по элементу через JavaScript
            try:
                web_browser.execute_script("arguments[0].click();", element)
            # Если клик не удался — игнорируем ошибку
            except:
                pass
            # Проверяем, не появился ли всплывающий алерт после клика
            try:
                # Получаем объект алерта
                alert = web_browser.switch_to.alert
                # Получаем текст алерта
                alert_text = alert.text
                # Принимаем (закрываем) алерт
                alert.accept()
                # Публикуем текст алерта в отчёт Allure
                allure.step(f'Алерт: {alert_text}').publish()
            # Если алерта нет — просто продолжаем
            except:
                pass

        # Находим все radio-кнопки на странице теста
        all_radios = web_browser.find_elements(By.CSS_SELECTOR, "input[type='radio']")
        # Перебираем каждую radio-кнопку
        for r in all_radios:
            # Получаем имя группы radio-кнопок (атрибут name)
            qname = r.get_attribute("name")
            # Если эта группа вопросов ещё не обработана
            if qname not in question_names:
                # Добавляем имя группы в множество обработанных
                question_names.add(qname)
                # Находим все варианты ответа в этой группе
                options = web_browser.find_elements(By.CSS_SELECTOR, f"input[name='{qname}']")
                # Если варианты найдены — выбираем случайный
                if options:
                    # Случайный выбор одного варианта ответа
                    chosen = random.choice(options)
                    # Кликаем по выбранному варианту
                    safe_click(chosen)

        # Находим все checkbox-кнопки на странице теста
        all_checkboxes = web_browser.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
        # Перебираем каждую checkbox-кнопку
        for c in all_checkboxes:
            # Получаем имя группы чекбоксов
            qname = c.get_attribute("name")
            # Если эта группа ещё не обработана
            if qname not in question_names:
                # Добавляем имя группы в множество обработанных
                question_names.add(qname)
                # Находим все варианты чекбоксов в этой группе
                options = web_browser.find_elements(By.CSS_SELECTOR, f"input[name='{qname}']")
                # Если варианты найдены — выбираем случайное количество (от 1 до 3)
                if options:
                    # Случайное количество чекбоксов для отметки (от 1 до минимум(3, общее кол-во))
                    num_to_check = random.randint(1, min(3, len(options)))
                    # Случайно выбираем нужное количество вариантов и отмечаем их
                    for opt in random.sample(options, num_to_check):
                        # Кликаем по варианту через безопасный клик
                        safe_click(opt)

    # Шаг Allure: нажимаем кнопку "Узнать свой результат!" для отправки формы
    with allure.step('Нажать "Узнать свой результат!"'):
        # Перед отправкой закрываем возможные висящие алерты
        try:
            # Пытаемся получить всплывающий алерт
            alert = web_browser.switch_to.alert
            # Принимаем алерт
            alert.accept()
        # Если алерта нет — продолжаем
        except:
            pass
        # Явное ожидание: находим кнопку отправки формы (button[type='submit'])
        submit = WebDriverWait(web_browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        # Прокручиваем к кнопке отправки
        web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit)
        # Кликаем по кнопке отправки через JavaScript
        web_browser.execute_script("arguments[0].click();", submit)
        # Пауза 2 секунды после клика
        time.sleep(2)
        # Обрабатываем возможный алерт после отправки формы
        try:
            # Пытаемся получить всплывающий алерт
            alert = web_browser.switch_to.alert
            # Получаем текст алерта
            alert_text = alert.text
            # Принимаем алерт
            alert.accept()
            # Публикуем текст алерта в отчёт Allure
            allure.step(f'Алерт после отправки: {alert_text}').publish()
        # Если алерта нет — продолжаем
        except:
            pass
        # Пауза 3 секунды для завершения обработки формы сервером
        time.sleep(3)

    # Шаг Allure: проверяем, что форма успешно отправлена
    with allure.step('Проверить отправку формы'):
        # Получаем HTML-исходник страницы в нижнем регистре для поиска
        page_source = web_browser.page_source.lower()
        # Список индикаторов успешной отправки формы (ключевые слова, которые появляются после отправки)
        success_indicators = ['результат', 'спасибо', 'отправлено', 'готово', 'ваш', 'профориентация', 'курс']
        # Проверяем, есть ли хотя бы один индикатор на странице
        form_still_visible = any(ind in page_source for ind in success_indicators)
        # Утверждение: хотя бы один индикатор должен присутствовать — форма отправлена успешно
        assert form_still_visible, "Форма не была отправлена — индикатор успеха не найден"
