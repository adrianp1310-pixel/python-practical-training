import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


def get_connection() -> psycopg2.extensions.connection:
    """
    Tworzy połączenie z bazą PostgreSQL na podstawie zmiennych z .env.

    Returns:
        psycopg2.extensions.connection: obiekt połączenia z bazą.
    """
    return psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        port=os.environ.get('DB_PORT'),
        dbname=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
    )


def get_engine():
    """
    Tworzy SQLAlchemy engine do połączenia z PostgreSQL.
    Używany przez pandas (read_sql / to_sql).

    Returns:
        Engine: obiekt silnika SQLAlchemy.
    """
    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASSWORD")
    host = os.environ.get("DB_HOST")
    port = os.environ.get("DB_PORT")
    dbname = os.environ.get("DB_NAME")
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    return create_engine(url)


def fetch_all_pogoda() -> list[tuple]:
    """
    Pobiera wszystkie wiersze z tabeli pogoda.

    Returns:
         list[tuple]: lista krotek z danymi pogodowymi.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pogoda')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def insert_pogoda(data: list[dict]) -> bool:
    """
    Zapisuje listę odczytów pogodowych do tabeli pogoda.
    Ta funkcja NIE woła API - dostaje gotowe dane.

    Args:
        data: lista słowników z kluczami miasto, temperatura, wiatr.

    Returns:
        bool: True gdy zapis się udał, False gdy błąd.
    """
    try:
        rows = [(d["miasto"], d["temperatura"], d["wiatr"]) for d in data]
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.executemany("INSERT INTO pogoda (miasto, temperatura, "
                                   "wiatr) VALUES (%s, %s, %s);", rows)
                conn.commit()
        return True
    except psycopg2.Error:
        return False


def srednia_temperatura_per_miasto() -> pd.DataFrame:
    """
    Czyta dane z tabeli pogoda i liczy średnią temperaturę per miasto.
    Ta funckja NIE woła API - czyta z bazy.

    Returns:
        pd.DataFrame: kolumny miasto, srednia_temp, posortowane malejąco.
    """
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM pogoda;", engine)
    result = (df.groupby("miasto")["temperatura"]
              .mean()
              .reset_index()
              .sort_values("temperatura", ascending=False))
    return result


if __name__ == '__main__':
    result = srednia_temperatura_per_miasto()
    print(result)

