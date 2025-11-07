"""
Servidor principal de la API
Inicia Flask, sirve la vista web y lee el potenciómetro
"""

import RPi.GPIO as GPIO
import time
from flask import Flask, jsonify, send_from_directory  
from datetime import datetime
import threading
import sys
import os

# Encuentra la carpeta raíz del proyecto 
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Define la ruta a la carpeta 'assets' 
ASSETS_DIR = os.path.join(ROOT_DIR, 'assets')

# Importación modular
from src.hardware.potentiometer import Potentiometer

POT_PIN = 4 

app = Flask(
    __name__,
    static_folder=ASSETS_DIR,  # Define la carpeta de assets
    static_url_path='/assets'  # Define la URL para los assets
)

# Variables globales, protegidas por un 'lock'
datos_sensor = {
    "Valor crudo": 0,
    "porcentaje": '0%',
    "resistencia aproximada": "0Ω",
    "ultima_actualizacion": None
}

datos_sensor_lock = threading.Lock() # Evita errores entre hilos

# Instancia del hardware
pot = Potentiometer(pin=POT_PIN)

# Endpoints de la API
@app.route('/')
def home():

    """Sirve la información principal de la API (endpoint /)"""

    return jsonify({
        "mensaje": "API del Sensor", 
        "endpoints": ["/api/sensor", "/api/estado"],
        "vista": "Ve a /vista para ver los datos en tiempo real" 
    })

@app.route('/vista') 
def get_vista(): 

    """Sirve la vista web 'index.html' enviando desde la raiz"""

    return send_from_directory(ROOT_DIR, 'index.html')

@app.route('/api/sensor')
def get_sensor_data():

    """Endpoint para obtener los datos actuales del sensor"""

    with datos_sensor_lock:
        return jsonify(datos_sensor.copy())

@app.route('/api/estado')
def get_status():

    """Endpoint para verificar que el servidor está funcionando"""

    return jsonify({
        "estado": "sistema funcionando", 
        "timestamp": datetime.now().isoformat()
    })

def sensor_update_loop():

    """Hilo que lee el potenciómetro y actualiza datos_sensor"""

    # Bucle que lee el sensor en segundo plano
    while True:
        try:
            # Llama al método de la clase de hardware
            value, normalized, resistance_approx = pot.get_normalized_value()
            
            # Imprimir en consola local 
            print(f"Valor crudo: {value:4d} -> {normalized:5.1f}% -> ~{resistance_approx:4.0f}Ω")

            # Actualizar datos globales usando lock por seguridad
            with datos_sensor_lock:
                datos_sensor["Valor crudo"] = value
                datos_sensor["porcentaje"] = f"{normalized:5.1f}%"
                datos_sensor["resistencia aproximada"] = f"~{resistance_approx:4.0f}Ω"
                datos_sensor["ultima_actualizacion"] = datetime.now().isoformat()
            
            time.sleep(0.3)
        
        except Exception as e:
            print(f"Error en el hilo sensor_update_loop(): {e}")
            time.sleep(2)

# Iniciar servidor
def start_server():

    """Inicia la calibración, el hilo del sensor y el servidor Flask"""

    try:

        pot.calibrate()
        
        print("Iniciando hilo de actualización del sensor...")
        sensor_thread = threading.Thread(target=sensor_update_loop, daemon=True)
        sensor_thread.start()

        print("\nIniciando servidor Flask en http://0.0.0.0:5000")
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

    except KeyboardInterrupt:
        print("\nDeteniendo servidor...")
    finally:
        GPIO.cleanup()
        print("GPIO limpiado.")

# Entrada
if __name__ == "__main__":
    start_server()