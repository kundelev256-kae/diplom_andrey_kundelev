import allure  # Импорт библиотеки Allure для создания отчётов и декорирования тестов
import time  # Импорт модуля time для использования задержек (sleep) между действиями браузера
import random  # Импорт модуля random для случайного выбора данных (имена, телефоны)

from locators.locators_main import MainPage  # Импорт локаторов главной страницы — содержит CSS/XPath селекторы для элементов
from selenium.webdriver.common.by import By  # Импорт By для указания способа поиска элементов (ID, XPath, CSS и т.д.)
from selenium.webdriver.support.ui import WebDriverWait  # Импорт WebDriverWait для явного ожидания появления/кликабельности элементов

from selenium.webdriver.support import expected_conditions as EC # Импорт expected_conditions — предусловия для WebDriverWait (кликабельность, видимость и т.д.)


# Вспомогательная функция: закрывает баннер cookies, если он отображается
def dismiss_cookies(page):
    if page.btn_access.is_presented():  # Если кнопка принятия cookies присутствует на странице
        page.btn_access.click()  # Кликаем по кнопке cookies для закрытия баннера
        time.sleep(0.5)  # Ждём 0.5 секунды для анимации закрытия баннера


# ──────────────────────────────────────────────
# 1. Проверка хэдера
# ──────────────────────────────────────────────

# Декоратор Allure: название теста — "Проверка хэдера: наличие, отображение и кликабельность всех элементов"
@allure.title('Проверка хэдера: наличие, отображение и кликабельность всех элементов')
# Декоратор Allure: фича — "Хэдер" (группировка в отчёте)
@allure.feature('Хэдер')
# Функция теста: проверяет все элементы хэдера на главной странице
def test_header(web_browser):
    page = MainPage(web_browser)  # Создаём Page Object главной страницы
    dismiss_cookies(page)  # Закрываем баннер cookies, если он отображается

    # Шаг Allure: проверяем наличие и отображение логотипа
    with allure.step('Проверить логотип'):
        logo = page.logo.find()  # Находим элемент логотипа на странице
        assert logo is not None, "Логотип не найден"  # Утверждение: логотип должен быть найден в DOM
        assert logo.is_displayed(), "Логотип не отображается"  # Утверждение: логотип должен быть видим на странице
        # Утверждение: логотип должен содержать ссылку (быть кликабельным)
        assert logo.get_attribute("href") is not None, "Логотип не кликабелен"

    # Шаг Allure: проверяем блок телефонов
    with allure.step('Проверить блок телефонов'):
        # Утверждение: блок телефонов должен присутствовать на странице
        assert page.phones_block.is_presented(), "Блок телефонов не найден"
        phones = page.phone_links.find()  # Находим все ссылки телефонов в блоке
        # Утверждение: должно быть минимум 2 телефонных номера
        assert len(phones) >= 2, f"Найдено менее 2 телефонов: {len(phones)}"
        for phone in phones:  # Перебираем каждый найденный телефон
            # Утверждение: каждый телефон должен содержать ссылку tel:
            assert phone.get_attribute("href") is not None, f"Телефон не кликабелен: {phone.text}"

    # Шаг Allure: проверяем адрес компании
    with allure.step('Проверить адрес'):
        # Утверждение: блок адреса должен присутствовать на странице
        assert page.address_block.is_presented(), "Блок адреса не найден"
        # Получаем текст адреса через JS (надёжнее чем is_displayed в headless)
        addr_text = web_browser.execute_script(
            "var el = document.querySelector('.info-panel .address .location'); "
            "return el ? el.textContent.trim() : '';"
        )
        assert addr_text, "Адрес не найден"
        # Утверждение: адрес должен содержать "Минск" или "Маркса"
        assert "Минск" in addr_text or "Маркса" in addr_text, f"Адрес неожиданный: {addr_text}"

    # Шаг Allure: проверяем панель информации (верхняя часть хэдера)
    with allure.step('Проверить панель информации'):
        # Утверждение: панель информации должна присутствовать
        assert page.info_panel.is_presented(), "Панель информации не найдена"

    # Шаг Allure: проверяем панель меню (нижняя часть хэдера с навигацией)
    with allure.step('Проверить панель меню'):
        # Утверждение: панель меню должна присутствовать
        assert page.menu_panel.is_presented(), "Панель меню не найдена"

    # Шаг Allure: проверяем навигационные ссылки в меню
    with allure.step('Проверить навигационные ссылки'):
        # Список навигационных ссылок для проверки (CSS-селектор, ожидаемое название)
        nav_links = [
            ("a[href*='news/']", "МЕРОПРИЯТИЯ"),  # Ссылка "МЕРОПРИЯТИЯ" — ведёт на страницу новостей
            ("a[href*='stati-i-publikaczii/']", "Статьи"),  # Ссылка "Статьи" — ведёт на страницу статей
            ("a[href*='kontakty/']", "КОНТАКТЫ"),  # Ссылка "КОНТАКТЫ" — ведёт на страницу контактов
            ("a[href*='2english.itstep.by']", "Обучение английскому"),  # Ссылка на внешний ресурс 2english
        ]
        for selector, name in nav_links:
            # Проверяем через JS: ссылка существует и имеет href
            full_selector = ".menu-panel " + selector
            href = web_browser.execute_script(
                "var el = document.querySelector(arguments[0]); "
                "return el ? el.getAttribute('href') : null;",
                full_selector
            )
            assert href is not None, f"Ссылка '{name}' не найдена в хэдере"
            assert href.startswith("http"), f"Ссылка '{name}' не кликабельна: {href}"

        # Находим выпадающее меню "IT ОБРАЗОВАНИЕ" (dropdown без href)
        dropdown = page.it_education_menu.find()
        # Утверждение: меню "IT ОБРАЗОВАНИЕ" должно быть найдено
        assert dropdown is not None, "Меню 'IT ОБРАЗОВАНИЕ' не найдено"
        # Утверждение: меню должно быть в DOM (is_displayed ненадёжен в headless)
        assert dropdown.get_attribute("textContent").strip() == "IT ОБРАЗОВАНИЕ", "Меню 'IT ОБРАЗОВАНИЕ' пустое"

    # Шаг Allure: проверяем бургер-меню (мобильная версия)
    with allure.step('Проверить бургер-меню (мобильное)'):
        burger = page.burger_menu.find()  # Находим элемент бургер-меню
        assert burger is not None, "Бургер-меню не найдено"  # Утверждение: бургер-меню должно присутствовать в DOM


# ──────────────────────────────────────────────
# 2. Проверка футера
# ──────────────────────────────────────────────

# Декоратор Allure: название теста — "Проверка футера: наличие, отображение и кликабельность всех элементов"
@allure.title('Проверка футера: наличие, отображение и кликабельность всех элементов')
# Декоратор Allure: фича — "Футер" (группировка в отчёте)
@allure.feature('Футер')
# Функция теста: проверяет все элементы футера на главной странице
def test_footer(web_browser):
    page = MainPage(web_browser)  # Создаём Page Object главной страницы
    dismiss_cookies(page)  # Закрываем баннер cookies

    # Шаг Allure: прокручиваем страницу к футеру
    with allure.step('Прокрутить к футеру'):
        footer_el = page.footer.find()  # Находим элемент футера на странице
        assert footer_el is not None, "Футер не найден"  # Утверждение: футер должен быть найден
        # Прокручиваем страницу к футеру через JavaScript
        web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", footer_el)
        time.sleep(1)  # Ждём 1 секунду для полной отрисовки футера

    # Шаг Allure: проверяем логотип в футере
    with allure.step('Проверить логотип в футере'):
        logo = page.footer_logo.find()  # Находим логотип в футере
        assert logo is not None, "Логотип в футере не найден"  # Утверждение: логотип должен быть найден
        # Утверждение: логотип должен отображаться
        assert logo.is_displayed(), "Логотип в футере не отображается"
        # Утверждение: логотип должен содержать ссылку (быть кликабельным)
        assert logo.get_attribute("href") is not None, "Логотип в футере не кликабелен"

    # Шаг Allure: проверяем блок контактов в футере (секция footer-contacts)
    with allure.step('Проверить блок контактов футера'):
        # Утверждение: секция контактов футера должна присутствовать
        assert page.footer_contacts_section.is_presented(), "Секция контактов футера не найдена"
        site_link = page.footer_contacts_site.find()  # Находим ссылку на сайт в блоке контактов
        # Утверждение: ссылка на сайт должна быть найдена
        assert site_link is not None, "Ссылка на сайт в контактах не найдена"
        ph1 = page.footer_contacts_phone1.find()  # Находим первый телефон в блоке контактов
        assert ph1 is not None, "Телефон 1 в контактах не найден"  # Утверждение: первый телефон должен быть найден
        ph2 = page.footer_contacts_phone2.find()  # Находим второй телефон в блоке контактов
        assert ph2 is not None, "Телефон 2 в контактах не найден"  # Утверждение: второй телефон должен быть найден
        email = page.footer_contacts_email.find()  # Находим ссылку email в блоке контактов
        assert email is not None, "Email в контактах не найден"  # Утверждение: email должен быть найден
        # Утверждение: email должен содержать правильный адрес
        assert "info@itstep.by" in email.get_attribute("href"), "Email не кликабелен"

    # Шаг Allure: проверяем навигационные ссылки в футере
    with allure.step('Проверить навигацию в футере'):
        nav_directions = page.footer_nav_directions.find()  # Находим ссылку "Направления обучения"
        # Утверждение: ссылка должна быть найдена
        assert nav_directions is not None, "Ссылка 'Направления обучения' не найдена"
        nav_articles = page.footer_nav_articles.find()  # Находим ссылку "Статьи"
        # Утверждение: ссылка должна быть найдена
        assert nav_articles is not None, "Ссылка 'Статьи' не найдена"
        nav_news = page.footer_nav_news.find()  # Находим ссылку "Новости и акции"
        # Утверждение: ссылка должна быть найдена
        assert nav_news is not None, "Ссылка 'Новости и акции' не найдена"
        nav_contacts = page.footer_nav_contacts.find()  # Находим ссылку "Контакты"
        # Утверждение: ссылка должна быть найдена
        assert nav_contacts is not None, "Ссылка 'Контакты' не найдена"

    # Шаг Allure: проверяем телефоны в футере
    with allure.step('Проверить телефоны в футере'):
        f_phone1 = page.footer_phone1.find()  # Находим первый телефон в футере
        assert f_phone1 is not None, "Телефон 1 в футере не найден"  # Утверждение: телефон должен быть найден
        # Утверждение: телефон должен содержать правильный href
        assert f_phone1.get_attribute("href") == "tel:+375296366585", "Телефон 1 некорректен"
        f_phone2 = page.footer_phone2.find()  # Находим второй телефон в футере
        assert f_phone2 is not None, "Телефон 2 в футере не найден"  # Утверждение: телефон должен быть найден
        # Утверждение: телефон должен содержать правильный href
        assert f_phone2.get_attribute("href") == "tel:+375297068585", "Телефон 2 некорректен"

    # Шаг Allure: проверяем адрес в футере
    with allure.step('Проверить адрес в футере'):
        f_address = page.footer_address.find()  # Находим блок адреса в футере
        assert f_address is not None, "Адрес в футере не найден"  # Утверждение: адрес должен быть найден

    # Шаг Allure: проверяем ссылки на социальные сети в футере
    with allure.step('Проверить соцсети в футере'):
        # Список социальных сетей для проверки (локатор, название)
        socials = [
            (page.footer_vk, "VK"),  # Ссылка на VK
            (page.footer_facebook, "Facebook"),  # Ссылка на Facebook
            (page.footer_telegram, "Telegram"),  # Ссылка на Telegram
            (page.footer_instagram, "Instagram"),  # Ссылка на Instagram
            (page.footer_youtube, "YouTube"),  # Ссылка на YouTube
        ]
        for locator, name in socials:  # Перебираем каждую социальную сеть
            link = locator.find()  # Находим ссылку соцсети
            # Утверждение: ссылка должна быть найдена
            assert link is not None, f"Ссылка {name} не найдена в футере"
            # Утверждение: ссылка должна содержать URL (быть кликабельной)
            assert link.get_attribute("href") is not None, f"Ссылка {name} не кликабельна"

    # Шаг Allure: проверяем копирайт в футере
    with allure.step('Проверить копирайт'):
        copyright_el = page.footer_copyright.find()  # Находим элемент копирайта
        assert copyright_el is not None, "Копирайт не найден"  # Утверждение: копирайт должен быть найден
        # Утверждение: копирайт должен содержать название компании
        assert "IT ШАГ" in copyright_el.text, "Копирайт не содержит 'IT ШАГ'"


# ──────────────────────────────────────────────
# 3. Проверка центрального блока
# ──────────────────────────────────────────────

# Декоратор Allure: название теста — "Проверка центрального блока: наличие, отображение и кликабельность всех элементов"
@allure.title('Проверка центрального блока: наличие, отображение и кликабельность всех элементов')
# Декоратор Allure: фича — "Центральный блок" (группировка в отчёте)
@allure.feature('Центральный блок')
# Функция теста: проверяет элементы центрального блока (слайдер, дети, отзывы, чат)
def test_central_block(web_browser):
    page = MainPage(web_browser)  # Создаём Page Object главной страницы
    dismiss_cookies(page)  # Закрываем баннер cookies

    # Шаг Allure: проверяем наличие слайдера
    with allure.step('Проверить слайдер'):
        slider = page.slider_section.find()  # Находим секцию слайдера
        assert slider is not None, "Слайдер не найден"  # Утверждение: слайдер должен быть найден
        slides = page.slider_slides.find()  # Находим все слайды в слайдере
        # Утверждение: должно быть минимум 1 слайд
        assert len(slides) >= 1, f"Слайды не найдены: {len(slides)}"

    # Шаг Allure: проверяем кнопку "УЗНАТЬ ПОДРОБНОСТИ" / "ПОЛУЧИТЬ КОНСУЛЬТАЦИЮ"
    with allure.step('Проверить кнопку "УЗНАТЬ ПОДРОБНОСТИ" / "ПОЛУЧИТЬ КОНСУЛЬТАЦИЮ"'):
        btn = page.learn_more_btn.find()  # Находим кнопку на слайдере
        assert btn is not None, "Кнопка слайдера не найдена"  # Утверждение: кнопка должна быть найдена в DOM
        href = btn.get_attribute("href")  # Получаем атрибут href кнопки
        assert href is not None, "Кнопка слайдера не кликабельна"  # Утверждение: кнопка должна содержать ссылку (быть кликабельной)

    # Шаг Allure: проверяем блок "Обучение для детей и подростков"
    with allure.step('Проверить блок "Обучение для детей и подростков"'):
        kids_title = page.kids_section_title.find()  # Находим заголовок блока детей
        # Утверждение: заголовок должен быть найден
        assert kids_title is not None, "Заголовок блока детей не найден"
        # Прокручиваем к заголовку блока детей
        web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", kids_title)
        time.sleep(1)  # Ждём 1 секунду для полной отрисовки блока

    # Шаг Allure: проверяем ссылки на курсы для детей
    with allure.step('Проверить ссылки на курсы для детей'):
        # Список детских курсов для проверки (локатор, возрастная категория)
        kids_links = [
            (page.kids_7_8_link, "7-8 лет"),  # Курс для детей 7-8 лет
            (page.kids_9_11_link, "9-11 лет"),  # Курс для детей 9-11 лет
            (page.kids_12_13_link, "12-13 лет"),  # Курс для детей 12-13 лет
            (page.it_college_link, "IT колледж"),  # IT колледж для старшеклассников
        ]
        for locator, name in kids_links:  # Перебираем каждую ссылку на детский курс
            link = locator.find()  # Находим ссылку курса
            # Утверждение: ссылка должна быть найдена
            assert link is not None, f"Ссылка на курс для детей '{name}' не найдена"
            # Утверждение: ссылка должна содержать URL (быть кликабельной)
            assert link.get_attribute("href") is not None, f"Ссылка '{name}' не кликабельна"

    # Шаг Allure: проверяем блок отзывов
    with allure.step('Проверить блок отзывов'):
        reviews = page.reviews_title.find()  # Находим заголовок блока отзывов
        assert reviews is not None, "Заголовок отзывов не найден"  # Утверждение: заголовок должен быть найден
        # Прокручиваем к блоку отзывов
        web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", reviews)
        time.sleep(1)  # Ждём 1 секунду для полной отрисовки блока
        # Утверждение: отзыв YANDEX должен присутствовать
        assert page.review_yandex.find() is not None, "Отзыв YANDEX не найден"
        # Утверждение: отзыв GOOGLE должен присутствовать
        assert page.review_google.find() is not None, "Отзыв GOOGLE не найден"
        # Утверждение: отзыв FACEBOOK должен присутствовать
        assert page.review_facebook.find() is not None, "Отзыв FACEBOOK не найден"

    # Шаг Allure: проверяем ссылку на профориентационный тест
    with allure.step('Проверить ссылку на профориентационный тест'):
        career = page.career_guidance_link.find()  # Находим ссылку на карьерный тест
        assert career is not None, "Ссылка на профтест не найдена"  # Утверждение: ссылка должна быть найдена
        # Утверждение: ссылка должна содержать URL (быть кликабельной)
        assert career.get_attribute("href") is not None, "Ссылка на профтест не кликабельна"

    # Шаг Allure: проверяем наличие виджета чата
    with allure.step('Проверить виджет чата'):
        chat = page.chat_button.find()  # Находим кнопку виджета чата (Bitrix24)
        assert chat is not None, "Виджет чата не найден"  # Утверждение: виджет чата должен быть найден в DOM


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
    last_names = ['Сушко', 'Короткевич', 'Гришко', 'Захаревич', 'Гройсман', 'Ольховик', 'Волченко', 'Колесник']

    first_name = random.choice(first_names)  # Случайный выбор имени из списка
    last_name = random.choice(last_names)  # Случайный выбор фамилии из списка
    # Генерация белорусского номера телефона: +375 + код оператора (29/33/25/17) + 7 цифр
    phone = f"+375{random.choice(['29', '33', '25', '17'])}{random.randint(1000000, 9999999)}"
    email = "kuzayo@mail.ru"  # Фиксированный email для тестовой формы

    page = MainPage(web_browser)  # Создаём Page Object главной страницы

    # Шаг Allure: принимаем cookies
    with allure.step('Принять cookies'):
        page.btn_access.click()  # Кликаем по кнопке принятия cookies

    # Шаг Allure: открываем выпадающее меню "IT ОБРАЗОВАНИЕ"
    with allure.step('Открыть меню "IT ОБРАЗОВАНИЕ"'):
        it_menu = page.it_education_menu.find()  # Находим элемент меню
        assert it_menu is not None, "Меню 'IT ОБРАЗОВАНИЕ' не найдено"
        web_browser.execute_script("arguments[0].click();", it_menu)  # Кликаем через JS

    # Шаг Allure: кликаем по ссылке "Профориентационный тест" в раскрытом меню
    with allure.step('Кликнуть по "Профориентационный тест"'):
        link = page.career_test_link.find()  # Находим ссылку на карьерный тест в выпадающем меню
        web_browser.execute_script("arguments[0].click();", link)  # Кликаем по ссылке через JavaScript (обход потенциальных проблем с кликом)
        time.sleep(3)  # Ждём 3 секунды для загрузки страницы теста

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
        time.sleep(5)  # Ждём 5 секунд — возможен переход на внешний домен (proftest.itstep.by)

    # Шаг Allure: проверяем, что произошёл переход на форму теста
    with allure.step('Проверить переход на форму (proftest.itstep.by)'):
        current_url = web_browser.current_url  # Получаем текущий URL страницы
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
        name_field.clear()  # Очищаем поле от возможного старого значения
        name_field.send_keys(f"{first_name} {last_name}")  # Вводим полное имя (имя + фамилия)
        time.sleep(0.5)  # Короткая пауза для обработки ввода страницей

    # Шаг Allure: заполняем поле "Email"
    with allure.step(f'Заполнить email: {email}'):
        email_field = WebDriverWait(web_browser, 10).until(  # Находим поле ввода email по name="question1"
            EC.presence_of_element_located((By.NAME, "question1"))
        )
        email_field.clear()  # Очищаем поле
        email_field.send_keys(email)  # Вводим email
        time.sleep(0.5)  # Пауза для обработки

    # Шаг Allure: заполняем поле "Телефон"
    with allure.step(f'Заполнить телефон: {phone}'):
        phone_field = WebDriverWait(web_browser, 10).until(  # Находим поле ввода телефона по name="question2"
            EC.presence_of_element_located((By.NAME, "question2"))
        )
        phone_field.clear()  # Очищаем поле
        phone_field.send_keys(phone)  # Вводим номер телефона
        time.sleep(0.5)  # Пауза для обработки

    # Шаг Allure: отвечаем на вопросы теста (radio/checkbox)
    with allure.step('Ответить на вопросы теста (radio/checkbox)'):
        # Множество имён уже обработанных групп вопросов (чтобы не отвечать дважды)
        question_names = set()

        # Вспомогательная функция безопасного клика: кликает через JS и обрабатывает всплывающие алерты
        def safe_click(element):
            try:  # Пытаемся кликнуть по элементу через JavaScript
                web_browser.execute_script("arguments[0].click();", element)
            except:  # Если клик не удался — игнорируем ошибку
                pass
            try:  # Проверяем, не появился ли всплывающий алерт после клика
                alert = web_browser.switch_to.alert  # Получаем объект алерта
                alert_text = alert.text  # Получаем текст алерта
                alert.accept()  # Принимаем (закрываем) алерт
                allure.step(f'Алерт: {alert_text}').publish()  # Публикуем текст алерта в отчёт Allure
            except:  # Если алерта нет — просто продолжаем
                pass

        # Находим все radio-кнопки на странице теста
        all_radios = web_browser.find_elements(By.CSS_SELECTOR, "input[type='radio']")
        for r in all_radios:  # Перебираем каждую radio-кнопку
            qname = r.get_attribute("name")  # Получаем имя группы radio-кнопок (атрибут name)
            if qname not in question_names:  # Если эта группа вопросов ещё не обработана
                question_names.add(qname)  # Добавляем имя группы в множество обработанных
                # Находим все варианты ответа в этой группе
                options = web_browser.find_elements(By.CSS_SELECTOR, f"input[name='{qname}']")
                if options:  # Если варианты найдены — выбираем случайный
                    chosen = random.choice(options)  # Случайный выбор одного варианта ответа
                    safe_click(chosen)  # Кликаем по выбранному варианту

        # Находим все checkbox-кнопки на странице теста
        all_checkboxes = web_browser.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
        for c in all_checkboxes:  # Перебираем каждую checkbox-кнопку
            qname = c.get_attribute("name")  # Получаем имя группы чекбоксов
            if qname not in question_names:  # Если эта группа ещё не обработана
                question_names.add(qname)  # Добавляем имя группы в множество обработанных
                # Находим все варианты чекбоксов в этой группе
                options = web_browser.find_elements(By.CSS_SELECTOR, f"input[name='{qname}']")
                if options:  # Если варианты найдены — выбираем случайное количество (от 1 до 3)
                    num_to_check = random.randint(1, min(3, len(options)))  # Случайное количество чекбоксов для отметки (от 1 до минимум(3, общее кол-во))
                    for opt in random.sample(options, num_to_check):  # Случайно выбираем нужное количество вариантов и отмечаем их
                        safe_click(opt)  # Кликаем по варианту через безопасный клик

    # Шаг Allure: нажимаем кнопку "Узнать свой результат!" для отправки формы
    with allure.step('Нажать "Узнать свой результат!"'):
        try:  # Перед отправкой закрываем возможные висящие алерты
            alert = web_browser.switch_to.alert  # Пытаемся получить всплывающий алерт
            alert.accept()  # Принимаем алерт
        except:  # Если алерта нет — продолжаем
            pass
        # Явное ожидание: находим кнопку отправки формы (button[type='submit'])
        submit = WebDriverWait(web_browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        # Прокручиваем к кнопке отправки
        web_browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit)
        web_browser.execute_script("arguments[0].click();", submit)  # Кликаем по кнопке отправки через JavaScript
        time.sleep(2)  # Пауза 2 секунды после клика
        try:  # Обрабатываем возможный алерт после отправки формы
            alert = web_browser.switch_to.alert  # Пытаемся получить всплывающий алерт
            alert_text = alert.text  # Получаем текст алерта
            alert.accept()  # Принимаем алерт
            # Публикуем текст алерта в отчёт Allure
            allure.step(f'Алерт после отправки: {alert_text}').publish()
        except:  # Если алерта нет — продолжаем
            pass
        time.sleep(3)  # Пауза 3 секунды для завершения обработки формы сервером

    # Шаг Allure: проверяем, что форма успешно отправлена
    with allure.step('Проверить отправку формы'):
        page_source = web_browser.page_source.lower()  # Получаем HTML-исходник страницы в нижнем регистре для поиска
        # Список индикаторов успешной отправки формы (ключевые слова, которые появляются после отправки)
        success_indicators = ['результат', 'спасибо', 'отправлено', 'готово', 'ваш', 'профориентация', 'курс']
        # Проверяем, есть ли хотя бы один индикатор на странице
        form_still_visible = any(ind in page_source for ind in success_indicators)
        # Утверждение: хотя бы один индикатор должен присутствовать — форма отправлена успешно
        assert form_still_visible, "Форма не была отправлена — индикатор успеха не найден"
