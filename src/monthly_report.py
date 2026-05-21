import pandas as pd
from pathlib import Path


def load_monthly_files(data_dir: Path) -> pd.DataFrame | None:
    """
    Wczytuje wszystkie pliki CSV z folderu i scala je w jeden DataFrame.

    Każdy plik musi mieć kolumny: product, category, quantity, unit_price.
    Do każdego wiersza dodawana jest kolumna 'month' z nazwą pliku
    bez rozszerzenia (np. "january").

    Args:
        data_dir: Ścieżka do folderu z plikami CSV.

    Returns:
        Scalony DataFrame ze wszystkich plików.
        None jeśli folder nie istnieje lub nie ma w nim plików CSV.
    """
    if not data_dir.exists():
        return None
    csv_files = list(data_dir.glob("*.csv"))
    if not csv_files:
        return None
    frames = []
    for file in csv_files:
        df = pd.read_csv(file)
        df["month"] = file.stem
        frames.append(df)
    return pd.concat(frames, ignore_index=True)



def revenue_by_month(df: pd.DataFrame) -> pd.DataFrame:
    """
    Liczy łączny przychód per miesiąc, posortowany malejąco.

    Args:
        df: Scalony DataFrame z kolumną 'month'.

    Returns:
        DataFrame z kolumnami 'month' i 'revenue', posortowany malejąco.
    """
    revenue = df["quantity"] * df["unit_price"]
    return (df.assign(revenue=revenue)
            .groupby("month")["revenue"]
            .sum()
            .reset_index()
            .sort_values(by="revenue", ascending=False)
    )

def best_month(df: pd.DataFrame) -> str:
    """
    Zwraca nazwę miesiąca z największym przychodem.

    Args:
        df: Scalony DataFrame z kolumną 'month'.

    Returns:
        Nazwa miesiąca jako string (np. "january").
    """
    best = revenue_by_month(df)
    return best.iloc[0]["month"]


def top_products_overall(df: pd.DataFrame, n: int = 3) -> pd.DataFrame:
    """
    Zwraca top-n produktów po łącznym przychodzie przez cały kwartał.

    Ten sam produkt może występować w wielu miesiącach —
    tutaj sumujemy jego przychód przez wszystkie miesiące razem.

    Args:
        df: Scalony DataFrame.
        n: Ile produktów zwrócić (domyślnie 3).

    Returns:
        DataFrame z kolumnami 'product' i 'revenue', n wierszy,
        posortowany malejąco.
    """
    revenue = df["quantity"] * df["unit_price"]
    df_copy = df.assign(revenue=revenue)
    return (df_copy.groupby("product")["revenue"]
            .sum()
            .reset_index()
            .nlargest(n, "revenue"))