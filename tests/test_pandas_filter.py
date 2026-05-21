import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pathlib import Path
import pandas as pd
from pandas_intro import load_sales
from pandas_filter import (
    filter_by_category,
    filter_expensive,
    filter_combined,
    revenue_by_category,
    count_by_category,
)

DATA_DIR = Path(__file__).parent.parent / "data"


def get_df():
    return load_sales(DATA_DIR / "sales.xlsx")


# --- filter_by_category ---

def test_filter_by_category_elektronika():
    df = get_df()
    result = filter_by_category(df, "Elektronika")
    assert len(result) == 3
    assert (result["category"] == "Elektronika").all()


def test_filter_by_category_no_match():
    df = get_df()
    result = filter_by_category(df, "NieIstnieje")
    assert len(result) == 0


def test_filter_by_category_does_not_mutate_original():
    df = get_df()
    original_len = len(df)
    filter_by_category(df, "Meble")
    assert len(df) == original_len  # oryginał nietknięty


# --- filter_expensive ---

def test_filter_expensive_threshold():
    df = get_df()
    result = filter_expensive(df, 1000)
    # Laptop 3500, Biurko 1200
    assert len(result) == 2


def test_filter_expensive_inclusive():
    df = get_df()
    # min_price=110 — Lampka LED ma dokładnie 110, powinna być w wyniku
    result = filter_expensive(df, 110)
    assert "Lampka LED" in result["product"].values


# # --- filter_combined ---

def test_filter_combined_basic():
    df = get_df()
    # Elektronika z quantity >= 15: Mysz (20), Klawiatura (15)
    result = filter_combined(df, "Elektronika", 15)
    assert len(result) == 2


def test_filter_combined_no_match():
    df = get_df()
    result = filter_combined(df, "Meble", 100)
    assert len(result) == 0


# # --- revenue_by_category ---

def test_revenue_by_category_columns():
    df = get_df()
    result = revenue_by_category(df)
    assert list(result.columns) == ["category", "revenue"]


def test_revenue_by_category_values():
    df = get_df()
    result = revenue_by_category(df)
    revenues = dict(zip(result["category"], result["revenue"]))
    # Elektronika: 5*3500 + 20*89 + 15*220 = 17500+1780+3300 = 22580
    # Meble: 8*750 + 3*1200 = 6000+3600 = 9600
    # Oświetlenie: 25*110 = 2750
    assert revenues["Elektronika"] == 22580
    assert revenues["Meble"] == 9600
    assert revenues["Oświetlenie"] == 2750


def test_revenue_by_category_sorted_descending():
    df = get_df()
    result = revenue_by_category(df)
    revenues = result["revenue"].tolist()
    assert revenues == sorted(revenues, reverse=True)


def test_revenue_does_not_mutate_original():
    df = get_df()
    original_columns = list(df.columns)
    revenue_by_category(df)
    assert list(df.columns) == original_columns  # bez 'revenue'!


# # --- count_by_category ---
#
# def test_count_by_category_values():
#     df = get_df()
#     result = count_by_category(df)
#     counts = dict(zip(result["category"], result["count"]))
#     assert counts["Elektronika"] == 3
#     assert counts["Meble"] == 2
#     assert counts["Oświetlenie"] == 1
#
#
# def test_count_by_category_sorted_descending():
#     df = get_df()
#     result = count_by_category(df)
#     counts = result["count"].tolist()
#     assert counts == sorted(counts, reverse=True)