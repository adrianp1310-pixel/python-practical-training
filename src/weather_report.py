import pandas as pd
from pathlib import Path
from db_pogoda import insert_pogoda, get_engine

DATA_DIR = Path(__file__).parent.parent / "data"


def generate_report(output_path: str | Path) -> bool:
    """
    Czyta dane pogodowe z bazy i zapisuje raport Excel ze średnią temperaturą
    per miasto.
    Ta funkcja NIE woła API - czyta z bazy.

    Args:
        output_path: ścieżka do pliku Excel.

    Returns:
        bool: True gdy raport zapisany, False gdy błąd.
    """
    try:
        engine = get_engine()
        df = pd.read_sql("SELECT * FROM pogoda;", engine)
        result = (df.groupby("miasto")["temperatura"]
                  .mean()
                  .reset_index()
                  .sort_values("temperatura", ascending=False))
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        result.to_excel(output_path, index=False)
        return True
    except OSError:
        return False


if __name__ == "__main__":
    scraped_data = [
        {"miasto": "Warszawa", "temperatura": 18.5, "wiatr": 12.3},
        {"miasto": "Kraków", "temperatura": 16.2, "wiatr": 8.7},
        {"miasto": "Gdańsk", "temperatura": 14.1, "wiatr": 20.5},
        {"miasto": "Warszawa", "temperatura": 20.1, "wiatr": 15.7},
        {"miasto": "Kraków", "temperatura": 18.9, "wiatr": 4.5},
    ]

    if insert_pogoda(scraped_data):
        print("Dane zapisane do bazy")
    else:
        print("Błąd zapisu do bazy")
    if generate_report(DATA_DIR / "raport_pogoda.xlsx"):
        print("Raport wygenerowany")
    else:
        print("Błąd generowania raportu")