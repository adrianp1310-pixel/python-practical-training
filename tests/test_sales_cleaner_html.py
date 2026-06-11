import requests
import pytest
from unittest.mock import patch, MagicMock


from sales_cleaner_html import (load_sales_page, parse_sales_page, clean_data,
                                save_to_csv)


@pytest.fixture
def sample_html():
    return """
        <html>
        <body>
          <h1>Raport sprzedaży Q1</h1>
          <table class="sales-report">
            <tr><th>Produkt</th><th>Cena</th><th>Ilość</th></tr>
            <tr><td> Laptop </td><td>3 499,99</td><td>12</td></tr>
            <tr><td>Monitor</td><td>1299,50</td><td></td></tr>
            <tr><td> Klawiatura</td><td>149.00</td><td>45</td></tr>
            <tr><td>Mysz</td><td></td><td>60</td></tr>
          </table>
        </body>
        </html>"""


@patch("sales_cleaner_html.requests.get")
def test_load_sales_page_success(mock_get):
    mock_response = MagicMock()
    mock_response.text = "<html>OK</html>"
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    result = load_sales_page("https://sales.com")
    assert result == "<html>OK</html>"


@patch("sales_cleaner_html.requests.get")
def test_load_sales_page_failure(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException
    result = load_sales_page("https://sales.com")
    assert result is None


def test_parse_sales_page_returns_list(sample_html):
    result = parse_sales_page(sample_html)
    assert len(result) == 4


def test_parse_sales_page_dirty_data(sample_html):
    result = parse_sales_page(sample_html)
    assert result[0]["Produkt"] == "Laptop"
    assert result[0]["Cena"] == 3499.99
    assert result[1]["Ilość"] is None


def test_parse_sales_page_no_table(empty_html):
    result = parse_sales_page(empty_html)
    assert result is None


@pytest.mark.parametrize("raw, expected", [
    ("18 500,50", 18500.50),
    ("", None),
    ("abc", None)
])
def test_clean_data(raw, expected):
    assert clean_data(raw) == expected


def test_save_to_csv(tmp_path):
    data = [{"Produkt": "Laptop", "cena": 3499.99, "Ilość": 12}]
    filepath = tmp_path / "sales.csv"
    result = save_to_csv(data, filepath)
    assert result is True
    assert filepath.exists()

