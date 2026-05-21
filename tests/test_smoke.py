# tests/test_smoke.py
# Cel: pierwszy test w projekcie. Sprawdza funkcje z src/smoke.py.

# Import — bierzemy funkcje z pliku smoke.py w folderze src.
# Jeszcze nie znasz importów — na razie skopiuj to dokładnie tak.
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from smoke import add, greet


def test_add_positive_numbers():
    # Sprawdzamy: czy add(2, 3) zwraca 5?
    result = add(2, 3)
    assert result == 5


def test_add_negative_number():
    # Sprawdzamy: czy add(-1, 1) zwraca 0?
    result = add(-1, 1)
    assert result == 0


def test_greet_returns_string():
    # Sprawdzamy: czy greet("Anna") zwraca "Cześć, Anna!"?
    result = greet("Anna")
    assert result == "Cześć, Anna!"


def test_greet_returns_correct_type():
    # Sprawdzamy: czy wynik greet() jest stringiem?
    result = greet("test")
    assert isinstance(result, str)