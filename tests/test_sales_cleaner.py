import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pathlib import Path
import pandas as pd
from sales_cleaner import (
    load_dirty_sales,
    clean_whitespace,
    normalize_categories,
    drop_invalid_rows,
    drop_duplicate_products,
    clean_sales,
)

DATA_DIR = Path(__file__).parent.parent / "data"


def test_load_dirty_sales_reads_file():
    df = load_dirty_sales(DATA_DIR / "sales_dirty.csv")
    assert df is not None
    assert len(df) == 13   # wszystkie wiersze, włącznie z pustym i niepełnymi


def test_load_dirty_sales_missing():
    assert load_dirty_sales(DATA_DIR / "brak.csv") is None


def test_clean_whitespace_removes_trailing_space():
    df = pd.DataFrame({
        "product": ["Laptop Dell ", "Mysz "],
        "category": ["Elektronika", "  meble  "],
        "quantity": [5, 20],
        "unit_price": [3500, 89],
    })
    result = clean_whitespace(df)
    assert result["product"].tolist() == ["Laptop Dell", "Mysz"]
    assert result["category"].tolist() == ["Elektronika", "meble"]


def test_clean_whitespace_does_not_mutate():
    df = pd.DataFrame({
        "product": ["Laptop "],
        "category": ["Elektronika"],
        "quantity": [5],
        "unit_price": [3500],
    })
    clean_whitespace(df)
    assert df["product"].iloc[0] == "Laptop "   # oryginał nietknięty


def test_normalize_categories():
    df = pd.DataFrame({
        "category": ["ELEKTRONIKA", "elektronika", "Elektronika", "meble"]
    })
    result = normalize_categories(df)
    assert result["category"].tolist() == ["Elektronika", "Elektronika", "Elektronika", "Meble"]


def test_drop_invalid_rows_removes_empty_product():
    df = pd.DataFrame({
        "product": ["Laptop", None, "Mysz"],
        "category": ["Elektronika", "Meble", "Elektronika"],
        "quantity": [5, 8, 20],
        "unit_price": [3500, 750, 89],
    })
    result = drop_invalid_rows(df)
    assert len(result) == 2


def test_drop_duplicate_products_removes_full_duplicates():
    df = pd.DataFrame({
        "product": ["Laptop", "Laptop", "Mysz"],
        "category": ["Elektronika", "Elektronika", "Elektronika"],
        "quantity": [5, 5, 20],
        "unit_price": [3500, 3500, 89],
    })
    result = drop_duplicate_products(df)
    assert len(result) == 2


# --- pełen pipeline ---

def test_clean_sales_full_pipeline():
    df = load_dirty_sales(DATA_DIR / "sales_dirty.csv")
    cleaned = clean_sales(df)
    # Po wszystkim: 11 prawidłowych wierszy
    # (13 surowych - 2 puste/niepełne - 1 duplikat = 10)
    # Sprawdź sam licząc co Ci zostaje
    assert len(cleaned) == 10


def test_clean_sales_no_uppercase_categories():
    df = load_dirty_sales(DATA_DIR / "sales_dirty.csv")
    cleaned = clean_sales(df)
    # Po normalizacji nie ma już "ELEKTRONIKA" ani "elektronika"
    categories = cleaned["category"].unique().tolist()
    assert "Elektronika" in categories
    assert "ELEKTRONIKA" not in categories
    assert "elektronika" not in categories