import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from unittest.mock import patch, MagicMock

from app.services.weather_api import get_forecast, get_forecast_by_city, cities

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
def test_get_forecast_by_city_calls_get_forecast(mock_get_forecast):
    mock_get_forecast.return_value = ["dummy"]

    result = get_forecast_by_city(cities["Warszawa"])

    mock_get_forecast.assert_called_once_with(
        cities["Warszawa"]["latitude"],
        cities["Warszawa"]["longitude"]
    )
    assert result == ["dummy"]
