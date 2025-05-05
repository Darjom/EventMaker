from datetime import datetime
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from io import BytesIO


class GenerateDelegationPaymentOrder:
    def __init__(self, tutor_nombre, tutor_ci, tutor_correo, convocatoria_nombre, estudiantes_info: dict):
        self.tutor_nombre = tutor_nombre
        self.tutor_ci = tutor_ci
        self.tutor_correo = tutor_correo
        self.convocatoria_nombre = convocatoria_nombre
        self.estudiantes_info = estudiantes_info
        self.fecha_emision = datetime.today().strftime('%d/%m/%Y')
        self.total = self.__calcular_total()

    def __calcular_total(self):
        total = 0.0
        for estudiante_data in self.estudiantes_info.values():
            for insc in estudiante_data["inscripciones"]:
                monto = insc.get("category_monto") or 0.0
                total += monto
        return total

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
        c.drawRightString(width - x_margin, y, f"Fecha de emisión: {self.fecha_emision}")
        y -= 20

        c.setFont("Helvetica-Bold", 14)
        c.drawString(x_margin, y, "FACULTAD DE CIENCIAS Y TECNOLOGÍA")
        y -= 20

        c.drawCentredString(width / 2, y, f"ORDEN DE PAGO – {self.convocatoria_nombre}")
        y -= 40

        # Datos del Tutor
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x_margin, y, "Datos del Tutor:")
        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(x_margin, y, f"Nombre completo: {self.tutor_nombre}")
        y -= 15
        c.drawString(x_margin, y, f"CI: {self.tutor_ci}")
        y -= 15
        c.drawString(x_margin, y, f"Correo electrónico: {self.tutor_correo}")
        y -= 30

        # Detalle de Inscripciones
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x_margin, y, "Detalle de Inscripciones por Estudiante:")
        y -= 20

        c.setFont("Helvetica-Bold", 10)
        c.drawString(x_margin, y, "Estudiante")
        c.drawString(x_margin + 150, y, "Curso")
        c.drawString(x_margin + 230, y, "Área")
        c.drawString(x_margin + 350, y, "Categoría")
        c.drawString(x_margin + 470, y, "Monto (Bs.)")
        y -= 15

        c.setFont("Helvetica", 10)
        for estudiante_nombre, datos in self.estudiantes_info.items():
            curso = datos.get("curso", "N/D") or "N/D"
            for insc in datos["inscripciones"]:
                area = insc.get("area_name", "N/D")
                categoria = insc.get("category_name", "N/D")
                monto = insc.get("category_monto") or 0.0

                c.drawString(x_margin, y, estudiante_nombre)
                c.drawString(x_margin + 150, y, curso)
                c.drawString(x_margin + 230, y, area)
                c.drawString(x_margin + 350, y, categoria)
                c.drawRightString(x_margin + 540, y, f"{monto:.2f}")
                y -= 15

                # Salto de página si se termina el espacio
                if y < 80:
                    c.showPage()
                    y = height - 50
                    c.setFont("Helvetica", 10)

        y -= 20
        c.setFont("Helvetica-Bold", 10)
        c.drawRightString(x_margin + 540, y, f"Total a pagar: Bs. {self.total:.2f}")

        c.save()
        buffer.seek(0)
        return buffer, self.total
