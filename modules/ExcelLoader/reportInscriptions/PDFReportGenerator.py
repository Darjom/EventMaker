import io
import os

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from typing import Dict, Any
from reportlab.lib import colors

from modules.events.domain.Event import Event


class PDFReportGenerator:
    """
    Generador de reportes en PDF en memoria:
    - Sección por categoría.
    - Cada sección con título y tabla con bordes.
    """
    def __init__(self, data: Dict[str, Any], event: Event):
        self.data = data
        self.event = event
        self.styles = getSampleStyleSheet()

    def generate(self):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=LETTER)
        width, height = LETTER
        x_margin = 50
        y = height - 50

        # Encabezado general
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width / 2, y, "UNIVERSIDAD MAYOR DE SAN SIMON")
        y -= 18
        c.setFont("Helvetica", 12)
        c.drawCentredString(width / 2, y, "FACULTAD DE CIENCIA Y TECNOLOGIA")
        y -= 30


        # Encabezado convocatoria

        # Título del evento y eslogan
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width / 2, y, f"{self.event.nombre_evento}")
        y -= 40
        c.setFont("Helvetica-BoldOblique", 12)
        c.drawString(x_margin, y, f"{self.event.slogan}")
        y -= 20

        # Fechas
        c.setFont("Helvetica", 9)
        c.drawString(x_margin, y, f"Fecha de inicio:         {self.event.inicio_evento}")
        y -= 20
        c.drawString(x_margin, y, f"Fecha de finalizacion:  {self.event.fin_evento}")

        # Posición y tamaño para el afiche
        afiche_path = os.path.join(os.getcwd(), self.event.afiche)

        afiche_x = width - x_margin - 100
        afiche_y = height - 140
        afiche_width = 100
        afiche_height = 100
        padding = 5

        # Verificar existencia del archivo e insertarlo
        if os.path.exists(afiche_path):
            c.drawImage(
                afiche_path,
                afiche_x + padding,
                afiche_y + padding,
                width=afiche_width - 2 * padding,
                height=afiche_height - 2 * padding,
                preserveAspectRatio=True,
                mask='auto'
            )
        else:
            c.setFont("Helvetica", 10)
            c.drawString(afiche_x, afiche_y, "Afiche no encontrado")
        # Reporte por categorías
        y -= 40
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(width / 2, y, "Reporte por categorías")
        y -= 20

        for cat_name, cat_info in self.data.items():
            # Título de categoría
            c.setFont("Helvetica-Bold", 11)
            c.drawString(x_margin, y, f"{cat_name}")
            y -= 30

            # Encabezado de tabla
            headers = ["Apellidos", "Nombres", "Colegio", "Departamento", "Provincia"]
            col_widths = [100, 100, 120, 80, 80]
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(colors.lightgrey)
            c.rect(x_margin, y, sum(col_widths), 18, fill=1, stroke=0)

            c.setFillColor(colors.black)
            x = x_margin
            for i, header in enumerate(headers):
                c.drawString(x + 2, y + 5, header)
                x += col_widths[i]
            y -= 18

            # Filas de estudiantes
            c.setFont("Helvetica", 9)
            for student in cat_info.get("students", []):
                if y < 80:
                    c.showPage()
                    y = height - 50
                x = x_margin
                values = [
                    student.get("last_name", ""),
                    student.get("first_name", ""),
                    student.get("school_name", ""),
                    student.get("department", ""),
                    student.get("province", "")
                ]
                for i, value in enumerate(values):
                    c.drawString(x + 2, y + 3, str(value))
                    x += col_widths[i]
                y -= 16

            y -= 24  # Espacio después de cada categoría

        c.save()
        buffer.seek(0)
        return buffer
