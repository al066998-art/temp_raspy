"""
Define la clase 'Servo' 

Encapsula la lógica para controlar un servomotor
usando pulsos PWM en un pin GPIO
"""

import RPi.GPIO as GPIO
import time

class Servo:

    """Maneja el control de un servomotor"""

    def __init__(self, pin):

        """Inicializa el servo en un pin específico"""

        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        
        # Inicializa PWM a 50Hz
        self.pwm = GPIO.PWM(self.pin, 50) 
        self.pwm.start(0) # Inicia el servo sin enviar pulso
        print(f"Servo inicializado en pin {pin}")

    def set_angle(self, angle):

        """
        Mueve el servo a un ángulo específico (0-180 grados)
        
        Args:
            angle (float): Ángulo deseado
        """
        # Limita el ángulo 
        angle = max(0, min(180, angle))
        
        # Convierte ángulo (0-180) a ciclo de trabajo (2-12)
        # 2% = 0 grados, 12% = 180 grados
        duty = (angle / 18) + 2
        
        # Envía el pulso PWM
        GPIO.output(self.pin, True)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(0.5) # Tiempo para que el servo llegue
        
        # Detiene el pulso para evitar "temblor"
        GPIO.output(self.pin, False)
        self.pwm.ChangeDutyCycle(0) 

    def cleanup(self):

        """Detiene el PWM y limpia el pin"""

        self.pwm.stop()
        print(f"PWM detenido en pin {self.pin}")