import unittest
import tkinter as tk
from unittest.mock import patch, MagicMock
from app.gui.main_window import WeatherAppUI

class TestIntegrationGUI(unittest.TestCase):
    
    def setUp(self):
        """Przygotowanie środowiska przed każdym testem (tworzenie okna)."""
        self.root = tk.Tk()
        # Ukrywamy okno podczas testów
        self.root.withdraw() 
        # Patchujemy 'root.after' aby nie uruchamiał się automat przy starcie inita
        with patch.object(tk.Tk, 'after'):
            self.app = WeatherAppUI(self.root)

    def tearDown(self):
        """Sprzątanie po testach."""
        self.root.destroy()

    @patch('app.gui.main_window.get_weather_now_by_city')
    @patch('app.gui.main_window.get_forecast_by_city')
    def test_pobierz_dane_flow(self, mock_forecast, mock_weather_now):
        """
        Test integracyjny: Sprawdza przepływ danych od 'API' do Etykiet w GUI.
        Symulujemy wybór miasta 'Wrocław' i sprawdzamy czy UI się zaktualizowało.
        """
        # 1. Przygotowanie danych (Mock API response)
        mock_weather_now.return_value = {
            "temp": 15.5,
            "wiatr": 20,
            "odczuwalna_temp": 14,
            "kod_pogody": 0
        }
        # Uproszczona prognoza
        mock_forecast.return_value = [{
            "data": "17.01.2026",
            "temp_max": 16,
            "temp_min": 10,
            "godziny": [{"kod_pogody": 0} for _ in range(24)] # Fake godziny
        }]

        # 2. Symulacja interakcji użytkownika
        self.app.city_combo.set("Wrocław")
        
        # 3. Wywołanie metody, która spina wszystko
        self.app.pobierz_dane()

        # 4. Sprawdzenie czy Mocki zostały wywołane
        mock_weather_now.assert_called_with("Wrocław")
        
        # 5. Weryfikacja stanu GUI (Czy etykiety wyświetlają to co zwróciło API?)
        self.assertEqual(self.app.location_label.cget("text"), "Wrocław")
        self.assertEqual(self.app.temp_label.cget("text"), "15.5°")
        self.assertEqual(self.app.wind_label.cget("text"), "20 km/h")
        # Sprawdzenie czy opis pogody zmapował się poprawnie (kod 0 -> Czyste niebo)
        self.assertEqual(self.app.desc_label.cget("text"), "Czyste niebo")

    @patch('app.gui.main_window.messagebox.showerror')
    @patch('app.gui.main_window.get_weather_now_by_city')
    def test_error_handling_flow(self, mock_weather_now, mock_msgbox):
        """Test integracyjny: Sprawdza czy błąd API wywołuje okno błędu w GUI."""
        # Symulacja błędu API (zwraca None)
        mock_weather_now.return_value = None
        
        self.app.city_combo.set("Gdańsk")
        self.app.pobierz_dane()

        # Sprawdź czy wywołano messagebox
        mock_msgbox.assert_called()
        # Sprawdź czy UI zostało wyczyszczone (pokazuje błąd)
        self.assertEqual(self.app.location_label.cget("text"), "Błąd")

if __name__ == '__main__':
    unittest.main()