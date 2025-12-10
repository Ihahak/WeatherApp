import requests
from datetime import datetime

Cities = {"Warszawa": {"latitude": 52.2298, "longitude": 21.0118},
          "Kraków": {"latitude": 50.0647, "longitude": 19.9450},
          "Łódź": {"latitude": 51.7592, "longitude": 19.4560},
          "Wrocław": {"latitude": 51.1079, "longitude": 17.0385},
          "Poznań": {"latitude": 52.4064, "longitude": 16.9252},
          "Gdańsk": {"latitude": 54.3520, "longitude": 18.6466},
          "Szczecin": {"latitude": 53.4285, "longitude": 14.5528},
          "Bydgoszcz": {"latitude": 53.1235, "longitude": 18.0076},
          "Lublin": {"latitude": 51.2465, "longitude": 22.5684},
          "Białystok": {"latitude": 53.1325, "longitude": 23.1688},
          "Rzeszów": {"latitude": 50.0413, "longitude": 21.9990},
          }

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
            "uv_index_max",
            "sunrise",
            "sunset"
        ],
        "hourly": [
            "temperature_2m",
            "apparent_temperature",
            "precipitation",
            "wind_speed_10m",
            "weather_code"
        ],
        "timezone": "Europe/Berlin"
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        dane = response.json()
    except Exception as e:
        print("Błąd podczas łączenia z API: ", e)
        return []

    days = dane["daily"]
    hours = dane["hourly"]
    days_formated = []

    for i in range(0, 7):
        date = datetime.strptime(days["time"][i], "%Y-%m-%d").strftime("%d.%m.%Y")
        start = i * 24
        end = min(start + 24, len(hours["time"]))
        hour_forecast = []
        for j in range(start, end):
            h = datetime.strptime(hours["time"][j], "%Y-%m-%dT%H:%M").strftime("%H:%M")
            h_forecast = {
                "godzina": h,
                "temp": hours['temperature_2m'][j],
                "odczuwalna_temp": hours['apparent_temperature'][j],
                "opady": hours['precipitation'][j],
                "wiatr": hours['wind_speed_10m'][j],
                "kod_pogody": hours['weather_code'][j]
            }
            hour_forecast.append(h_forecast)

        day_forecast = {
            "data": date,
            "temp_max": days['temperature_2m_max'][i],
            "temp_min": days['temperature_2m_min'][i],
            "opady_proc": days['precipitation_probability_max'][i],
            "wiatr_predkosc": days['wind_speed_10m_max'][i],
            "indeks_uv": days['uv_index_max'][i],
            "wschód słońca": days['sunrise'][i],
            "zachód słońca": days['sunset'][i],
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
    city_data = Cities[city]
    return get_forecast(city_data["latitude"], city_data["longitude"])

def get_weather_now(latitude, longitude):
    """
    Funkcja zwracająca dane pogodowe dla aktualnej godziny dla danego miejsca.
    :param latitude: szerokość geograficzna
    :param longitude: długość geograficzna
    :return: słownik z danymi pogodowymi dla aktualnej godziny
    """
    whole_forecast = get_forecast(latitude, longitude)
    if not whole_forecast:
        return None
    now = datetime.now().hour
    godziny = whole_forecast[0]["godziny"]
    return godziny[now]

def get_weather_now_by_city(city):
    """
    Funkcja zwracająca słownik z danymi pogodowymi dla aktualnej godziny dla danego miasta.
    :param city: miasto, dla którego funkcja pobiera dane pogodowe
    :return: słownik z danymi pogodowymi
    """
    latitude = Cities[city]["latitude"]
    longitude = Cities[city]["longitude"]
    return get_weather_now(latitude, longitude)

# print(get_forecast_by_city("Warszawa"))
# print(get_weather_now_by_city("Warszawa"))