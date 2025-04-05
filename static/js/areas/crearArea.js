document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('miFormulario');
    const imagenInput = document.getElementById('imagen');
    const previewContainer = document.getElementById('preview-container');
    const previewImage = document.getElementById('preview-image');
    const errorMessage = document.getElementById('image-error');
    const mensajeDiv = document.getElementById('mensaje');
    const submitBtn = form.querySelector('button[type="submit"]');
    const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];

    // Función para mostrar mensajes
    const showMessage = (text, isError = false) => {
        mensajeDiv.textContent = text;
        mensajeDiv.style.color = isError ? 'red' : 'green';
        mensajeDiv.style.display = 'block';
        if (!isError) {
            setTimeout(() => mensajeDiv.style.display = 'none', 3000);
        }
    };

    // Preview de imagen
    imagenInput.addEventListener('change', function() {
        const file = this.files[0];
        errorMessage.textContent = '';
        previewContainer.style.display = 'none';

        if (file) {
            if (!allowedTypes.includes(file.type)) {
                errorMessage.textContent = 'Solo se permiten imágenes (JPEG, PNG, WEBP)';
                this.value = '';
                return;
            }

            const reader = new FileReader();
            reader.onload = (e) => {
                previewImage.src = e.target.result;
                previewContainer.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    });

    // Envío del formulario
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        showMessage(''); // Limpiar mensajes anteriores
        const originalBtnText = submitBtn.innerHTML;

        try {
            // Validaciones
            if (!document.getElementById('Terminos y condiciones').checked) {
                throw new Error('Debe aceptar los términos y condiciones');
            }

            const file = imagenInput.files[0];
            if (file && !allowedTypes.includes(file.type)) {
                throw new Error('Tipo de archivo no permitido');
            }

            // Deshabilitar botón durante el envío
            submitBtn.disabled = true;
            submitBtn.innerHTML = 'Creando...';

            // Crear FormData
            const formData = new FormData(form);
            formData.append('idevento', '3');

            const response = await fetch('/area/crear', {
                method: 'POST',
                body: formData,
                headers: {
                    'Accept': 'application/json'
                }
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'Error en el servidor');
            }

            // Éxito
            showMessage(result.message);
            form.reset();
            previewContainer.style.display = 'none';
            setTimeout(() => window.location.href = '/area/crear', 1500);

        } catch (error) {
            console.error('Error:', error);
            showMessage(`Error: ${error.message}`, true);
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnText;
        }
    });
});