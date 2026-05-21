# tests/test_json_handler.py

import sys
import os
import shutil
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pathlib import Path
from json_handler import read_json, write_json, csv_people_to_json, filter_json_by_field

TEST_DIR = Path(__file__).parent / "temp"
DATA_DIR = Path(__file__).parent.parent / "data"


def setup_function():
    if TEST_DIR.exists():
        if TEST_DIR.is_dir():
            shutil.rmtree(TEST_DIR)
        else:
            TEST_DIR.unlink()
    TEST_DIR.mkdir(parents=True)


def teardown_function():
    if TEST_DIR.exists():
        shutil.rmtree(TEST_DIR)


# --- read_json ---

def test_read_json_dict():
    path = TEST_DIR / "data.json"
    path.write_text('{"name": "Anna", "age": 30}', encoding="utf-8")
    result = read_json(path)
    assert result == {"name": "Anna", "age": 30}

def test_read_json_list():
    path = TEST_DIR / "data.json"
    path.write_text('[1, 2, 3]', encoding="utf-8")
    assert read_json(path) == [1, 2, 3]

def test_read_json_nonexistent_returns_none():
    assert read_json(TEST_DIR / "brak.json") is None

def test_read_json_invalid_returns_none():
    path = TEST_DIR / "broken.json"
    path.write_text('{nieprawidłowy json}', encoding="utf-8")
    assert read_json(path) is None


# # --- write_json ---

def test_write_json_dict():
    path = TEST_DIR / "out.json"
    data = {"name": "Anna", "age": 30}
    assert write_json(path, data) is True
    # Czytamy z powrotem przez naszą funkcję
    assert read_json(path) == data

def test_write_json_polish_chars():
    path = TEST_DIR / "out.json"
    write_json(path, {"city": "Łódź"})
    # Polskie znaki mają być widoczne, nie escape'owane
    content = path.read_text(encoding="utf-8")
    assert "Łódź" in content
    assert "\\u" not in content


# # --- csv_people_to_json ---

def test_csv_to_json_creates_file():
    out_path = TEST_DIR / "people.json"
    result = csv_people_to_json(DATA_DIR / "people.csv", out_path)
    assert result is True
    assert out_path.exists()

def test_csv_to_json_content():
    out_path = TEST_DIR / "people.json"
    csv_people_to_json(DATA_DIR / "people.csv", out_path)
    data = read_json(out_path)
    assert isinstance(data, list)
    assert len(data) == 6
    assert data[0]["name"] == "Anna"
    assert isinstance(data[0]["age"], int)
    assert isinstance(data[0]["salary"], int)

def test_csv_to_json_missing_csv_returns_false():
    out_path = TEST_DIR / "people.json"
    result = csv_people_to_json("brak.csv", out_path)
    assert result is False


# # --- filter_json_by_field ---

def test_filter_json_basic():
    path = TEST_DIR / "people.json"
    write_json(path, [
        {"name": "Anna", "city": "Warszawa"},
        {"name": "Bartosz", "city": "Kraków"},
        {"name": "Celina", "city": "Warszawa"},
    ])
    result = filter_json_by_field(path, "city", "Warszawa")
    assert len(result) == 2
    assert all(p["city"] == "Warszawa" for p in result)

def test_filter_json_no_match():
    path = TEST_DIR / "people.json"
    write_json(path, [{"name": "Anna", "city": "Warszawa"}])
    assert filter_json_by_field(path, "city", "Poznań") == []

def test_filter_json_nonexistent_file_returns_none():
    assert filter_json_by_field(TEST_DIR / "brak.json", "city", "X") is None