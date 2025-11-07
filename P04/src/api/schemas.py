"""

Define los "schemas" de datos para la API

"""

# Esquema para el endpoint /api/sensor
SENSOR_DATA_SCHEMA = {
    "Valor crudo": int,
    "porcentaje": str, 
    "resistencia aproximada": str, 
    "ultima_actualizacion": str
}

# Para el endpoint /api/estado
STATUS_SCHEMA = {
    "estado": str,
    "timestamp": str 
}

# Para el endpoint /
API_INFO_SCHEMA = {
    "mensaje": str,
    "endpoints": list
}