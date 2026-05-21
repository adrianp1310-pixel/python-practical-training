import sys
import os
import shutil
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pathlib import Path
from csv_handler import read_people, filter_by_city, total_salary, write_summary

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


# Przykładowe dane testowe
SAMPLE_PEOPLE = [
    {"name": "Anna", "age": 30, "city": "Warszawa", "salary": 8500},
    {"name": "Bartosz", "age": 25, "city": "Kraków", "salary": 6200},
    {"name": "Celina", "age": 35, "city": "Gdańsk", "salary": 9100},
    {"name": "Dawid", "age": 28, "city": "Warszawa", "salary": 7300},
    {"name": "Ewa", "age": 42, "city": "Wrocław", "salary": 11200},
    {"name": "Filip", "age": 31, "city": "Kraków", "salary": 7800},
]


# --- read_people ---

def test_read_people_returns_list_of_dicts():
    result = read_people(DATA_DIR / "people.csv")
    assert isinstance(result, list)
    assert len(result) == 6
    assert isinstance(result[0], dict)

def test_read_people_converts_age_to_int():
    result = read_people(DATA_DIR / "people.csv")
    assert isinstance(result[0]["age"], int)
    assert result[0]["age"] == 30

def test_read_people_converts_salary_to_int():
    result = read_people(DATA_DIR / "people.csv")
    assert isinstance(result[0]["salary"], int)

def test_read_people_nonexistent_returns_none():
    assert read_people("nie_ma_takiego_pliku.csv") is None


# # --- filter_by_city ---

def test_filter_by_city_warsaw():
    result = filter_by_city(SAMPLE_PEOPLE, "Warszawa")
    assert len(result) == 2
    assert all(p["city"] == "Warszawa" for p in result)

def test_filter_by_city_no_match():
    result = filter_by_city(SAMPLE_PEOPLE, "Poznań")
    assert result == []


# # --- total_salary ---

def test_total_salary_full_list():
    assert total_salary(SAMPLE_PEOPLE) == 50100

def test_total_salary_empty_list():
    assert total_salary([]) == 0

def test_total_salary_after_filter():
    warsaw = filter_by_city(SAMPLE_PEOPLE, "Warszawa")
    assert total_salary(warsaw) == 15800


# # --- write_summary ---

def test_write_summary_creates_file():
    path = TEST_DIR / "summary.csv"
    result = write_summary(path, SAMPLE_PEOPLE)
    assert result is True
    assert path.exists()

def test_write_summary_content():
    path = TEST_DIR / "summary.csv"
    write_summary(path, SAMPLE_PEOPLE)
    rows = read_people_summary(path)
    assert {"city": "Warszawa", "total_salary": 15800, "count": 2} in rows
    assert {"city": "Kraków", "total_salary": 14000, "count": 2} in rows
    assert {"city": "Gdańsk", "total_salary": 9100, "count": 1} in rows


def read_people_summary(path):
    """Helper testowy do czytania pliku summary."""
    import csv
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [
            {
                "city": row["city"],
                "total_salary": int(row["total_salary"]),
                "count": int(row["count"]),
            }
            for row in reader
        ]
