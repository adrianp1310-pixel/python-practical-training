import pandas as pd


def total_revenue(df: pd.DataFrame) -> float:
    """
    Liczy łączny przychód: sum(quantity * unit_price).

    Args:
        df: Wyczyszczony DataFrame.

    Returns:
        Łączny przychód jako float.
    """
    revenue = df["quantity"] * df["unit_price"]
    return float(revenue.sum())


def revenue_per_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Łączny przychód per kategoria, posortowany malejąco.

    Args:
        df: Wyczyszczony DataFrame.

    Returns:
        DataFrame z kolumnami 'category', 'revenue', posortowany malejąco.
    """
    revenue = df["quantity"] * df["unit_price"]
    return (df.assign(revenue=revenue)
            .groupby("category")["revenue"]
            .sum()
            .reset_index()
            .sort_values("revenue", ascending=False)
    )


def top_products(df: pd.DataFrame, n: int = 3) -> pd.DataFrame:
    """
    Zwraca top-n produktów po przychodzie (quantity * unit_price).

    Args:
        df: Wyczyszczony DataFrame.
        n: Ile pozycji zwrócić (domyślnie 3).

    Returns:
        DataFrame z kolumnami 'product', 'revenue', n wierszy,
        posortowany malejąco.
    """
    revenue = df["quantity"] * df["unit_price"]
    top = pd.DataFrame({"product": df["product"], "revenue": revenue})
    return top.nlargest(n, "revenue")