from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler
from telegram.ext import filters
import os
import zipfile
import time
import asyncio
from pathlib import Path


async def execute_command(cmd: str, update: Update, context: ContextTypes.DEFAULT_TYPE, timeout: int = 300) -> str:
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
    """Запуск всех UI тестов и генерация Allure отчета"""
    await update.message.reply_text("🔍 Запускаю все UI тесты...")

    results_dir = Path("./results")
    results_dir.mkdir(exist_ok=True)

    for file in results_dir.glob("*"):
        file.unlink()

    result = await execute_command(
        "pytest -s -v test/ --alluredir=./results",
        update, context
    )

    short_result = "\n".join([line for line in result.split("\n") if "FAILED" in line or "ERROR" in line])
    await update.message.reply_text(
        f"📊 Результаты тестов:\n{short_result[:3000]}" if short_result else "✅ Все тесты прошли успешно!"
    )

    await generate_allure_report(update, context)

async def run_ui_tests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запуск UI тестов и генерация Allure отчета"""
    await update.message.reply_text("🔍 Запускаю UI тесты...")

    results_dir = Path("./results")
    results_dir.mkdir(exist_ok=True)

    for file in results_dir.glob("*"):
        file.unlink()

    result = await execute_command(
        "pytest -s -v test/ --alluredir=./results",
        update, context
    )

    short_result = "\n".join([line for line in result.split("\n") if "FAILED" in line or "ERROR" in line])
    await update.message.reply_text(
        f"📊 Результаты тестов:\n{short_result[:3000]}" if short_result else "✅ Все тесты прошли успешно!"
    )

    await generate_allure_report(update, context)

async def run_api_tests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запуск API тестов (заглушка)"""
    await update.message.reply_text("⚠️ API тесты пока не добавлены в проект")


async def generate_allure_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Генерация отчета и отправка архива"""
    try:
        results_dir = Path("./results")
        if not results_dir.exists() or not any(results_dir.iterdir()):
            await update.message.reply_text("❌ Нет данных для отчета: папка results пуста или отсутствует")
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
                f"⚠️ Allure CLI не установлен или ошибка генерации.\n"
                f"Отправляю сырые результаты тестов.\n\n"
                f"Ошибка: {gen_result[:500]}"
            )

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
                    caption="📊 Результаты тестов (сырые Allure данные)"
                )

            os.remove(zip_name)
            return

        await update.message.reply_text("📦 Создаю архив...")
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

        await update.message.reply_text("📤 Отправляю архив...")
        with open(zip_name, 'rb') as zip_file:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=zip_file,
                filename=zip_name,
                caption="📊 Allure Report (включая исходные данные)"
            )

        os.remove(zip_name)
        await update.message.reply_text("✅ Отчет успешно отправлен!")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Критическая ошибка: {str(e)}")


async def full_cycle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Полный цикл: все тесты + Allure отчет"""
    await run_all_tests(update, context)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['running_process'] = None
    keyboard = [
        [KeyboardButton("🚀 Запустить все тесты"), KeyboardButton("⏹ Стоп")],
        [KeyboardButton("🧪 Запустить UI тесты")],
        [KeyboardButton("📊 Получить Allure отчет")],
        [KeyboardButton("ℹ️ О проекте")],
        [KeyboardButton("📂 GitHub")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='👋 Добро пожаловать в бот для запуска автотестов!\n\nВыберите действие:',
        reply_markup=reply_markup
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = (
        "📋 Дипломный проект: UI автотесты\n\n"
        "🎯 Тестируемый сайт: itstep.by (IT Академия ШАГ)\n\n"
        "✅ Что проверяется:\n"
        "• Навигация (Вакансии, Контакты, Мероприятия, Статьи)\n"
        "• Меню IT ОБРАЗОВАНИЕ (6 курсов)\n"
        "• Программы для детей (7-8, 9-11, 12-13 лет)\n"
        "• Слайдер и кнопки\n"
        "• Форма обратной связи и чат\n"
        "• Контактная информация\n"
        "• Карточки курсов и отзывов\n"
        "• Проверка на JS ошибки\n\n"
        "🛠 Технологии:\n"
        "• Python + Selenium\n"
        "• Pytest + Allure\n"
        "• Паттерн Page Object Model\n"
        "• Telegram бот для управления тестами"
    )
    await update.message.reply_text(about_text)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текстовых сообщений (кнопок)"""
    text = update.message.text

    if text == "🚀 Запустить все тесты":
        await run_all_tests(update, context)
    elif text == "🧪 Запустить UI тесты":
        await run_ui_tests(update, context)
    elif text == "📊 Получить Allure отчет":
        await generate_allure_report(update, context)
    elif text == "ℹ️ О проекте":
        await about(update, context)
    elif text == "📂 GitHub":
        await update.message.reply_text(
            "🔗 GitHub проекта:\nhttps://github.com/your-repo/diplom_andrey_kundelev"
        )
    elif text == "⏹ Стоп":
        proc = context.user_data.get('running_process')
        if proc and proc.returncode is None:
            proc.kill()
            context.user_data['running_process'] = None
            await update.message.reply_text("⛔ Тесты остановлены!")
        else:
            await update.message.reply_text("ℹ️ Нет запущенных тестов")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ошибок"""
    await update.message.reply_text(f"⚠️ Произошла ошибка: {context.error}")


def main():
    application = Application.builder().token('7683227185:AAHjeK3ScoB9b51hm82O55JXBYbPWwWTx1c').build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("run_all_test", run_all_tests))
    application.add_handler(CommandHandler("run_ui_test", run_ui_tests))
    application.add_handler(CommandHandler("run_api_test", run_api_tests))
    application.add_handler(CommandHandler("allurereport", generate_allure_report))
    application.add_handler(CommandHandler("fullreport", full_cycle))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.add_error_handler(error_handler)

    application.run_polling()


if __name__ == "__main__":
    main()