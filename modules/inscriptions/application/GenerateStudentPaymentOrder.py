from datetime import datetime
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from io import BytesIO

class GenerateStudentPaymentOrder:
    def __init__(
        self,
        nombre_estudiante: str,
        ci: str,
        correo: str,
        convocatoria_nombre: str,
        areas: list,
        total: float,
        orden_number: str
    ):
        self.nombre_estudiante = nombre_estudiante
        self.ci = ci
        self.correo              = correo
        self.convocatoria_nombre = convocatoria_nombre
        self.fecha_emision       = datetime.today().strftime('%d/%m/%Y')
        self.areas               = areas
        self.total               = total
        self.orden_number        = orden_number

    def generar_orden_pago(self):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=LETTER)
        width, height = LETTER

        x_margin = 50
        y = height - 50

        # Encabezado
        c.setFont("Helvetica-Bold", 14)
        c.drawString(x_margin, y, "UNIVERSIDAD MAYOR DE SAN SIMÓN")
        c.setFont("Helvetica", 10)
        c.drawRightString(width - x_margin,
                          y,
                          f"Fecha de emisión: {self.fecha_emision}")
        y -= 20

        # Aquí imprimimos el número de orden:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x_margin, y, f"Código de Orden: {self.orden_number}")
        y -= 30

        # Título de la convocatoria
        c.setFont("Helvetica-Bold", 14)
        c.drawString(x_margin, y, "FACULTAD DE CIENCIAS Y TECNOLOGÍA")
        y -= 20
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width / 2,
                            y,
                            f"ORDEN DE PAGO – {self.convocatoria_nombre}")
        y -= 40

        # Datos del Estudiante
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x_margin, y, "Datos del Estudiante:")
        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(x_margin, y, f"Nombre completo: {self.nombre_estudiante}")
        y -= 15
        c.drawString(x_margin, y, f"CI: {self.ci}")
        y -= 15
        c.drawString(x_margin, y, f"Correo electrónico: {self.correo}")
        y -= 30

        # Tabla de áreas
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x_margin, y, "Áreas Seleccionadas:")
        y -= 20

        c.setFont("Helvetica-Bold", 10)
        c.drawString(x_margin, y, "N°")
        c.drawString(x_margin + 30, y, "Área")
        c.drawString(x_margin + 200, y, "Categoría")
        c.drawString(x_margin + 370, y, "Monto (Bs.)")
        y -= 15

        c.setFont("Helvetica", 10)
        for i, area in enumerate(self.areas, 1):
            nombre_area = area.get('area', 'N/D')
            categoria = area.get('categoria', 'N/D')
            monto = area.get('monto') or 0.0

            c.drawString(x_margin, y, str(i))
            c.drawString(x_margin + 30, y, nombre_area)
            c.drawString(x_margin + 200, y, categoria)
            c.drawString(x_margin + 370, y, f"{monto:.2f}")
            y -= 15

        # Total
        y -= 20
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x_margin + 300,
                     y,
                     f"Total a pagar: Bs. {self.total:.2f}")

        c.save()
        buffer.seek(0)
        return buffer
