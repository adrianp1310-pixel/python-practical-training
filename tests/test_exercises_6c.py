import os
import pytest


def divide(a: float, b: float) -> float:
    """ Dzieli a przez b. Rzuca ValueError gdy b==0."""
    if b == 0:
        raise ValueError
    return a / b


def test_divide_success():
    assert divide(10, 2) == 5.0


def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)


def test_approx_sum():
    lst = [0.1, 0.2, 0.3]
    assert sum(lst) == pytest.approx(0.6)


def get_api_key() -> str | None:
    """Zwraca klucz API ze zmiennej środowiskowej API_KEY"""
    return os.environ.get("API_KEY")


def test_api_key_exists(monkeypatch):
    monkeypatch.setenv("API_KEY", "abc123")
    assert get_api_key() == "abc123"


def test_api_key_missing(monkeypatch):
    monkeypatch.delenv("API_KEY", raising=False)
    assert get_api_key() is None