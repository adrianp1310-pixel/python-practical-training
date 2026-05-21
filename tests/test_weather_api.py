import requests
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from unittest.mock import patch, MagicMock
from weather_api import (get_current_weather, parse_weather, get_weather,
                         save_weather_to_csv, get_weather_for_cities,
                         save_cities_weather_to_csv,
                         save_cities_weather_to_json)


def test_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"temp": 20}
    with patch("weather_api.requests.get", return_value=mock_response):
        result = get_current_weather(52.23, 21.01)
        assert result == {"temp": 20}


def test_not_200():
    mock_response = MagicMock()
    mock_response.status_code = 404
    with patch("weather_api.requests.get", return_value=mock_response):
        result = get_current_weather(52.23, 21.01)
        assert result is None


def test_network_error():
    with patch("weather_api.requests.get",
               side_effect=requests.exceptions.ConnectionError):
        result = get_current_weather(52.23, 21.01)
        assert result is None


def test_parse_success():
    data = {
        "current_weather": {
            "temperature": 10.1,
            "windspeed": 15.8,
            "weathercode": 3,
            "time": "2026-05-13T09:15",
        }
    }
    result = parse_weather(data)
    assert result == {'temperature': 10.1,
                    "windspeed": 15.8,
                    "weathercode": 3,
                    "time": "2026-05-13T09:15",
                    }


def test_parse_missing_key():
    data = {"temperature": 10.1,
        "windspeed": 15.8,
        "weathercode": 3,
        "time": "2026-05-13T09:15",
        }
    result = parse_weather(data)
    assert result is None


def test_save_success(tmp_path):
    data = {"temperature": 10.1,
            "windspeed": 15.8,
            "weathercode": 3,
            "time": "2026-05-13T09:15",
            }
    result = save_weather_to_csv(data, tmp_path / "test.csv")
    assert result is True


def test_save_bad_path():
    data = {"temperature": 10.1,
            "windspeed": 15.8,
            "weathercode": 3,
            "time": "2026-05-13T09:15",
            }
    result = save_weather_to_csv(data, "/brak/takiego/katalogu/test.csv")
    assert result is False


def test_timeout():
    with patch("weather_api.requests.get",
               side_effect=requests.exceptions.Timeout):
        result = get_current_weather(52.23, 21.01)
        assert result is None


def test_get_weather_for_cities_returns_all():
    cities = [
            {"name": "Warszawa", "latitude": 52.23, "longitude": 21.01},
            {"name": "Kraków", "latitude": 50.06, "longitude": 19.94},
            ]
    fake_weather = {"temperature": 10.0,
                    "windspeed": 5.0,
                    "weathercode": 3,
                    "time": "2026-05-14T10:00"
                    }

    with patch("weather_api.get_weather", return_value=fake_weather):
        result = get_weather_for_cities(cities)
        assert len(result) == 2


def test_get_weather_for_cities_returns_one_city():
    cities = [
            {"name": "Warszawa", "latitude": 52.23, "longitude": 21.01},
            {"name": "Kraków", "latitude": 50.06, "longitude": 19.94},
            ]
    fake_weather = {"temperature": 10.0,
                    "windspeed": 5.0,
                    "weathercode": 3,
                    "time": "2026-05-14T10:00"
                    }

    with patch("weather_api.get_weather", side_effect=[fake_weather, None]):
        result = get_weather_for_cities(cities)
        assert len(result) == 1


def test_get_weather_for_cities_returns_all_none():
    cities = [
            {"name": "Warszawa", "latitude": 52.23, "longitude": 21.01},
            {"name": "Kraków", "latitude": 50.06, "longitude": 19.94},
            ]

    with patch("weather_api.get_weather", side_effect=[None, None]):
        result = get_weather_for_cities(cities)
        assert result == []


def test_save_cities_success(tmp_path):
    data = [
        {"name": "Warszawa", "temperature": 10.0, "windspeed": 5.0,
         "weathercode": 3, "time": "2026-05-14T10:00"},
        {"name": "Kraków", "temperature": 12.0, "windspeed": 8.0,
         "weathercode": 1, "time": "2026-05-14T10:00"},
        ]
    result = save_cities_weather_to_csv(data, tmp_path / "cities.csv")
    assert result is True


def test_save_cities_bad_path():
    data = [
        {"name": "Warszawa", "temperature": 10.0, "windspeed": 5.0,
         "weathercode": 3, "time": "2026-05-14T10:00"},
        {"name": "Kraków", "temperature": 12.0, "windspeed": 8.0,
         "weathercode": 1, "time": "2026-05-14T10:00"},
        ]
    result = save_cities_weather_to_csv(data, "/brak/zla_sciezka.csv")
    assert result is False


def test_save_json_success(tmp_path):
    data = [
        {"name": "Warszawa", "temperature": 10.0, "windspeed": 5.0,
         "weathercode": 3, "time": "2026-05-14T10:00"},
        {"name": "Kraków", "temperature": 12.0, "windspeed": 8.0,
         "weathercode": 1, "time": "2026-05-14T10:00"},
    ]
    result = save_cities_weather_to_json(data, tmp_path / "weather.json")
    assert result is True


def test_save_json_bad_path():
    data = [
        {"name": "Warszawa", "temperature": 10.0, "windspeed": 5.0,
         "weathercode": 3, "time": "2026-05-14T10:00"},
        {"name": "Kraków", "temperature": 12.0, "windspeed": 8.0,
         "weathercode": 1, "time": "2026-05-14T10:00"},
    ]
    result = save_cities_weather_to_json(data, "/brak/weather.json")
    assert result is False