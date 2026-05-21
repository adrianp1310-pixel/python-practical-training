import pandas as pd
from pathlib import Path


def load_sales(path: Path) -> pd.DataFrame | None:
    """
    Wczytuje arkusz sprzedaży z pliku Excel.

    Args:
        path: Ścieżka do pliku .xlsx.

    Returns:
        DataFrame z danymi. None jeśli plik nie istnieje.
    """
    try:
        return pd.read_excel(path)
    except FileNotFoundError:
        return None


def total_quantity(df: pd.DataFrame) -> int:
    """
    Sumuje wartości w kolumnie 'quantity'.

    Args:
        df: DataFrame z kolumną 'quantity'.

    Returns:
        Suma wszystkich quantity jako int.
    """
    return int(df["quantity"].sum())


def total_revenue(df: pd.DataFrame) -> float:
    """
    Liczy łączny przychód: suma (quantity * unit_price).

    Args:
        df: DataFrame z kolumnami 'quantity' i 'unit_price'.

    Returns:
        Łączny przychód jako float.
    """
    revenue = df["quantity"] * df["unit_price"]
    return float(revenue.sum())


def save_to_csv(df: pd.DataFrame, path: Path) -> bool:
    """
    Zapisuje DataFrame do pliku CSV.

    Args:
        df: DataFrame do zapisania.
        path: Docelowa ścieżka pliku CSV.

    Returns:
        True jeśli zapis się udał, False przy błędzie.
    """
    try:
        df.to_csv(path, index=False)
        return True
    except OSError:
        return False