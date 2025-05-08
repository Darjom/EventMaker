# ManejoArchivosService.py
import os
import uuid
import cv2
from werkzeug.utils import secure_filename
from flask import url_for, current_app

class GestorArchivosOriginales:
    def __init__(self):
        # Definir como atributo de instancia
        self.CARPETA_UPLOADS = os.path.join(current_app.root_path, 'static', 'uploads')
        self.crear_directorio()

    def crear_directorio(self):
        """Crea el directorio usando la ruta de la aplicación"""
        try:
            os.makedirs(self.CARPETA_UPLOADS, exist_ok=True)
        except Exception as e:
            raise RuntimeError(f"Error creando directorio: {str(e)}")

    def guardar_original(self, archivo):
        """Guarda el archivo en static/uploads"""
        try:
            if not archivo or archivo.filename == '':
                raise ValueError("Archivo inválido")
            
            extension = os.path.splitext(archivo.filename)[1].lower()
            nombre_unico = f"{uuid.uuid4().hex}{extension}"
            nombre_seguro = secure_filename(nombre_unico)
            
            ruta_completa = os.path.join(self.CARPETA_UPLOADS, nombre_seguro)
            archivo.save(ruta_completa)
            
            if not os.path.exists(ruta_completa):
                raise RuntimeError("Falló el guardado del archivo")
            
            return nombre_seguro
            
        except Exception as e:
            raise RuntimeError(f"Error guardando archivo: {str(e)}")

    def obtener_ruta_original(self, nombre_archivo):
        return os.path.join(self.CARPETA_UPLOADS, nombre_archivo)
    
    def eliminar_original(self, nombre_archivo):
        ruta = self.obtener_ruta_original(nombre_archivo)
        if os.path.exists(ruta):
            os.remove(ruta)
    
    def generar_url_original(self, nombre_archivo):
        return url_for('static', filename=f'uploads/{nombre_archivo}')
    
    def guardar_preview(self, imagen_cv, tipo):
        """Guarda una imagen temporal para previsualización"""
        try:
            nombre = f"{tipo}_{uuid.uuid4().hex}.jpg"
            ruta = os.path.join(self.CARPETA_UPLOADS, nombre)
            cv2.imwrite(ruta, imagen_cv)
            return nombre
        except Exception as e:
            raise RuntimeError(f"Error guardando preview: {str(e)}")