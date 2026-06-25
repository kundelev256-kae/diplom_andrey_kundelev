import pytest
from unittest.mock import MagicMock, patch
from page.elements import WebElement, ManyWebElements


class TestWebElementInit:
    """Тесты инициализации WebElement."""

    def test_default_timeout(self):
        elem = WebElement()
        assert elem._timeout == 10

    def test_custom_timeout(self):
        elem = WebElement(timeout=5)
        assert elem._timeout == 5

    def test_default_wait_after_click(self):
        elem = WebElement()
        assert elem._wait_after_click is False

    def test_xpath_locator(self):
        elem = WebElement(xpath="//div[@class='test']")
        assert elem._locator == ("xpath", "//div[@class='test']")

    def test_id_locator(self):
        elem = WebElement(id="my-button")
        assert elem._locator == ("id", "my-button")

    def test_css_selector_locator(self):
        elem = WebElement(css_selector=".btn-primary")
        assert elem._locator == ("css selector", ".btn-primary")

    def test_class_name_locator(self):
        elem = WebElement(class_name="container")
        assert elem._locator == ("class name", "container")

    def test_name_locator(self):
        elem = WebElement(name="email")
        assert elem._locator == ("name", "email")


class TestWebElementFind:
    """Тесты метода find()."""

    def test_find_returns_element(self):
        elem = WebElement(xpath="//div")
        mock_driver = MagicMock()
        mock_element = MagicMock()
        mock_driver.find_element.return_value = mock_element
        elem._web_driver = mock_driver

        with patch("page.elements.WebDriverWait") as mock_wait:
            mock_wait.return_value.until.return_value = mock_element
            result = elem.find()
            assert result is mock_element

    def test_find_returns_none_on_exception(self):
        elem = WebElement(xpath="//div")
        mock_driver = MagicMock()
        elem._web_driver = mock_driver

        with patch("page.elements.WebDriverWait") as mock_wait:
            mock_wait.return_value.until.side_effect = Exception("not found")
            result = elem.find()
            assert result is None


class TestWebElementIsPresented:
    """Тесты метода is_presented()."""

    def test_is_presented_true(self):
        elem = WebElement(xpath="//div")
        mock_driver = MagicMock()
        elem._web_driver = mock_driver

        with patch("page.elements.WebDriverWait") as mock_wait:
            mock_wait.return_value.until.return_value = MagicMock()
            assert elem.is_presented() is True

    def test_is_presented_false(self):
        elem = WebElement(xpath="//div")
        mock_driver = MagicMock()
        elem._web_driver = mock_driver

        with patch("page.elements.WebDriverWait") as mock_wait:
            mock_wait.return_value.until.side_effect = Exception("not found")
            assert elem.is_presented() is False


class TestWebElementIsVisible:
    """Тесты метода is_visible()."""

    def test_is_visible_true(self):
        elem = WebElement(xpath="//div")
        mock_driver = MagicMock()
        mock_element = MagicMock()
        mock_element.is_displayed.return_value = True
        elem._web_driver = mock_driver

        with patch("page.elements.WebDriverWait") as mock_wait:
            mock_wait.return_value.until.return_value = mock_element
            assert elem.is_visible() is True

    def test_is_visible_no_element(self):
        elem = WebElement(xpath="//div")
        mock_driver = MagicMock()
        elem._web_driver = mock_driver

        with patch("page.elements.WebDriverWait") as mock_wait:
            mock_wait.return_value.until.side_effect = Exception("not found")
            assert elem.is_visible() is False


class TestWebElementGetText:
    """Тесты метода get_text()."""

    def test_get_text_returns_string(self):
        elem = WebElement(xpath="//div")
        mock_driver = MagicMock()
        mock_element = MagicMock()
        mock_element.text = "Hello World"
        elem._web_driver = mock_driver

        with patch("page.elements.WebDriverWait") as mock_wait:
            mock_wait.return_value.until.return_value = mock_element
            assert elem.get_text() == "Hello World"

    def test_get_text_returns_empty_on_error(self):
        elem = WebElement(xpath="//div")
        mock_driver = MagicMock()
        elem._web_driver = mock_driver

        with patch("page.elements.WebDriverWait") as mock_wait:
            mock_wait.return_value.until.side_effect = Exception("not found")
            assert elem.get_text() == ""


class TestManyWebElements:
    """Тесты класса ManyWebElements."""

    def test_find_returns_list(self):
        elem = ManyWebElements(xpath="//div")
        mock_driver = MagicMock()
        elem._web_driver = mock_driver

        with patch("page.elements.WebDriverWait") as mock_wait:
            mock_wait.return_value.until.return_value = [MagicMock(), MagicMock()]
            result = elem.find()
            assert isinstance(result, list)
            assert len(result) == 2

    def test_count(self):
        elem = ManyWebElements(xpath="//div")
        mock_driver = MagicMock()
        elem._web_driver = mock_driver

        with patch("page.elements.WebDriverWait") as mock_wait:
            mock_wait.return_value.until.return_value = [MagicMock(), MagicMock(), MagicMock()]
            assert elem.count() == 3

    def test_getitem(self):
        elem = ManyWebElements(xpath="//div")
        mock_driver = MagicMock()
        mock_items = [MagicMock(name="first"), MagicMock(name="second")]
        elem._web_driver = mock_driver

        with patch("page.elements.WebDriverWait") as mock_wait:
            mock_wait.return_value.until.return_value = mock_items
            assert elem[0] is mock_items[0]
            assert elem[1] is mock_items[1]

    def test_set_value_raises(self):
        elem = ManyWebElements(xpath="//div")
        with pytest.raises(TypeError):
            elem._set_value(MagicMock(), "value")

    def test_click_raises(self):
        elem = ManyWebElements(xpath="//div")
        with pytest.raises(TypeError):
            elem.click()
