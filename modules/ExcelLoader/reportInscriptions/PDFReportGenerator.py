import io
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from typing import Dict, Any


class PDFReportGenerator:
    """
    Generador de reportes en PDF en memoria:
    - Sección por categoría.
    - Cada sección con título y tabla con bordes.
    """
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.styles = getSampleStyleSheet()

    def generate(self) -> io.BytesIO:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []

        for cat_name, cat_info in self.data.items():
            # Título de sección
            elements.append(Paragraph(cat_name, self.styles['Heading2']))
            elements.append(Spacer(1, 12))

            # Preparar datos de la tabla
            table_data = [["Apellidos", "Nombres", "Colegio", "Departamento", "Provincia"]]
            for student in cat_info["students"]:
                table_data.append([
                    student["last_name"],
                    student["first_name"],
                    student["school_name"],
                    student["department"],
                    student["province"]
                ])

            table = Table(table_data, repeatRows=1)
            table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER')
            ]))
            elements.append(table)
            elements.append(Spacer(1, 24))

        doc.build(elements)
        buffer.seek(0)
        return buffer
