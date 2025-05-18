from typing import List, Dict, Any
from modules.ExcelLoader.students.ExcelStudentLoader import ExcelStudentLoader
from modules.delegations.application.AssignStudentToDelegation import AssignStudentToDelegation
from modules.delegations.domain.DelegationRepository import DelegationRepository
from modules.schools.application.FindSchoolByName import FindSchoolByName
from modules.schools.application.SchoolCreator import SchoolCreator
from modules.schools.application.dtos.SchoolDTO import SchoolDTO
from modules.user.application.GetUserByEmail import GetUserByEmail
from modules.students.application.GetStudentByCI import GetStudentByCI
from modules.students.application.dtos.StudentDTO import StudentDTO
from modules.students.application.StudentCreator import StudentCreator

class BulkStudentDelegationAdder:

    def __init__(
        self,
        school_finder: FindSchoolByName,
        school_creator: SchoolCreator,
        user_email_checker: GetUserByEmail,
        student_ci_checker: GetStudentByCI,
        student_creator: StudentCreator,
        add_delegation: AssignStudentToDelegation
    ):
        self.school_finder = school_finder
        self.school_creator = school_creator
        self.user_email_checker = user_email_checker
        self.student_ci_checker = student_ci_checker
        self.student_creator = student_creator
        self.add_delegation = add_delegation

        self.colegios_de_excel: List[Dict[str, Any]] = []  # [{"id": int, "name": str}]
        self.observaciones: List[Dict[str, str]] = []      # [{"observacion": str, "motivo": str}]

    def execute(self, excel_file, delegacion_id: int):
        loader = ExcelStudentLoader(excel_file)
        students_data = loader.load()

        for student_data in students_data:
            email = student_data.get("email")
            ci = student_data.get("ci")
            school_name = student_data.get("school_name")

            # 1. Validar si el email ya está registrado
            if self.user_email_checker.execute(email):
                self.observaciones.append({"observacion": email, "motivo": "El correo ya fue registrado"})
                continue

            # 2. Validar si el CI ya está registrado
            if self.student_ci_checker.execute(ci):
                self.observaciones.append({"observacion": ci, "motivo": "La cédula de identidad ya fue registrada"})
                continue

            # 3. Buscar o crear el colegio
            school_id = self.get_or_create_school(school_name)

            # 4. Crear DTO y asignar colegio y delegación
            student_dto = StudentDTO(**student_data)
            student_dto.school_id = school_id
            # Aquí puedes también agregar el delegacion_id al DTO si tu modelo lo requiere

            # 5. Registrar estudiante
            student_registed = self.student_creator.create_student(student_dto)

            # 6. Agregar a Delegacion
            self.add_delegation.execute(delegacion_id, student_registed.id)

        return self.observaciones


    def get_or_create_school(self, school_name: str) -> int:
        # Verificar si el colegio ya está en la lista cargada desde el Excel
        for colegio in self.colegios_de_excel:
            if colegio["name"].lower() == school_name.lower():
                return colegio["id"]

        # Buscar en la base de datos
        found_school = self.school_finder.execute(school_name)
        if found_school:
            self.colegios_de_excel.append({"id": found_school.id, "name": found_school.name})
            return found_school.id

        # Crear nuevo colegio si no existe
        nuevo_dto = SchoolDTO(name=school_name)
        nuevo_school = self.school_creator.execute(nuevo_dto)
        self.colegios_de_excel.append({"id": nuevo_school.id, "name": nuevo_school.name})
        return nuevo_school.id
