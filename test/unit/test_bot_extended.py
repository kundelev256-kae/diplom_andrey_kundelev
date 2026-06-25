import pytest
import asyncio
import os
import time
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock, mock_open

import bot as bot_module

pytestmark = pytest.mark.asyncio


def make_update(text="test"):
    update = MagicMock()
    update.message = MagicMock()
    update.message.reply_text = AsyncMock()
    update.message.text = text
    update.effective_chat = MagicMock()
    update.effective_chat.id = 123
    return update


def make_context(**extra_user_data):
    context = MagicMock()
    context.user_data = {'running_process': None}
    context.user_data.update(extra_user_data)
    context.bot = MagicMock()
    context.bot.send_document = AsyncMock()
    context.bot.send_message = AsyncMock()
    return context


class TestReportHandler:

    def test_log_message_silenced(self):
        handler = bot_module.ReportHandler.__new__(bot_module.ReportHandler)
        handler.log_message("format", "arg1")
        assert True


class TestStartReportServer:

    @patch("bot.HTTPServer")
    @patch("bot.threading.Thread")
    def test_creates_server(self, mock_thread, mock_http):
        bot_module.report_server = None
        bot_module.start_report_server("/tmp/test_report", port=9999)
        mock_http.assert_called_once()
        mock_thread.assert_called_once()

    @patch("bot.HTTPServer")
    @patch("bot.threading.Thread")
    def test_replaces_existing_server(self, mock_thread, mock_http):
        old_server = MagicMock()
        bot_module.report_server = old_server
        bot_module.start_report_server("/tmp/test_report", port=9999)
        old_server.shutdown.assert_called_once()

    @patch("bot.HTTPServer")
    @patch("bot.threading.Thread")
    def test_shutdown_error_ignored(self, mock_thread, mock_http):
        old_server = MagicMock()
        old_server.shutdown.side_effect = Exception("already stopped")
        bot_module.report_server = old_server
        bot_module.start_report_server("/tmp/test_report", port=9999)
        assert bot_module.report_server is not None
        bot_module.report_server = None


class TestExecuteCommand:

    @pytest.mark.asyncio
    async def test_success_command(self):
        update = make_update()
        context = make_context()
        result = await bot_module.execute_command("echo hello", update, context)
        assert "hello" in result
        assert "STDOUT" in result

    @pytest.mark.asyncio
    async def test_stderr_output(self):
        update = make_update()
        context = make_context()
        result = await bot_module.execute_command("echo err >&2", update, context)
        assert "STDERR" in result
        assert "err" in result

    @pytest.mark.asyncio
    async def test_timeout(self):
        update = make_update()
        context = make_context()
        result = await bot_module.execute_command("sleep 100", update, context, timeout=1)
        assert "Таймаут" in result

    @pytest.mark.asyncio
    async def test_process_saved_to_user_data(self):
        update = make_update()
        context = make_context()
        await bot_module.execute_command("echo ok", update, context)
        assert context.user_data['running_process'] is None

    @pytest.mark.asyncio
    async def test_invalid_command(self):
        update = make_update()
        context = make_context()
        result = await bot_module.execute_command("nonexistent_command_xyz", update, context)
        assert "Ошибка" in result or "STDERR" in result


class TestAbout:

    @pytest.mark.asyncio
    async def test_about_sends_text(self):
        update = make_update()
        context = make_context()
        await bot_module.about(update, context)
        update.message.reply_text.assert_called_once()
        text = update.message.reply_text.call_args[0][0]
        assert "Дипломный проект" in text
        assert "UI тесты" in text
        assert "API тесты" in text


class TestAiStartStop:

    @pytest.mark.asyncio
    async def test_ai_start(self):
        update = make_update()
        context = make_context()
        await bot_module.ai_start(update, context)
        assert context.user_data['ai_mode'] is True
        assert context.user_data['ai_history'] == []

    @pytest.mark.asyncio
    async def test_ai_stop(self):
        update = make_update()
        context = make_context(ai_mode=True, ai_history=[{"user": "hi", "bot": "hello"}])
        await bot_module.ai_stop(update, context)
        assert context.user_data['ai_mode'] is False
        assert context.user_data['ai_history'] == []


class TestHandleAiMessage:

    @pytest.mark.asyncio
    async def test_returns_false_when_ai_off(self):
        update = make_update()
        context = make_context()
        result = await bot_module.handle_ai_message(update, context, "hello")
        assert result is False

    @pytest.mark.asyncio
    @patch("bot.query_ai", return_value="AI response")
    async def test_returns_true_when_ai_on(self, mock_qa):
        update = make_update()
        context = make_context(ai_mode=True, ai_history=[])
        result = await bot_module.handle_ai_message(update, context, "hello")
        assert result is True
        mock_qa.assert_called_once()
        call_args = mock_qa.call_args
        assert call_args[0][0] == "hello"
        assert context.user_data['ai_history'] == [{"user": "hello", "bot": "AI response"}]

    @pytest.mark.asyncio
    @patch("bot.query_ai", return_value="resp")
    async def test_history_limited_to_10(self, mock_qa):
        history = [{"user": f"q{i}", "bot": f"a{i}"} for i in range(10)]
        update = make_update()
        context = make_context(ai_mode=True, ai_history=history)
        await bot_module.handle_ai_message(update, context, "new")
        assert len(context.user_data['ai_history']) == 10

    @pytest.mark.asyncio
    @patch("bot.query_ai", return_value="resp")
    async def test_ai_message_sends_reply(self, mock_qa):
        update = make_update()
        context = make_context(ai_mode=True, ai_history=[])
        await bot_module.handle_ai_message(update, context, "question")
        calls = [c[0][0] for c in update.message.reply_text.call_args_list]
        assert any("Думаю" in c for c in calls)
        assert any("resp" in c for c in calls)


class TestStart:

    @pytest.mark.asyncio
    async def test_start_sends_keyboard(self):
        update = make_update()
        context = make_context()
        await bot_module.start(update, context)
        context.bot.send_message.assert_called_once()
        call_kwargs = context.bot.send_message.call_args[1]
        assert call_kwargs['chat_id'] == 123
        assert "Добро пожаловать" in call_kwargs['text']
        assert 'reply_markup' in call_kwargs

    @pytest.mark.asyncio
    async def test_start_initializes_user_data(self):
        update = make_update()
        context = make_context()
        await bot_module.start(update, context)
        assert context.user_data['running_process'] is None


class TestHandleMessage:

    @pytest.mark.asyncio
    async def test_route_to_run_all(self):
        update = make_update(text="🚀 Все тесты (UI+API)")
        context = make_context()
        with patch("bot.run_all_tests", new_callable=AsyncMock) as mock_run:
            await bot_module.handle_message(update, context)
            mock_run.assert_called_once()

    @pytest.mark.asyncio
    async def test_route_to_ui_tests(self):
        update = make_update(text="🧪 UI тесты")
        context = make_context()
        with patch("bot.run_ui_tests", new_callable=AsyncMock) as mock_run:
            await bot_module.handle_message(update, context)
            mock_run.assert_called_once()

    @pytest.mark.asyncio
    async def test_route_to_api_tests(self):
        update = make_update(text="🔌 API тесты")
        context = make_context()
        with patch("bot.run_api_tests", new_callable=AsyncMock) as mock_run:
            await bot_module.handle_message(update, context)
            mock_run.assert_called_once()

    @pytest.mark.asyncio
    async def test_route_to_load_tests(self):
        update = make_update(text="⚡ Нагрузочные тесты")
        context = make_context()
        with patch("bot.run_load_tests", new_callable=AsyncMock) as mock_run:
            await bot_module.handle_message(update, context)
            mock_run.assert_called_once()

    @pytest.mark.asyncio
    async def test_route_to_configure_load(self):
        update = make_update(text="⚙️ Настроить нагрузку")
        context = make_context()
        with patch("bot.configure_load_tests", new_callable=AsyncMock) as mock_run:
            await bot_module.handle_message(update, context)
            mock_run.assert_called_once()

    @pytest.mark.asyncio
    async def test_route_to_serve_report(self):
        update = make_update(text="🌐 Открыть Allure отчет")
        context = make_context()
        with patch("bot.serve_report", new_callable=AsyncMock) as mock_run:
            await bot_module.handle_message(update, context)
            mock_run.assert_called_once()

    @pytest.mark.asyncio
    async def test_route_to_generate_report(self):
        update = make_update(text="📦 Скачать отчет")
        context = make_context()
        with patch("bot.generate_and_serve_report", new_callable=AsyncMock) as mock_run:
            await bot_module.handle_message(update, context)
            mock_run.assert_called_once()

    @pytest.mark.asyncio
    async def test_route_to_about(self):
        update = make_update(text="ℹ️ О проекте")
        context = make_context()
        with patch("bot.about", new_callable=AsyncMock) as mock_run:
            await bot_module.handle_message(update, context)
            mock_run.assert_called_once()

    @pytest.mark.asyncio
    async def test_route_to_ai_start(self):
        update = make_update(text="🤖 Нейросеть (ON)")
        context = make_context()
        with patch("bot.ai_start", new_callable=AsyncMock) as mock_run:
            await bot_module.handle_message(update, context)
            mock_run.assert_called_once()

    @pytest.mark.asyncio
    async def test_route_to_ai_stop(self):
        update = make_update(text="🤖 Нейросеть (OFF)")
        context = make_context()
        with patch("bot.ai_stop", new_callable=AsyncMock) as mock_run:
            await bot_module.handle_message(update, context)
            mock_run.assert_called_once()

    @pytest.mark.asyncio
    async def test_stop_with_running_process(self):
        proc = MagicMock()
        proc.returncode = None
        update = make_update(text="⏹ Стоп")
        context = make_context(running_process=proc)
        await bot_module.handle_message(update, context)
        proc.kill.assert_called_once()
        update.message.reply_text.assert_called_once()
        text = update.message.reply_text.call_args[0][0]
        assert "остановлены" in text

    @pytest.mark.asyncio
    async def test_stop_no_process(self):
        update = make_update(text="⏹ Стоп")
        context = make_context()
        await bot_module.handle_message(update, context)
        text = update.message.reply_text.call_args[0][0]
        assert "Нет запущенных" in text

    @pytest.mark.asyncio
    async def test_stop_finished_process(self):
        proc = MagicMock()
        proc.returncode = 0
        update = make_update(text="⏹ Стоп")
        context = make_context(running_process=proc)
        await bot_module.handle_message(update, context)
        text = update.message.reply_text.call_args[0][0]
        assert "Нет запущенных" in text


class TestLoadTestConfig:

    @pytest.mark.asyncio
    async def test_configure_load_tests_sets_state(self):
        update = make_update()
        context = make_context()
        await bot_module.configure_load_tests(update, context)
        assert context.user_data['loadtest_state'] == 'waiting_users'

    @pytest.mark.asyncio
    async def test_handle_message_waiting_users_valid(self):
        update = make_update(text="5")
        context = make_context(loadtest_state='waiting_users')
        await bot_module.handle_message(update, context)
        assert context.user_data['loadtest_users'] == 5
        assert context.user_data['loadtest_state'] == 'waiting_time'

    @pytest.mark.asyncio
    async def test_handle_message_waiting_users_invalid(self):
        update = make_update(text="abc")
        context = make_context(loadtest_state='waiting_users')
        await bot_module.handle_message(update, context)
        text = update.message.reply_text.call_args[0][0]
        assert "Ошибка" in text or "Введите число" in text

    @pytest.mark.asyncio
    async def test_handle_message_waiting_users_out_of_range(self):
        update = make_update(text="200")
        context = make_context(loadtest_state='waiting_users')
        await bot_module.handle_message(update, context)
        text = update.message.reply_text.call_args[0][0]
        assert "Введите число" in text

    @pytest.mark.asyncio
    async def test_handle_message_waiting_time_valid(self):
        update = make_update(text="30s")
        context = make_context(loadtest_state='waiting_time', loadtest_users=5)
        with patch("bot._execute_load_test", new_callable=AsyncMock) as mock_exec:
            await bot_module.handle_message(update, context)
            mock_exec.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_message_waiting_time_invalid(self):
        update = make_update(text="abc")
        context = make_context(loadtest_state='waiting_time')
        await bot_module.handle_message(update, context)
        text = update.message.reply_text.call_args[0][0]
        assert "Неверный формат" in text

    @pytest.mark.asyncio
    async def test_handle_message_waiting_time_minutes(self):
        update = make_update(text="2m")
        context = make_context(loadtest_state='waiting_time', loadtest_users=10)
        with patch("bot._execute_load_test", new_callable=AsyncMock) as mock_exec:
            await bot_module.handle_message(update, context)
            mock_exec.assert_called_once()


class TestHandleMessageAiMode:

    @pytest.mark.asyncio
    @patch("bot.query_ai", return_value="response")
    async def test_ai_mode_intercepts_message(self, mock_qa):
        update = make_update(text="hello")
        context = make_context(ai_mode=True, ai_history=[])
        with patch("bot.run_all_tests", new_callable=AsyncMock) as mock_run:
            await bot_module.handle_message(update, context)
            mock_run.assert_not_called()


class TestServeReport:

    @pytest.mark.asyncio
    async def test_no_report_found(self):
        update = make_update()
        context = make_context()
        with patch("bot.Path") as mock_path:
            mock_path.return_value.exists.return_value = False
            await bot_module.serve_report(update, context)
            text = update.message.reply_text.call_args[0][0]
            assert "не сгенерирован" in text

    @pytest.mark.asyncio
    async def test_report_found(self):
        update = make_update()
        context = make_context()
        with patch("bot.Path") as mock_path_cls:
            mock_report_dir = MagicMock()
            mock_report_dir.exists.return_value = True
            mock_index = MagicMock()
            mock_index.exists.return_value = True
            mock_report_dir.__truediv__ = MagicMock(return_value=mock_index)
            mock_path_cls.return_value = mock_report_dir
            with patch("bot.start_report_server"):
                await bot_module.serve_report(update, context)
                update.message.reply_text.assert_called()
                text = update.message.reply_text.call_args[0][0]
                assert "localhost" in text


class TestGenerateAndServeReport:

    @pytest.mark.asyncio
    async def test_no_results_dir(self):
        update = make_update()
        context = make_context()
        with patch("bot.Path") as mock_path:
            mock_path.return_value.exists.return_value = False
            await bot_module.generate_and_serve_report(update, context)
            text = update.message.reply_text.call_args[0][0]
            assert "Нет данных" in text

    @pytest.mark.asyncio
    async def test_empty_results_dir(self):
        update = make_update()
        context = make_context()
        with patch("bot.Path") as mock_path:
            mock_path.return_value.exists.return_value = True
            mock_path.return_value.iterdir.return_value = []
            await bot_module.generate_and_serve_report(update, context)
            text = update.message.reply_text.call_args[0][0]
            assert "Нет данных" in text


class TestErrorHandler:

    @pytest.mark.asyncio
    async def test_error_handler_logs_and_replies(self):
        update = make_update()
        context = make_context()
        context.error = Exception("test error")
        with patch("bot.logging") as mock_log:
            await bot_module.error_handler(update, context)
            mock_log.error.assert_called_once()
            text = update.message.reply_text.call_args[0][0]
            assert "Ошибка" in text

    @pytest.mark.asyncio
    async def test_error_handler_no_message(self):
        update = MagicMock()
        update.message = None
        context = make_context()
        context.error = Exception("test error")
        with patch("bot.logging"):
            await bot_module.error_handler(update, context)


class TestLoadTestValidation:

    @pytest.mark.asyncio
    async def test_handle_message_waiting_time_no_suffix(self):
        update = make_update(text="30")
        context = make_context(loadtest_state='waiting_time')
        await bot_module.handle_message(update, context)
        text = update.message.reply_text.call_args[0][0]
        assert "Неверный формат" in text

    @pytest.mark.asyncio
    async def test_handle_message_waiting_time_float(self):
        update = make_update(text="1.5m")
        context = make_context(loadtest_state='waiting_time', loadtest_users=10)
        with patch("bot._execute_load_test", new_callable=AsyncMock) as mock_exec:
            await bot_module.handle_message(update, context)
            mock_exec.assert_called_once()

    @pytest.mark.asyncio
    async def test_spawn_rate_calculation(self):
        context = make_context(loadtest_state='waiting_time', loadtest_users=50)
        update = make_update(text="30s")
        with patch("bot._execute_load_test", new_callable=AsyncMock) as mock_exec:
            await bot_module.handle_message(update, context)
            call_kwargs = mock_exec.call_args[1]
            assert call_kwargs['users'] == 50
            assert 1 <= call_kwargs['spawn_rate'] <= 10


class TestRunAllTests:

    @pytest.mark.asyncio
    @patch("bot.generate_and_serve_report", new_callable=AsyncMock)
    @patch("bot.execute_command", new_callable=AsyncMock)
    async def test_run_all_tests(self, mock_exec, mock_report):
        mock_exec.return_value = "PASSED 1\nPASSED 2\nFAILED 1"
        update = make_update()
        context = make_context()
        with patch("bot.Path") as mock_path:
            mock_path.return_value.mkdir.return_value = None
            mock_path.return_value.glob.return_value = []
            await bot_module.run_all_tests(update, context)
        assert update.message.reply_text.call_count >= 2
        mock_report.assert_called_once()


class TestRunUiTests:

    @pytest.mark.asyncio
    @patch("bot.generate_and_serve_report", new_callable=AsyncMock)
    @patch("bot.execute_command", new_callable=AsyncMock)
    async def test_run_ui_tests(self, mock_exec, mock_report):
        mock_exec.return_value = "PASSED 3\nPASSED 4"
        update = make_update()
        context = make_context()
        with patch("bot.Path") as mock_path:
            mock_path.return_value.mkdir.return_value = None
            mock_path.return_value.glob.return_value = []
            await bot_module.run_ui_tests(update, context)
        mock_report.assert_called_once()


class TestRunApiTests:

    @pytest.mark.asyncio
    @patch("bot.generate_and_serve_report", new_callable=AsyncMock)
    @patch("bot.execute_command", new_callable=AsyncMock)
    async def test_run_api_tests(self, mock_exec, mock_report):
        mock_exec.return_value = "FAILED 1\nPASSED 1"
        update = make_update()
        context = make_context()
        with patch("bot.Path") as mock_path:
            mock_path.return_value.mkdir.return_value = None
            mock_path.return_value.glob.return_value = []
            await bot_module.run_api_tests(update, context)
        mock_report.assert_called_once()


class TestRunLoadTests:

    @pytest.mark.asyncio
    @patch("bot._execute_load_test", new_callable=AsyncMock)
    async def test_run_load_tests_defaults(self, mock_exec):
        update = make_update()
        context = make_context()
        await bot_module.run_load_tests(update, context)
        mock_exec.assert_called_once_with(update, context, users=10, spawn_rate=2, run_time="30s")


class TestExecuteLoadTest:

    @pytest.mark.asyncio
    @patch("bot.asyncio.create_subprocess_shell", new_callable=AsyncMock)
    async def test_loadtest_timeout(self, mock_proc):
        mock_proc_obj = AsyncMock()
        mock_proc_obj.communicate.side_effect = asyncio.TimeoutError
        mock_proc.return_value = mock_proc_obj
        update = make_update()
        context = make_context()
        with patch("bot.sys"):
            await bot_module._execute_load_test(update, context, users=5, spawn_rate=1, run_time="10s")
        text = update.message.reply_text.call_args[0][0]
        assert "Таймаут" in text or "нагрузочн" in text

    @pytest.mark.asyncio
    @patch("bot.asyncio.create_subprocess_shell", new_callable=AsyncMock)
    @patch("bot.asyncio.wait_for", new_callable=AsyncMock)
    async def test_loadtest_exception(self, mock_wait, mock_proc):
        mock_proc_obj = AsyncMock()
        mock_proc.return_value = mock_proc_obj
        mock_wait.side_effect = Exception("subprocess error")
        update = make_update()
        context = make_context()
        with patch("bot.sys"):
            await bot_module._execute_load_test(update, context, users=5, spawn_rate=1, run_time="10s")
        text = update.message.reply_text.call_args[0][0]
        assert "Ошибка" in text


class TestGenerateAndServeReportFull:

    @pytest.mark.asyncio
    @patch("bot.os.remove")
    @patch("bot.zipfile.ZipFile")
    @patch("bot.start_report_server")
    @patch("bot.execute_command", new_callable=AsyncMock)
    async def test_full_report_generation(self, mock_exec, mock_server, mock_zip, mock_remove):
        mock_exec.return_value = ""
        update = make_update()
        context = make_context()
        with patch("bot.Path") as mock_path:
            results = MagicMock()
            results.exists.return_value = True
            results.iterdir.return_value = [MagicMock()]
            report = MagicMock()
            report.exists.return_value = True
            report_index = MagicMock()
            report_index.exists.return_value = True

            def path_side_effect(p):
                if p == "./results":
                    return results
                elif p == "./allure-report":
                    return report
                elif str(p) == str(report / "index.html"):
                    return report_index
                return MagicMock()

            mock_path.side_effect = path_side_effect
            mock_path.return_value.exists.return_value = True
            mock_path.return_value.iterdir.return_value = [MagicMock()]

            with patch("bot.os.walk", return_value=[("./allure-report", [], ["index.html"])]):
                with patch("builtins.open", mock_open(read_data=b"zipcontent")):
                    await bot_module.generate_and_serve_report(update, context)


class TestSendRawResults:

    @pytest.mark.asyncio
    @patch("bot.os.remove")
    @patch("bot.zipfile.ZipFile")
    async def test_send_raw_results(self, mock_zip, mock_remove):
        update = make_update()
        context = make_context()
        results_dir = Path("/tmp/results")
        with patch("bot.os.walk", return_value=[("/tmp/results", [], ["data.json"])]):
            with patch("builtins.open", mock_open(read_data=b"zipcontent")):
                await bot_module.send_raw_results(update, context, results_dir)
        context.bot.send_document.assert_called_once()


class TestMain:

    @patch("bot.Application")
    def test_main_registers_handlers(self, mock_app_cls):
        mock_app = MagicMock()
        mock_builder = MagicMock()
        mock_builder.build.return_value = mock_app
        mock_builder.token.return_value = mock_builder
        mock_app_cls.builder.return_value = mock_builder
        with patch("bot.os.getenv", return_value="fake_token"):
            bot_module.main()
        assert mock_app.add_handler.call_count >= 10
        mock_app.run_polling.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_report_exception(self):
        update = make_update()
        context = make_context()
        with patch("bot.Path") as mock_path:
            mock_path.return_value.exists.side_effect = Exception("disk error")
            await bot_module.generate_and_serve_report(update, context)
            text = update.message.reply_text.call_args[0][0]
            assert "Ошибка" in text


class TestEdgeCases:

    @pytest.mark.asyncio
    async def test_handle_message_unknown_button(self):
        update = make_update(text="Неизвестная кнопка")
        context = make_context()
        await bot_module.handle_message(update, context)
        update.message.reply_text.assert_not_called()

    @pytest.mark.asyncio
    async def test_waiting_users_zero(self):
        update = make_update(text="0")
        context = make_context(loadtest_state='waiting_users')
        await bot_module.handle_message(update, context)
        text = update.message.reply_text.call_args[0][0]
        assert "Введите число" in text

    @pytest.mark.asyncio
    async def test_waiting_users_negative(self):
        update = make_update(text="-5")
        context = make_context(loadtest_state='waiting_users')
        await bot_module.handle_message(update, context)
        text = update.message.reply_text.call_args[0][0]
        assert "Введите число" in text
