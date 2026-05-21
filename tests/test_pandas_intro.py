import sys
import os
import shutil
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pathlib import Path
import pandas as pd
from pandas_intro import load_sales, total_quantity, total_revenue, save_to_csv

DATA_DIR = Path(__file__).parent.parent / "data"
TEST_DIR = Path(__file__).parent / "temp"


def setup_function():
    if TEST_DIR.exists():
        shutil.rmtree(TEST_DIR)
    TEST_DIR.mkdir(parents=True)


def teardown_function():
    if TEST_DIR.exists():
        shutil.rmtree(TEST_DIR)


# --- load_sales ---

def test_load_sales_returns_dataframe():
    df = load_sales(DATA_DIR / "sales.xlsx")
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 6

def test_load_sales_columns():
    df = load_sales(DATA_DIR / "sales.xlsx")
    assert list(df.columns) == ["product", "category", "quantity", "unit_price"]

def test_load_sales_nonexistent_returns_none():
    assert load_sales(TEST_DIR / "brak.xlsx") is None


# # --- total_quantity ---

def test_total_quantity():
    df = load_sales(DATA_DIR / "sales.xlsx")
    assert total_quantity(df) == 76  # 5+20+8+3+15+25

def test_total_quantity_returns_int():
    df = load_sales(DATA_DIR / "sales.xlsx")
    result = total_quantity(df)
    assert isinstance(result, int)
    assert not isinstance(result, bool)  # bool to też int w Pythonie!


# # --- total_revenue ---

def test_total_revenue():
    df = load_sales(DATA_DIR / "sales.xlsx")
    # 5*3500 + 20*89 + 8*750 + 3*1200 + 15*220 + 25*110
    expected = 17500 + 1780 + 6000 + 3600 + 3300 + 2750
    assert total_revenue(df) == expected


# # --- save_to_csv ---

def test_save_to_csv_creates_file():
    df = load_sales(DATA_DIR / "sales.xlsx")
    out = TEST_DIR / "out.csv"
    assert save_to_csv(df, out) is True
    assert out.exists()

def test_save_to_csv_content_matches():
    df = load_sales(DATA_DIR / "sales.xlsx")
    out = TEST_DIR / "out.csv"
    save_to_csv(df, out)

    # Wczytujemy CSV z powrotem i porównujemy
    df_back = pd.read_csv(out)
    assert len(df_back) == 6
    assert list(df_back.columns) == ["product", "category", "quantity", "unit_price"]