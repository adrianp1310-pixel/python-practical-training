import shutil
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from pathlib import Path
import pandas as pd
from excel_report import (save_report, style_header, set_column_widths, 
                          freeze_header, stripe_rows, add_borders,
                          auto_fit_columns)

TEST_DIR = Path(__file__).parent / "temp"


def setup_function():
    TEST_DIR.mkdir(parents=True, exist_ok=True)


def teardown_function():
    shutil.rmtree(TEST_DIR)


def pomocniczy_df():
    return pd.DataFrame([
        {"product": "Laptop", "category": "Elektronika", "revenue": 17500},
    ])


def test_save_report_creates_file():
    path = TEST_DIR / "raport.xlsx"
    df = pomocniczy_df()
    save_report(df, path)
    assert path.exists()


def test_save_report_return_true():
    path = TEST_DIR / "raport.xlsx"
    df = pomocniczy_df()
    result = save_report(df, path)
    assert result is True


def test_style_header_returns_true():
    path = TEST_DIR / "raport.xlsx"
    df = pomocniczy_df()
    save_report(df, path)
    result = style_header(path)
    assert result is True


def test_style_header_missing_file_returns_false():
    path = TEST_DIR / "nieistniejący.xlsx"
    result = style_header(path)
    assert result is False


def test_set_column_widths_returns_true():
    path = TEST_DIR / "raport.xlsx"
    df = pomocniczy_df()
    save_report(df, path)
    result = set_column_widths(path, {"A": 20, "B": 15, "C": 12})
    assert result is True
    
    
def test_freeze_header_returns_true():
    path = TEST_DIR / "raport.xlsx"
    df = pomocniczy_df()
    save_report(df, path)
    result = freeze_header(path)
    assert result is True

def test_stripe_rows_returns_true():
    path = TEST_DIR / "raport.xlsx"
    df = pomocniczy_df()
    save_report(df, path)
    result = stripe_rows(path)
    assert result is True


def test_add_borders_returns_true():
    path = TEST_DIR / "raport.xlsx"
    df = pomocniczy_df()
    save_report(df, path)
    result = add_borders(path)
    assert result is True


def test_auto_fit_columns_returns_true():
    path = TEST_DIR / "raport.xlsx"
    df = pomocniczy_df()
    save_report(df, path)
    result = auto_fit_columns(path)
    assert result is True
