# tests/test_file_handler.py

import sys
import os
import shutil
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pathlib import Path
from file_handler import save_text, read_text, read_lines, append_line

TEST_DIR = Path(__file__).parent / "temp"


def setup_function():
    """Czyści i tworzy folder tymczasowy przed każdym testem."""
    if TEST_DIR.exists():
        if TEST_DIR.is_dir():
            shutil.rmtree(TEST_DIR)
        else:
            TEST_DIR.unlink()
    TEST_DIR.mkdir(parents=True)


def teardown_function():
    """Sprząta folder tymczasowy po każdym teście."""
    if TEST_DIR.exists():
        shutil.rmtree(TEST_DIR)


# --- save_text i read_text ---

def test_save_and_read_roundtrip():
    path = TEST_DIR / "test.txt"
    save_text(path, "Witaj świecie")
    assert read_text(path) == "Witaj świecie"

def test_save_overwrites_existing():
    path = TEST_DIR / "test.txt"
    save_text(path, "pierwsza wersja")
    save_text(path, "druga wersja")
    assert read_text(path) == "druga wersja"

def test_read_nonexistent_returns_none():
    path = TEST_DIR / "nie_istnieje.txt"
    assert read_text(path) is None

def test_save_returns_true_on_success():
    path = TEST_DIR / "test.txt"
    assert save_text(path, "cokolwiek") is True


# --- read_lines ---

def test_read_lines_basic():
    path = TEST_DIR / "lines.txt"
    save_text(path, "Anna\nBart\nCelina")
    assert read_lines(path) == ["Anna", "Bart", "Celina"]

def test_read_lines_skips_empty():
    path = TEST_DIR / "lines.txt"
    save_text(path, "Anna\n\nBart\n\nCelina")
    assert read_lines(path) == ["Anna", "Bart", "Celina"]

def test_read_lines_nonexistent_returns_none():
    path = TEST_DIR / "nie_istnieje.txt"
    assert read_lines(path) is None


# --- append_line ---

def test_append_adds_line():
    path = TEST_DIR / "log.txt"
    save_text(path, "linia 1")
    append_line(path, "linia 2")
    assert read_lines(path) == ["linia 1", "linia 2"]

def test_append_creates_file_if_not_exists():
    path = TEST_DIR / "nowy.txt"
    result = append_line(path, "pierwsza linia")
    assert result is True
    assert read_lines(path) == ["pierwsza linia"]