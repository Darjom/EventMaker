import os
from datetime import datetime
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib import colors

class GenerateDelegationPaymentOrder:
    def __init__(
        self,
        tutor_nombre: str,
        tutor_ci: str,
        tutor_correo: str,
        convocatoria_nombre: str,
        estudiantes_info: dict,
        total: float,
        orden_number: str
    ):
        self.tutor_nombre = tutor_nombre
        self.tutor_ci = tutor_ci
        self.tutor_correo = tutor_correo
        self.convocatoria_nombre = convocatoria_nombre
        self.fecha_emision = datetime.today().strftime('%d/%m/%Y')
        self.estudiantes_info = estudiantes_info
        self.total = total
        self.orden_number = orden_number

    def generar_orden_pago(self):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=LETTER)
        width, height = LETTER

        x_margin = 50
        y = height - 50

        # === Encabezado ===
        logo_x = x_margin
        logo_y = height - 120
        logo_width = 100
        logo_height = 100

        c.setStrokeColorRGB(1, 0, 0)  # rojo
        c.setLineWidth(1.5)
        c.rect(logo_x, logo_y, logo_width, logo_height)

        try:
            PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
            image_path = os.path.join(PROJECT_ROOT, 'static', 'img', 'FondoBoleta', 'logo_umss.png')
        except Exception:
            # fallback si __file__ no está definido
            image_path = "EventMaker/static/img/FondoBoleta/logo_umss.png"

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

        c.setFont("Helvetica-Bold", 9)
        c.setFillColorRGB(0, 0, 0)
        c.drawCentredString(logo_x + logo_width / 2, logo_y - 12, f" {self.convocatoria_nombre}")

        # Información derecha encabezado
        c.setFont("Helvetica-Bold", 14)
        c.setFillColorRGB(0, 0, 0)
        right_x = width / 2 + 60
        c.drawCentredString(right_x, height - 50, "ORDEN DE PAGO")

        c.setFont("Helvetica", 10)
        c.drawString(right_x, height - 65, f"Fecha: {self.fecha_emision}")
        c.drawString(right_x, height - 80, f"Código de Orden: {self.orden_number}")

        # Títulos centrales
        y = logo_y - 40
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(width / 2, y, "UNIVERSIDAD MAYOR DE SAN SIMÓN")
        y -= 15
        c.drawCentredString(width / 2, y, "FACULTAD DE CIENCIAS Y TECNOLOGÍA")
        y -= 25

        # Datos del Tutor
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x_margin, y, "Datos del Tutor:")
        y -= 20

        c.setFont("Helvetica-Bold", 10)
        c.drawString(x_margin, y, "Nombre completo:")
        y -= 12
        c.setFont("Helvetica", 10)
        c.drawString(x_margin + 15, y, self.tutor_nombre)
        y -= 18

        c.setFont("Helvetica-Bold", 10)
        c.drawString(x_margin, y, "CI:")
        y -= 12
        c.setFont("Helvetica", 10)
        c.drawString(x_margin + 15, y, self.tutor_ci)
        y -= 18

        c.setFont("Helvetica-Bold", 10)
        c.drawString(x_margin, y, "Correo electrónico:")
        y -= 12
        c.setFont("Helvetica", 10)
        c.drawString(x_margin + 15, y, self.tutor_correo)
        y -= 30

        # Detalle inscripciones por estudiante - tabla
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x_margin, y, "Detalle de Inscripciones por Estudiante:")
        y -= 20

        # Encabezado tabla
        c.setFont("Helvetica-Bold", 10)
        header_height = 18
        row_height = 18
        table_top = y
        table_width = width - 2 * x_margin + 10

        # Fondo gris encabezado tabla
        c.setFillColor(colors.lightgrey)
        c.rect(x_margin - 5, table_top - header_height + 4, table_width, header_height, fill=1, stroke=0)

        # Texto encabezado tabla con márgenes
        text_y = table_top - header_height + 8
        c.setFillColor(colors.black)
        c.drawString(x_margin, text_y, "Estudiante")
        c.drawString(x_margin + 150, text_y, "Curso")
        c.drawString(x_margin + 230, text_y, "Área")
        c.drawString(x_margin + 350, text_y, "Categoría")
        c.drawString(x_margin + 470, text_y, "Monto (Bs.)")

        # Posición inicial filas datos
        y = table_top - header_height - 8
        c.setFont("Helvetica", 10)

        for estudiante_nombre, datos in self.estudiantes_info.items():
            curso = datos.get("curso") or "N/D"
            for insc in datos.get("inscripciones", []):
                area = insc.get("area_name", "N/D")
                categoria = insc.get("category_name", "N/D")
                monto = insc.get("category_monto") or 0.0
                monto_str = f"{monto:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

                c.drawString(x_margin, y, estudiante_nombre)
                c.drawString(x_margin + 150, y, curso)
                c.drawString(x_margin + 230, y, area)
                c.drawString(x_margin + 350, y, categoria)
                c.drawRightString(x_margin + 540, y, monto_str)
                y -= row_height

                # Salto de página si queda poco espacio
                if y < 80:
                    c.showPage()
                    y = height - 50
                    c.setFont("Helvetica", 10)

        # Línea y total
        y -= 20
        c.setStrokeColor(colors.lightgrey)
        c.setLineWidth(1)
        c.line(x_margin - 5, y, width - x_margin + 5, y)

        y -= 20
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x_margin, y, "Total a pagar:")
        c.drawRightString(x_margin + 540, y, f"Bs {self.total:,.2f}")

        # Pie de página
        y -= 90
        c.setFont("Helvetica", 9)
        c.drawRightString(width - x_margin, y, "EventMaker")
        c.drawRightString(width - x_margin, y - 12, "Universidad Mayor de San Simón")
        c.drawRightString(width - x_margin, y - 24, "Cochabamba - Bolivia")

        c.save()
        buffer.seek(0)
        return buffer
