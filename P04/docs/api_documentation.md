Documentación de la API 

Esta API expone las lecturas de un potenciómetro conectado a una Raspberry Pi y sirve una interfaz web para visualizarlas en tiempo real.

Endpoints de la API

1. GET /

Muestra información básica de la API, los endpoints de datos disponibles y el enlace a la vista web.

Respuesta Ejemplo (JSON):

{
  "mensaje": "API del Sensor",
  "endpoints": [
    "/api/sensor",
    "/api/estado"
  ],
  "vista": "Ve a /vista para ver los datos en tiempo real"
}


2. GET /api/sensor

Obtiene la última lectura procesada del potenciómetro. Este es el endpoint que consumen el cliente del servo (main.py) y el frontend (script.js).

Respuesta Ejemplo (JSON):

{
  "Valor crudo": 1530,
  "porcentaje": "45.1%",
  "resistencia aproximada": "~4510Ω",
  "ultima_actualizacion": "2025-11-07T01:30:01.123456"
}


3. GET /api/estado

Verifica que el servidor de la API esté funcionando.

Respuesta Ejemplo (JSON):

{
  "estado": "sistema funcionando",
  "timestamp": "2025-11-07T01:31:05.654321"
}


Endpoints de la Interfaz Web (Frontend)

4. GET /vista

Sirve la página web principal (index.html), que es el panel de control (dashboard) visual. El navegador cargará esta página, la cual internamente llamará a /api/sensor para obtener los datos en vivo.

Respuesta:

Content-Type: text/html

El contenido del archivo index.html.