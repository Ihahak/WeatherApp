import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

from PIL import Image, ImageTk

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_root)
from app.services.weather_api import get_weather_now_by_city


class WeatherAppUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikacja Pogodowa")
        self.root.geometry("420x750")
        self.root.resizable(False, False)

        # odklikiwanie
        self.root.bind("<Button-1>", lambda event: self.root.focus_set())

        # kolory
        self.colors = {
            "bg_window": "#D0D6B3",
            "bg_card": "#F7F7F7",
            "text_main": "#143109",
            "accent": "#73877B",
            "input_bg": "#EFEFEF"
        }
        self.root.configure(bg=self.colors["bg_window"])

        # ikony
        base_dir = os.path.dirname(__file__)
        self.icons_dir = os.path.join(base_dir, "icons")

        # lista miast
        self.dostepne_miasta = [
            "Warszawa", "Kraków", "Łódź", "Wrocław", "Poznań",
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

    def _konfiguruj_style(self):
        self.style = ttk.Style()
        try:
            self.style.theme_use('clam')  # windows blokuje zmiany kolorów
        except ttk.TclError:
            pass

        # Mainframe
        self.style.configure("Main.TFrame", background=self.colors["bg_window"])

        # ramka
        self.style.configure("Card.TFrame", background=self.colors["bg_card"], relief="flat")
        self.style.configure("Card.TLabelframe", background=self.colors["bg_card"], relief="flat")
        self.style.configure("Card.TLabelframe.Label",
                             background=self.colors["bg_card"],
                             foreground=self.colors["accent"],
                             font=("Helvetica", 10, "bold"))

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

        self.style.configure("Temp.TLabel",
                             background=self.colors["bg_card"],
                             foreground=self.colors["text_main"],
                             font=("Helvetica", 64, "bold"))

        self.style.configure("Small.TLabel",
                             background=self.colors["bg_card"],
                             foreground=self.colors["accent"],
                             font=("Helvetica", 10))

        # przycisk
        self.style.configure("TButton",
                             font=("Helvetica", 10, "bold"),
                             background=self.colors["accent"],
                             foreground="white",
                             borderwidth=0)
        self.style.map("TButton", background=[("active", self.colors["text_main"])])

        # combobox - lista
        self.style.configure("TCombobox",
                             fieldbackground=self.colors["input_bg"],
                             background=self.colors["accent"],
                             foreground=self.colors["text_main"],
                             arrowcolor="white")

        # tutaj usuwam zaznaczenie tekstu (brzydko wyglada)
        self.style.map('TCombobox', fieldbackground=[('readonly', self.colors["input_bg"])],
                       selectbackground=[('readonly', self.colors["input_bg"])],
                       selectforeground=[('readonly', self.colors["text_main"])])

        # to też do usunięcia zaznaczenia tekstu (zabieramy focus)

    def _buduj_gui(self):
        main_frame = ttk.Frame(self.root, padding="25", style="Main.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # tytul
        title_label = ttk.Label(main_frame, text="Pogoda", style="Title.TLabel")
        title_label.pack(pady=(10, 25))

        # wyszukiwanie
        input_frame = ttk.Frame(main_frame, style="Main.TFrame")
        input_frame.pack(fill=tk.X, pady=(0, 25))

        # combobox (blokuje wpisywanie, ma wartosc domyslna)
        self.city_combo = ttk.Combobox(input_frame,
                                       values=self.dostepne_miasta,
                                       font=("Helvetica", 12),
                                       state="readonly")

        self.city_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=8)
        self.city_combo.set("Warszawa")

        # do czyszczenia zaznaczenia
        self.city_combo.bind("<<ComboboxSelected>>", self._po_wyborze_miasta)
        self.city_combo.bind("<Return>", lambda event: self.pobierz_dane())

        # Obsługa Enter + szukanie po kliknięciu myszką
        self.city_combo.bind("<Return>", lambda event: self.pobierz_dane())
        self.city_combo.bind("<<ComboboxSelected>>",
                             lambda event: self.pobierz_dane())

        search_btn = ttk.Button(input_frame, text="SZUKAJ", command=self.pobierz_dane, cursor="hand2")
        search_btn.pack(side=tk.RIGHT, ipadx=10, ipady=5)

        # wyniki
        self.result_frame = ttk.LabelFrame(main_frame, padding="20", style="Card.TLabelframe")
        self.result_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # wnętrze
        self.location_label = ttk.Label(self.result_frame, text="Wybierz miasto", font=("Helvetica", 20, "bold"),
                                        style="CardInfo.TLabel")
        self.location_label.pack(pady=(10, 5))

        self.icon_label = ttk.Label(self.result_frame, style="CardInfo.TLabel")
        self.icon_label.pack(pady=10)

        self.temp_label = ttk.Label(self.result_frame, text="--°", style="Temp.TLabel")
        self.temp_label.pack()

        self.desc_label = ttk.Label(self.result_frame, text="...", style="CardInfo.TLabel")
        self.desc_label.pack(pady=(0, 20))

        # Separator
        ttk.Separator(self.result_frame, orient='horizontal').pack(fill='x', pady=10)

        # Szczegóły
        details_frame = ttk.Frame(self.result_frame, style="Card.TFrame")
        details_frame.pack(pady=10)

        # Kol 1
        ttk.Label(details_frame, text="WIATR", style="Small.TLabel").grid(row=0, column=0, padx=20)
        self.wind_label = ttk.Label(details_frame, text="-- km/h", font=("Helvetica", 14, "bold"),
                                    style="CardInfo.TLabel")
        self.wind_label.grid(row=1, column=0, padx=20)

        # Kol 2
        ttk.Label(details_frame, text="ODCZUWALNA", style="Small.TLabel").grid(row=0, column=1, padx=20)
        self.feels_like_label = ttk.Label(details_frame, text="--°", font=("Helvetica", 14, "bold"),
                                          style="CardInfo.TLabel")
        self.feels_like_label.grid(row=1, column=1, padx=20)

    def _po_wyborze_miasta(self, event):
        self.city_combo.selection_clear()
        self.root.focus_set()
        self.pobierz_dane()

    # Ida zwraca: {'temp': X, 'wiatr': Y, 'kod_pogody': Z, ...}
    def aktualizuj_ui(self, dane_pogodowe, nazwa_miasta):

        temp = dane_pogodowe.get("temp", "--")
        wiatr = dane_pogodowe.get("wiatr", "--")
        kod_wmo = dane_pogodowe.get("kod_pogody", 0)
        odczuwalna = dane_pogodowe.get("odczuwalna_temp", "--")

        self.location_label.config(text=nazwa_miasta)
        self.temp_label.config(text=f"{temp}°")
        self.wind_label.config(text=f"{wiatr} km/h")
        self.feels_like_label.config(text=f"{odczuwalna}°")

        info = self.weather_map.get(kod_wmo, {"opis": "Nieznana", "ikona": "cloudy.png"})
        self.desc_label.config(text=info["opis"])
        self._laduj_ikone(info["ikona"])

    def _laduj_ikone(self, nazwa_pliku):
        pelna_sciezka = os.path.join(self.icons_dir, nazwa_pliku)
        if not os.path.exists(pelna_sciezka):
            self.icon_label.config(text="[Brak ikony]", image="")
            return
        try:
            image = Image.open(pelna_sciezka)
            image = image.resize((140, 140))
            photo = ImageTk.PhotoImage(image)
            self.icon_label.config(image=photo)
            self.icon_label.image = photo
        except Exception as e:
            print(f"Błąd: {e}")

    def pobierz_dane(self):
        miasto = self.city_combo.get().strip()

        self.root.config(cursor="watch")
        self.root.update()

        try:
            dane = get_weather_now_by_city(miasto)

            if dane is None:
                messagebox.showerror("Błąd",
                                     f"Nie udało się pobrać danych dla miasta: {miasto}.\nSprawdź połączenie lub spróbuj później.")
                self.czysc_widok_po_bledzie()
            else:
                self.aktualizuj_ui(dane, miasto)

        except Exception as e:
            print(f"Błąd krytyczny: {e}")
            messagebox.showerror("Błąd", "Wystąpił nieoczekiwany błąd aplikacji.")

        finally:
            self.root.config(cursor="")

    def czysc_widok_po_bledzie(self):
        self.location_label.config(text="Błąd")
        self.temp_label.config(text="--")
        self.desc_label.config(text="Brak danych")
        self.wind_label.config(text="--")
        self.feels_like_label.config(text="--")
        self.icon_label.config(image="", text="❌")


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherAppUI(root)
    root.mainloop()
