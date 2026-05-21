import requests
import csv
import sys
from bs4 import BeautifulSoup


def load_sales_page(url: str) -> str | None:
    """
    Wczytuje stronę z danymi sprzedaży.

    Args:
        url: Adres strony do wczytania.

    Returns:
        str | None: Tekst strony HTML. None jeśli nie uda się wczytać strony.
    """
    try:
        headers = {"User-Agent": "SalesScraper (kontakt@example.pl)"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return None


def parse_sales_page(html: str) -> list[dict] | None:
    """
    Parsuje stronę HTML z danymi sprzedaży.

    Args:
        html: Tekst strony HTML do sparsowania.

    Returns:
        list[dict] | None: Lista słowników z danymi sprzedaży. None jeśli brak
        tabeli.
    """
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", class_="sales-report")
    if table is None:
        return None
    rows = table.find_all("tr")
    sales_data = []
    for row in rows[1:]:
        cells = row.find_all("td")
        sales = {"Produkt": cells[0].text.strip(),
                 "Cena": clean_data(cells[1].text.strip()),
                 "Ilość": clean_data(cells[2].text.strip()),
                 }
        sales_data.append(sales)
    return sales_data


def clean_data(raw: str) -> float | None:
    """
    Konwertuje tekst na liczbę zmiennoprzecinkową, usuwa spacje, zamienia
    przecinek na kropkę

    Args:
        raw: Surowy tekst z komórki HTML.

    Returns:
        float | None: liczba lub None jeśli konwersja niemożliwa.
    """
    try:
        raw = raw.strip()
        if raw == "":
            return None
        raw = raw.replace(" ", "")
        raw = raw.replace(",", ".")
        return float(raw)
    except ValueError:
        return None


def save_to_csv(data: list[dict], filepath: str) -> bool:
    """
    Zapisuje listę słowników do pliku CSV.

    Args:
        data: Lista słowników z danymi do zapisu.
        filepath: ścieżka do pliku CSV.

    Returns:
        bool: True jeśli zapis się udał. False jeśli błąd.
    """
    try:
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        return True
    except OSError:
        return False


if __name__ == "__main__":
    url = "https://sales.com"
    html = load_sales_page(url)
    if html is None:
        print("Pusta strona")
        sys.exit()
    data = parse_sales_page(html)
    if data is None:
        print("Brak danych")
        sys.exit()
    result = save_to_csv(data, "sales.csv")
    if result is True:
        print("Zapisano do pliku")
    else:
        print("Błąd zapisu")