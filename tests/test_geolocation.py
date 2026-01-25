import unittest
from unittest.mock import patch, MagicMock

from app.services.user_geolocation import get_location


class TestUserGeolocation(unittest.TestCase):

    @patch('app.services.user_geolocation.geocoder')
    def test_get_location_success(self, mock_geocoder):
        """Testuje scenariusz, gdy geocoder zwraca poprawną lokalizację."""
        # Konfiguracja mocka
        mock_location = MagicMock()
        mock_location.ok = True
        mock_location.latlng = [52.2297, 21.0122]
        mock_geocoder.ip.return_value = mock_location

        # Wywołanie funkcji
        result = get_location()

        # Asercje
        self.assertEqual(result, [52.2297, 21.0122])
        mock_geocoder.ip.assert_called_with('me')

    @patch('app.services.user_geolocation.geocoder')
    def test_get_location_failure(self, mock_geocoder):
        """Testuje scenariusz, gdy nie uda się pobrać lokalizacji (np. brak IP)."""
        mock_location = MagicMock()
        mock_location.ok = False
        mock_geocoder.ip.return_value = mock_location

        result = get_location()

        self.assertIsNone(result)

    @patch('app.services.user_geolocation.geocoder')
    def test_get_location_exception(self, mock_geocoder):
        """Testuje scenariusz, gdy wystąpi wyjątek (np. brak internetu)."""
        mock_geocoder.ip.side_effect = Exception("Brak sieci")

        result = get_location()

        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
