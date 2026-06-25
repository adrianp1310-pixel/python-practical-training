from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Weather API działa"}


def test_get_weather():
    response = client.get("/weather/Warszawa")
    assert response.status_code == 200
    assert response.json()["city"] == "Warszawa"


def test_create_weather():
    payload = {"city": "Kraków", "temperature": 18.5, "windspeed": 12.0}
    response = client.post("/weather", json=payload)
    assert response.status_code == 200
    assert response.json() == payload


def test_create_weather_invalid_type():
    payload = {"city": "Kraków", "temperature": "ciepło", "windspeed": 12.0}
    response = client.post("/weather", json=payload)
    assert response.status_code == 422