import tkinter as tk
from tkinter import ttk
import os
import random
from PIL import Image, ImageTk


class WeatherAppUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikacja Pogodowa")
        self.root.geometry("400x650")
        self.root.resizable(False, False)

        # Ścieżka do ikon (żeby u każdego działało)
        base_dir = os.path.dirname(__file__)
        self.icons_dir = os.path.join(base_dir, "icons")


        # Kod WMO z meteo: opis, plik
        self.weather_map = {
            # Czyste niebo
            0: {"opis": "Czyste niebo", "ikona": "sun.png"},

            # Zachmurzenie
            1: {"opis": "Przeważnie słonecznie", "ikona": "cloudy.png"},
            2: {"opis": "Częściowe zachmurzenie", "ikona": "cloudy.png"},
            3: {"opis": "Pochmurno", "ikona": "cloudy.png"},

            # Mgła
            45: {"opis": "Mgła", "ikona": "fog.png"},
            48: {"opis": "Mgła osadzająca szadź", "ikona": "fog.png"},

            # Mżawka
            51: {"opis": "Lekka mżawka", "ikona": "drizzle.png"},
            53: {"opis": "Umiarkowana mżawka", "ikona": "drizzle.png"},
            55: {"opis": "Gęsta mżawka", "ikona": "drizzle.png"},

            # Deszcz
            61: {"opis": "Słaby deszcz", "ikona": "rain.png"},
            63: {"opis": "Umiarkowany deszcz", "ikona": "rain.png"},
            65: {"opis": "Ulewny deszcz", "ikona": "rain.png"},

            # Śnieg
            71: {"opis": "Słaby śnieg", "ikona": "snow.png"},
            73: {"opis": "Umiarkowany śnieg", "ikona": "snow.png"},
            75: {"opis": "Silny śnieg", "ikona": "snow.png"},

            # Deszcz2
            80: {"opis": "Przelotny deszcz", "ikona": "rain.png"},
            81: {"opis": "Ulewa", "ikona": "rain.png"},
            82: {"opis": "Gwałtowna ulewa", "ikona": "rain.png"},

            # Burze
            95: {"opis": "Burza", "ikona": "thunder.png"},
            96: {"opis": "Burza z gradem", "ikona": "thunder.png"},
            99: {"opis": "Silna burza z gradem", "ikona": "thunder.png"},
        }

        # STYLE
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Helvetica", 12))
        self.style.configure("Title.TLabel", font=("Helvetica", 24, "bold"))
        self.style.configure("Temp.TLabel", font=("Helvetica", 48, "bold"))

        # MAINFRAME
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self._buduj_gui()

    def _buduj_gui(self):
        """Metoda pomocnicza do ułożenia elementów w oknie"""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # TYTUŁ
        title_label = ttk.Label(main_frame, text="Pogoda", style="Title.TLabel")
        title_label.pack(pady=(0, 20))

        # WYSZUKIWANIE
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 20))

        self.city_entry = ttk.Entry(input_frame)
        self.city_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.city_entry.insert(0, "Warszawa")

        search_btn = ttk.Button(input_frame, text="Szukaj", command=self.pobierz_dane)
        search_btn.pack(side=tk.RIGHT)

        # WYNIKI
        self.result_frame = ttk.LabelFrame(main_frame, text="Aktualne warunki", padding="15")
        self.result_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        # Miasto
        self.location_label = ttk.Label(self.result_frame, text="Wpisz miasto...", font=("Helvetica", 16))
        self.location_label.pack(pady=5)

        # Ikona Pogody (Label na obrazek)
        self.icon_label = ttk.Label(self.result_frame)
        self.icon_label.pack(pady=10)

        # Temperatura
        self.temp_label = ttk.Label(self.result_frame, text="--°C", style="Temp.TLabel")
        self.temp_label.pack()

        # Opis
        self.desc_label = ttk.Label(self.result_frame, text="Oczekiwanie na dane...")
        self.desc_label.pack()

        # Dodatkowe info (Wiatr, Wilgotność)
        details_frame = ttk.Frame(self.result_frame)
        details_frame.pack(pady=20)

        ttk.Label(details_frame, text="Wiatr:").grid(row=0, column=0, padx=10, sticky="e")
        self.wind_label = ttk.Label(details_frame, text="-- km/h", font=("Helvetica", 10, "bold"))
        self.wind_label.grid(row=0, column=1, padx=10, sticky="w")

    def aktualizuj_pogode_ui(self, kod_wmo):
        """
        Główna logika aktualizacji wyglądu (Ikona + Tekst)
        """
        # Pobranie danych ze slownika, nieznany kod - chumra
        dane = self.weather_map.get(kod_wmo, {"opis": "Nieznana pogoda", "ikona": "cloudy.png"})

        opis_tekstowy = dane["opis"]
        plik_ikony = dane["ikona"]

        # OPIS
        self.desc_label.config(text=opis_tekstowy)

        # OBRAZEK
        pelna_sciezka = os.path.join(self.icons_dir, plik_ikony)

        # Upewnienie ze plik istnieje
        if not os.path.exists(pelna_sciezka):
            print(f"BŁĄD: Nie znaleziono pliku ikony: {pelna_sciezka}")
            self.icon_label.config(text=f"[Brak pliku: {plik_ikony}]", image="")
            return

        try:
            image = Image.open(pelna_sciezka)
            image = image.resize((150, 150))  # Rozmiar ikony
            photo = ImageTk.PhotoImage(image)

            self.icon_label.config(image=photo)
            self.icon_label.image = photo # to jest dla garbage collectora
        except Exception as e:
            print(f"Błąd podczas ładowania obrazka: {e}")

    def pobierz_dane(self):
        """
        Symulacja
        """
        miasto = self.city_entry.get()
        print(f"--- Symulacja API dla: {miasto} ---")

        # losowanie kodu ze zdefiniowanych
        dostepne_kody = list(self.weather_map.keys())
        wylosowany_kod = random.choice(dostepne_kody)

        temp = random.randint(-10, 35)

        # Aktualizacja
        self.location_label.config(text=f"📍 {miasto}")
        self.temp_label.config(text=f"{temp}°C")
        self.aktualizuj_pogode_ui(wylosowany_kod)

# URUCHOMIENIE
if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherAppUI(root)
    root.mainloop()


# głownie pack(), bo jest najprostszy do ukladu jedno pod drugim
# ikd czy nie zmienie na grid(), tak jak w szegolach, dla wyrownania etykiet
