import os
from datetime import datetime
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib import colors

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
        # Recuadro rojo
        logo_x = x_margin
        logo_y = height - 120
        logo_width = 100
        logo_height = 100

        c.setStrokeColorRGB(1, 0, 0)  # rojo
        c.setLineWidth(1.5)
        c.rect(logo_x, logo_y, logo_width, logo_height)

        # Imagen dentro del recuadro
        PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))  # Sube desde el archivo actual

        PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))  # Sube desde el módulo

        image_path = os.path.join(PROJECT_ROOT, 'static', 'img', 'FondoBoleta', 'logo_umss.png')
        padding = 5
 
        c.drawImage(
            image_path,
            logo_x + padding,
            logo_y + padding,
            width=logo_width - 2 * padding,
            height=logo_height - 2 * padding,
            preserveAspectRatio=True,
            mask='auto'
        )

        # Texto bajo el recuadro
        c.setFont("Helvetica-Bold", 9)
        c.setFillColorRGB(0, 0, 0)
        c.drawCentredString(logo_x + logo_width / 2, logo_y - 12, f" {self.convocatoria_nombre}")

        # INFORMACIÓN DEL ENCABEZADO derecha
        c.setFont("Helvetica-Bold", 14)
        c.setFillColorRGB(0, 0, 0)
        c.drawCentredString(width / 2 + 60, height - 50, "ORDEN DE PAGO")

        c.setFont("Helvetica", 10)
        c.drawString(width / 2 + 60, height - 65, f"Fecha: {self.fecha_emision}")
        c.drawString(width / 2 + 60, height - 80, f"Boleta: {self.orden_number}")




        # Título de la convocatoria
        y = logo_y - 40
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(width / 2, y, "UNIVERSIDAD MAYOR DE SAN SIMÓN")
        y -= 15
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(width / 2, y, "FACULTAD DE CIENCIAS Y TECNOLOGÍA")
        y -= 25


        # Datos del Estudiante
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x_margin, y, "Datos del Estudiante:")
        y -= 20

        c.setFont("Helvetica-Bold", 10)
        c.drawString(x_margin, y, "Nombre completo:")
        y -= 12
        c.setFont("Helvetica", 10)
        c.drawString(x_margin + 15, y, self.nombre_estudiante)
        y -= 18

        c.setFont("Helvetica-Bold", 10)
        c.drawString(x_margin, y, "CI:")
        y -= 12
        c.setFont("Helvetica", 10)
        c.drawString(x_margin + 15, y, self.ci)
        y -= 18

        c.setFont("Helvetica-Bold", 10)
        c.drawString(x_margin, y, "Correo electrónico:")
        y -= 12
        c.setFont("Helvetica", 10)
        c.drawString(x_margin + 15, y, self.correo)
        y -= 30

        # tabla
        c.setFont("Helvetica-Bold", 10)
        header_height = 18
        row_height = 18
        table_top = y  # Posición superior de la tabla
        table_bottom = y  # Iremos bajando para calcular esto

        header_x = x_margin
        header_width = width - 2 * x_margin
        header_height = 18

        # Dibuja el rectángulo gris para el fondo del encabezado
        c.setFillColor(colors.lightgrey)
        c.rect(header_x, y - header_height + 4, header_width, header_height, fill=1, stroke=0)

        # Texto del encabezado (con un poco de margen vertical)
        text_y = y - header_height + 8
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(header_x + 5, text_y, "Nro")
        c.drawString(header_x + 45, text_y, "Área")
        c.drawString(header_x + 225, text_y, "Categoría")
        c.drawString(header_x + 385, text_y, "Monto(Bs)")

        # Posición inicial para filas
        y = table_top - header_height - 18
        table_bottom = y - (len(self.areas) * row_height)

        try:
            PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
            image_path = os.path.join(PROJECT_ROOT, 'static', 'img', 'FondoBoleta', 'logo_umss.png')

            logo_width = 130
            logo_height = 130
            logo_x = (width - logo_width) / 2
            logo_y = table_bottom - 100  # Debajo de filas

            c.saveState()
            c.setFillAlpha(0.1)
            c.drawImage(
                image_path,
                logo_x,
                logo_y,
                width=logo_width,
                height=logo_height,
                preserveAspectRatio=True,
                mask='auto'
            )
            c.restoreState()
        except Exception as e:
            print("No se pudo cargar la imagen como marca de agua:", e)

        # Filas de datos
        c.setFont("Helvetica", 10)
        y = table_top - header_height - 8
        for i, area in enumerate(self.areas, 1):
            nombre_area = area.get('area', 'N/D')
            categoria = area.get('categoria', 'N/D')
            monto = area.get('monto') or 0.0
            monto_str = f"{monto:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            c.drawString(header_x + 5, y, str(i))
            c.drawString(header_x + 45, y, nombre_area)
            c.drawString(header_x + 225, y, categoria)
            c.drawRightString(header_x + 455, y, monto_str)
            y -= row_height

        # Línea y total — ya fue bajado arriba
        y -= 120  # espacio antes del total
        c.setStrokeColor(colors.lightgrey)
        c.setLineWidth(1)
        c.line(x_margin - 5, y, width - x_margin + 5, y)

        y -= 20
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x_margin, y, "Total a pagar:")
        c.drawRightString(x_margin + 450, y, f"Bs  {self.total:,.2f}")

        # Pie de página — se baja aún más
        y -= 90  # bjar posicion
        c.setFont("Helvetica", 9)
        c.drawRightString(width - x_margin, y, "EventMaker")
        c.drawRightString(width - x_margin, y - 12, "Universidad Mayor de San Simón")
        c.drawRightString(width - x_margin, y - 24, "Cochabamba - Bolivia")

        c.save()
        buffer.seek(0)
        return buffer
