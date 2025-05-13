import cv2
import numpy as np
from PIL import Image, ImageOps
from pdf2image import convert_from_bytes

class ImageProcessorService:
    def __init__(self):
        self.tamano_objetivo = (1920, 1080)
        self.tolerancia_bordes = 10

    @staticmethod
    def process_uploaded_image(file_stream):
        img = Image.open(file_stream)
        img = ImageOps.exif_transpose(img)
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        return ImageProcessorService.recortar_y_rescalar(img_cv)
    
    @staticmethod
    def recortar_y_rescalar(img):
        # 1. Redimensionamiento inicial
        resized = cv2.resize(img, (1920, 1080), interpolation=cv2.INTER_LANCZOS4)
        
        # 2. Preprocesamiento para detección de bordes
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 50, 150)
        
        # 3. Detección de contornos
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 4. Parámetros de recorte
        img_height, img_width = resized.shape[:2]
        x, y, w, h = 0, 0, img_width, img_height
        
        if contours:
            main_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(main_contour)
            
            # Validación de bordes con tolerancia
            bordes_tocados = (
                x <= 10 or
                y <= 10 or
                (x + w) >= (img_width - 10) or
                (y + h) >= (img_height - 10)
            )
            
            if bordes_tocados:
                x, y, w, h = 0, 0, img_width, img_height
        
        # 5. Operación de recorte
        cropped = resized[y:y+h, x:x+w]
        
        # 6. Redimensionado final
        return cv2.resize(cropped, (1920, 1080), interpolation=cv2.INTER_LANCZOS4)
    
    @staticmethod
    def grisado(img):
        gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return gris
    
    @staticmethod
    def rescalado(img):
        factor_escala = 3
        rescalado = cv2.resize(
            img,
            None,
            fx=factor_escala,
            fy=factor_escala,
            interpolation=cv2.INTER_CUBIC
        )
        return rescalado
    
    @staticmethod
    def nitidizacion(img):
        blurred = cv2.GaussianBlur(img, (0, 0), sigmaX=3)
        nitido = cv2.addWeighted(img, 1.5, blurred, -0.5, 0)
        return nitido
    
    @staticmethod
    def binarizacion(img):
        _, binario = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binario

    @staticmethod
    def RecortarNumero(img):
        """Recorta el área del número de la papeleta"""
        try:
            return img[0:100, 1550:1920]
        except Exception as e:
            raise RuntimeError(f"Error recortando número: {str(e)}")
        
    @staticmethod
    def RecortarNombre(img):
        """Recorta el área del nombre en la papeleta"""
        try:
            return img[510:560, 330:1060]
        except Exception as e:
            raise RuntimeError(f"Error recortando nombre: {str(e)}")
        
    @staticmethod
    def RecortarMonto(img):
        """Recorta el área del monto en la papeleta"""
        try:
            return img[630:690, 1750:1890]
        except Exception as e:
            raise RuntimeError(f"Error recortando monto: {str(e)}")
    
    @staticmethod    
    def preprocesar_para_ocr(img):
        # Corregido: Usar métodos estáticos existentes
        gris = ImageProcessorService.grisado(img)
        rescala = ImageProcessorService.rescalado(gris)
        nitido = ImageProcessorService.nitidizacion(rescala)
        return ImageProcessorService.binarizacion(nitido)