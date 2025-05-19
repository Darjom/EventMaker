import io
import os
from typing import Dict, Any
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

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

        # Posición y tamaño del afiche
        afiche_width = 200
        afiche_height = 150
        afiche_x = width - afiche_width - x_margin
        afiche_y = y - afiche_height - 20
        padding = 5

        if self.event.afiche:
            print(self.event.afiche)
            PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
            # Si self.event.afiche ya comienza con 'static/', no agregues 'static' otra vez.
            afiche_rel_path = self.event.afiche
            if afiche_rel_path.startswith("static/"):
                afiche_path = os.path.join(PROJECT_ROOT, afiche_rel_path)
            else:
                afiche_path = os.path.join(PROJECT_ROOT, "static", afiche_rel_path)

            print(f"[DEBUG] Ruta del afiche: {afiche_path}")
            if os.path.exists(afiche_path):
                print(f"[✔] Afiche encontrado: {afiche_path}")
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
                print(f"[✘] Archivo NO encontrado en: {afiche_path}")
        y = afiche_y - 40

        # Reporte por categorías
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
