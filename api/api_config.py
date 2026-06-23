import os # Импорт модуля os для доступа к переменным окружения


BASE_URL = os.getenv("API_BASE_URL", "https://itstep.by") # Базовый URL API: читается из переменной окружения или используется значение по умолчанию

ENDPOINTS = { # Словарь всех эндпоинтов (путей) API, используемых в тестах
    "main": "/", # Главная страница сайта
    "vacancies": "/careers/", # Страница вакансий и карьеры
    "contacts": "/kontakty/", # Страница контактной информации
    "news": "/news/", # Страница новостей компании
    "articles": "/stati-i-publikaczii/", # Страница статей и публикаций
    "qa_course": "/testirovanie-po-qa/", # Страница курса по тестированию (QA)
    "python_course": "/razrabotka-po-na-python/", # Страница курса по Python-разработке
    "java_course": "/razrabotka-po-na-java/", # Страница курса по Java-разработке
    "ux_ui_course": "/ux-ui-dizajn/", # Страница курса по UX/UI дизайну
    "data_analyst": "/analitik-dannyh-v-it-data-analyst/", # Страница курса по анализу данных (Data Analyst)
    "pm_course": "/upravlenie-proektami-v-it-pm/", # Страница курса по управлению проектами (PM)
    "devops": "/devops-engineer/", # Страница курса по DevOps-инженерии
    "it_start": "/it-start/", # Страница стартовой программы по IT
    "career_test": "/career-guidance-test/", # Тест для определения карьерного направления
    "kids_7_8": "/kursy-dlya-detej-7-8-let/", # Страница курсов для детей 7-8 лет
    "kids_9_11": "/kursy-dlya-detej-9-11-let/", # Страница курсов для детей 9-11 лет
    "kids_12_13": "/kursy-dlya-detej-12-13-let/", # Страница курсов для детей 12-13 лет
    "english": "https://2english.itstep.by/", # Внешний URL платформы изучения английского языка (отдельный домен)
    "robots_txt": "/robots.txt", # Файл robots.txt для проверки корректности SEO-настроек
    "sitemap": "/sitemap.xml", # Файл sitemap.xml для проверки карты сайта
}

HEADERS = { # Словарь HTTP-заголовков, имитирующих запрос из веб-браузера Chrome
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " # Идентификатор клиента:仿-сия Chrome под Windows 10 x64
                  "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36", # Продолжение User-Agent для корректного распознавания сервером
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", # Предпочтительные типы контента: HTML, XHTML, XML с приоритетами
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7", # Предпочтительные языки: русский (приоритет 0.9), затем американский и британский английский
}

TIMEOUT = 15 # Максимальное время ожидания ответа от сервера в секундах для HTTP-запросов
MAX_RESPONSE_TIME = 5 # Максимально допустимое время ответа сервера в секундах для проверки производительности
