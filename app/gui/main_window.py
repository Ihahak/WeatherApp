import os
import sys
import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox

from PIL import Image, ImageTk

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_root)
from app.services.weather_api import get_weather_now_by_city, get_forecast_by_city, get_weather_now, get_forecast
from app.services.user_geolocation import get_location


class WeatherAppUI:
    def __init__(self, root):
        """
        Konstruktor klasy.
        Robi główne okno aplikacji (ustawia tytuł, wymiary i kolory okna)
        Wczytuje ikony oraz tworzy listę miast do wybrania.
        Wczytuje mapę kodów pogodowych z naszego źródła i przypisuje im odpowiednią ikonę.
        Wywołuje metody konfigurujące style i budujące interfejs oraz planuje pierwsze automatyczne pobieranie danych.
        """
        self.root = root
        self.root.title("Aplikacja Pogodowa")
        self.root.geometry("800x550")
        self.root.resizable(False, False)

        # odklikiwanie
        self.root.bind("<Button-1>", lambda event: self.root.focus_set())

        # kolory
        self.colors = {
            "bg_window": "#D0D6B3",
            "bg_card": "#F7F7F7",
            "text_main": "#143109",
            "accent": "#73877B",
            "input_bg": "#EFEFEF",
            "chart_line": "#2F5233"
        }
        self.root.configure(bg=self.colors["bg_window"])

        # ikony
        base_dir = os.path.dirname(__file__)
        self.icons_dir = os.path.join(base_dir, "icons")
        self.chart_icons_cache = []

        # lista miast
        self.dostepne_miasta = [
            "Moja lokalizacja", "Warszawa", "Kraków", "Łódź", "Wrocław", "Poznań",
            "Gdańsk", "Szczecin", "Bydgoszcz", "Lublin", "Białystok", "Rzeszów"
        ]

        # Kody WMO
        self.weather_map = {
            0: {"opis": "Czyste niebo", "ikona": "sun.png"},
            1: {"opis": "Przeważnie słonecznie", "ikona": "cloudy.png"},
            2: {"opis": "Częściowe zachmurzenie", "ikona": "cloudy.png"},
            3: {"opis": "Pochmurno", "ikona": "cloudy.png"},
            45: {"opis": "Mgła", "ikona": "fog.png"},
            48: {"opis": "Mgła osadzająca szadź", "ikona": "fog.png"},
            51: {"opis": "Lekka mżawka", "ikona": "drizzle.png"},
            53: {"opis": "Umiarkowana mżawka", "ikona": "drizzle.png"},
            55: {"opis": "Gęsta mżawka", "ikona": "drizzle.png"},
            61: {"opis": "Słaby deszcz", "ikona": "rain.png"},
            63: {"opis": "Umiarkowany deszcz", "ikona": "rain.png"},
            65: {"opis": "Ulewny deszcz", "ikona": "rain.png"},
            71: {"opis": "Słaby śnieg", "ikona": "snow.png"},
            73: {"opis": "Umiarkowany śnieg", "ikona": "snow.png"},
            75: {"opis": "Silny śnieg", "ikona": "snow.png"},
            80: {"opis": "Przelotny deszcz", "ikona": "rain.png"},
            81: {"opis": "Ulewa", "ikona": "rain.png"},
            82: {"opis": "Gwałtowna ulewa", "ikona": "rain.png"},
            95: {"opis": "Burza", "ikona": "thunder.png"},
            96: {"opis": "Burza z gradem", "ikona": "thunder.png"},
            99: {"opis": "Silna burza z gradem", "ikona": "thunder.png"},
        }
        self._konfiguruj_style()
        self._buduj_gui()

        self.root.after(100, self.pobierz_dane)

    def _konfiguruj_style(self):
        """
        Odpowiada za wygląd aplikacji. Definiuje style tkk (czcionki, kolory tła/tekstu) dla różnych elementów interfejsu
        (etykiety, przyciski itp.).
        :raises tk.TclError: Idzie dalej, jeśli theme nie może być zastosowany
        """
        self.style = ttk.Style()
        try:
            self.style.theme_use('clam')
        except tk.TclError:
            pass

        # Mainframe
        self.style.configure("Main.TFrame", background=self.colors["bg_window"])

        # ramka
        self.style.configure("Card.TFrame", background=self.colors["bg_card"], relief="flat")
        self.style.configure("Card.TLabelframe", background=self.colors["bg_card"], relief="flat", borderwidth=0)

        # labele
        self.style.configure("TLabel",
                             background=self.colors["bg_card"],
                             foreground=self.colors["text_main"],
                             font=("Helvetica", 12))

        self.style.configure("Title.TLabel",
                             background=self.colors["bg_window"],
                             foreground=self.colors["text_main"],
                             font=("Helvetica", 28, "bold"))

        self.style.configure("CardInfo.TLabel",
                             background=self.colors["bg_card"],
                             foreground=self.colors["text_main"],
                             font=("Helvetica", 12))

        self.style.configure("ChartTitle.TLabel",
                             background=self.colors["bg_card"],
                             foreground=self.colors["text_main"],
                             font=("Helvetica", 11, "bold"))

        self.style.configure("Temp.TLabel",
                             background=self.colors["bg_card"],
                             foreground=self.colors["text_main"],
                             font=("Helvetica", 48, "bold"))

        self.style.configure("Small.TLabel",
                             background=self.colors["bg_card"],
                             foreground=self.colors["accent"],
                             font=("Helvetica", 9))

        self.style.configure("Value.TLabel",
                             background=self.colors["bg_card"],
                             foreground=self.colors["text_main"],
                             font=("Helvetica", 14, "bold"))

        self.style.configure("Search.TButton",
                             font=("Helvetica", 10, "bold"),
                             background=self.colors["accent"],
                             foreground="white", borderwidth=0)

        self.style.map("Search.TButton",
                       background=[("active", self.colors["text_main"])])

        self.style.configure("TCombobox",
                             fieldbackground=self.colors["input_bg"],
                             background=self.colors["accent"],
                             arrowcolor="black")

    def _buduj_gui(self):
        """
        Buduje i organizuje graficzny układ aplikacji.
        Dodaje widżety (kontenery, napisy, przyciski, wybór miasta, pole na wykres) i
        układa je w odpowiednie miejsca w oknie.
        """
        main_frame = ttk.Frame(self.root, padding="15", style="Main.TFrame")
        main_frame.pack(fill="both", expand=True)

        # góra
        top_bar = ttk.Frame(main_frame, style="Main.TFrame")
        top_bar.pack(fill="x", pady=(0, 15))
        ttk.Label(top_bar, text="Pogoda", style="Title.TLabel").pack(side="left", padx=(0, 20))

        # wyszukiwanie
        input_frame = ttk.Frame(top_bar, style="Main.TFrame")
        input_frame.pack(side="right", fill="x", expand=True)

        # combobox (blokuje wpisywanie, ma wartość domyślną)
        self.city_combo = ttk.Combobox(input_frame,
                                       values=self.dostepne_miasta,
                                       font=("Helvetica", 11),
                                       state="readonly")

        self.city_combo.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=4)
        self.city_combo.set("Moja lokalizacja")

        # enter + klikniecie myszka
        self.city_combo.bind("<<ComboboxSelected>>", self._po_wyborze_miasta)
        self.city_combo.bind("<Return>", lambda event: self.pobierz_dane())

        ttk.Button(input_frame, text="SZUKAJ", style="Search.TButton", command=self.pobierz_dane, cursor="hand2").pack(
            side="right", ipadx=10, ipady=4)

        # glowna karta
        self.result_frame = ttk.LabelFrame(main_frame, padding="0", style="Card.TLabelframe")
        self.result_frame.pack(fill="both", expand=True)

        inner_frame = ttk.Frame(self.result_frame, style="Card.TFrame", padding="20")
        inner_frame.pack(fill="both", expand=True)

        # środek
        middle_container = ttk.Frame(inner_frame, style="Card.TFrame")
        middle_container.pack(fill="both", expand=True)

        # lewo
        left_panel = ttk.Frame(middle_container, style="Card.TFrame")
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.location_label = ttk.Label(left_panel, text="Wybierz miasto", font=("Helvetica", 20, "bold"),
                                        style="CardInfo.TLabel")
        self.location_label.pack(pady=(0, 5))

        self.icon_label = ttk.Label(left_panel, style="CardInfo.TLabel")
        self.icon_label.pack(pady=5)

        self.temp_label = ttk.Label(left_panel, text="--°", style="Temp.TLabel")
        self.temp_label.pack(pady=0)

        self.desc_label = ttk.Label(left_panel, text="...", style="CardInfo.TLabel")
        self.desc_label.pack(pady=(0, 10))

        # Separator pionowy
        ttk.Separator(middle_container, orient='vertical').pack(side="left", fill='y', padx=10, pady=10)

        # prawo — wykres
        right_panel = ttk.Frame(middle_container, style="Card.TFrame")
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))

        ttk.Label(right_panel, text="Prognoza na tydzień",
                  style="ChartTitle.TLabel").pack(pady=(15, 10))

        self.chart_canvas = tk.Canvas(right_panel, width=400, height=200, bg=self.colors["bg_card"],
                                      highlightthickness=0)
        self.chart_canvas.pack(fill="both", expand=True)

        # dół
        ttk.Separator(inner_frame, orient='horizontal').pack(fill='x', pady=(10, 15))

        details_frame = ttk.Frame(inner_frame, style="Card.TFrame")
        details_frame.pack(fill="x", pady=(0, 5))
        details_frame.columnconfigure(0, weight=1)
        details_frame.columnconfigure(1, weight=1)

        ttk.Label(details_frame, text="WIATR", style="Small.TLabel").grid(row=0, column=0)
        self.wind_label = ttk.Label(details_frame, text="-- km/h", style="Value.TLabel")
        self.wind_label.grid(row=1, column=0)

        ttk.Label(details_frame, text="ODCZUWALNA", style="Small.TLabel").grid(row=0, column=1)
        self.feels_like_label = ttk.Label(details_frame, text="--°", style="Value.TLabel")
        self.feels_like_label.grid(row=1, column=1)

    def _po_wyborze_miasta(self, _):
        """
        Funkcja pomocnicza, która uruchamia się automatycznie po wybraniu miasta z listy.
        Ma za zadanie wywołanie pobierania danych, a potem usunięcie zaznaczenia tekstu w polu wyboru i
        przeniesienie focusu do root widżetu.
        """
        self.city_combo.selection_clear()
        self.root.focus_set()
        self.pobierz_dane()

    # Ida zwraca: {'temp': X, 'wiatr': Y, 'kod_pogody': Z, ...}
    def aktualizuj_ui(self, dane_obecne, dane_prognoza, nazwa_miasta):
        """
        Funkcja odświeżająca widok. Przyjmuje pobrane dane — obecne i prognozę i wpisuje je w odpowiednie etykiety.
        Wywołuje ładowanie ikony oraz zleca narysowanie wykresu.
        :param dane_obecne: Słownik z obecnymi danymi pogodowymi.
        :param dane_prognoza: Słownik z prognozowanymi danymi pogodowymi.
        :param nazwa_miasta: Nazwa wyświetlająca się.
        """

        temp = dane_obecne.get("temp", "--")
        wiatr_wart = dane_obecne.get("wiatr")
        wiatr = wiatr_wart if wiatr_wart is not None else "--"
        kod_wmo = dane_obecne.get("kod_pogody", 0)
        odczuwalna_wart = dane_obecne.get("odczuwalna_temp")
        odczuwalna = odczuwalna_wart if odczuwalna_wart is not None else "--"

        self.location_label.config(text=nazwa_miasta)
        self.temp_label.config(text=f"{temp}°")
        self.wind_label.config(text=f"{wiatr} km/h")
        self.feels_like_label.config(text=f"{odczuwalna}°")

        info = self.weather_map.get(kod_wmo, {"opis": "Nieznana", "ikona": "cloudy.png"})
        self.desc_label.config(text=info["opis"])
        self._laduj_ikone_glowna(info["ikona"])

        przetworzona_prognoza = self._przetworz_prognoze(dane_prognoza)
        self._rysuj_wykres(przetworzona_prognoza)

    def _przetworz_prognoze(self, dane_prognoza):
        """
        Funkcja pomocnicza, która tworzy listę — tłumaczy dane z API na format potrzebny do wykresu,
        zawiera nazwę dnia, maksymalną temperaturę, ikonę.
        :param dane_prognoza: Lista słowników, gdzie każdy słownik zawiera dane prognozy dla konkretnego dnia.
        :return: Lista słowników, gdzie każdy zawiera dzień, temperaturę i ikonę.
        """
        wynik = []
        dni_tygodnia = ["Pon", "Wt", "Śr", "Czw", "Pt", "Sob", "Ndz"]

        for dzien_dane in dane_prognoza:
            try:
                data_obj = datetime.strptime(dzien_dane["data"], "%d.%m.%Y")
                nazwa_dnia = dni_tygodnia[data_obj.weekday()]
            except ValueError:
                nazwa_dnia = "?"

            temp = dzien_dane["temp_max"]

            try:
                kod_wmo = dzien_dane["godziny"][12]["kod_pogody"]
            except (IndexError, KeyError):
                kod_wmo = 0

            ikona = self.weather_map.get(kod_wmo, {}).get("ikona", "sun.png")

            wynik.append({
                "dzien": nazwa_dnia,
                "temp": temp,
                "ikona": ikona
            })
        return wynik

    def _laduj_ikone_glowna(self, nazwa_pliku):
        """
        Wczytuje odpowiednią ikonę z dysku, przeskalowuje ją i wyświetla na głównym panelu.
        Obsługuje brak ikony — wyświetla "placeholder" (napis brak ikony)
        """
        pelna_sciezka = os.path.join(self.icons_dir, nazwa_pliku)
        if not os.path.exists(pelna_sciezka):
            self.icon_label.config(text="[Brak ikony]", image="")
            return
        try:
            image = Image.open(pelna_sciezka)
            image = image.resize((100, 100), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.icon_label.config(image=photo)
            self.icon_label.image = photo
        except Exception as e:
            print(f"Błąd: {e}")

    def _rysuj_wykres(self, dane):
        """
        Rysuje wykres w Canvas. Oblicza współrzędne punktów na podstawie temperatur, rysuje linię łączącą
        oraz kropki dla poszczególnych dni, podpisy i mini ikonki.
        Obsługuje brak danych.
        :param dane: lista słowników z danymi prognozy.
        """
        self.chart_canvas.delete("all")
        self.chart_icons_cache = []

        width = 400
        height = 180
        margin_x = 30
        margin_y_top = 40
        margin_y_bottom = 50

        if not dane:
            self.chart_canvas.create_text(width / 2, height / 2, text="Brak danych wykresu")
            return

        temps = [d["temp"] for d in dane]
        min_t, max_t = min(temps), max(temps)
        diff = max_t - min_t if max_t != min_t else 1
        available_h = height - margin_y_top - margin_y_bottom

        points = []
        step_x = (width - 2 * margin_x) / (len(dane) - 1) if len(dane) > 1 else 0

        for i, entry in enumerate(dane):
            x = margin_x + i * step_x
            normalized = (entry["temp"] - min_t) / diff
            y = (height - margin_y_bottom) - (normalized * available_h)
            points.append((x, y, entry))

        coords = []
        for p in points:
            coords.extend([p[0], p[1]])

        if len(coords) >= 4:
            self.chart_canvas.create_line(coords, fill=self.colors["chart_line"], width=3, smooth=True)

        for x, y, entry in points:
            r = 4
            self.chart_canvas.create_oval(x - r, y - r, x + r, y + r, fill=self.colors["chart_line"],
                                          outline=self.colors["bg_card"], width=2)

            self.chart_canvas.create_text(x, y - 15, text=f"{int(entry['temp'])}°", font=("Helvetica", 9, "bold"),
                                          fill="#555")

            self.chart_canvas.create_text(x, height - 30, text=entry["dzien"], font=("Helvetica", 9), fill="#333")

            icon_path = os.path.join(self.icons_dir, entry["ikona"])
            if os.path.exists(icon_path):
                img = Image.open(icon_path)
                img = img.resize((20, 20), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.chart_icons_cache.append(photo)
                self.chart_canvas.create_image(x, height - 10, image=photo)

    def pobierz_dane(self):
        """
        Pobiera dane dla aktualnego wyboru użytkownika (miasto lub aktualna lokalizacja) i aktualizuje interfejs.
        Jeśli wystąpi błąd — powiadamia użytkownika i czyści interfejs.
        """
        wybor = self.city_combo.get().strip()

        self.root.config(cursor="watch")
        self.root.update()

        try:
            if wybor == "Moja lokalizacja":
                # Zwraca [lat, lng] lub None
                wspolrzedne = get_location()

                if not wspolrzedne:
                    raise Exception("Nie udało się wykryć Twojej lokalizacji (sprawdź połączenie).")

                lat, lon = wspolrzedne
                obecna = get_weather_now(lat, lon)
                prognoza = get_forecast(lat, lon)

                nazwa_do_wyswietlenia = "Twoja lokalizacja"
            else:
                obecna = get_weather_now_by_city(wybor)
                prognoza = get_forecast_by_city(wybor)
                nazwa_do_wyswietlenia = wybor

            if obecna is None or not prognoza:
                messagebox.showerror("Błąd", f"Nie udało się pobrać danych dla: {wybor}")
                self.czysc_widok_po_bledzie()
            else:
                self.aktualizuj_ui(obecna, prognoza, nazwa_do_wyswietlenia)

        except Exception as e:
            print(f"Błąd krytyczny: {e}")
            messagebox.showerror("Błąd", f"Wystąpił błąd: {e}")
            self.czysc_widok_po_bledzie()
        finally:
            self.root.config(cursor="")

    def czysc_widok_po_bledzie(self):
        """
        Czyści interfejs, gdy wystąpi błąd (np. brak internetu).
        Ustawia wszystkie pola tekstowe na wartości domyślne i usuwa nieaktualne ikony.
        """
        self.location_label.config(text="Błąd")
        self.temp_label.config(text="--")
        self.desc_label.config(text="Brak danych")
        self.wind_label.config(text="--")
        self.feels_like_label.config(text="--")
        self.icon_label.config(image="", text="❌")


if __name__ == "__main__":
    main_window = tk.Tk()
    app = WeatherAppUI(main_window)
    main_window.mainloop()
