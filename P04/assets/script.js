const apiUrl = '/api/sensor'; // Llamar a la API en el mismo servidor
const statusLight = document.getElementById('status-light');
const dataPorcentaje = document.getElementById('data-porcentaje');
const dataCrudo = document.getElementById('data-crudo');
const dataResistencia = document.getElementById('data-resistencia');
const dataActualizacion = document.getElementById('data-actualizacion');

async function fetchData() {
    try {
        // Obtener datos
        const response = await fetch(apiUrl);
        
        if (!response.ok) {
            throw new Error('Error en la red');
        }
        
        const data = await response.json();
        
        // Actualizar
        dataPorcentaje.textContent = data.porcentaje;
        dataCrudo.textContent = data['Valor crudo'];
        dataResistencia.textContent = data['resistencia aproximada'];
        
        // Formatear la fecha para que sea legible
        const fecha = new Date(data.ultima_actualizacion);
        dataActualizacion.textContent = fecha.toLocaleTimeString();
        
        // Verde = conectado
        statusLight.style.backgroundColor = '#28a745';

    } catch (error) {
        // Rojo = error
        console.error('Error al obtener datos:', error);
        statusLight.style.backgroundColor = '#dc3545';
        dataPorcentaje.textContent = 'Error';
        dataCrudo.textContent = 'Error';
        dataResistencia.textContent = 'Error';
        dataActualizacion.textContent = 'Desconectado';
    }
}

// Llama a fetchData cada 0.5 segundos
setInterval(fetchData, 500);

// LLamar al inicio sin espera
fetchData();