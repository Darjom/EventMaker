console.log('JS cargado correctamente');

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('miFormulario');
    const imagenInput = document.getElementById('imagen');
    const previewContainer = document.getElementById('preview-container');
    const previewImage = document.getElementById('preview-image');
    const errorMessage = document.getElementById('image-error');
    const mensajeDiv = document.getElementById('mensaje');
    const submitBtn = form.querySelector('button[type="submit"]');
    const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];

    const showMessage = (text, isError = false) => {
        mensajeDiv.textContent = text;
        mensajeDiv.style.color = isError ? 'red' : 'green';
        mensajeDiv.style.display = 'block';
        if (!isError) {
            setTimeout(() => mensajeDiv.style.display = 'none', 3000);
        }
    };

    imagenInput.addEventListener('change', function() {
        const file = this.files[0];
        errorMessage.textContent = '';
        previewContainer.style.display = 'none';

        if (file) {
            if (!allowedTypes.includes(file.type)) {
                errorMessage.textContent = 'Solo se permiten imágenes (JPEG, PNG, WEBP)';
                this.value = '';
                previewImage.src = '#'; // Limpiar la vista previa
                return;
            }

            const reader = new FileReader();
            reader.onload = (e) => {
                previewImage.src = e.target.result;
                previewContainer.style.display = 'block';
                previewImage.style.display = 'block'; // Asegurar visibilidad
            };
            reader.onerror = (error) => {
                console.error('Error al leer la imagen:', error);
                errorMessage.textContent = 'Error al cargar la imagen';
            };
            reader.readAsDataURL(file);
            
        } else {
            previewImage.src = '#'; // Limpiar si no hay archivo
            previewContainer.style.display = 'none';
        }
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        showMessage('');
        const originalBtnText = submitBtn.innerHTML;

        try {
            if (!document.getElementById('TerminosYCondiciones').checked) {
                throw new Error('Debe aceptar los términos y condiciones');
            }

            const file = imagenInput.files[0];
            if (file && !allowedTypes.includes(file.type)) {
                throw new Error('Tipo de archivo no permitido');
            }

            submitBtn.disabled = true;
            submitBtn.innerHTML = 'Creando...';

            const formData = new FormData(form);

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

            // Redirección al evento
            const eventoId = formData.get('idevento');
            window.location.href = `/evento/ver/${eventoId}`;

        } catch (error) {
            console.error('Error:', error);
            showMessage(`Error: ${error.message}`, true);
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnText;
        }
    });

});
