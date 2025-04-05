document.getElementById('miFormulario').addEventListener('submit',async(e) =>{
    e.preventDefault()
    const datos ={
        titulo: document.getElementById('titulo').value,
        imagen: document.getElementById('imagen').value,
    };

    try {
        // Enviar datos al backend
        const respuesta = await fetch('/crearArea', {
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