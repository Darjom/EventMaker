# ProcesamientoOCR.py
import pytesseract

class ProcesadorOCR:
    @staticmethod
    def extraer_numero(imagen_preprocesada):
        """Extrae el número de la región procesada"""
        try:
            return pytesseract.image_to_string(
                imagen_preprocesada,
                lang='spa',
                config='--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789.,'
            ).strip()
        except Exception as e:
            raise RuntimeError(f"Error extrayendo número: {str(e)}")

    @staticmethod
    def extraer_nombre(imagen_preprocesada):
        """Extrae el nombre de la región procesada"""
        try:
            return pytesseract.image_to_string(
                imagen_preprocesada,
                lang='spa',
                config='--psm 6 --oem 3'
            ).strip()
        except Exception as e:
            raise RuntimeError(f"Error extrayendo nombre: {str(e)}")

    @staticmethod
    def extraer_monto(imagen_preprocesada):
        """Extrae el monto de la región procesada"""
        try:
            return pytesseract.image_to_string(
                imagen_preprocesada,
                lang='spa',
                config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789.,'
            ).strip()
        except Exception as e:
            raise RuntimeError(f"Error extrayendo monto: {str(e)}")

    @classmethod
    def procesar_todo(cls, numero_img, nombre_img, monto_img):
        """Procesa todas las regiones y devuelve los resultados"""
        return {
            'numero': cls.extraer_numero(numero_img),
            'nombre': cls.extraer_nombre(nombre_img),
            'monto': cls.extraer_monto(monto_img)
        }