import pandas as pd
from pathlib import Path


def load_dirty_sales(path: Path) -> pd.DataFrame | None:
    """
    Wczytuje surowy plik CSV ze sprzedażą.

    Args:
        path: Ścieżka do pliku CSV.

    Returns:
        DataFrame z surowymi danymi. None jeśli plik nie istnieje.
    """
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        return None


def clean_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    """
    Usuwa białe znaki (spacje, taby) z początków i końców wartości
    w kolumnach tekstowych: 'product' i 'category'.

    Args:
        df: DataFrame z kolumnami 'product' i 'category'.

    Returns:
        Nowy DataFrame z oczyszczonymi tekstami. Oryginał nietknięty.
    """
    df = df.copy()
    df["product"] = df["product"].str.strip()
    df["category"] = df["category"].str.strip()
    return df


def normalize_categories(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ujednolica wielkość liter w kolumnie 'category' do formatu 'Title Case'.

    "ELEKTRONIKA" -> "Elektronika"
    "elektronika" -> "Elektronika"
    "Elektronika" -> "Elektronika"

    Args:
        df: DataFrame z kolumną 'category'.

    Returns:
        Nowy DataFrame z ujednoliconą kategorią. Oryginał nietknięty.
    """
    df = df.copy()
    df["category"] = df["category"].str.capitalize()
    return df


def drop_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Usuwa wiersze gdzie 'product' lub 'category' są puste/NaN.

    Args:
        df: DataFrame.

    Returns:
        Nowy DataFrame bez wierszy z brakami w kluczowych kolumnach.
    """
    df = df.copy()
    df = df.dropna(subset=["product"])
    df = df.dropna(subset=["category"])
    return df


def drop_duplicate_products(df: pd.DataFrame) -> pd.DataFrame:
    """
    Usuwa zduplikowane wiersze (te same product+category+quantity+unit_price).

    Args:
        df: DataFrame.

    Returns:
        Nowy DataFrame bez duplikatów.
    """
    df = df.copy()
    return df.drop_duplicates()


def clean_sales(df: pd.DataFrame) -> pd.DataFrame:
    """
    Główny pipeline czyszczenia. Stosuje wszystkie kroki w kolejności.

    Args:
        df: Surowy DataFrame.

    Returns:
        Wyczyszczony DataFrame gotowy do analizy.
    """
    df = clean_whitespace(df)
    df = normalize_categories(df)
    df = drop_invalid_rows(df)
    df = drop_duplicate_products(df)
    return df