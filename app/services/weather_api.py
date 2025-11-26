import requests
from datetime import datetime

cities = {"Warszawa": {"latitude": 52.2298, "longitude": 21.0118}}  # to do: dodać więcej miast


def get_forecast(latitude, longitude):
    """
    Funkcja zwracająca sformatowane dane z prognozą pogody na najbliższe 7 dni dla danych współrzędnych geograficznych.
    :param latitude: szerokość geograficzna
    :param longitude: długość geograficzna
    :return: lista ze sformatowanymi danymi prognozy pogody
    """
    base_url = "https://api.open-meteo.com/v1/forecast?"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_probability_max",
            "wind_speed_10m_max",
            "uv_index_max"
        ],
        "hourly": [
            "temperature_2m",
            "apparent_temperature",
            "precipitation",
            "wind_speed_10m"
        ],
        "timezone": "Europe/Berlin"
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        dane = response.json()
    except requests.exceptions.RequestException as e:
        print("Błąd podczas łączenia z API: ", e)
        return []

    days = dane["daily"]
    hours = dane["hourly"]
    days_formated = []

    for i in range(0, 7):
        date = datetime.strptime(days["time"][i], "%Y-%m-%d").strftime("%d.%m.%Y")
        start = i * 24
        end = start + 24
        hour_forecast = []
        for j in range(start, end):
            h = datetime.strptime(hours["time"][j], "%Y-%m-%dT%H:%M").strftime("%H:%M")
            h_forecast = {
                "godzina": h,
                "temp": hours['temperature_2m'][j],
                "odczuwalna_temp": hours['apparent_temperature'][j],
                "opady": hours['precipitation'][j],
                "wiatr": hours['wind_speed_10m'][j]
            }
            hour_forecast.append(h_forecast)

        day_forecast = {
            "data": date,
            "temp_max": days['temperature_2m_max'][i],
            "temp_min": days['temperature_2m_min'][i],
            "opady_proc": days['precipitation_probability_max'][i],
            "wiatr_predkosc": days['wind_speed_10m_max'][i],
            "indeks_uv": days['uv_index_max'][i],
            "godziny": hour_forecast
        }
        days_formated.append(day_forecast)

    return days_formated


def get_forecast_by_city(city):
    """
    Funkcja pobiera nazwę miasta razem z jego współrzędnymi geograficznymi i zwraca sformatowane dane prognozy pogody najbliższych 7 dni.
    :param city: Miasto, dla którego funkcja pobiera prognozę pogody i jego koordynaty
    :return: lista ze sformatowanymi danymi prognozy pogody
    """
    latitude = city["latitude"]
    longitude = city["longitude"]
    return get_forecast(latitude, longitude)


print(get_forecast_by_city(cities["Warszawa"]))
