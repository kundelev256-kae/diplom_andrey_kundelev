import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import bot as bot_module


class TestFallbackResponse:
    """Тесты локальных ответов при недоступности API."""

    def test_greeting_detected(self):
        assert bot_module._fallback_response("Привет") == "Привет! Чем могу помочь?"

    def test_greeting_with_punctuation(self):
        assert bot_module._fallback_response("Привет!") == "Привет! Чем могу помочь?"

    def test_how_are_you(self):
        assert bot_module._fallback_response("как дела?") == "Отлично, спасибо! Как у тебя?"

    def test_help(self):
        assert bot_module._fallback_response("помощь") == "Я могу ответить на вопросы. Просто напиши мне!"

    def test_who_are_you(self):
        assert bot_module._fallback_response("кто ты") == "Я Telegram-бот с нейросетью для автотестов."

    def test_hello_english(self):
        assert bot_module._fallback_response("hello") == "Hello! How can I help you?"

    def test_hi_english(self):
        assert bot_module._fallback_response("hi") == "Hi there!"

    def test_unknown_keyword_returns_fallback(self):
        result = bot_module._fallback_response("что-то непонятное")
        assert "непонятное" in result
        assert "API нейросети сейчас недоступен" in result

    def test_case_insensitive(self):
        assert bot_module._fallback_response("ПРИВЕТ") == "Привет! Чем могу помочь?"

    def test_whitespace_stripped(self):
        assert bot_module._fallback_response("  привет  ") == "Привет! Чем могу помочь?"

    def test_partial_match(self):
        result = bot_module._fallback_response("приветик")
        assert result == "Привет! Чем могу помочь?"


class TestQueryAi:
    """Тесты функции запроса к нейросети."""

    @patch("bot.requests.post")
    def test_success_response(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "choices": [{"message": {"content": "Hello from AI"}}]
        }
        mock_post.return_value = mock_resp

        result = bot_module.query_ai("hi")
        assert result == "Hello from AI"
        mock_post.assert_called_once()

    @patch("bot.requests.post")
    def test_unauthorized_fallback(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 401
        mock_post.return_value = mock_resp

        result = bot_module.query_ai("привет")
        assert result == "Привет! Чем могу помочь?"

    @patch("bot.requests.post")
    def test_server_error_fallback(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        mock_post.return_value = mock_resp

        result = bot_module.query_ai("привет")
        assert result == "Привет! Чем могу помочь?"

    @patch("bot.requests.post")
    def test_connection_error_fallback(self, mock_post):
        mock_post.side_effect = bot_module.requests.ConnectionError

        result = bot_module.query_ai("привет")
        assert result == "Привет! Чем могу помочь?"

    @patch("bot.requests.post")
    def test_timeout_returns_message(self, mock_post):
        mock_post.side_effect = bot_module.requests.Timeout

        result = bot_module.query_ai("test")
        assert "Таймаут" in result

    @patch("bot.requests.post")
    def test_unexpected_exception_fallback(self, mock_post):
        mock_post.side_effect = RuntimeError("boom")

        result = bot_module.query_ai("привет")
        assert result == "Привет! Чем могу помочь?"

    @patch("bot.requests.post")
    def test_history_included_in_messages(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "choices": [{"message": {"content": "ok"}}]
        }
        mock_post.return_value = mock_resp

        history = [{"user": "hello", "bot": "hi"}]
        bot_module.query_ai("bye", history=history)

        call_kwargs = mock_post.call_args
        messages = call_kwargs[1]["json"]["messages"]
        assert len(messages) == 4
        assert messages[1]["content"] == "hello"
        assert messages[2]["content"] == "hi"
        assert messages[3]["content"] == "bye"

    @patch("bot.requests.post")
    def test_no_history(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "choices": [{"message": {"content": "ok"}}]
        }
        mock_post.return_value = mock_resp

        bot_module.query_ai("test")

        call_kwargs = mock_post.call_args
        messages = call_kwargs[1]["json"]["messages"]
        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[1]["content"] == "test"


class TestApiKeyAndConfig:
    """Тесты конфигурации API."""

    def test_groq_url_defined(self):
        assert bot_module.GROQ_API_URL == "https://api.groq.com/openai/v1/chat/completions"

    def test_offline_responses_not_empty(self):
        assert len(bot_module.OFFLINE_RESPONSES) > 0

    def test_offline_responses_keys_are_strings(self):
        for key in bot_module.OFFLINE_RESPONSES:
            assert isinstance(key, str)

    def test_offline_responses_values_are_strings(self):
        for val in bot_module.OFFLINE_RESPONSES.values():
            assert isinstance(val, str)
