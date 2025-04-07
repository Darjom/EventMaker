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
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in cls.ALLOWED_EXTENSIONS

    @staticmethod
    def save_rotated_image(file, angle=0):
        upload_dir = os.path.join(
            current_app.root_path,
            'static',
            'img',
            'uploads'
        )

        filename = secure_filename(file.filename)
        unique_filename = f"{datetime.now().timestamp()}_{filename}"
        save_path = os.path.join(upload_dir, unique_filename)

        try:
            image = Image.open(file.stream)
            rotated_image = image.rotate(angle, expand=True)
            rotated_image.save(save_path)
        except Exception as e:
            raise RuntimeError(f"Error al procesar la imagen: {str(e)}")

        # ⚠️ Esta es la línea que soluciona tu problema:
        return os.path.join('img', 'uploads', unique_filename).replace("\\", "/")
