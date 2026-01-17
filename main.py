import tkinter as tk
from app.gui.main_window import WeatherAppUI

def main():
    """
    Główna funkcja uruchamiająca aplikację pogodową.
    """
    # Tworzenie głównego okna instancji Tkinter
    root = tk.Tk()
    
    # Ustawienie tytułu okna aplikacji
    root.title("Aplikacja Pogodowa")
    
    # Inicjalizacja interfejsu użytkownika
    # Przekazujemy 'root' do klasy, która zarządza widokiem
    app = WeatherAppUI(root)
    
    # Uruchomienie pętli zdarzeń (aplikacja czeka na interakcję użytkownika)
    root.mainloop()

if __name__ == "__main__":
    main()