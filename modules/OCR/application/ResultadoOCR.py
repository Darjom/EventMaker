class ResultadoOCR:
    """
    DTO que encapsula todos los datos resultantes del proceso OCR
    Attributes:
        numero: str         # código de factura/recibo
        nombre: str         # nombre extraído (opcional)
        monto: str          # monto extraído
        url_original: str   # URL de la imagen completa
        previews: dict      # URLs de vistas previas recortadas
    """
    def __init__(self, numero, nombre, monto, url_original, previews):
        self.numero = numero
        self.nombre = nombre
        self.monto = monto
        self.url_original = url_original
        self.previews = previews
