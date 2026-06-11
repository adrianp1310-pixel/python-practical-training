import pytest

from validator import validate_email, validate_price, load_config


@pytest.mark.parametrize("raw, expected", [
    ("adrianp1310@gmail.com", "adrianp1310@gmail.com"),
    ("adrianp1310@gmail.com ", "adrianp1310@gmail.com"),
    (" adrianp1310@gmail.com", "adrianp1310@gmail.com"),
    ("adrianp1310@gmail.com.pl", "adrianp1310@gmail.com.pl")
])
def test_valid_email(raw, expected):
    assert validate_email(raw) == expected


@pytest.mark.parametrize("bad_email", [
    "adrianp1310gmail.com",
    "adrianp@1310@gmail.com",
    "adrianp1310@gmailcom"
])
def test_invalid_email(bad_email):
    with pytest.raises(ValueError):
        validate_email(bad_email)


@pytest.mark.parametrize("raw, expected", [
    ("3 499,99", 3499.99),
    ("149.00", 149.0),
])
def test_valid_price(raw, expected):
    assert validate_price(raw) == pytest.approx(expected)


@pytest.mark.parametrize("bad_price", ["abc", "", "-50", "0"])
def test_invalid_price(bad_price):
    with pytest.raises(ValueError):
        validate_price(bad_price)


def test_load_config_full(monkeypatch):
    monkeypatch.setenv("APP_NAME", "TestApp")
    monkeypatch.setenv("APP_DEBUG", "true")
    result = load_config()
    assert result == {"app_name": "TestApp", "debug": True}


def test_load_config_debug_off(monkeypatch):
    monkeypatch.setenv("APP_NAME", "TestApp")
    monkeypatch.setenv("APP_DEBUG", "false")
    result = load_config()
    assert result["debug"] is False


def test_load_config_missing_name(monkeypatch):
    monkeypatch.delenv("APP_NAME", raising=False)
    with pytest.raises(ValueError):
        load_config()