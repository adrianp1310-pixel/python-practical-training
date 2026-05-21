import requests
import csv
from pathlib import Path
import json

DATA_DIR = Path(__file__).parent.parent / "data"


def get_current_weather(latitude: float, longitude: float) -> dict | None:
    """
    Zwraca słownik z danymi w formacie JSON.

    Args:
        latitude: szerokość geograficzna.
        longitude: długość geograficzna.

    Returns:
        dict | None: słownik z danymi pogodowymi lub None
        gdy status != 200 lub wystąpi błąd sieci.
    """
    try:
        params = {"latitude": latitude,
                  "longitude": longitude,
                  "current_weather": True,
        }
        response = requests.get("https://api.open-meteo.com/v1/forecast",
            params=params, timeout=10
        )
        if response.status_code != 200:
            return None
        return response.json()
    except requests.exceptions.RequestException:
        return None


def parse_weather(data: dict) -> dict | None:
    """
    Wyciąga i zwraca nowy płaski słownik danych pogodowych.

    Args:
        data: słownik danych do obrobienia.

    Returns:
        dict | None: Nowy słownik z danymi pogodowymi lub None gdy słownika
        nie ma w danych.
    """
    try:
        current_weather = {
            "temperature": data["current_weather"]["temperature"],
            "windspeed": data["current_weather"]["windspeed"],
            "weathercode": data["current_weather"]["weathercode"],
            "time": data["current_weather"]["time"],
        }
        return current_weather
    except KeyError:
        return None


def get_weather(latitude: float, longitude: float) -> dict | None:
    """
    Pobiera dane z API i parsuje je.

    Args:
        latitude: szerokość geograficzna.
        longitude: długość geograficzna.

    Returns:
        dict | None: słownik z danymi pogodowymi lub None
        gdy wystąpi błąd
    """
    current_weather = get_current_weather(latitude, longitude)
    if current_weather is None:
        return None
    parsed_weather = parse_weather(current_weather)
    return parsed_weather


def save_weather_to_csv(data: dict, filepath: str) -> bool:
    """
    Zapisuje dane pogodowe do plik CSV.

    Args:
        data: słownik z danymi pogodowymi.
        filepath: ścieżka do zapisania pliku CSV

    Returns:
        bool: True jeśli zapis się uda. False jeśli wystąpi błąd.
    """
    try:
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            fieldnames = ["temperature", "windspeed", "weathercode", "time"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(data)
        return True
    except OSError:
        return False


def get_weather_for_cities(cities: list) -> list:
    """
    Pobiera dane pogodowe dla listy miast.

    Args:
        cities: Lista miast z szerokościami i długościami geograficznymi.

    Returns:
        list: Nowa lista jeśli dane pogodowe zostaną pobrane (może być pusta).
    """
    weather_for_cities = []
    for city in cities:
        name = city["name"]
        weather = get_weather(city["latitude"], city["longitude"])
        if weather is None:
            continue
        weather["name"] = name
        weather_for_cities.append(weather)
    return weather_for_cities


def save_cities_weather_to_csv(data: list, filepath: str) -> bool:
    """
    Zapisuje dane pogodowe miast do pliku CSV.

    Args:
        data: lista słowników z danymi pogodowymi miast.
        filepath: ścieżka do zapisania pliku CSV

    Returns:
        bool: True jeśli zapis się uda. False jeśli wystąpi błąd.
    """
    try:
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            fieldnames = ["name", "temperature", "windspeed", "weathercode", "time"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        return True
    except OSError:
        return False


def save_cities_weather_to_json(data: list, filepath: str) -> bool:
    """
    Zapisuje dane pogodowe miast w formacie JSON.

    Args:
        data: lista słowników z danymi pogodowymi miast.
        filepath: ścieżka do zapisania pliku JSON.

    Returns:
        bool: True jeśli zapis się uda. False jeśli wystąpi błąd.
    """
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except OSError:
        return False


if __name__ == "__main__":
    cities = [
        {"name": "Warszawa", "latitude": 52.23, "longitude": 21.01},
        {"name": "Kraków", "latitude": 50.06, "longitude": 19.94},
        {"name": "Gdańsk", "latitude": 54.35, "longitude": 18.65},
    ]
    data = get_weather_for_cities(cities)
    if not data:
        print("Brak danych pogodowych")
    else:
        DATA_DIR.mkdir(exist_ok=True)
        result = save_cities_weather_to_json(data, DATA_DIR / "weather.json")
        print(result)