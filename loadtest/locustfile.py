from locust import HttpUser, task, between, events # Импорт основных компонентов Locust: HttpUser — класс пользователя для HTTP-запросов, task — декоратор для определения задач, between — функция задержки между запросами, events — система событий Locust
import json # Импорт модуля для работы с JSON-файлами (сериализация результатов)
import time # Импорт модуля для работы со временем (замер длительности теста)
import os # Импорт модуля для работы с файловой системой (получение пути к файлу)

RESULTS_FILE = "loadtest_results.json" # Имя файла для сохранения результатов тестирования


class ItStepUser(HttpUser): # Определение класса пользователя, наследующего HttpUser — описывает поведение виртуального пользователя
    wait_time = between(1, 3) # Задержка между запросами от 1 до 3 секунд (имитация реального поведения)
    host = "https://itstep.by" # Базовый URL целевого сервера для тестирования

    def on_start(self): # Метод, вызываемый при старте каждого виртуального пользователя (аналог открытия браузера)
        self.client.headers.update({ # Установка заголовков HTTP-запросов для имитации реального браузера
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36", # Идентификация клиента как обычного Chrome-браузера
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8", # Указание принимаемых типов контента
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7", # Приоритет языков: русский, затем английский
            "Accept-Encoding": "gzip, deflate, br", # Поддержка сжатия ответов для уменьшения размера передачи
            "Connection": "keep-alive", # Поддержание постоянного соединения с сервером
            "Upgrade-Insecure-Requests": "1", # Запрос обновления незащищённых соединений на HTTPS
            "Sec-Fetch-Dest": "document", # Заголовок безопасности: тип ресурса — документ
            "Sec-Fetch-Mode": "navigate", # Режим навигации (переход по ссылке, не AJAX)
            "Sec-Fetch-Site": "none", # Источник запроса — прямой переход (не с другого сайта)
            "Sec-Fetch-User": "?1", # Указание, что запрос инициирован пользователем
            "Cache-Control": "max-age=0", # Отключение кэширования — всегда запрашивать свежую версию
        })

    @task(5) # Декоратор задачи с весом 5 (выполняется в 5 раз чаще задач с весом 1)
    def main_page(self): # Задача: запрос главной страницы сайта
        self.client.get("/", name="Главная страница") # GET-запрос корневого URL с меткой для отчёта

    @task(3) # Вес 3 — третья по частоте задача
    def vacancies_page(self): # Задача: запрос страницы с вакансиями
        self.client.get("/careers/", name="Вакансии") # GET-запрос раздела карьеры

    @task(3) # Вес 3
    def contacts_page(self): # Задача: запрос страницы контактов
        self.client.get("/kontakty/", name="Контакты") # GET-запрос контактной информации

    @task(2) # Вес 2
    def news_page(self): # Задача: запрос страницы новостей
        self.client.get("/news/", name="Новости") # GET-запрос раздела новостей

    @task(2) # Вес 2
    def articles_page(self): # Задача: запрос страницы со статьями
        self.client.get("/stati-i-publikaczii/", name="Статьи") # GET-запрос раздела публикаций

    @task(2) # Вес 2
    def qa_course(self): # Задача: запрос страницы курса QA-тестирования
        self.client.get("/testirovanie-po-qa/", name="Курс QA") # GET-запрос страницы курса по тестированию

    @task(1) # Вес 1 — наименее частая задача
    def python_course(self): # Задача: запрос страницы курса Python
        self.client.get("/razrabotka-po-na-python/", name="Курс Python") # GET-запрос страницы курса Python-разработки

    @task(1) # Вес 1
    def java_course(self): # Задача: запрос страницы курса Java
        self.client.get("/razrabotka-po-na-java/", name="Курс Java") # GET-запрос страницы курса Java-разработки

    @task(1) # Вес 1
    def ux_ui_course(self): # Задача: запрос страницы курса UX/UI-дизайна
        self.client.get("/ux-ui-dizajn/", name="Курс UX/UI") # GET-запрос страницы курса по дизайну

    @task(1) # Вес 1
    def devops_course(self): # Задача: запрос страницы курса DevOps
        self.client.get("/devops-engineer/", name="Курс DevOps") # GET-запрос страницы курса DevOps-инженера

    @task(1) # Вес 1
    def robots_txt(self): # Задача: запрос файла robots.txt (имитация поискового робота)
        self.client.get("/robots.txt", name="robots.txt") # GET-запрос файла с директивами для поисковиков


results_data = { # Словарь для хранения агрегированных результатов тестирования
    "start_time": None, # Время начала теста (Unix-таймстамп)
    "end_time": None, # Время окончания теста
    "total_requests": 0, # Общее количество выполненных запросов
    "failed_requests": 0, # Количество неудачных запросов (с ошибками)
    "avg_response_time": 0, # Среднее время ответа (мс)
    "rps": 0, # Запросов в секунду
    "min_response_time": 0, # Минимальное время ответа
    "max_response_time": 0, # Максимальное время ответа
    "p50": 0, # 50-й процентиль (медиана) времени ответа
    "p90": 0, # 90-й процентиль времени ответа
    "p95": 0, # 95-й процентиль времени ответа
    "p99": 0, # 99-й процентиль времени ответа
    "status_codes": {}, # Словарь: код статуса HTTP → количество таких ответов
    "errors": [], # Список ошибок, возникших во время теста
}


@events.test_start.add_listener # Регистрация обработчика события начала теста
def on_test_start(environment, **kwargs): # Функция, вызываемая при старте теста
    results_data["start_time"] = time.time() # Сохранение времени начала теста
    results_data["total_requests"] = 0 # Сброс счётчика запросов
    results_data["failed_requests"] = 0 # Сброс счётчика ошибок
    results_data["status_codes"] = {} # Сброс словаря кодов статусов
    results_data["errors"] = [] # Сброс списка ошибок


@events.request.add_listener # Регистрация обработчика каждого HTTP-запроса
def on_request(request_type, name, response_time, response_length, # Параметры запроса: тип (GET/POST), имя, время ответа, размер ответа
               exception, context, start_time, **kwargs): # Исключение (если было), контекст, время начала запроса
    results_data["total_requests"] += 1 # Увеличение счётчика общих запросов на 1

    if response_time: # Проверка, что время ответа существует (не None)
        if results_data["min_response_time"] == 0 or response_time < results_data["min_response_time"]: # Обновление минимального времени, если текущее меньше
            results_data["min_response_time"] = response_time # Запоминание нового минимума
        if response_time > results_data["max_response_time"]: # Обновление максимального времени, если текущее больше
            results_data["max_response_time"] = response_time # Запоминание нового максимума

    if exception: # Если при запросе произошла ошибка
        results_data["failed_requests"] += 1 # Увеличение счётчика неудачных запросов
        results_data["errors"].append({ # Добавление информации об ошибке в список
            "name": name, # Имя запроса (метка)
            "error": str(exception), # Текстовое описание ошибки
            "time": response_time, # Время ответа на момент ошибки
        })


@events.quitting.add_listener # Регистрация обработчика завершения теста (вызывается при остановке)
def on_quit(environment, **kwargs): # Функция, выполняемая при завершении теста
    results_data["end_time"] = time.time() # Фиксация времени окончания теста
    stats = environment.runner.stats # Получение объекта статистики от runner-а Locust

    total_time = results_data["end_time"] - results_data["start_time"] # Вычисление общей длительности теста в секундах
    results_data["rps"] = results_data["total_requests"] / total_time if total_time > 0 else 0 # Расчёт среднего количества запросов в секунду

    try: # Блок обработки ошибок при извлечении статистики (на случай отсутствия данных)
        if stats.total.use_response_time_counts: # Проверка, что статистика по времени ответов доступна
            results_data["p50"] = stats.total.get_response_time_percentile(0.5) # Вычисление 50-го процентиля (медианы)
            results_data["p90"] = stats.total.get_response_time_percentile(0.9) # Вычисление 90-го процентиля
            results_data["p95"] = stats.total.get_response_time_percentile(0.95) # Вычисление 95-го процентиля
            results_data["p99"] = stats.total.get_response_time_percentile(0.99) # Вычисление 99-го процентиля

        results_data["avg_response_time"] = stats.total.get_response_time_mean() # Вычисление среднего времени ответа

        for stat in stats.entries.values(): # Перебор статистики по каждому отдельному эндпоинту
            code = "N/A" # Значение по умолчанию, если код статуса неизвестен
            if hasattr(stat, 'last_request') and stat.last_request and hasattr(stat.last_request, 'metadata') and stat.last_request.metadata: # Проверка наличия метаданных последнего запроса
                code = f"{stat.last_request.metadata.get('response_code', 'N/A')}" # Извлечение HTTP-кода статуса из метаданных
            results_data["status_codes"][code] = results_data["status_codes"].get(code, 0) + stat.num_requests # Увеличение счётчика для данного кода статуса
    except Exception: # Игнорирование любых ошибок при чтении статистики
        pass # Пропуск ошибки — результаты будут частичными, но тест не упадёт

    results_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), RESULTS_FILE) # Формирование полного пути к файлу результатов (рядом со скриптом)
    with open(results_path, "w", encoding="utf-8") as f: # Открытие файла для записи в UTF-8 кодировке
        json.dump(results_data, f, ensure_ascii=False, indent=2) # Сохранение результатов в JSON с красивым форматированием
