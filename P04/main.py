import RPi.GPIO as GPIO
import time
import logging
import sys
import os

# Añade la carpeta raíz al path de Python
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR) 

# CLIENTE
# Importaciones modulares
from src.client.api_client import SensorAPIClient
from src.hardware.servo import Servo

SERVO_PIN = 18 
API_BASE_URL = "http://192.168.137.225:5000" 

# Configurar mensajes de estado
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main_loop():

    """Inicia y ejecuta el bucle principal del cliente"""

    try: 
        # Inicializar componentes
        client = SensorAPIClient(API_BASE_URL)
        servo = Servo(SERVO_PIN)
        logging.info("Cliente de API y Servo iniciados.")
    except Exception as e:
        logging.error(f"No se pudo inicializar el hardware o cliente: {e}")
        return 

    # Bucle principal
    logging.info("Iniciando bucle de control...")
    while True:
        try:
            # Obtener datos de la API
            data = client.get_sensor_data(retries=2)
            
            if data is None:
                # Si la API falla, se reintenta tras una pausa
                logging.warning("No se pudieron obtener datos de la API. Reintentando...")
                time.sleep(2)
                continue

            # Procesar datos
            percentage_str = data.get("porcentaje", "0%").replace('%', '')
            percentage = float(percentage_str)
            
            # Calcular ángulo (0-100% -> 0-180 grados)
            angle = (percentage / 100) * 180
            
            # Mover servo
            logging.info(f"API: {percentage:.1f}% -> Servo movido a {angle:.1f} grados.")
            servo.set_angle(angle)
            time.sleep(0.5) # Pausa para no saturar

        except (KeyboardInterrupt, SystemExit):
            logging.info("Deteniendo bucle de control...")
            break # Sale del bucle 'while True'
        except Exception as e:
            logging.error(f"Error en el bucle principal: {e}")
            time.sleep(2)

    logging.info("Limpiando recursos...")
    servo.cleanup()
    GPIO.cleanup() 
    logging.info("Aplicación cliente detenida.")

if __name__ == "__main__":

    """Punto de entrada principal para el cliente"""
    try:
        main_loop()
    except Exception as e:
        # Captura final para asegurar la limpieza de GPIO
        logging.critical(f"Error crítico, forzando limpieza: {e}")
        GPIO.cleanup()