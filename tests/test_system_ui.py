import unittest
import tkinter as tk
from unittest.mock import patch
from app.gui.main_window import WeatherAppUI

class TestSystemStructure(unittest.TestCase):
    """Testy sprawdzające strukturę i inicjalizację GUI (Smoke Tests)."""

    def setUp(self):
        self.root = tk.Tk()
        # Ukrywamy okno podczas testów
        self.root.withdraw()
        # Blokujemy automatyczne zapytania sieciowe przy starcie
        with patch.object(tk.Tk, 'after'):
            self.app = WeatherAppUI(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_initial_window_properties(self):
        """Sprawdza czy tytuł i rozmiar okna są poprawne."""
        # WYMUSZENIE ODŚWIEŻENIA
        self.root.update()
        """Sprawdza czy tytuł i rozmiar okna są poprawne."""
        self.assertEqual(self.root.title(), "Aplikacja Pogodowa")
        # Sprawdzenie czy geometria została ustawiona
        self.assertTrue(self.root.geometry().startswith("800x550"))

    def test_widgets_existence(self):
        """Sprawdza czy kluczowe elementy interfejsu zostały utworzone."""
        # Czy istnieje pole wyboru miasta
        self.assertIsInstance(self.app.city_combo, tk.ttk.Combobox)
        # Czy istnieje etykieta temperatury
        self.assertIsInstance(self.app.temp_label, tk.ttk.Label)
        # Czy istnieje Canvas do wykresu
        self.assertIsInstance(self.app.chart_canvas, tk.Canvas)

    def test_city_list_completeness(self):
        """Sprawdza czy lista miast w Comboboxie zawiera wymagane pozycje."""
        wymagane_miasta = ["Warszawa", "Kraków", "Łódź", "Wrocław", "Poznań", "Moja lokalizacja"]
        dostepne = self.app.dostepne_miasta
        
        for miasto in wymagane_miasta:
            self.assertIn(miasto, dostepne, f"Brakuje miasta {miasto} na liście")

    def test_default_selection(self):
        """Sprawdza domyślny stan aplikacji po uruchomieniu."""
        # Domyślny tekst w combo
        self.assertEqual(self.app.city_combo.get(), "Moja lokalizacja")
        # Domyślny tekst temperatury (przed pobraniem danych)
        self.assertEqual(self.app.temp_label.cget("text"), "--°")

if __name__ == '__main__':
    unittest.main()