"""
Define la clase 'SensorAPIClient'

Esta clase se encarga de toda la lógica de charla con la API del sensor,
incluyendo el manejo de errores y los reintentos
"""

import requests
import time

class SensorAPIClient:

    """Maneja la comunicación con la API del sensor"""

    def __init__(self, base_url="http://127.0.0.1:5000"):

        """Inicializa el cliente con la URL base de la API"""

        self.base_url = base_url
        print(f"Cliente de API inicializado para {base_url}")

    def get_sensor_data(self, retries=3, delay=1):

        """
        Obtiene los datos del sensor (/api/sensor) con reintentos
        
        Args:
            retries (int): Número de intentos
            delay (int): Segundos de espera entre intentos
        
        Returns:
            dict: Los datos JSON del sensor, o None si falla
        """

        url = f"{self.base_url}/api/sensor"
        
        # Bucle de reintentos
        for attempt in range(retries):
            try:
                # Intentar conectarse (timeout de 2s)
                response = requests.get(url, timeout=2)
                response.raise_for_status() # Lanza error si es 4xx o 5xx
                return response.json() # Devuelve los datos si todo va bien
            
            except requests.exceptions.ConnectionError as e:
                # Falla si el servidor está apagado
                print(f"Intento {attempt + 1}/{retries}: Error de conexión. Reintentando en {delay}s...")
                time.sleep(delay)
            except requests.exceptions.RequestException as e:
                # Cualquier otro error 
                print(f"Intento {attempt + 1}/{retries}: Error en la API: {e}")
                time.sleep(delay)
        
        # Si el bucle termina sin éxito
        print(f"Fallo al obtener datos después de {retries} intentos.")
        return None

    def get_status(self):

        """Obtiene el estado del servidor (/api/status)"""

        try:
            response = requests.get(f"{self.base_url}/api/status", timeout=2)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al verificar estado de la API: {e}")
            return None