import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pathlib import Path
import pandas as pd
from monthly_report import (
    load_monthly_files,
    revenue_by_month,
    best_month,
    top_products_overall,
)

DATA_DIR = Path(__file__).parent.parent / "data" / "monthly"


def get_df():
    return load_monthly_files(DATA_DIR)


# --- load_monthly_files ---

def test_load_returns_dataframe():
    df = get_df()
    assert isinstance(df, pd.DataFrame)


def test_load_has_month_column():
    df = get_df()
    assert "month" in df.columns


def test_load_combines_all_rows():
    df = get_df()
    # 3 pliki: 3 + 4 + 3 wiersze = 10 łącznie
    assert len(df) == 10


def test_load_month_values():
    df = get_df()
    months = set(df["month"].unique())
    assert months == {"january", "february", "march"}


def test_load_missing_folder_returns_none():
    result = load_monthly_files(Path("data/nieistniejacy_folder"))
    assert result is None


# # --- revenue_by_month ---

def test_revenue_by_month_columns():
    df = get_df()
    result = revenue_by_month(df)
    assert list(result.columns) == ["month", "revenue"]


def test_revenue_by_month_sorted():
    df = get_df()
    result = revenue_by_month(df)
    revenues = result["revenue"].tolist()
    assert revenues == sorted(revenues, reverse=True)


def test_revenue_by_month_values():
    df = get_df()
    result = revenue_by_month(df)
    rev = dict(zip(result["month"], result["revenue"]))
    # january: 5*3500 + 20*89 + 8*750 = 17500+1780+6000 = 25280
    # february: 3*3500 + 4*1200 + 15*220 + 25*110 = 10500+4800+3300+2750 = 21350
    # march: 7*1800 + 12*450 + 2*1200 = 12600+5400+2400 = 20400
    assert rev["january"] == 25280
    assert rev["february"] == 21350
    assert rev["march"] == 20400


# --- best_month ---

def test_best_month_returns_string():
    df = get_df()
    result = best_month(df)
    assert isinstance(result, str)


def test_best_month_is_january():
    df = get_df()
    assert best_month(df) == "january"


# # --- top_products_overall ---

def test_top_products_overall_columns():
    df = get_df()
    result = top_products_overall(df)
    assert list(result.columns) == ["product", "revenue"]


def test_top_products_overall_count():
    df = get_df()
    result = top_products_overall(df, n=3)
    assert len(result) == 3


def test_top_products_overall_laptop_first():
    df = get_df()
    result = top_products_overall(df)
    # Laptop Dell: styczeń 5*3500=17500 + luty 3*3500=10500 = 28000
    assert result.iloc[0]["product"] == "Laptop Dell"
    assert result.iloc[0]["revenue"] == 28000