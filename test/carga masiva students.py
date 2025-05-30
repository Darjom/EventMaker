import os
from modules.ExcelLoader.students.ExcelStudentLoader import ExcelStudentLoader


def test_load_students_from_excel(excel_file_path: str):
    """
    Prueba la carga de estudiantes desde un archivo Excel.
    Imprime la lista de diccionarios con los datos de los estudiantes.
    """
    if not os.path.exists(excel_file_path):
        print(f"❌ Archivo no encontrado: {excel_file_path}")
        return

    try:
        with open(excel_file_path, "rb") as f:
            loader = ExcelStudentLoader(f)
            students = loader.load()  # Ahora es List[dict]

            print(f"✅ Se cargaron {len(students)} estudiantes.")
            for i, student in enumerate(students, 1):
                print(f"\nEstudiante #{i}")
                # student es un diccionario con los campos
                for key, value in student.items():
                    print(f"{key}: {value}")

    except ValueError as e:
        print(f"⚠️ Error durante la carga: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    # Reemplaza esta ruta con la ubicación real de tu archivo Excel
    ruta_excel = "/Users/jose/Documents/Pycharm/EventMaker/test/Registrar estudiantes-2.xlsx"
    test_load_students_from_excel(ruta_excel)
