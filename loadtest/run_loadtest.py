import subprocess # Импорт модуля для запуска внешних процессов (locust как подпроцесс)
import sys # Импорт модуля для работы с системными параметрами (путь к интерпретатору Python)
import os # Импорт модуля для работы с файловой системой (пути, проверка файлов)
import json # Импорт модуля для работы с JSON (не используется напрямую, но может пригодиться)
import time # Импорт модуля для работы со временем (для форматирования даты в отчёте)

RESULTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "loadtest_results.json") # Полный путь к JSON-файлу с результатами (рядом со скриптом)


def run_locust_test(users=10, spawn_rate=2, run_time="30s"): # Функция запуска теста Locust: по умолчанию 10 пользователей, 2 в секунду, 30 секунд
    locustfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "locustfile.py") # Полный путь к файлу с определениями пользователей Locust

    cmd = [ # Формирование командной строки для запуска Locust
        sys.executable, "-m", "locust", # Запуск locust как модуля текущего интерпретатора Python
        "-f", locustfile, # Указание файла с определениями пользователей (locustfile.py)
        "--headless", # Режим без GUI (для запуска в консоли/CI)
        "-u", str(users), # Количество виртуальных пользователей
        "-r", str(spawn_rate), # Скорость появления пользователей (пользователей в секунду)
        "--run-time", run_time, # Продолжительность теста (например, "30s", "1m", "5m")
        "--host", "https://itstep.by", # Целевой хост для тестирования
        "--only-summary", # Выводить только итоговую сводку, без деталей по запросам
        "--csv=loadtest_results", # Сохранение статистики в CSV-файлы (loadtest_results_stats.csv и др.)
    ]

    env = os.environ.copy() # Копирование текущих переменных окружения
    env["PYTHONIOENCODING"] = "utf-8" # Принудительная установка UTF-8 для вывода Python (защита от проблем с кодировкой в Windows)

    process = subprocess.Popen( # Запуск внешнего процесса (locust) с перехватом stdout и stderr
        cmd, # Команда для выполнения
        stdout=subprocess.PIPE, # Перенаправление стандартного вывода в pipe (для чтения)
        stderr=subprocess.PIPE, # Перенаправление.stderr в pipe (для чтения)
        cwd=os.path.dirname(os.path.abspath(__file__)), # Установка рабочей директории — папка со скриптом
        env=env, # Передача модифицированных переменных окружения
    )

    stdout, stderr = process.communicate(timeout=120) # Ожидание завершения процесса с таймаутом 120 секунд; возвращает stdout и stderr
    return stdout.decode("utf-8", errors="replace"), stderr.decode("utf-8", errors="replace"), process.returncode # Декодирование вывода в строки и возврат кода возврата процесса


def get_results(): # Функция чтения агрегированной статистики из CSV-файла, сгенерированного Locust
    stats_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "loadtest_results_stats.csv") # Путь к CSV-файлу со статистикой

    if not os.path.exists(stats_file): # Если файл статистики не существует — тест не создал его
        return None # Возврат None — нет данных

    for encoding in ["utf-8", "utf-8-sig", "cp1251", "latin-1"]: # Попытки чтения файла в разных кодировках (Windows может сохранять в cp1251)
        try:
            with open(stats_file, "r", encoding=encoding) as f: # Открытие файла с текущей кодировкой
                lines = f.readlines() # Чтение всех строк файла
            break # Успешное чтение — выход из цикла
        except (UnicodeDecodeError, UnicodeError): # Если кодировка не подходит — попробовать следующую
            continue
    else: # Цикл завершился без break — ни одна кодировка не подошла
        return None # Возврат None — файл не читается

    if len(lines) < 2: # Если в файле меньше 2 строк (нет данных, только заголовок или пусто)
        return None # Возврат None — недостаточно данных

    headers = lines[0].strip().split(",") # Парсинг заголовков CSV (первая строка)

    aggregated_line = None # Переменная для хранения агрегированной строки статистики
    for line in lines[1:]: # Перебор всех строк данных (кроме заголовка)
        if "Aggregated" in line: # Locust записывает строку "Aggregated" с суммарной статистикой
            aggregated_line = line.strip().split(",") # Парсинг агрегированной строки
            break

    if not aggregated_line: # Если строка "Aggregated" не найдена — берём последнюю строку как альтернативу
        aggregated_line = lines[-1].strip().split(",") # Парсинг последней строки файла

    results = {} # Словарь для результата: ключ (название метрики) → значение
    for i, header in enumerate(headers): # Перебор заголовков с их индексами
        if i < len(aggregated_line): # Защита от несовпадения количества заголовков и значений
            results[header.strip()] = aggregated_line[i].strip() # Сохранение пары: очищенный заголовок → очищенное значение

    return results # Возврат словаря со статистикой


def format_results(raw_output, stats): # Функция форматирования итогового отчёта из вывода Locust и статистики
    report_lines = [] # Список строк отчёта
    report_lines.append("=" * 50) # Разделитель-заголовок
    report_lines.append("ОТЧЕТ ПО НАГРУЗОЧНОМУ ТЕСТИРОВАНИЮ") # Заголовок отчёта
    report_lines.append("=" * 50) # Закрывающий разделитель
    report_lines.append(f"Цель: https://itstep.by") # URL тестируемого сервера
    report_lines.append(f"Дата: {time.strftime('%Y-%m-%d %H:%M:%S')}") # Текущая дата и время формирования отчёта
    report_lines.append("") # Пустая строка-отступ

    if stats: # Если статистика была успешно загружена из CSV
        report_lines.append("СТАТИСТИКА:") # Заголовок секции статистики
        report_lines.append("-" * 50) # Разделитель

        stat_map = {} # Словарь для нормализации ключей (в нижний регистр)
        for key, value in stats.items(): # Перебор всех пар ключ-значение из статистики
            stat_map[key.lower().strip()] = value # Сохранение с нижним регистром и без пробелов

        stat_names = { # Маппинг английских ключей CSV на русские названия для отчёта
            "request count": "Всего запросов", # Количество выполненных запросов
            "failure count": "Неудачных запросов", # Количество завершившихся ошибкой запросов
            "median response time": "Медианное время (мс)", # Медианное время ответа
            "average response time": "Среднее время (мс)", # Среднее арифметическое время ответа
            "min response time": "Мин. время (мс)", # Минимальное время ответа
            "max response time": "Макс. время (мс)", # Максимальное время ответа
            "average size": "Ср. размер ответа (байт)", # Средний размер тела ответа
            "requests/s": "Запросов/сек", # Скорость обработки запросов
        }

        for key, label in stat_names.items(): # Перебор маппинга ключ → русское название
            for stat_key, stat_value in stat_map.items(): # Поиск совпадения среди ключей статистики
                if key in stat_key: # Если ключ маппинга содержится в ключе статистики (нечёткий поиск)
                    report_lines.append(f"  {label}: {stat_value}") # Добавление строки с метрикой в отчёт
                    break # Переход к следующей метрике

        report_lines.append("") # Пустая строка-отступ после блока статистики
    else: # Если статистика не загружена
        report_lines.append("Статистика не загружена") # Сообщение об отсутствии данных
        report_lines.append("") # Пустая строка-отступ

    if raw_output: # Если есть сырой вывод Locust (stdout)
        report_lines.append("ВЫВОД LOCUST:") # Заголовок секции с выводом Locust
        report_lines.append("-" * 50) # Разделитель
        lines = raw_output.strip().split("\n") # Разбиение вывода на отдельные строки
        for line in lines[-30:]: # Вывод только последних 30 строк (чтобы не засорять отчёт)
            report_lines.append(f"  {line}") # Добавление строки с отступом

    report_lines.append("") # Пустая строка перед финальным разделителем
    report_lines.append("=" * 50) # Финальный разделитель

    return "\n".join(report_lines) # Объединение всех строк в одну строку с переводами строк


if __name__ == "__main__": # Точка входа: скрипт выполняется напрямую (не импортируется как модуль)
    import io # Импорт модуля для работы с потоками ввода-вывода
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace') # Перенастройка stdout на UTF-8 (решает проблему кодировки в Windows-консоли)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace') # Перенастройка stderr на UTF-8

    users = int(sys.argv[1]) if len(sys.argv) > 1 else 10 # Чтение количества пользователей из аргументов командной строки (по умолчанию 10)
    spawn_rate = int(sys.argv[2]) if len(sys.argv) > 2 else 2 # Чтение скорости появления пользователей (по умолчанию 2)
    run_time = sys.argv[3] if len(sys.argv) > 3 else "30s" # Чтение длительности теста (по умолчанию 30 секунд)

    print(f"Запуск нагрузочного тестирования: {users} пользователей, {run_time}...") # Информационное сообщение о начале теста

    stdout, stderr, returncode = run_locust_test(users, spawn_rate, run_time) # Запуск теста Locust и получение его вывода

    stats = get_results() # Чтение статистики из CSV-файла, сгенерированного Locust
    report = format_results(stdout, stats) # Форматирование итогового отчёта
    print(report) # Вывод отчёта в консоль

    report_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "loadtest_report.txt") # Путь к файлу отчёта (рядом со скриптом)
    with open(report_file, "w", encoding="utf-8") as f: # Открытие файла для записи отчёта
        f.write(report) # Сохранение отчёта в текстовый файл

    print(f"\nОтчет сохранен: {report_file}") # Сообщение о месте сохранения отчёта
