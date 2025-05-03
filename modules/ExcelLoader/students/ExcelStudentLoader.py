# excel_students_loader/loader.py

from typing import List
from datetime import datetime

from modules.ExcelLoader.students.ExcelStudentReader import ExcelStudentReader
from modules.students.application.dtos.StudentDTO import StudentDTO
from modules.ExcelLoader.students.StudentExcelHeaders import StudentExcelHeaders as H


class ExcelStudentLoader:
    def __init__(self, file):
        self.reader = ExcelStudentReader(file)

    def parse_date(self, date_value) -> datetime | None:
        if isinstance(date_value, datetime):
            return date_value
        try:
            return datetime.strptime(str(date_value), "%d/%m/%Y")
        except Exception:
            return None

    def validate_required_headers(self, headers: List[str]) -> List[str]:
        required = [h.value for h in H]
        missing = [h for h in required if h not in headers]
        return missing

    def validate_header_order(self, headers: List[str]) -> bool:
        expected = [h.value for h in H]
        return headers == expected

    def load(self) -> List[StudentDTO]:
        raw_data = self.reader.read()
        if not raw_data:
            raise ValueError("El archivo está vacío o no tiene datos.")

        headers = self.reader.get_headers()
        missing = self.validate_required_headers(headers)
        if missing:
            raise ValueError(f"Faltan los siguientes encabezados requeridos: {missing}")

        # Descomenta si quieres validar también el orden exacto
        # if not self.validate_header_order(headers):
        #     raise ValueError("El orden de los encabezados no coincide con el esperado.")

        students = []
        for row in raw_data:
            # Reemplazamos valores None por cadenas vacías
            dto = StudentDTO(
                first_name=str(row.get(H.FIRST_NAME) or "").strip(),
                last_name=str(row.get(H.LAST_NAME) or "").strip(),
                email=str(row.get(H.EMAIL) or "").strip(),
                password="temporal",  # se puede generar temporalmente si no viene
                ci=str(row.get(H.CI) or "").strip(),
                expedito_ci=str(row.get(H.EXPEDITO_CI) or "").strip(),
                fecha_nacimiento=self.parse_date(row.get(H.BIRTHDATE)),
                phone_number=None,  # no está en el Excel
                school_id=None,  # no está en el Excel, usamos colegio como string
                course=str(row.get(H.COURSE) or "").strip(),
                department=str(row.get(H.DEPARTMENT) or "").strip(),
                province=str(row.get(H.PROVINCE) or "").strip(),
            )
            students.append(dto)

        return students
