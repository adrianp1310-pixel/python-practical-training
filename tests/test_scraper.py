import os
import sys
import requests
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from scraper import (parse_weather_page, parse_city_links,
                     fetch_weather_page, save_to_csv, clean_float,
                     scrape_all_cities)


html = """
<html>
<body>
  <table class="weather-data">
    <tr><th>Miasto</th><th>Temperatura</th><th>Wiatr</th></tr>
    <tr><td>Warszawa</td><td>18.5</td><td>12.3</td></tr>
    <tr><td>Kraków</td><td>16.2</td><td>8.7</td></tr>
  </table>
</body>
</html>
"""

html_none_table = """
<html>
<body>
  None
</body>
</html>
"""

html_2 = """
<html>
<body>
  <div class="city-links">
    <a href="https://pogoda.pl/warszawa" class="city-link">Warszawa</a>
    <a href="https://pogoda.pl/krakow" class="city-link">Kraków</a>
    <a href="https://pogoda.pl/gdansk" class="city-link">Gdańsk</a>
  </div>
</body>
</html>
"""

html_2_none_div = """
<html>
<body>
  None
</body>
</html>
"""

html_3 = """
<html>
<body>
  <table class="weather-data">
    <tr><th>Miasto</th><th>Temperatura</th><th>Wiatr</th></tr>
    <tr><td> Warszawa </td><td>18,5</td><td>12.3</td></tr>
    <tr><td>Kraków</td><td></td><td>8,7</td></tr>
  </table>
</body>
</html>
"""

main_html = """
<html><body>
  <div class="city-links">
    <a href="https://pogoda.pl/warszawa" class="city-link">Warszawa</a>
    <a href="https://pogoda.pl/krakow" class="city-link">Kraków</a>
  </div>
</body></html>
"""

warszawa_html = """
<html><body>
  <table class="weather-data">
    <tr><th>Miasto</th><th>Temperatura</th><th>Wiatr</th></tr>
    <tr><td>Warszawa</td><td>18.5</td><td>12.3</td></tr>
  </table>
</body></html>
"""

krakow_html = """
<html><body>
  <table class="weather-data">
    <tr><th>Miasto</th><th>Temperatura</th><th>Wiatr</th></tr>
    <tr><td>Kraków</td><td>16.2</td><td>8.7</td></tr>
  </table>
</body></html>
"""

def test_parse_weather_page_returns_list():
    result = parse_weather_page(html)
    assert len(result) == 2


def test_parse_weather_page_data_values():
    test = [
    {"miasto": "Warszawa", "temperatura": 18.5, "wiatr": 12.3},
    {"miasto": "Kraków", "temperatura": 16.2, "wiatr": 8.7},
    ]
    result = parse_weather_page(html)
    assert result[0] == test[0]


def test_parse_weather_page_no_table():
    result = parse_weather_page(html_none_table)
    assert result is None


def test_parse_city_links_returns_list():
    result = parse_city_links(html_2)
    assert len(result) == 3


def test_parse_city_links_data_values():
    test = {"miasto": "Warszawa", "url": "https://pogoda.pl/warszawa"}
    result = parse_city_links(html_2)
    assert result[0] == test


def test_parse_city_links_no_container():
    result = parse_city_links(html_2_none_div)
    assert result is None


@patch("scraper.requests.get")
def test_fetch_weather_page_success(mock_get):
    mock_response = MagicMock()
    mock_response.text = "<html>Dane</html>"
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    result = fetch_weather_page("https://pogoda.pl")
    assert result == "<html>Dane</html>"


@patch("scraper.requests.get")
def test_fetch_weather_page_error(mock_get):
    mock_get.side_effect = requests.RequestException("Błąd połączenia")
    result = fetch_weather_page("https://pogoda.pl")
    assert result is None


def test_save_to_csv_success(tmp_path):
    data = [
    {"miasto": "Warszawa", "temperatura": 18.5, "wiatr": 12.3},
    {"miasto": "Kraków", "temperatura": 16.2, "wiatr": 8.7},
    ]
    filepath = tmp_path / "dane.csv"
    result = save_to_csv(data, filepath)
    assert result is True
    assert filepath.exists()


def test_save_to_csv_content(tmp_path):
    data = [
    {"miasto": "Warszawa", "temperatura": 18.5, "wiatr": 12.3},
    {"miasto": "Kraków", "temperatura": 16.2, "wiatr": 8.7},
    ]
    filepath = tmp_path / "dane.csv"
    save_to_csv(data, filepath)
    text = filepath.read_text(encoding="utf-8")
    assert "miasto" in text
    assert "Warszawa" in text


def test_clean_float_normal():
    result = clean_float("18.5")
    assert result == 18.5


def test_clean_float_comma():
    result = clean_float("18,5")
    assert result == 18.5


def test_clean_float_spaces():
    result = clean_float(" 18.5 ")
    assert result == 18.5


def test_clean_float_empty():
    result = clean_float("")
    assert result is None


def test_clean_float_invalid():
    result = clean_float("abc")
    assert result is None


def test_parse_weather_page_dirty_data():
    result = parse_weather_page(html_3)
    assert result[0]["miasto"] == "Warszawa"
    assert result[0]["temperatura"] == 18.5
    assert result[1]["temperatura"] is None


@patch("scraper.fetch_weather_page")
def test_scrape_all_cities(mock_fetch):
    mock_fetch.side_effect = [main_html, warszawa_html, krakow_html]
    result = scrape_all_cities("https://pogoda.pl")
    assert len(result) == 2
    assert result[0]["miasto"] == "Warszawa"
    assert result[1]["miasto"] == "Kraków"


