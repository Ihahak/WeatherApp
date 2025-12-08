import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from freezegun import freeze_time

from app.services.weather_api import get_forecast, get_forecast_by_city, get_weather_now, get_weather_now_by_city, Cities

# --- Pzykładowe dane API ---

MOCK_API_RESPONSE = {
    "daily": {
        "time": ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", "2025-01-05", "2025-01-06", "2025-01-07"],
        "temperature_2m_max": [5, 6, 7, 8, 9, 10, 11],
        "temperature_2m_min": [-1, 0, 1, 2, 3, 4, 5],
        "precipitation_probability_max": [10, 20, 30, 40, 50, 60, 70],
        "wind_speed_10m_max": [3, 4, 5, 6, 7, 8, 9],
        "uv_index_max": [1, 2, 3, 4, 5, 6, 7],
        "sunrise": ["07:00"] * 7,
        "sunset": ["16:00"] * 7
    },
    "hourly": {
        "time": [f"2025-01-01T{str(h).zfill(2)}:00" for h in range(0, 24)] +
                [f"2025-01-02T{str(h).zfill(2)}:00" for h in range(0, 24)] +
                [f"2025-01-03T{str(h).zfill(2)}:00" for h in range(0, 24)] +
                [f"2025-01-04T{str(h).zfill(2)}:00" for h in range(0, 24)] +
                [f"2025-01-05T{str(h).zfill(2)}:00" for h in range(0, 24)] +
                [f"2025-01-06T{str(h).zfill(2)}:00" for h in range(0, 24)] +
                [f"2025-01-07T{str(h).zfill(2)}:00" for h in range(0, 24)],
        "temperature_2m": [1] * (24 * 7),
        "apparent_temperature": [0] * (24 * 7),
        "precipitation": [0.1] * (24 * 7),
        "wind_speed_10m": [3] * (24 * 7),
        "weather_code": [2] * (24 * 7)
    },
}

# --- TESTY ---

@patch("app.services.weather_api.requests.get")
def test_get_forecast_success(mock_get):
    # symulacja poprawnej odpowiedzi z API
    mock_get.return_value = MagicMock(status_code=200, json=lambda: MOCK_API_RESPONSE)

    result = get_forecast(52.2298, 21.0118)

    assert len(result) == 7
    assert "data" in result[0]
    assert "godziny" in result[0]
    assert len(result[0]["godziny"]) == 24


@patch("app.services.weather_api.requests.get")
def test_get_forecast_api_error(mock_get):
    # symulowanie wyjątku
    mock_get.side_effect = Exception("API error")

    result = get_forecast(52.2298, 21.0118)

    assert result == []


@patch("app.services.weather_api.get_forecast")
@freeze_time("2025-01-01 10:30:00") # Ustawiamy aktualny czas na 10:30 (godzina 10)
def test_get_weather_now_success(mock_get_forecast):
    # Mockujemy wynik get_forecast tak, aby zwracał listę sformatowanych danych
    # Wklejamy tutaj przykładową, już sformatowaną prognozę na 7 dni.
    mock_hourly_data = []
    for h in range(24):
        # Symulujemy, że dla godziny 10:00 jest wyjątkowy kod pogody i temperatura
        temp = 10 if h == 10 else 1 
        kod_pogody = 3 if h == 10 else 2 

        mock_hourly_data.append({
            "godzina": f"{str(h).zfill(2)}:00",
            "temp": temp,
            "odczuwalna_temp": 0,
            "opady": 0.1,
            "wiatr": 3,
            "kod_pogody": kod_pogody
        })

    mock_forecast_result = [
        {"data": "01.01.2025", "godziny": mock_hourly_data},
        # ... pozostałe 6 dni nie są potrzebne do tego testu ...
    ]

    mock_get_forecast.return_value = mock_forecast_result

    result = get_weather_now(52.2298, 21.0118)

    # Oczekujemy, że zwróci prognozę dla godziny 10 (indeks 10)
    assert result["godzina"] == "10:00"
    assert result["temp"] == 10
    assert result["kod_pogody"] == 3


@patch("app.services.weather_api.get_forecast")
def test_get_weather_now_no_forecast(mock_get_forecast):
    # Symulujemy, że get_forecast zwraca pustą listę (np. z powodu błędu API)
    mock_get_forecast.return_value = []

    result = get_weather_now(52.2298, 21.0118)

    # Oczekujemy, że w takim przypadku funkcja zwróci None
    assert result is None

@patch("app.services.weather_api.get_weather_now")
def test_get_weather_now_by_city_calls_get_weather_now(mock_get_weather_now):
    miasto = "Kraków"
    mock_get_weather_now.return_value = {"temp": 5}

    result = get_weather_now_by_city(miasto)

    # Sprawdzamy, czy get_weather_now zostało wywołane z danymi dla Krakowa
    mock_get_weather_now.assert_called_once_with(
        Cities[miasto]["latitude"],
        Cities[miasto]["longitude"]
    )
    assert result["temp"] == 5 