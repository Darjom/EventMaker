from modules.OCR.application.ManejoArchivosService import GestorArchivosOriginales
from modules.OCR.application.PreprocesamientoOCRService import ImageProcessorService
from modules.OCR.application.ProcesamientoOCRService import ProcesadorOCR
from modules.OCR.application.ResultadoOCR import ResultadoOCR


class OrquestadorOCRService:
    def __init__(self,
                 gestor: GestorArchivosOriginales = None,
                 procesador_img: ImageProcessorService = None,
                 ocr_proc: ProcesadorOCR = None):
        # Inyección de dependencias con valores por defecto
        self.gestor = gestor or GestorArchivosOriginales()
        self.procesador = procesador_img or ImageProcessorService()
        self.ocr = ocr_proc or ProcesadorOCR()

    def procesar_factura(self, archivo) -> ResultadoOCR:
        """
        Orquesta flujo completo:
          1) Guarda la imagen original
          2) Genera recortes de número, nombre y monto
          3) Preprocesa esas regiones para OCR
          4) Extrae texto con Tesseract
          5) Genera URLs de vistas previas
        """
        # 1. Guardar original y obtener URL
        nombre_archivo = self.gestor.guardar_original(archivo)
        url_original = self.gestor.generar_url_original(nombre_archivo)

        # 2. Cargar y procesar imagen completa
        ruta = self.gestor.obtener_ruta_original(nombre_archivo)
        with open(ruta, 'rb') as f:
            img = self.procesador.process_uploaded_image(f)

        # 3. Recortar regiones de interés
        regiones = {
            'numero': self.procesador.RecortarNumero(img),
            'nombre': self.procesador.RecortarNombre(img),
            'monto': self.procesador.RecortarMonto(img)
        }

        # 4. Preprocesar y extraer cada región
        resultados = {}
        previews = {}
        for key, region in regiones.items():
            pre = self.procesador.preprocesar_para_ocr(region)
            # extraer valor (solo números para numero/monto, texto libre para nombre)
            if key == 'numero':
                resultados[key] = self.ocr.extraer_numero(pre)
            elif key == 'monto':
                resultados[key] = self.ocr.extraer_monto(pre)
            else:
                resultados[key] = self.ocr.extraer_nombre(pre)

            # guardar preview y generar URL
            nombre_prev = self.gestor.guardar_preview(region, key)
            previews[key] = self.gestor.generar_url_original(nombre_prev)

        # 5. Construir DTO y devolver
        return ResultadoOCR(
            numero=resultados['numero'],
            nombre=resultados['nombre'],
            monto=resultados['monto'],
            url_original=url_original,
            previews=previews
        )