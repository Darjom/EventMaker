import io
from openpyxl import Workbook
from typing import Dict, Any


class ExcelReportGenerator:
    """
    Generador de reportes en Excel en memoria:
    - Una hoja por categoría.
    - Cabecera con nombre de categoría y columnas fijas.
    """
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    def generate(self) -> io.BytesIO:
        wb = Workbook()
        # Eliminar la hoja por defecto
        default = wb.active
        wb.remove(default)

        for cat_name, cat_info in self.data.items():
            # Título de hoja (máx 31 caracteres)
            ws = wb.create_sheet(title=cat_name[:31])

            # Título de categoría en la primera fila
            ws.append([cat_name])
            # Encabezados de columna
            ws.append(["Apellidos", "Nombres", "Colegio", "Departamento", "Provincia"])

            # Filas con datos de cada estudiante
            for student in cat_info["students"]:
                ws.append([
                    student["last_name"],
                    student["first_name"],
                    student["school_name"],
                    student["department"],
                    student["province"]
                ])

            # Una fila en blanco para separar (opcional)
            ws.append([])

        # Guardar en memoria
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)  # Volver al inicio del buffer
        return output
