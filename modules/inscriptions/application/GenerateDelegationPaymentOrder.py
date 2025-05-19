import os
from datetime import datetime
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfbase.pdfmetrics import stringWidth
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

        # Encabezado
        # Posición y tamaño de la imagen
        logo_x = x_margin
        logo_y = height - 120
        logo_width = 100
        logo_height = 100

        # Ruta de la imagen
        PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
        image_path = os.path.join(PROJECT_ROOT, 'static', 'img', 'FondoBoleta', 'logo_umss.png')

        # Padding interno de la imagen
        padding = 5

        # imagen sin cuadro
        c.drawImage(
            image_path,
            logo_x + padding,
            logo_y + padding,
            width=logo_width - 2 * padding,
            height=logo_height - 2 * padding,
            preserveAspectRatio=True,
            mask='auto'
        )

        # Nombre de la convocatoria
        c.setFont("Helvetica-Bold", 9)
        c.setFillColorRGB(0, 0, 0)

        max_width = 150
        font_name = "Helvetica-Bold"
        font_size = 9
        line_height = 11
        text = str(self.convocatoria_nombre)

        # Word wrap manual
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if c.stringWidth(test_line, font_name, font_size) <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        # centradas debajo del logo
        for idx, line in enumerate(lines):
            y_offset = logo_y - 12 - (idx * line_height)
            c.drawCentredString(logo_x + logo_width / 2, y_offset, line)

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
        c.drawString(x_margin, y, "Detalle de Inscripciones por Estudiantes:")
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
        c.drawString(x_margin + 250, text_y, "Área")
        c.drawString(x_margin + 350, text_y, "Categoría")
        c.drawString(x_margin + 450, text_y, "Monto (Bs.)")

        # Posición inicial
        y = table_top - header_height - 8
        c.setFont("Helvetica", 9)

        # Anchos de columnas (ajusta según tu layout)
        col_widths = [150, 100, 110, 100, 40]  # Nombre, Curso, Área, Categoría, Monto
        line_height = 10  # altura de línea

        for estudiante_nombre, datos in self.estudiantes_info.items():
            curso = datos.get("curso") or "N/D"
            for insc in datos.get("inscripciones", []):
                area = insc.get("area_name", "N/D")
                categoria = insc.get("category_name", "N/D")
                monto = insc.get("category_monto") or 0.0
                monto_str = f"{monto:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

                values = [estudiante_nombre, curso, area, categoria, monto_str]
                wrapped_values = []
                max_lines = 1

                # Envolver texto por columna si se excede
                for i, value in enumerate(values):
                    col_width = col_widths[i]
                    text = str(value)
                    if stringWidth(text, "Helvetica", 9) > col_width:
                        approx_chars = int(col_width / stringWidth("A", "Helvetica", 9))
                        lines = [text[j:j + approx_chars] for j in range(0, len(text), approx_chars)]
                    else:
                        lines = [text]
                    wrapped_values.append(lines)
                    max_lines = max(max_lines, len(lines))

                # Dibujar línea por línea
                x = x_margin
                for line_idx in range(max_lines):
                    x = x_margin
                    for col_idx, lines in enumerate(wrapped_values):
                        if line_idx < len(lines):
                            if col_idx == 4:
                                c.drawRightString(x + col_widths[col_idx], y - line_idx * line_height, lines[line_idx])
                            else:
                                c.drawString(x, y - line_idx * line_height, lines[line_idx])
                        x += col_widths[col_idx]

                y -= max_lines * 9

                # Salto de página si se acaba el espacio
                if y < 80:
                    c.showPage()
                    y = height - 50
                    c.setFont("Helvetica", 9)

        #Espacio antes del total
        y -= 80

        #Logo marca de agua
        try:
            PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
            image_path = os.path.join(PROJECT_ROOT, 'static', 'img', 'FondoBoleta', 'logo_umss.png')

            print("Ruta imagen:", image_path)
            print("¿Existe?", os.path.exists(image_path))  # Verificación útil

            logo_width = 200
            logo_height = 200
            logo_x = (width - logo_width) / 2
            logo_y = (height - logo_height) / 2 - 50

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

        # Línea horizontal
        c.setStrokeColor(colors.lightgrey)
        c.setLineWidth(1)
        c.line(x_margin - 5, y, width - x_margin + 5, y)

        # Texto de total
        y -= 20
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x_margin, y, "Total a pagar:")
        c.drawRightString(x_margin + 500, y, f"Bs {self.total:,.2f}")

        # Pie de página
        y -= 70
        c.setFont("Helvetica", 9)
        c.drawRightString(width - x_margin, y, "EventMaker")
        c.drawRightString(width - x_margin, y - 12, "Universidad Mayor de San Simón")
        c.drawRightString(width - x_margin, y - 24, "Cochabamba - Bolivia")

        c.save()
        buffer.seek(0)
        return buffer
