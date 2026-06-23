import os


BASE_URL = os.getenv("API_BASE_URL", "https://itstep.by")

ENDPOINTS = {
    "main": "/",
    "vacancies": "/careers/",
    "contacts": "/kontakty/",
    "news": "/news/",
    "articles": "/stati-i-publikaczii/",
    "qa_course": "/testirovanie-po-qa/",
    "python_course": "/razrabotka-po-na-python/",
    "java_course": "/razrabotka-po-na-java/",
    "ux_ui_course": "/ux-ui-dizajn/",
    "data_analyst": "/analitik-dannyh-v-it-data-analyst/",
    "pm_course": "/upravlenie-proektami-v-it-pm/",
    "devops": "/devops-engineer/",
    "it_start": "/it-start/",
    "career_test": "/career-guidance-test/",
    "kids_7_8": "/kursy-dlya-detej-7-8-let/",
    "kids_9_11": "/kursy-dlya-detej-9-11-let/",
    "kids_12_13": "/kursy-dlya-detej-12-13-let/",
    "english": "https://2english.itstep.by/",
    "robots_txt": "/robots.txt",
    "sitemap": "/sitemap.xml",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
}

TIMEOUT = 15
MAX_RESPONSE_TIME = 5
