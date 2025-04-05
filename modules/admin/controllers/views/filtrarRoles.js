// Función para cargar opciones
async function cargarOpcionesSelect() {
    const select = document.querySelector("#tipoUsuario");
    
    try {
        // Realizar solicitud GET
        const respuesta = await fetch("https://tu-api.com/tipos-usuarios");
        const datos = await respuesta.json();

        // Limpiar opciones iniciales
        select.innerHTML = "";

        // Añadir primera opción (placeholder)
        const opcionDefault = new Option("Tipo de Usuario", "");
        opcionDefault.disabled = true;
        opcionDefault.selected = true;
        select.add(opcionDefault);

        // Crear opciones dinámicamente
        datos.forEach(tipo => {
            const opcion = new Option(tipo.nombre, tipo.valor);
            select.add(opcion);
        });

    } catch (error) {
        // Manejar errores
        console.error("Error al cargar opciones:", error);
        select.innerHTML = '<option value="" disabled selected>Error al cargar datos</option>';
    }
}

// Ejecutar al cargar la página
document.addEventListener("DOMContentLoaded", cargarOpcionesSelect);