from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler
from telegram.ext import filters
import logging
import os
import zipfile
import time
import asyncio
import threading
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import subprocess
import sys


REPORT_PORT = 9090
report_server = None


class ReportHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)

    def log_message(self, format, *args):
        pass


def start_report_server(report_path: str, port: int = REPORT_PORT):
    global report_server
    if report_server:
        try:
            report_server.shutdown()
        except Exception:
            pass
    handler = lambda *a, **kw: ReportHandler(*a, directory=report_path, **kw)
    report_server = HTTPServer(("0.0.0.0", port), handler)
    thread = threading.Thread(target=report_server.serve_forever, daemon=True)
    thread.start()


async def execute_command(cmd: str, update: Update, context: ContextTypes.DEFAULT_TYPE, timeout: int = 600) -> str:
    """Выполняет shell-команду с таймаутом и возвращает результат"""
    try:
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        context.user_data['running_process'] = proc
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout)
        output = f"STDOUT:\n{stdout.decode().strip()}" if stdout else ""
        output += f"\nSTDERR:\n{stderr.decode().strip()}" if stderr else ""
        return output.strip()
    except asyncio.TimeoutError:
        return f"❌ Таймаут ({timeout} сек)"
    except asyncio.CancelledError:
        proc.kill()
        return "⛔ Тесты остановлены пользователем"
    except Exception as e:
        return f"⚠️ Ошибка: {str(e)}"
    finally:
        context.user_data['running_process'] = None


async def run_all_tests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запуск всех тестов (UI + API) и генерация Allure отчета"""
    await update.message.reply_text("🔍 Запускаю все тесты (UI + API)...")

    results_dir = Path("./results")
    results_dir.mkdir(exist_ok=True)
    for file in results_dir.glob("*"):
        file.unlink()

    result = await execute_command(
        "pytest -s -v test/test_main.py test/test_api.py --alluredir=./results",
        update, context
    )

    passed = result.count("PASSED")
    failed = result.count("FAILED")
    summary = f"✅ Пройдено: {passed}\n❌ Провалено: {failed}" if failed else f"✅ Все {passed} тестов прошли успешно!"
    await update.message.reply_text(f"📊 Результаты:\n{summary}")

    await generate_and_serve_report(update, context)


async def run_ui_tests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запуск UI тестов и генерация Allure отчета"""
    await update.message.reply_text("🔍 Запускаю UI тесты...")

    results_dir = Path("./results")
    results_dir.mkdir(exist_ok=True)
    for file in results_dir.glob("*"):
        file.unlink()

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
    """Запуск API тестов и генерация Allure отчета"""
    await update.message.reply_text("🔍 Запускаю API тесты...")

    results_dir = Path("./results")
    results_dir.mkdir(exist_ok=True)
    for file in results_dir.glob("*"):
        file.unlink()

    result = await execute_command(
        "pytest -s -v test/test_api.py --alluredir=./results",
        update, context
    )

    passed = result.count("PASSED")
    failed = result.count("FAILED")
    summary = f"✅ Пройдено: {passed}\n❌ Провалено: {failed}" if failed else f"✅ Все {passed} API тестов прошли успешно!"
    await update.message.reply_text(f"📊 Результаты:\n{summary}")

    await generate_and_serve_report(update, context)


async def generate_and_serve_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Генерация отчета, запуск HTTP-сервера и отправка архива"""
    try:
        results_dir = Path("./results")
        if not results_dir.exists() or not any(results_dir.iterdir()):
            await update.message.reply_text("❌ Нет данных для отчета: папка results пуста")
            return

        await update.message.reply_text("📈 Генерирую Allure-отчет...")

        gen_result = await execute_command(
            "allure generate ./results --clean -o ./allure-report",
            update, context
        )

        report_dir = Path("./allure-report")
        report_index = report_dir / "index.html"

        if not report_index.exists():
            await update.message.reply_text(
                f"⚠️ Ошибка генерации отчета. Отправляю сырые данные.\n{gen_result[:500]}"
            )
            await send_raw_results(update, context, results_dir)
            return

        start_report_server(str(report_dir), REPORT_PORT)

        timestamp = int(time.time())
        zip_name = f"allure_report_{timestamp}.zip"

        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(report_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = os.path.join("allure-report", os.path.relpath(file_path, report_dir))
                    zipf.write(file_path, arcname=arcname)
            for root, _, files in os.walk(results_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = os.path.join("results", os.path.relpath(file_path, results_dir))
                    zipf.write(file_path, arcname=arcname)

        with open(zip_name, 'rb') as zip_file:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=zip_file,
                filename=zip_name,
                caption="📊 Allure Report"
            )
        os.remove(zip_name)

        await update.message.reply_text(
            f"✅ Отчет готов!\n\n"
            f"🌐 Откройте в браузере:\nhttp://localhost:{REPORT_PORT}\n\n"
            f"📦 Или распакуйте полученный архив и откройте index.html"
        )

    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {str(e)}")


async def send_raw_results(update: Update, context: ContextTypes.DEFAULT_TYPE, results_dir: Path):
    """Отправка сырых Allure результатов как zip"""
    timestamp = int(time.time())
    zip_name = f"allure_results_{timestamp}.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(results_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = os.path.join("results", os.path.relpath(file_path, results_dir))
                zipf.write(file_path, arcname=arcname)
    with open(zip_name, 'rb') as zip_file:
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=zip_file,
            filename=zip_name,
            caption="📊 Сырые Allure данные"
        )
    os.remove(zip_name)


async def serve_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запуск HTTP-сервера для уже сгенерированного отчета"""
    report_dir = Path("./allure-report")
    if not report_dir.exists() or not (report_dir / "index.html").exists():
        await update.message.reply_text(
            "❌ Отчет еще не сгенерирован.\n"
            "Сначала запустите тесты или нажмите '📊 Получить Allure отчет'"
        )
        return

    start_report_server(str(report_dir), REPORT_PORT)
    await update.message.reply_text(
        f"🌐 Allure отчет доступен по адресу:\n"
        f"http://localhost:{REPORT_PORT}\n\n"
        f"Откройте эту ссылку в браузере."
    )


async def run_load_tests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запуск нагрузочного тестирования с параметрами по умолчанию"""
    await _execute_load_test(update, context, users=10, spawn_rate=2, run_time="30s")


async def configure_load_tests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало диалога настройки нагрузочных тестов"""
    context.user_data['loadtest_state'] = 'waiting_users'
    await update.message.reply_text(
        "⚙️ Настройка нагрузочного тестирования\n\n"
        "Введите количество виртуальных пользователей (1-100):"
    )


async def _execute_load_test(update: Update, context: ContextTypes.DEFAULT_TYPE,
                              users: int = 10, spawn_rate: int = 2, run_time: str = "30s"):
    """Выполнение нагрузочного тестирования"""
    await update.message.reply_text(
        f"⚡ Запускаю нагрузочное тестирование itstep.by...\n"
        f"👥 Пользователей: {users}\n"
        f"⏱ Длительность: {run_time}\n"
        f"⏳ Это может занять некоторое время..."
    )

    loadtest_dir = Path(__file__).parent / "loadtest"
    run_script = loadtest_dir / "run_loadtest.py"

    if not run_script.exists():
        await update.message.reply_text("❌ Файл запуска нагрузочных тестов не найден")
        return

    cmd = f'"{sys.executable}" "{run_script}" {users} {spawn_rate} {run_time}'

    try:
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(loadtest_dir)
        )
        context.user_data['running_process'] = proc
        timeout = max(60, users * 5 + 30)
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)

        stdout_text = stdout.decode("utf-8", errors="replace") if stdout else ""
        stderr_text = stderr.decode("utf-8", errors="replace") if stderr else ""

        report_file = loadtest_dir / "loadtest_report.txt"
        if report_file.exists():
            with open(report_file, "r", encoding="utf-8") as f:
                report_content = f.read()

            if len(report_content) > 3000:
                report_content = report_content[:3000] + "\n\n... (отчет обрезан)"

            await update.message.reply_text(f"📊 Результаты нагрузочного тестирования:\n\n{report_content}")

            timestamp = int(time.time())
            zip_name = f"loadtest_results_{timestamp}.zip"
            with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for ext in ["_stats.csv", "_failures.csv", "_stats_history.csv", "_report.html", ".json", "_report.txt"]:
                    for f in loadtest_dir.glob(f"*{ext}"):
                        zipf.write(f, arcname=f"loadtest/{f.name}")

            with open(zip_name, 'rb') as zip_file:
                await context.bot.send_document(
                    chat_id=update.effective_chat.id,
                    document=zip_file,
                    filename=zip_name,
                    caption="📦 Файлы результатов нагрузочного тестирования"
                )
            os.remove(zip_name)
        else:
            output = stdout_text[-2000:] if stdout_text else "Нет вывода"
            await update.message.reply_text(f"📊 Вывод:\n{output}")

    except asyncio.TimeoutError:
        await update.message.reply_text("❌ Таймаут: нагрузочное тестирование заняло слишком много времени")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")
    finally:
        context.user_data['running_process'] = None
        context.user_data.pop('loadtest_state', None)
        context.user_data.pop('loadtest_users', None)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['running_process'] = None
    keyboard = [
        [KeyboardButton("🚀 Все тесты (UI+API)"), KeyboardButton("⏹ Стоп")],
        [KeyboardButton("🧪 UI тесты"), KeyboardButton("🔌 API тесты")],
        [KeyboardButton("⚡ Нагрузочные тесты"), KeyboardButton("⚙️ Настроить нагрузку")],
        [KeyboardButton("🌐 Открыть Allure отчет"), KeyboardButton("📦 Скачать отчет")],
        [KeyboardButton("ℹ️ О проекте")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='👋 Добро пожаловать в бот автотестов IT ШАГ!\n\nВыберите действие:',
        reply_markup=reply_markup
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        "🛠 Технологии:\n"
        "• Python + Selenium + Requests\n"
        "• Pytest + Allure + Locust\n"
        "• Page Object Model\n"
        "• Telegram бот для управления"
    )
    await update.message.reply_text(about_text)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка кнопок и диалога настройки"""
    text = update.message.text

    state = context.user_data.get('loadtest_state')

    if state == 'waiting_users':
        try:
            users = int(text)
            if users < 1 or users > 100:
                raise ValueError
            context.user_data['loadtest_users'] = users
            context.user_data['loadtest_state'] = 'waiting_time'
            await update.message.reply_text(
                f"👥 Пользователей: {users}\n\n"
                "Введите длительность теста (например: 30s, 1m, 2m30s):"
            )
            return
        except ValueError:
            await update.message.reply_text("❌ Введите число от 1 до 100:")
            return

    if state == 'waiting_time':
        run_time = text.strip().lower()
        valid = False
        for fmt in ['s', 'm']:
            if run_time.endswith(fmt):
                valid = True
                break
        if not valid or not run_time[:-1].replace('.', '').isdigit():
            await update.message.reply_text(
                "❌ Неверный формат. Примеры: 30s, 1m, 2m30s"
            )
            return

        users = context.user_data.get('loadtest_users', 10)
        spawn_rate = min(max(1, users // 5), 10)
        await _execute_load_test(update, context, users=users, spawn_rate=spawn_rate, run_time=run_time)
        return

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
    elif text == "⏹ Стоп":
        context.user_data.pop('loadtest_state', None)
        context.user_data.pop('loadtest_users', None)
        proc = context.user_data.get('running_process')
        if proc and proc.returncode is None:
            proc.kill()
            context.user_data['running_process'] = None
            await update.message.reply_text("⛔ Тесты остановлены!")
        else:
            await update.message.reply_text("ℹ️ Нет запущенных тестов")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Exception while handling an update: {context.error}", exc_info=context.error)
    if update and update.message:
        await update.message.reply_text(f"⚠️ Ошибка: {context.error}")


def main():
    application = Application.builder().token('7683227185:AAHjeK3ScoB9b51hm82O55JXBYbPWwWTx1c').build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("run_all", run_all_tests))
    application.add_handler(CommandHandler("run_ui", run_ui_tests))
    application.add_handler(CommandHandler("run_api", run_api_tests))
    application.add_handler(CommandHandler("run_load", run_load_tests))
    application.add_handler(CommandHandler("report", serve_report))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.add_error_handler(error_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
