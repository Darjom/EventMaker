document.getElementById('miFormulario').addEventListener('submit',async(e) =>{
    e.preventDefault()
    const datos ={
        titulo: document.getElementById('nombre').value,
        descripción: document.getElementById('descripción').value,
        fecha_inicio: document.getElementById('fecha_inicio').value,
        fecha_fin: document.getElementById('fecha_fin').value,
        capacidad: document.getElementById('capacidad').value,
        requisitos: document.getElementById('requisitos').value,
        mensaje: document.getElementById('mensaje').value,
        imagen: document.getElementById('imagen').value,
    };

    try {
        // Enviar datos al backend
        const respuesta = await fetch('/crearEvento', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datos)
        });

        const resultado = await respuesta.json();
        
        if (respuesta.ok) {
            document.getElementById('mensaje').textContent = "Tutor registrado exitosamente!";
        } else {
            throw new Error(resultado.error || 'Error en el servidor');
        }
    } catch (error) {
        document.getElementById('mensaje').textContent = `Error: ${error.message}`;
    }
});