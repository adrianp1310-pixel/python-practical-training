from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Weather(BaseModel):
    city: str
    temperature: float
    windspeed: float


@app.get("/")
def read_root() -> dict:
    """
    Zwraca powitalny komunikat na ścieżce głównej.

    Returns:
        dict: słownik z komunikatem powitalnym.
    """
    return {"message": "Weather API działa"}


@app.get("/weather/{city}", response_model=Weather)
def get_weather(city: str) -> Weather:
    """
    Zwraca symulowane dane pogodowe dla danego miasta.

    Args:
        city: nazwa miasta z parametru ścieżki.

    Returns:
        Weather: model z danymi pogodowymi miasta.
    """
    return Weather(city=city, temperature=20.5, windspeed=10.0)


@app.post("/weather", response_model=Weather)
def create_weather(weather: Weather) -> Weather:
    """
    Przyjmuje dane pogodowe od klienta i zwraca je jako potwierdzenie.
    Ta funkcja NIE woła API ani bazy - przyjmuje gotowe dane z body żądania.

    Args:
        weather: dane pogodowe z ciała żądania, walidowane przez model Weather.

    Returns:
        Weather: przyjęte dane pogodowe jako potwierdzenie.
    """
    return weather


