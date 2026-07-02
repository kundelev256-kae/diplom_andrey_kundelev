# Импорт базового класса WebPage из модуля base_page — родительский класс для всех страниц
from page.base_page import WebPage
# Импорт модуля os для работы с переменными окружения (получение URL из env)
import os
# Импорт классов WebElement и ManyWebElements — кастомные элементы страницы для работы с локаторами
from page.elements import WebElement, ManyWebElements
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

    # === Cookies ===

    # Кнопка принятия куки (cookies-уведомление) — ищется по ID кнопки
    btn_access = WebElement(id="button-accept-cookies")

    # === Header ===

    # Логотип сайта — ищется по CSS-селектору .logo a (ссылка внутри блока логотипа)
    logo = WebElement(css_selector=".logo a")
    # Блок телефонов — ищется по CSS-селектору .phones
    phones_block = WebElement(css_selector=".phones")
    # Все ссылки телефонов в блоке контактов — ManyWebElements для получения списка всех номеров
    phone_links = ManyWebElements(css_selector=".info-panel .phone a[href^='tel:']")
    # Блок адреса компании — ищется по CSS-селектору .address
    address_block = WebElement(css_selector=".address")
    # Текст адреса — ищется по CSS-селектору .address .location
    address_text = WebElement(css_selector=".address .location")
    # Верхняя панель информации (логотип, телефоны, адрес) — ищется по CSS-селектору .info-panel
    info_panel = WebElement(css_selector=".info-panel")
    # Панель меню (навигация) — ищется по CSS-селектору .menu-panel
    menu_panel = WebElement(css_selector=".menu-panel")

    # === Header navigation links ===

    # Выпадающее меню "IT ОБРАЗОВАНИЕ" — dropdown без href, ищется по тексту в панели меню
    it_education_menu = WebElement(xpath="//div[contains(@class,'menu-panel')]//div[@class='menu']//a[contains(text(), 'IT ОБРАЗОВАНИЕ')]")
    # Ссылка "МЕРОПРИЯТИЯ" (Новости) — ведёт на страницу новостей, ищется по href в панели меню
    nav_news = WebElement(xpath="//div[contains(@class,'menu-panel')]//a[@href='https://itstep.by/news/']")
    # Ссылка "Статьи" — ведёт на страницу статей, ищется по href в панели меню
    nav_articles = WebElement(xpath="//div[contains(@class,'menu-panel')]//a[@href='https://itstep.by/stati-i-publikaczii/']")
    # Ссылка "КОНТАКТЫ" — ведёт на страницу контактов, ищется по href в панели меню
    nav_contacts = WebElement(xpath="//div[contains(@class,'menu-panel')]//a[@href='https://itstep.by/kontakty/']")
    # Ссылка "Обучение английскому языку" — ведёт на внешний ресурс 2english.itstep.by
    nav_english = WebElement(xpath="//div[contains(@class,'menu-panel')]//a[@href='https://2english.itstep.by/']")
    # Ссылка "Вакансии" — ведёт на страницу карьеры, ищется по части href в панели меню
    nav_vacancies = WebElement(xpath="//div[contains(@class,'menu-panel')]//a[contains(@href, 'careers')]")
    # Бургер-меню (мобильная версия навигации) — ищется по CSS-селектору .burger-menu
    burger_menu = WebElement(css_selector=".burger-menu")

    # === Header IT Education sub-menu courses (курсы в выпадающем меню "IT ОБРАЗОВАНИЕ") ===

    # Ссылка на курс тестирования QA — ищется по части URL в href
    qa_course_link = WebElement(xpath="//a[contains(@href, 'testirovanie-po-qa')]")
    # Ссылка на курс разработки на Python — ищется по части URL в href
    python_course_link = WebElement(xpath="//a[contains(@href, 'razrabotka-po-na-python')]")
    # Ссылка на курс разработки на Java — ищется по части URL в href
    java_course_link = WebElement(xpath="//a[contains(@href, 'razrabotka-po-na-java')]")
    # Ссылка на курс UX/UI дизайна — ищется по части URL в href
    ux_ui_course_link = WebElement(xpath="//a[contains(@href, 'ux-ui-dizajn')]")
    # Ссылка на курс анализа данных (Data Analyst) — ищется по части URL в href
    data_analyst_link = WebElement(xpath="//a[contains(@href, 'analitik-dannyh-v-it-data-analyst')]")
    # Ссылка на курс управления проектами (PM) — ищется по части URL в href
    pm_course_link = WebElement(xpath="//a[contains(@href, 'upravlenie-proektami-v-it-pm')]")
    # Ссылка на курс DevOps Engineer — ищется по части URL в href
    devops_link = WebElement(xpath="//a[contains(@href, 'devops-engineer')]")
    # Ссылка на курс IT Start (введение в IT) — ищется по части URL в href
    it_start_link = WebElement(xpath="//a[contains(@href, 'it-start/')]")
    # Ссылка на тест по профориентации (career guidance test) — ищется по части URL в href
    career_test_link = WebElement(xpath="//a[contains(@href, 'career-guidance-test')]")

    # === Kids course links in mega-menu (ссылки на детские курсы в мега-меню) ===

    # Ссылка на курс для детей 7-8 лет — ищется по части URL
    kids_7_8_link = WebElement(xpath="//a[contains(@href, 'kursy-dlya-detej-7-8-let')]")
    # Ссылка на курс для детей 9-11 лет — ищется по части URL
    kids_9_11_link = WebElement(xpath="//a[contains(@href, 'kursy-dlya-detej-9-11-let')]")
    # Ссылка на курс для детей 12-13 лет — ищется по части URL
    kids_12_13_link = WebElement(xpath="//a[contains(@href, 'kursy-dlya-detej-12-13-let')]")
    # Ссылка на IT-колледж — ищется по домену в href
    it_college_link = WebElement(xpath="//a[contains(@href, 'it-college.itstep.by')]")

    # === Central block (центральный блок между хэдером и футером) ===

    # Секция слайдера — ищется по CSS-селектору section.block-1
    slider_section = WebElement(css_selector="section.block-1")
    # Все слайды в слайдере — ManyWebElements для получения списка всех слайдов
    slider_slides = ManyWebElements(css_selector=".slide-container")
    # Кнопка "УЗНАТЬ ПОДРОБНОСТИ" / "ПОЛУЧИТЬ КОНСУЛЬТАЦИЮ" на слайдерах — ищется по комбинации CSS-классов
    learn_more_btn = WebElement(xpath="//a[contains(@class, 'btn-info') and contains(@class, 'btn-styled')]")

    # Заголовок блока "Обучение для детей и подростков" — ищется по тексту в теге h1
    kids_section_title = WebElement(xpath="//h1[contains(text(), 'ДЕТЕЙ И ПОДРОСТКОВ')]")

    # === Reviews section (блок отзывов) ===

    # Заголовок блока отзывов — ищется по тексту "ОТЗЫВЫ" в div с классом title
    reviews_title = WebElement(xpath="//div[contains(@class,'title') and contains(text(),'ОТЗЫВЫ')]")
    # Все карточки отзывов — ищется по CSS-селектору .slide-container (переиспользуется от слайдера)
    review_cards = WebElement(css_selector=".slide-container")
    # Отзыв YANDEX — ищется по тексту "YANDEX" в div с классом slide-title
    review_yandex = WebElement(xpath="//div[contains(@class,'slide-title') and text()='YANDEX']")
    # Отзыв GOOGLE — ищется по тексту "GOOGLE" в div с классом slide-title
    review_google = WebElement(xpath="//div[contains(@class,'slide-title') and text()='GOOGLE']")
    # Отзыв FACEBOOK — ищется по тексту "FACEBOOK" в div с классом slide-title
    review_facebook = WebElement(xpath="//div[contains(@class,'slide-title') and text()='FACEBOOK']")

    # Ссылка на профориентационный тест — ищется по части URL в href
    career_guidance_link = WebElement(xpath="//a[contains(@href, 'career-guidance-test')]")

    # === Chat widget (виджет чата Bitrix24) ===

    # Кнопка всплывающего виджета чата (Bitrix24) — ищется по классу виджета
    chat_button = WebElement(xpath="//*[contains(@class,'b24-widget-button')]")
    # Кнопка формы обратной связи CRM (Bitrix24) — отдельная кнопка от основного чата
    feedback_button = WebElement(xpath="//a[contains(@class,'b24-widget-button-crmform')]")

    # === Footer (футер) ===

    # Блок футера — ищется по CSS-селектору footer.footer
    footer = WebElement(css_selector="footer.footer")
    # Логотип в футере — ищется внутри футера по CSS-селектору .logo
    footer_logo = WebElement(css_selector="footer.footer .logo")
    # Блок копирайта — ищется по CSS-селектору .footer-copyright
    footer_copyright = WebElement(css_selector=".footer-copyright")

    # === Footer navigation (навигация в футере) ===

    # Заголовок "НАВИГАЦИЯ" в футере — ищется по тексту в div с классом h4 title
    footer_nav_title = WebElement(xpath="//footer//div[@class='h4 title' and text()='НАВИГАЦИЯ']")
    # Ссылка "Направления обучения" — ведёт на главную страницу, ищется в футере по href
    footer_nav_directions = WebElement(xpath="//footer//a[@href='https://itstep.by/']")
    # Ссылка "Статьи" — ведёт на страницу статей, ищется в футере по href
    footer_nav_articles = WebElement(xpath="//footer//a[@href='https://itstep.by/stati-i-publikaczii/']")
    # Ссылка "Новости и акции" — ведёт на страницу новостей, ищется в футере по href
    footer_nav_news = WebElement(xpath="//footer//a[@href='https://itstep.by/news/']")
    # Ссылка "Контакты" — ведёт на страницу контактов, ищется в футере по href
    footer_nav_contacts = WebElement(xpath="//footer//a[@href='https://itstep.by/kontakty/']")

    # === Footer contacts (контакты в футере) ===

    # Телефон 1 в футере (+375 29 636 65 85) — ищется в футере по href с протоколом tel:
    footer_phone1 = WebElement(xpath="//footer//a[@href='tel:+375296366585']")
    # Телефон 2 в футере (+375 29 706 85 85) — ищется в футере по href с протоколом tel:
    footer_phone2 = WebElement(xpath="//footer//a[@href='tel:+375297068585']")
    # Адрес компании в футере — ищется в футере по CSS-классу address
    footer_address = WebElement(xpath="//footer//div[contains(@class, 'address')]")
    # Ссылка на вакансии в футере — ведёт на страницу карьеры
    footer_vacancies = WebElement(xpath="//footer//a[@href='https://itstep.by/careers/']")

    # === Footer socials (ссылки на социальные сети в футере) ===

    # Ссылка на VK — ищется в футере по href
    footer_vk = WebElement(xpath="//footer//a[@href='https://vk.com/itstepby']")
    # Ссылка на Facebook — ищется в футере по href
    footer_facebook = WebElement(xpath="//footer//a[@href='https://www.facebook.com/itstepby']")
    # Ссылка на Telegram — ищется в футере по href
    footer_telegram = WebElement(xpath="//footer//a[@href='https://t.me/itstepminsk']")
    # Ссылка на Instagram — ищется в футере по href
    footer_instagram = WebElement(xpath="//footer//a[@href='https://www.instagram.com/itstep.by']")
    # Ссылка на YouTube — ищется в футере по href
    footer_youtube = WebElement(xpath="//footer//a[@href='https://www.youtube.com/@itstep_by']")

    # === Footer contacts section (секция контактов над футером) ===

    # Секция контактов футера — ищется по CSS-селектору section.footer-contacts
    footer_contacts_section = WebElement(css_selector="section.footer-contacts")
    # Ссылка на сайт в секции контактов — ведёт на главную страницу
    footer_contacts_site = WebElement(xpath="//section[@class='footer-contacts']//a[@href='https://itstep.by/']")
    # Телефон 1 в секции контактов — ищется по href с протоколом tel:
    footer_contacts_phone1 = WebElement(xpath="//section[@class='footer-contacts']//a[@href='tel:+375296366585']")
    # Телефон 2 в секции контактов — ищется по href с протоколом tel:
    footer_contacts_phone2 = WebElement(xpath="//section[@class='footer-contacts']//a[@href='tel:+375297068585']")
    # Email в секции контактов — ищется по href с протоколом mailto:
    footer_contacts_email = WebElement(xpath="//section[@class='footer-contacts']//a[@href='mailto:info@itstep.by']")
