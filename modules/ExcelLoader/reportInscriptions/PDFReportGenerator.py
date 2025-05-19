import io
import os
from typing import Dict, Any

from reportlab.pdfbase.pdfmetrics import stringWidth
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

        # Título del evento
        c.setFont("Helvetica-Bold", 15)
        c.drawCentredString(width / 2, y, f"{self.event.nombre_evento}")
        y -= 60

        # Guarda la posición actual de y para no afectar el resto
        y_guardado = y

        # --- INICIO Sección dividida en dos columnas ---
        column_mid = width / 2
        left_margin = x_margin
        right_margin = column_mid + 20

        # Usamos y_guardado como altura de inicio de esta sección
        y_local = y_guardado

        # Columna izquierda - texto
        c.setFont("Helvetica-BoldOblique", 12)
        c.drawString(left_margin, y_local, self.event.slogan)
        y_local -= 30

        c.setFont("Helvetica", 10)
        c.drawString(left_margin, y_local, f"Fecha de inicio:      {self.event.inicio_evento.strftime('%Y-%m-%d')}")
        y_local -= 20
        c.drawString(left_margin, y_local, f"Fecha de finalización: {self.event.fin_evento.strftime('%Y-%m-%d')}")

        # Columna derecha - imagen del afiche
        PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        afiche_rel_path = self.event.afiche

        if afiche_rel_path:
            if afiche_rel_path.startswith("static/"):
                afiche_path = os.path.join(PROJECT_ROOT, afiche_rel_path)
            else:
                afiche_path = os.path.join(PROJECT_ROOT, "static", afiche_rel_path)

            afiche_width = 150
            afiche_height = 100
            afiche_x = right_margin + 30
            afiche_y = y_guardado - afiche_height + 40  # Alineado con el texto

            padding = 5

            if os.path.exists(afiche_path):
                c.drawImage(
                    afiche_path,
                    afiche_x + padding,
                    afiche_y,
                    width=afiche_width - 2 * padding,
                    height=afiche_height - 2 * padding,
                    preserveAspectRatio=True,
                    mask='auto'
                )
            else:
                c.setFont("Helvetica", 9)
                c.drawString(afiche_x, afiche_y + 10, "Afiche no encontrado")

        # --- FIN Sección dividida en columnas ---

        # Continúa el contenido más abajo sin perder y global
        y = min(afiche_y, y_local) - 30

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
                max_lines = 1
                values = [
                    student.get("last_name", ""),
                    student.get("first_name", ""),
                    student.get("school_name", ""),
                    student.get("department", ""),
                    student.get("province", "")
                ]
                wrapped_values = []  # Lista de líneas divididas por columna
                for i, value in enumerate(values):
                    col_width = col_widths[i]
                    text = str(value)
                    if stringWidth(text, "Helvetica", 9) > col_width:
                        # Si se desborda, dividimos en múltiples líneas
                        approx_chars = int(col_width / stringWidth("A", "Helvetica", 9))
                        lines = [text[i:i + approx_chars] for i in range(0, len(text), approx_chars)]
                    else:
                        lines = [text]
                    wrapped_values.append(lines)
                    max_lines = max(max_lines, len(lines))  # Guardamos el máximo de líneas de esta fila

                # Dibujamos línea por línea cada valor
                for line_idx in range(max_lines):
                    x = x_margin
                    for col_idx, lines in enumerate(wrapped_values):
                        if line_idx < len(lines):
                            c.drawString(x + 2, y + 3 - line_idx * 10, lines[line_idx])
                        x += col_widths[col_idx]

                y -= max_lines * 14 #espacio entre estudiantes

            y -= 22  # Espacio después de cada categoría

        c.save()
        buffer.seek(0)
        return buffer
