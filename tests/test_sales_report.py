import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pathlib import Path
import pandas as pd
from sales_cleaner import load_dirty_sales, clean_sales
from sales_report import total_revenue, revenue_per_category, top_products

DATA_DIR = Path(__file__).parent.parent / "data"


def get_clean_df():
    df = load_dirty_sales(DATA_DIR / "sales_dirty.csv")
    return clean_sales(df)


def test_total_revenue():
    df = get_clean_df()
    # Policz w głowie / w arkuszu — powinno wyjść konkretną wartość
    # Po oczyszczeniu: 10 wierszy
    # Laptop Dell 5*3500=17500, Mysz 20*89=1780, Krzesło 8*750=6000,
    # Biurko 3*1200=3600, Klawiatura 15*220=3300, Lampka 25*110=2750,
    # Monitor 7*1800=12600, Słuchawki 12*450=5400, Lampa 4*320=1280,
    # Stół 2*2400=4800
    # Razem: 17500+1780+6000+3600+3300+2750+12600+5400+1280+4800 = 59010
    assert total_revenue(df) == 59010


def test_revenue_per_category_columns():
    df = get_clean_df()
    result = revenue_per_category(df)
    assert list(result.columns) == ["category", "revenue"]


def test_revenue_per_category_sorted():
    df = get_clean_df()
    result = revenue_per_category(df)
    assert result["revenue"].tolist() == sorted(
        result["revenue"].tolist(), reverse=True
    )


def test_top_products_returns_three():
    df = get_clean_df()
    result = top_products(df, n=3)
    assert len(result) == 3


def test_top_products_first_is_laptop():
    df = get_clean_df()
    result = top_products(df, n=3)
    # Laptop Dell ma 5*3500=17500 — najwięcej
    assert result.iloc[0]["product"] == "Laptop Dell"


def test_top_products_default_n_is_three():
    df = get_clean_df()
    result = top_products(df)   # bez argumentu n
    assert len(result) == 3