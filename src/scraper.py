import csv
import sys
import requests
import time
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser


def parse_weather_page(html: str) -> list[dict] | None:
    """
    Parsuje stronę HTML z tabelą pogodową.

    Args:
        html: tekst HTML do sparsowania.

    Returns:
        list[dict] | None: lista słowników z danymi pogodowymi
        lub None gdy nie znajdzie tabeli.
    """
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", class_="weather-data")
    if table is None:
        return None
    rows = table.find_all("tr")
    weather_data = []
    for row in rows[1:]:
        cells = row.find_all("td")
        city = {"miasto": cells[0].text.strip(),
                "temperatura": clean_float(cells[1].text),
                "wiatr": clean_float(cells[2].text),
                }
        weather_data.append(city)
    return weather_data


def parse_city_links(html: str) -> list[dict] | None:
    """
    Wyciąga linki do miast ze strony HTML.

    Args:
        html: tekst HTML do sparsowania.

    Returns:
        list[dict] | None: lista słowników {"miasto": ..., "url": ...}
        lub None gdy nie znajdzie kontenera z linkami.
    """
    soup = BeautifulSoup(html, "html.parser")
    container = soup.find("div", class_="city-links")
    if container is None:
        return None
    links = container.find_all("a", class_="city-link")
    cities = []
    for link in links:
        city = {"miasto": link.text, "url": link["href"]}
        cities.append(city)
    return cities


def fetch_weather_page(url: str) -> str | None:
    """
    Pobiera stronę HTML z podanego adresu.

    Args:
        url: adres strony do pobrania.

    Returns:
        str | None: tekst HTML strony lub None gdy błąd.
    """
    try:
        headers = {"User-Agent": "WeatherScraper/1.0 (kontakt@example.pl)"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return None


def save_to_csv(data: list, filepath: str) -> bool:
    """
    Zapisuje listę słowników do pliku CSV.

    Args:
        data: lista słowników z danymi do zapisu.
        filepath: ścieżka do pliku CSV.

    Returns:
        bool: True jeśli zapis się udał. False gdy błąd.
    """
    try:
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        return True
    except OSError:
        return False


def clean_float(raw: str) -> float | None:
    """
    Konwertuje tekst na liczbę zmiennoprzecinkową.
    Obsługuje przecinek jako separator, spacje, puste stringi.

    Args:
        raw: surowy tekst z komórki HTML.

    Returns:
        float | None: liczba lub None gdy konwersja niemożliwa.
    """
    try:
        raw = raw.strip()
        if raw == "":
            return None
        raw = raw.replace(",", ".")
        return float(raw)
    except ValueError:
        return None


def scrape_all_cities(main_url: str) -> list[dict]:
    """
    Pobiera stronę główną, wyciąga linki do miast,
    pobiera dane z każdego miasta.

    Args:
        main_url: adres strony głównej z linkami do miast.

    Returns:
        list[dict]: lista słowników z danymi pogodowymi
        ze wszystkich miast. Pusta lista gdy brak danych.
    """
    html = fetch_weather_page(main_url)
    if html is None:
        return []
    cities = parse_city_links(html)
    if cities is None:
        return []
    all_data = []
    for city in cities:
        city_html = fetch_weather_page(city["url"])
        time.sleep(1)
        if city_html is None:
            continue
        data = parse_weather_page(city_html)
        if data is None:
            continue
        all_data.extend(data)
    return all_data


def check_robots(url: str) -> bool:
    """
    Sprawdza czy robots.txt pozwala na scrapowanie danego URL.

    Args:
        url: adres strony do sprawdzenia

    Returns:
        bool: True jeśli można scrapować. False jeśli nie.
    """
    rp = RobotFileParser()
    rp.set_url(url.rstrip("/") + "/robots.txt")
    rp.read()
    return rp.can_fetch("*", url)


if __name__ == "__main__":
    url = "https://example.com/pogoda"
    html = fetch_weather_page(url)
    if html is None:
        print("Pusta strona.")
        sys.exit()
    data = parse_weather_page(html)
    if data is None:
        print("Brak danych do sparsowania.")
        sys.exit()
    result = save_to_csv(data, "pogoda.csv")
    if result is True:
        print("Zapisano do pliku")
    else:
        print("Błąd zapisu")



