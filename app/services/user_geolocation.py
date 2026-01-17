import geocoder

def get_location():
    """
    Funkcja zwracająca przybliżone współrzędne geograficzne urządzenia na podstawie adresu IP.
    :return: Współrzędne geograficzne urządzenia w postaci [lat, lng]
    """
    try:
        # Przeniesiono tę linię do środka bloku try, aby wyłapać błąd braku sieci
        location = geocoder.ip('me')

        if location.ok:
            return location.latlng
        else:
            print("Nie udało się pobrać lokalizacji")
            return None
    except Exception as e:
        print(f"Błąd: {e}")
        return None