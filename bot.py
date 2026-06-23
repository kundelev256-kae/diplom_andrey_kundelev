# -*- coding: utf-8 -*-
"""
Telegram-бот для запуска UI, API и нагрузочных тестов.
Управляет pytest, Allure-отчётами, Locust и интеграцией с нейросетью Groq.
"""

# Загрузка переменных окружения из файла .env (токены, ключи API)
from dotenv import load_dotenv
load_dotenv()  # Считывает .env и устанавливает переменные в os.environ

# Импорт компонентов Telegram API
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup  # Обновления, кнопки и клавиатуры
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler  # Регистрация обработчиков
from telegram.ext import filters  # Фильтры для обработки типов сообщений

import logging  # Логирование ошибок и событий
import os  # Доступ к переменным окружения и файловым операциям
import zipfile  # Создание ZIP-архивов для отправки отчётов
import time  # Генерация timestamp для уникальных имён файлов
import asyncio  # Асинхронное выполнение команд и таймауты
import threading  # Запуск HTTP-сервера в фоновом потоке
from pathlib import Path  # Удобная работа с файловыми путями
from http.server import HTTPServer, SimpleHTTPRequestHandler  # Простой HTTP-сервер для просмотра отчётов
import subprocess  # Запуск внешних процессов (не используется напрямую)
import sys  # Доступ к sys.executable для запуска Python-скриптов
import requests  # HTTP-запросы к Groq API (нейросеть)
import json  # Работа с JSON (не используется напрямую, но импортирован)
import hashlib  # Хеширование (не используется напрямую, но импортирован)

# ─── Константы ───────────────────────────────────────────────────────

REPORT_PORT = 9090  # Порт для HTTP-сервера, отдающего Allure-отчёт
report_server = None  # Ссылка на текущий экземпляр HTTP-сервера (None = не запущен)

# Ключ API для доступа к Groq (нейросеть Llama 3)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")  # Читается из переменной окружения GROQ_API_KEY
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"  # Endpoint для Groq Chat API

# Локальные ответы бота на случай недоступности API нейросети
OFFLINE_RESPONSES = {
    "привет": "Привет! Чем могу помочь?",  # Ответ на приветствие
    "как дела": "Отлично, спасибо! Как у тебя?",  # Ответ на вопрос о самочувствии
    "помощь": "Я могу ответить на вопросы. Просто напиши мне!",  # Ответ на запрос помощи
    "кто ты": "Я Telegram-бот с нейросетью для автотестов.",  # Ответ на вопрос о боте
    "hello": "Hello! How can I help you?",  # Английское приветствие
    "hi": "Hi there!",  # Английское приветствие
}


# ─── Функция запроса к нейросети ──────────────────────────────────────

def query_ai(prompt: str, history: list = None) -> str:
    """Запрос к нейросети через Groq API (Llama 3).
    Принимает текст пользователя и историю диалога, возвращает ответ нейросети.
    При недоступности API используется локальный fallback."""
    try:
        # Формируем список сообщений для API
        messages = [{"role": "system", "content": "Ты полезный ассистент. Отвечай кратко и по делу на русском языке."}]
        # Добавляем предыдущие пары вопрос-ответ из истории диалога
        if history:
            for h in history:
                messages.append({"role": "user", "content": h["user"]})  # Сообщение пользователя
                messages.append({"role": "assistant", "content": h["bot"]})  # Ответ бота
        # Добавляем текущий вопрос пользователя
        messages.append({"role": "user", "content": prompt})

        # Тело запроса к API
        payload = {
            "model": "llama3-8b-8192",  # Модель Llama 3 от Meta (8K контекст)
            "messages": messages,  # Список сообщений
            "max_tokens": 1024,  # Максимальное количество токенов в ответе
            "temperature": 0.7  # Случайность ответа (0 = детерминированный, 1 = максимальная)
        }

        # Отправляем POST-запрос к Groq API
        response = requests.post(
            GROQ_API_URL,  # URL API
            json=payload,  # Тело запроса в формате JSON
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},  # Авторизация
            timeout=30  # Таймаут запроса — 30 секунд
        )

        # Обработка ответа API
        if response.status_code == 200:  # Успешный ответ
            result = response.json()  # Декодируем JSON-ответ
            return result["choices"][0]["message"]["content"]  # Извлекаем текст ответа нейросети
        elif response.status_code == 401:  # Невалидный API-ключ
            return _fallback_response(prompt)  # Используем локальный ответ
        else:  # Любая другая ошибка
            return _fallback_response(prompt)  # Используем локальный ответ
    except requests.ConnectionError:  # Нет подключения к интернету
        return _fallback_response(prompt)
    except requests.Timeout:  # Превышен таймаут запроса
        return "⚠️ Таймаут: нейросеть не ответила вовремя"
    except Exception:  # Любая другая непредвиденная ошибка
        return _fallback_response(prompt)


def _fallback_response(prompt: str) -> str:
    """Локальный ответ когда API недоступен.
    Ищет ключевое слово во вводе пользователя и возвращает соответствующий ответ.
    Если не найдено — возвращает общее сообщение об ошибке."""
    # Приводим ввод к нижнему регистру и убираем знаки препинания
    low = prompt.lower().strip().rstrip("?!.,")

    # Ищем совпадение с ключами в словаре локальных ответов
    for key, answer in OFFLINE_RESPONSES.items():
        if key in low:  # Если ключевое слово найдено в тексте
            return answer

    # Если ни одно ключевое слово не совпало — общее сообщение
    return (f"🤖 Вы спросили: «{prompt}»\n\n"
            "К сожалению, API нейросети сейчас недоступен. "
            "Задайте простой вопрос (привет, помощь, кто ты) или попробуйте позже.")


# ─── HTTP-сервер для отчётов ──────────────────────────────────────────

class ReportHandler(SimpleHTTPRequestHandler):
    """Обработчик HTTP-запросов для раздачи файлов отчёта.
    Наследует SimpleHTTPRequestHandler для раздачи静态 файлов."""
    def __init__(self, *args, directory=None, **kwargs):
        # Передаём директорию с отчётом в родительский класс
        super().__init__(*args, directory=directory, **kwargs)

    def log_message(self, format, *args):
        # Подавляем вывод HTTP-логов в консоль (чтобы не засорять вывод)
        pass


def start_report_server(report_path: str, port: int = REPORT_PORT):
    """Запуск HTTP-сервера для отдачи файлов отчёта.
    Если сервер уже запущен — останавливает его перед перезапуском."""
    global report_server  # Глобальная переменная для хранения экземпляра сервера
    if report_server:  # Если сервер уже работает
        try:
            report_server.shutdown()  # Останавливаем предыдущий сервер
        except Exception:
            pass  # Игнорируем ошибки при остановке
    # Создаём обработчик с указанной директорией
    handler = lambda *a, **kw: ReportHandler(*a, directory=report_path, **kw)
    # Запускаем HTTP-сервер на 0.0.0.0 (все интерфейсы) с указанным портом
    report_server = HTTPServer(("0.0.0.0", port), handler)
    # Запускаем сервер в фоновом демон-потоке (не блокирует основной поток)
    thread = threading.Thread(target=report_server.serve_forever, daemon=True)
    thread.start()


# ─── Выполнение shell-команд ──────────────────────────────────────────

async def execute_command(cmd: str, update: Update, context: ContextTypes.DEFAULT_TYPE, timeout: int = 600) -> str:
    """Выполняет shell-команду асинхронно с таймаутом.
    Сохраняет процесс в user_data для возможности отмены.
    Возвращает объединённый stdout + stderr."""
    try:
        # Создаём асинхронный subprocess для выполнения shell-команды
        proc = await asyncio.create_subprocess_shell(
            cmd,  # Команда для выполнения
            stdout=asyncio.subprocess.PIPE,  # Перехватываем stdout
            stderr=asyncio.subprocess.PIPE  # Перехватываем stderr
        )
        # Сохраняем процесс в user_data, чтобы пользователь мог его остановить
        context.user_data['running_process'] = proc
        # Ждём завершения процесса с таймаутом
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout)
        # Форматируем вывод: добавляем метки STDOUT и STDERR
        output = f"STDOUT:\n{stdout.decode().strip()}" if stdout else ""
        output += f"\nSTDERR:\n{stderr.decode().strip()}" if stderr else ""
        return output.strip()
    except asyncio.TimeoutError:  # Процесс выполнялся дольше таймаута
        return f"❌ Таймаут ({timeout} сек)"
    except asyncio.CancelledError:  # Процесс был отменён пользователем
        proc.kill()  # Принудительно завершаем процесс
        return "⛔ Тесты остановлены пользователем"
    except Exception as e:  # Любая другая ошибка
        return f"⚠️ Ошибка: {str(e)}"
    finally:
        # Очищаем ссылку на процесс (независимо от результата)
        context.user_data['running_process'] = None


# ─── Запуск тестов ────────────────────────────────────────────────────

async def run_all_tests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запуск всех тестов (UI + API) и генерация Allure-отчёта.
    Выполняет pytest для обоих файлов тестов и создаёт HTML-отчёт."""
    # Уведомляем пользователя о начале запуска
    await update.message.reply_text("🔍 Запускаю все тесты (UI + API)...")

    # Создаём директорию для результатов (или очищаем существующую)
    results_dir = Path("./results")
    results_dir.mkdir(exist_ok=True)  # Создаём, если не существует
    for file in results_dir.glob("*"):  # Удаляем старые файлы результатов
        file.unlink()

    # Запускаем pytest с Allure-репортёрскими опциями
    result = await execute_command(
        "pytest -s -v test/test_main.py test/test_api.py --alluredir=./results",  # -s: без захвата, -v: подробный вывод
        update, context
    )

    # Подсчитываем количество пройденных и проваленных тестов
    passed = result.count("PASSED")  # Ищем строки PASSED в выводе pytest
    failed = result.count("FAILED")  # Ищем строки FAILED в выводе pytest
    # Формируем сводку результатов
    summary = f"✅ Пройдено: {passed}\n❌ Провалено: {failed}" if failed else f"✅ Все {passed} тестов прошли успешно!"
    await update.message.reply_text(f"📊 Результаты:\n{summary}")

    # Генерируем и отправляем Allure-отчёт
    await generate_and_serve_report(update, context)


async def run_ui_tests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запуск UI-тестов и генерация Allure-отчёта.
    Тестирует навигацию, меню, формы и другие элементы интерфейса."""
    await update.message.reply_text("🔍 Запускаю UI тесты...")

    # Очищаем директорию результатов перед новым запуском
    results_dir = Path("./results")
    results_dir.mkdir(exist_ok=True)
    for file in results_dir.glob("*"):
        file.unlink()

    # Запускаем только UI-тесты (test_main.py)
    result = await execute_command(
        "pytest -s -v test/test_main.py --alluredir=./results",
        update, context
    )

    passed = result.count("PASSED")
    failed = result.count("FAILED")
    summary = f"✅ Пройдено: {passed}\n❌ Провалено: {failed}" if failed else f"✅ Все {passed} UI тестов прошли успешно!"
    await update.message.reply_text(f"📊 Результаты:\n{summary}")

    await generate_and_serve_report(update, context)


async def run_api_tests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запуск API-тестов и генерация Allure-отчёта.
    Тестирует HTTP-статусы, время отклика, редиректы и SSL."""
    await update.message.reply_text("🔍 Запускаю API тесты...")

    results_dir = Path("./results")
    results_dir.mkdir(exist_ok=True)
    for file in results_dir.glob("*"):
        file.unlink()

    # Запускаем только API-тесты (test_api.py)
    result = await execute_command(
        "pytest -s -v test/test_api.py --alluredir=./results",
        update, context
    )

    passed = result.count("PASSED")
    failed = result.count("FAILED")
    summary = f"✅ Пройдено: {passed}\n❌ Провалено: {failed}" if failed else f"✅ Все {passed} API тестов прошли успешно!"
    await update.message.reply_text(f"📊 Результаты:\n{summary}")

    await generate_and_serve_report(update, context)


# ─── Генерация и отправка отчёта ──────────────────────────────────────

async def generate_and_serve_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Генерация HTML-отчёта Allure, запуск HTTP-сервера и отправка ZIP-архива.
    Включает полный цикл: генерация → валидация → упаковка → отправка → ссылка."""
    try:
        # Проверяем, есть ли данные для отчёта
        results_dir = Path("./results")
        if not results_dir.exists() or not any(results_dir.iterdir()):
            await update.message.reply_text("❌ Нет данных для отчета: папка results пуста")
            return

        # Уведомляем о начале генерации
        await update.message.reply_text("📈 Генерирую Allure-отчет...")

        # Генерируем HTML-отчёт из сырых данных Allure
        gen_result = await execute_command(
            "allure generate ./results --clean -o ./allure-report",  # --clean: перезапись, -o: выходная папка
            update, context
        )

        # Проверяем, что отчёт успешно сгенерировался
        report_dir = Path("./allure-report")
        report_index = report_dir / "index.html"  # Главный файл отчёта

        if not report_index.exists():  # Если файл не создан — ошибка генерации
            await update.message.reply_text(
                f"⚠️ Ошибка генерации отчета. Отправляю сырые данные.\n{gen_result[:500]}"
            )
            await send_raw_results(update, context, results_dir)  # Отправляем сырые данные
            return

        # Запускаем HTTP-сервер для просмотра отчёта в браузере
        start_report_server(str(report_dir), REPORT_PORT)

        # Создаём ZIP-архив с отчётом и сырыми данными
        timestamp = int(time.time())  # Уникальное имя файла на основе времени
        zip_name = f"allure_report_{timestamp}.zip"

        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:  # ZIP_DEFLATED: сжатие
            # Добавляем все файлы HTML-отчёта в архив
            for root, _, files in os.walk(report_dir):  # Рекурсивный обход папки
                for file in files:
                    file_path = Path(root) / file
                    arcname = os.path.join("allure-report", os.path.relpath(file_path, report_dir))  # Путь внутри архива
                    zipf.write(file_path, arcname=arcname)
            # Добавляем сырые данные Allure в архив
            for root, _, files in os.walk(results_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = os.path.join("results", os.path.relpath(file_path, results_dir))
                    zipf.write(file_path, arcname=arcname)

        # Отправляем ZIP-архив пользователю в Telegram
        with open(zip_name, 'rb') as zip_file:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,  # ID текущего чата
                document=zip_file,  # Файл для отправки
                filename=zip_name,  # Имя файла при скачивании
                caption="📊 Allure Report"  # Подпись к файлу
            )
        os.remove(zip_name)  # Удаляем временный ZIP-файл с диска

        # Отправляем ссылку для просмотра отчёта в браузере
        await update.message.reply_text(
            f"✅ Отчет готов!\n\n"
            f"🌐 Откройте в браузере:\nhttp://localhost:{REPORT_PORT}\n\n"
            f"📦 Или распакуйте полученный архив и откройте index.html"
        )

    except Exception as e:  # Обработка любых непредвиденных ошибок
        await update.message.reply_text(f"⚠️ Ошибка: {str(e)}")


async def send_raw_results(update: Update, context: ContextTypes.DEFAULT_TYPE, results_dir: Path):
    """Отправка сырых Allure-результатов как ZIP-архива.
    Используется как fallback, когда генерация HTML-отчёта не удалась."""
    # Формируем уникальное имя архива
    timestamp = int(time.time())
    zip_name = f"allure_results_{timestamp}.zip"
    # Упаковываем все файлы из results_dir в ZIP
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(results_dir):  # Рекурсивный обход
            for file in files:
                file_path = Path(root) / file
                arcname = os.path.join("results", os.path.relpath(file_path, results_dir))
                zipf.write(file_path, arcname=arcname)
    # Отправляем архив пользователю
    with open(zip_name, 'rb') as zip_file:
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=zip_file,
            filename=zip_name,
            caption="📊 Сырые Allure данные"
        )
    os.remove(zip_name)  # Удаляем временный файл


async def serve_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запуск HTTP-сервера для уже сгенерированного отчёта.
    Проверяет наличие отчёта и запускает сервер, если он есть."""
    report_dir = Path("./allure-report")
    # Проверяем существование отчёта
    if not report_dir.exists() or not (report_dir / "index.html").exists():
        await update.message.reply_text(
            "❌ Отчет еще не сгенерирован.\n"
            "Сначала запустите тесты или нажмите '📊 Получить Allure отчет'"
        )
        return

    # Запускаем HTTP-сервер и отправляем ссылку
    start_report_server(str(report_dir), REPORT_PORT)
    await update.message.reply_text(
        f"🌐 Allure отчет доступен по адресу:\n"
        f"http://localhost:{REPORT_PORT}\n\n"
        f"Откройте эту ссылку в браузере."
    )


# ─── Нагрузочное тестирование ─────────────────────────────────────────

async def run_load_tests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запуск нагрузочного тестирования с параметрами по умолчанию.
    10 пользователей, 2 в секунду, 30 секунд."""
    await _execute_load_test(update, context, users=10, spawn_rate=2, run_time="30s")


async def configure_load_tests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало диалога настройки нагрузочных тестов.
    Устанавливает состояние 'waiting_users' для обработки ввода."""
    context.user_data['loadtest_state'] = 'waiting_users'  # Состояние: ожидание количества пользователей
    await update.message.reply_text(
        "⚙️ Настройка нагрузочного тестирования\n\n"
        "Введите количество виртуальных пользователей (1-100):"
    )


async def _execute_load_test(update: Update, context: ContextTypes.DEFAULT_TYPE,
                              users: int = 10, spawn_rate: int = 2, run_time: str = "30s"):
    """Выполнение нагрузочного тестирования через Locust.
    Запускает скрипт run_loadtest.py с переданными параметрами.
    Читает отчёт и отправляет архив с результатами."""
    # Уведомляем пользователя о запуске
    await update.message.reply_text(
        f"⚡ Запускаю нагрузочное тестирование itstep.by...\n"
        f"👥 Пользователей: {users}\n"
        f"⏱ Длительность: {run_time}\n"
        f"⏳ Это может занять некоторое время..."
    )

    # Формируем пути к скрипту нагрузочных тестов
    loadtest_dir = Path(__file__).parent / "loadtest"  # Папка loadtest рядом с bot.py
    run_script = loadtest_dir / "run_loadtest.py"  # Скрипт запуска

    if not run_script.exists():  # Проверяем существование скрипта
        await update.message.reply_text("❌ Файл запуска нагрузочных тестов не найден")
        return

    # Формируем команду для запуска: python run_loadtest.py <users> <spawn_rate> <run_time>
    cmd = f'"{sys.executable}" "{run_script}" {users} {spawn_rate} {run_time}'

    try:
        # Запускаем процесс в поддиректории loadtest
        proc = await asyncio.create_subprocess_shell(
            cmd,  # Команда запуска
            stdout=asyncio.subprocess.PIPE,  # Перехват stdout
            stderr=asyncio.subprocess.PIPE,  # Перехват stderr
            cwd=str(loadtest_dir)  # Рабочая директория — папка loadtest
        )
        context.user_data['running_process'] = proc  # Сохраняем для возможности отмены
        # Динамический таймаут: минимум 60 сек, или 5 сек на пользователя + 30 сек запаса
        timeout = max(60, users * 5 + 30)
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)

        # Декодируем вывод (заменяем невалидные символы)
        stdout_text = stdout.decode("utf-8", errors="replace") if stdout else ""
        stderr_text = stderr.decode("utf-8", errors="replace") if stderr else ""

        # Проверяем наличие отчёта в файле
        report_file = loadtest_dir / "loadtest_report.txt"
        if report_file.exists():
            # Читаем содержимое отчёта
            with open(report_file, "r", encoding="utf-8") as f:
                report_content = f.read()

            # Ограничиваем длину отчёта для Telegram (лимит ~4096 символов)
            if len(report_content) > 3000:
                report_content = report_content[:3000] + "\n\n... (отчет обрезан)"

            # Отправляем отчёт пользователю
            await update.message.reply_text(f"📊 Результаты нагрузочного тестирования:\n\n{report_content}")

            # Создаём ZIP-архив со всеми файлами результатов Locust
            timestamp = int(time.time())
            zip_name = f"loadtest_results_{timestamp}.zip"
            with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Добавляем CSV, HTML и JSON файлы результатов
                for ext in ["_stats.csv", "_failures.csv", "_stats_history.csv", "_report.html", ".json", "_report.txt"]:
                    for f in loadtest_dir.glob(f"*{ext}"):  # Поиск по шаблону
                        zipf.write(f, arcname=f"loadtest/{f.name}")

            # Отправляем архив пользователю
            with open(zip_name, 'rb') as zip_file:
                await context.bot.send_document(
                    chat_id=update.effective_chat.id,
                    document=zip_file,
                    filename=zip_name,
                    caption="📦 Файлы результатов нагрузочного тестирования"
                )
            os.remove(zip_name)  # Удаляем временный архив
        else:
            # Если отчёт не найден — отправляем последние строки stdout
            output = stdout_text[-2000:] if stdout_text else "Нет вывода"
            await update.message.reply_text(f"📊 Вывод:\n{output}")

    except asyncio.TimeoutError:  # Тестирование заняло слишком много времени
        await update.message.reply_text("❌ Таймаут: нагрузочное тестирование заняло слишком много времени")
    except Exception as e:  # Любая другая ошибка
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")
    finally:
        # Очищаем состояние пользователя
        context.user_data['running_process'] = None
        context.user_data.pop('loadtest_state', None)  # Удаляем состояние диалога
        context.user_data.pop('loadtest_users', None)  # Удаляем сохранённых пользователей


# ─── Команды Telegram-бота ────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start — приветствие и главное меню.
    Создаёт клавиатуру с кнопками для всех функций бота."""
    context.user_data['running_process'] = None  # Инициализируем состояние
    # Создаём кнопки клавиатуры (каждая строка — список кнопок)
    keyboard = [
        [KeyboardButton("🚀 Все тесты (UI+API)"), KeyboardButton("⏹ Стоп")],  # Запуск всех тестов и остановка
        [KeyboardButton("🧪 UI тесты"), KeyboardButton("🔌 API тесты")],  # UI и API тесты
        [KeyboardButton("⚡ Нагрузочные тесты"), KeyboardButton("⚙️ Настроить нагрузку")],  # Нагрузочные тесты
        [KeyboardButton("🌐 Открыть Allure отчет"), KeyboardButton("📦 Скачать отчет")],  # Просмотр и скачивание
        [KeyboardButton("🤖 Нейросеть (ON)"), KeyboardButton("🤖 Нейросеть (OFF)")],  # Включение/выключение нейросети
        [KeyboardButton("ℹ️ О проекте")],  # Информация о проекте
    ]
    # Создаём markup с автоматическим изменением размера (не one_time — остаётся)
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

    # Отправляем приветственное сообщение с клавиатурой
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='👋 Добро пожаловать в бот автотестов IT ШАГ!\n\nВыберите действие:',
        reply_markup=reply_markup
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /about — подробная информация о проекте.
    Описывает все компоненты: UI-тесты, API-тесты, нагрузочные тесты, нейросеть и технологии."""
    about_text = (
        "📋 Дипломный проект: UI + API + Load автотесты\n\n"
        "🎯 Тестируемый сайт: itstep.by\n\n"
        "✅ UI тесты (5):\n"
        "• Навигация (Вакансии, Контакты)\n"
        "• Меню IT ОБРАЗОВАНИЕ (курс QA)\n"
        "• Форма обратной связи (чат)\n"
        "• Заголовок страницы\n\n"
        "✅ API тесты (5):\n"
        "• HTTP-статус главной страницы\n"
        "• Время отклика\n"
        "• HTTP→HTTPS редирект\n"
        "• robots.txt\n"
        "• SSL-сертификат\n\n"
        "⚡ Нагрузочные тесты:\n"
        "• 11 сценариев (главная, вакансии, курсы и др.)\n"
        "• 10 виртуальных пользователей\n"
        "• Метрики: RPS, percentile, время отклика\n\n"
        "🤖 Нейросеть:\n"
        "• Бесплатная модель blenderbot-400M-distill\n"
        "• Ввод /ai для начала диалога\n"
        "• Ввод /ai_stop для остановки\n\n"
        "🛠 Технологии:\n"
        "• Python + Selenium + Requests\n"
        "• Pytest + Allure + Locust\n"
        "• Page Object Model\n"
        "• Telegram бот для управления"
    )
    await update.message.reply_text(about_text)  # Отправляем текст информации


# ─── Нейросеть ( Grove AI) ────────────────────────────────────────────

async def ai_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /ai — начало диалога с нейросетью.
    Активирует режим AI и инициализирует пустую историю."""
    context.user_data['ai_mode'] = True  # Включаем режим нейросети
    context.user_data['ai_history'] = []  # Очищаем историю диалога
    await update.message.reply_text(
        "🤖 Нейросеть активирована!\n\n"
        "Задайте любой вопрос, и я постараюсь ответить.\n"
        "Для остановки введите /ai_stop"
    )


async def ai_stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /ai_stop — остановка диалога с нейросетью.
    Выключает режим AI и очищает историю."""
    context.user_data['ai_mode'] = False  # Выключаем режим нейросети
    context.user_data['ai_history'] = []  # Очищаем историю диалога
    await update.message.reply_text("🤖 Диалог с нейросетью завершен.")


async def handle_ai_message(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str) -> bool:
    """Обработка сообщения в режиме нейросети.
    Возвращает True, если сообщение обработано (режим AI активен).
    Отправляет вопрос в query_ai и сохраняет историю (максимум 10 пар)."""
    if not context.user_data.get('ai_mode'):  # Если режим AI выключен — пропускаем
        return False

    await update.message.reply_text("⏳ Думаю...")  # Индикатор ожидания

    # Получаем историю диалога и отправляем запрос к нейросети
    history = context.user_data.get('ai_history', [])
    response = query_ai(text, history)

    # Сохраняем пару вопрос-ответ в историю
    history.append({"user": text, "bot": response})
    # Ограничиваем историю 10 последними exchanges (чтобы не превысить лимит контекста)
    if len(history) > 10:
        history = history[-10:]
    context.user_data['ai_history'] = history

    await update.message.reply_text(f"🤖 {response}")  # Отправляем ответ пользователю
    return True


# ─── Обработка сообщений (главный диспетчер) ─────────────────────────

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главный обработчик текстовых сообщений.
    Направляет сообщения в соответствующие обработчики:
    - Режим нейросети (если активен)
    - Диалог настройки нагрузочных тестов
    - Обработка нажатий кнопок клавиатуры"""
    text = update.message.text  # Текст сообщения от пользователя

    # Если активен режим нейросети — обрабатываем через AI
    if await handle_ai_message(update, context, text):
        return

    # Проверяем состояние диалога настройки нагрузочных тестов
    state = context.user_data.get('loadtest_state')

    # Состояние: ожидание количества пользователей
    if state == 'waiting_users':
        try:
            users = int(text)  # Пытаемся преобразовать ввод в число
            if users < 1 or users > 100:  # Проверяем диапазон
                raise ValueError
            context.user_data['loadtest_users'] = users  # Сохраняем количество пользователей
            context.user_data['loadtest_state'] = 'waiting_time'  # Переходим к следующему шагу
            await update.message.reply_text(
                f"👥 Пользователей: {users}\n\n"
                "Введите длительность теста (например: 30s, 1m, 2m30s):"
            )
            return
        except ValueError:  # Невалидный ввод
            await update.message.reply_text("❌ Введите число от 1 до 100:")
            return

    # Состояние: ожидание длительности теста
    if state == 'waiting_time':
        run_time = text.strip().lower()  # Нормализуем ввод
        valid = False
        for fmt in ['s', 'm']:  # Проверяем, заканчивается ли на 's' (секунды) или 'm' (минуты)
            if run_time.endswith(fmt):
                valid = True
                break
        if not valid or not run_time[:-1].replace('.', '').isdigit():  # Проверяем, что перед суффиксом число
            await update.message.reply_text(
                "❌ Неверный формат. Примеры: 30s, 1m, 2m30s"
            )
            return

        # Получаем ранее введённое количество пользователей (по умолчанию 10)
        users = context.user_data.get('loadtest_users', 10)
        # Вычисляем скорость появления пользователей (от 1 до 10, пропорционально числу пользователей)
        spawn_rate = min(max(1, users // 5), 10)
        await _execute_load_test(update, context, users=users, spawn_rate=spawn_rate, run_time=run_time)
        return

    # Обработка нажатий кнопок клавиатуры
    if text == "🚀 Все тесты (UI+API)":
        await run_all_tests(update, context)
    elif text == "🧪 UI тесты":
        await run_ui_tests(update, context)
    elif text == "🔌 API тесты":
        await run_api_tests(update, context)
    elif text == "⚡ Нагрузочные тесты":
        await run_load_tests(update, context)
    elif text == "⚙️ Настроить нагрузку":
        await configure_load_tests(update, context)
    elif text == "🌐 Открыть Allure отчет":
        await serve_report(update, context)
    elif text == "📦 Скачать отчет":
        await generate_and_serve_report(update, context)
    elif text == "ℹ️ О проекте":
        await about(update, context)
    elif text == "🤖 Нейросеть (ON)":
        await ai_start(update, context)
    elif text == "🤖 Нейросеть (OFF)":
        await ai_stop(update, context)
    elif text == "⏹ Стоп":
        # Остановка выполняющегося процесса
        context.user_data.pop('loadtest_state', None)  # Сбрасываем состояние диалога
        context.user_data.pop('loadtest_users', None)  # Сбрасываем сохранённых пользователей
        proc = context.user_data.get('running_process')
        if proc and proc.returncode is None:  # Если процесс ещё запущен
            proc.kill()  # Принудительно завершаем
            context.user_data['running_process'] = None
            await update.message.reply_text("⛔ Тесты остановлены!")
        else:
            await update.message.reply_text("ℹ️ Нет запущенных тестов")


# ─── Обработчик ошибок ────────────────────────────────────────────────

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Глобальный обработчик ошибок Telegram-бота.
    Логирует ошибку и отправляет пользователю сообщение об ошибке."""
    logging.error(f"Exception while handling an update: {context.error}", exc_info=context.error)
    if update and update.message:  # Если есть сообщение — уведомляем пользователя
        await update.message.reply_text(f"⚠️ Ошибка: {context.error}")


# ─── Точка входа ──────────────────────────────────────────────────────

def main():
    """Основная функция: инициализация бота, регистрация обработчиков и запуск polling."""
    # Получаем токен бота из переменных окружения
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    # Создаём приложение бота
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Регистрируем обработчики команд (/start, /about и т.д.)
    application.add_handler(CommandHandler("start", start))  # /start — приветствие
    application.add_handler(CommandHandler("about", about))  # /about — информация о проекте
    application.add_handler(CommandHandler("run_all", run_all_tests))  # /run_all — все тесты
    application.add_handler(CommandHandler("run_ui", run_ui_tests))  # /run_ui — UI тесты
    application.add_handler(CommandHandler("run_api", run_api_tests))  # /run_api — API тесты
    application.add_handler(CommandHandler("run_load", run_load_tests))  # /run_load — нагрузочные тесты
    application.add_handler(CommandHandler("report", serve_report))  # /report — открыть отчёт
    application.add_handler(CommandHandler("ai", ai_start))  # /ai — начать диалог с нейросетью
    application.add_handler(CommandHandler("ai_stop", ai_stop))  # /ai_stop — остановить нейросеть

    # Обработчик всех текстовых сообщений (не команд) — кнопки и диалоги
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Глобальный обработчик ошибок
    application.add_error_handler(error_handler)

    # Запуск long-polling (бот постоянно опрачивает Telegram API на наличие обновлений)
    application.run_polling()


# Запуск main() при прямом запуске скрипта (не при импорте)
if __name__ == "__main__":
    main()
