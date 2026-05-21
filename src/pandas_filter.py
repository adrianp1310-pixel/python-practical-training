import pandas as pd


def filter_by_category(df: pd.DataFrame, category: str) -> pd.DataFrame:
    """
    Zwraca tylko wiersze gdzie kolumna 'category' równa się category.

    Args:
        df: DataFrame z kolumną 'category'.
        category: Nazwa kategorii do filtrowania.

    Returns:
        Nowy DataFrame zawierający tylko pasujące wiersze.
    """
    return df[df["category"] == category]


def filter_expensive(df: pd.DataFrame, min_price: float) -> pd.DataFrame:
    """
    Zwraca produkty z ceną >= min_price.

    Args:
        df: DataFrame z kolumną 'unit_price'.
        min_price: Próg ceny (włącznie).

    Returns:
        Nowy DataFrame z droższymi produktami.
    """
    return df[df["unit_price"] >= min_price]


def filter_combined(
        df: pd.DataFrame,
        category: str,
        min_quantity: int,
) -> pd.DataFrame:
    """
    Zwraca wiersze pasujące do dwóch warunków: category i quantity >= min_quantity.

    Args:
        df: DataFrame z kolumnami 'category' i 'quantity'.
        category: Wymagana kategoria.
        min_quantity: Minimalna ilość (włącznie).

    Returns:
        Nowy DataFrame z wierszami spełniającymi oba warunki.
    """
    return df[
        (df["category"] == category)
        & (df["quantity"] >= min_quantity)
        ]


def revenue_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Liczy łączny przychód per kategoria.

    Przychód wiersza: quantity * unit_price.

    Args:
        df: DataFrame z kolumnami 'category', 'quantity', 'unit_price'.

    Returns:
        DataFrame z kolumnami 'category' i 'revenue', posortowany
        malejąco po 'revenue'.
    """
    revenue = df["quantity"] * df["unit_price"]
    df_copy = (df.assign(revenue=revenue).groupby("category")["revenue"]
               .sum()
               .reset_index()
               .sort_values("revenue", ascending=False)
               )
    return df_copy


def count_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Liczy ile produktów jest w każdej kategorii.

    Args:
        df: DataFrame z kolumną 'category'.

    Returns:
        DataFrame z kolumnami 'category' i 'count', posortowany
        malejąco po 'count'.
    """
    return (df.groupby("category")
            .size().reset_index(name="count")
            .sort_values("count", ascending=False)
            )
