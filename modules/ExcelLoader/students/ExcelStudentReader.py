import openpyxl
from typing import List, Dict, IO
from modules.ExcelLoader.students.StudentExcelHeaders import StudentExcelHeaders as H


class ExcelStudentReader:
    def __init__(self, file: IO):
        self.file = file

    def validate_row_data(self, row_dict: Dict[str, str]) -> bool:
        """Valida que todos los campos no sean vacíos o nulos, excepto el campo 'COMPLEMENTO'."""
        for key, value in row_dict.items():
            if key == H.COMPLEMENTO.value:
                continue  # este campo es opcional
            if value is None or str(value).strip() == "":
                raise ValueError("")
        return True

    def read(self) -> List[Dict[str, str]]:
        workbook = openpyxl.load_workbook(self.file)
        sheet = workbook.active

        headers = [cell.value for cell in sheet[2]]
        self.headers = headers  # guardamos para validación posterior
        data = []

        for row in sheet.iter_rows(min_row=3, values_only=True):
            row_dict = {headers[i]: (row[i] if i < len(row) else None) for i in range(len(headers))}
            try:
                if self.validate_row_data(row_dict):
                    data.append(row_dict)
            except ValueError as e:
                print(f"Fila omitida: {e}")

        return data

    def get_headers(self) -> List[str]:
        if not hasattr(self, 'headers'):
            self.read()  # asegura que headers estén disponibles
        return self.headers
