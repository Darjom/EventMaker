# shared/image_rotator.py
import os
from datetime import datetime
from PIL import Image
from werkzeug.utils import secure_filename
from flask import current_app


class ImageRotator:
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

    @classmethod
    def is_allowed_file(cls, filename):
        """
        Verifica si la extensión del archivo está permitida.
        :param filename: Nombre del archivo a verificar
        :return: True si la extensión es válida, False en caso contrario
        """
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in cls.ALLOWED_EXTENSIONS

    @staticmethod
    def save_rotated_image(file, angle=90):
        """
        Guarda la imagen rotada en el directorio predeterminado.

        :param file: Archivo de imagen de Flask/Werkzeug
        :param angle: Ángulo de rotación (90 grados por defecto)
        :return: Ruta relativa para la base de datos (ej: 'img/uploads/filename.jpg')
        """
        # Directorio absoluto (basado en la raíz de la app Flask)
        upload_dir = os.path.join(
            current_app.root_path,  # Raíz del proyecto (EventMaker/)
            'static',
            'img',
            'uploads'
        )

        # Generar nombre seguro y único
        filename = secure_filename(file.filename)
        unique_filename = f"{datetime.now().timestamp()}_{filename}"
        save_path = os.path.join(upload_dir, unique_filename)

        # Rotar y guardar la imagen
        try:
            image = Image.open(file.stream)
            rotated_image = image.rotate(angle, expand=True)
            rotated_image.save(save_path)
        except Exception as e:
            raise RuntimeError(f"Error al procesar la imagen: {str(e)}")

        # Retornar ruta relativa (para guardar en DB)
        return os.path.join('img', 'uploads', unique_filename)