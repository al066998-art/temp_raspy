"""
Define la clase 'Potentiometer'

Encapsula toda la lógica para leer y calibrar el potenciómetro
conectado a un pin GPIO.
"""

import RPi.GPIO as GPIO
import time

class Potentiometer:

    """Maneja la lectura y calibración de un potenciómetro"""

    def __init__(self, pin):

        """Inicializa el potenciómetro en un pin específico"""

        self.pin = pin
        self.min_value = 0   # mínimo 
        self.max_value = 100 # máximo 
        GPIO.setmode(GPIO.BCM) # Usar numeración de pines BCM
        print(f"Potenciómetro inicializado en pin {pin}")

    def read_raw_value(self):

        """
        Mide el tiempo de carga del capacitor
        
        Este es el método "RC Time" para leer un sensor analógico
        en un pin digital de la Raspberry Pi
        
        Returns:
            int: El "valor crudo" (tiempo de carga)
        """
        count = 0
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, False)
        time.sleep(0.1)  # Descarga completa del capacitor

        # Cambia el pin a modo ENTRADA para leerlo
        GPIO.setup(self.pin, GPIO.IN)

        # Mide cuánto tiempo tarda en cargarse (pasar a HIGH)
        while GPIO.input(self.pin) == GPIO.LOW:
            count += 1
            if count > 100000:  # Timeout para evitar un bucle infinito
                break
        return count

    def calibrate(self):

        """Inicia el proceso de calibración por el usuario"""

        print("CALIBRACIÓN DEL POTENCIÓMETRO")
        input("Gira completamente a la izquierda (mínimo) y presiona Enter...")
        self.min_value = self.read_raw_value()
        print(f"Valor mínimo registrado: {self.min_value}")

        input("Gira completamente a la derecha (máximo) y presiona Enter...")
        self.max_value = self.read_raw_value()
        print(f"Valor máximo registrado: {self.max_value}")

        # Evita división por cero si max <= min
        if self.max_value <= self.min_value:
            print("¡Advertencia! Mínimo y máximo son iguales o invertidos. Ajustando...")
            self.max_value = self.min_value + 100 

        print(f"Calibración completada: Mínimo={self.min_value}, Máximo={self.max_value}")

    def get_normalized_value(self):

        """
        Obtiene la lectura actual y la convierte a valores útiles
        
        Returns:
            tuple (int, float, float):
                - value (valor crudo)
                - normalized (porcentaje 0-100)
                - resistance_approx (resistencia 0-10000)
        """
        value = self.read_raw_value()
        normalized = 0.0

        # Normaliza el valor crudo a un porcentaje (0-100)
        if (self.max_value - self.min_value) > 0:
            normalized = (value - self.min_value) / (self.max_value - self.min_value) * 100.0
            # Asegura que el valor esté entre 0 y 100
            normalized = max(0, min(100, normalized)) 

        resistance_approx = (normalized / 100) * 10000  
        
        return value, normalized, resistance_approx