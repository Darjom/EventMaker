from .AssignStudentToDelegation import AssignStudentToDelegation
from ..domain.DelegationRepository import DelegationRepository
from ...user.application.GetUserByEmail import GetUserByEmail
from ...user.domain.UserRepository import UserRepository


class AssignStudentToDelegationByEmail:
    def __init__(self, repository: DelegationRepository, repository_user: UserRepository):
        self.__repository = repository
        self.__repository_user = repository_user

    def execute(self, delegation_id: int, student_email: str) -> int:
        student = GetUserByEmail(self.__repository_user).execute(student_email)

        if student is None:
            return 0  # No existe un usuario con ese correo

        if not isinstance(student.roles, list) or "student" not in student.roles:
            return 3  # El usuario no tiene rol de estudiante

        success = AssignStudentToDelegation(self.__repository).execute(delegation_id, student.id)

        return 1 if success else 2  # 1: agregado, 2: ya estaba
