# WeatherApp - Aplikacja Pogodowa
Projekt zaliczeniowy stworzony w języku Python, służący do sprawdzania aktualnej pogody oraz prognozy długoterminowej. Aplikacja wykorzystuje API Open-Meteo oraz bibliotekę Tkinter do obsługi interfejsu graficznego.

## Autorzy
* Bazyluk Anna
* Gasik Zuzanna
* Hankus Ida

## Funkcjonalności
* **Aktualna pogoda**: Wyświetlanie temperatury, odczuwalnej temperatury, prędkości wiatru oraz opisu zjawisk atmosferycznych.
* **Prognoza 7-dniowa**: Wykres temperatury na najbliższy tydzień wraz z ikonami pogody.
* **Geolokalizacja**: Automatyczne wykrywanie lokalizacji użytkownika (na podstawie IP).
* **Wyszukiwanie miast**: Możliwość sprawdzenia pogody dla wybranych miast Polski (m.in. Warszawa, Kraków, Wrocław, Gdańsk).
* **Interfejs graficzny**: Przejrzyste okno aplikacji z obsługą błędów (np. brak połączenia).

## Foldery i pliki projektu:
* app - folder zawierający w sobie pliki aplikacji
  * gui - folder zawierający pliki dotyczące interfejsu graficznego
    * main_window.py: odpowiada za warstwę wizualną (okna przyciski, wykresy); łączy logikę biznesową z interfejsem
  * services - folder zawierający komunikację z API oraz ustalanie lokalizacji geograficznej użytkownika
    * weather_api.py: moduł komunikacji z Open-Meteo API; pobiera i formatuje dane JSON
    * user_geolocation.py: moduł odpowiedzialny za namierzanie użytkownika przy użyciu biblioteki geocoder
  * models - folder zawierający klasy danych
  * core - folder z funkcjami pomocniczymi i plikiem konfiguracji
* tests - zestaw testów jednostkowych i integracyjnych sprawdzających działanie API oraz GUI; finalny test systemowy
* main.py - główny plik uruchamiający aplikację, nicjalizuje okno Tkinter
* README.md - opis projektu

## Potrzebne biblioteki:
* pillow - do wyświetlania ikon
* requests - do komunikacji z API
* geocoder - do wykrywania lokalizacji użytkownika na podstawie adresu IP

## Wymagania i Instalacja

Aby uruchomić aplikację, potrzebujesz zainstalowanego Pythona (wersja 3.x).

1. **Pobierz repozytorium** na swój dysk.
2. **Zainstaluj wymagane biblioteki** wpisując w terminalu:
   ```bash
   pip install -r requirements.txt

# Instrukcje
## Jak uruchomić aplikację?
Aplikację uruchamiamy z głównego katalogu projektu za pomocą pliku startowego:
python main.py

## User Manual
1. Start: Po uruchomieniu aplikacja automatycznie spróbuje pobrać dane dla Twojej lokalizacji.
2. Wyszukiwanie:
* Kliknij w pole wyboru na górze okna ("Moja lokalizacja").
* Wybierz miasto z listy (np. "Wrocław") lub zostaw "Moja lokalizacja".
* Kliknij przycisk SZUKAJ lub wciśnij klawisz Enter.
3. Odczyt danych:
* Po lewej stronie zobaczysz obecny stan szczegółowy.
* Po prawej stronie znajduje się wykres prognozy na kolejne dni. Najedź kursorem na punkty wykresu, aby zobaczyć dokładną temperaturę.

## Testowanie 
Projekt posiada zestaw testów automatycznych. Aby je uruchomić, wpisz w terminalu:
python -m unittest discover tests