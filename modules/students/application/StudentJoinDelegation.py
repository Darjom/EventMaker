from modules.delegations.application.AssignStudentToDelegation import AssignStudentToDelegation
from modules.delegations.domain.DelegationRepository import DelegationRepository
from modules.user.domain.UserRepository import UserRepository


class StudentJoinDelegation:
    USER_NOT_FOUND = 0
    NOT_A_STUDENT = 1
    DELEGATION_NOT_FOUND = 2
    SUCCESSFULLY_ASSOCIATED = 3
    ALREADY_ASSOCIATED = 4

    def __init__(self, user_repository: UserRepository, delegation_repository: DelegationRepository):
        self.__user_repository = user_repository
        self.__delegation_repository = delegation_repository

    def execute(self, code: str, student_id: int) -> int:
        # Verifica si el usuario existe
        student = self.__user_repository.get_by_id(student_id)
        if student is None:
            return self.USER_NOT_FOUND

        # Verifica si el usuario tiene rol de estudiante
        if not isinstance(student.roles, list) or "student" not in student.roles:
            return self.NOT_A_STUDENT

        # Verifica si la delegación existe a partir del código
        delegation = self.__delegation_repository.find_by_code(code)
        if delegation is None:
            return self.DELEGATION_NOT_FOUND

        # Intenta asociar al estudiante a la delegación
        assigner = AssignStudentToDelegation(self.__delegation_repository)
        was_associated = assigner.execute(delegation.id_delegacion, student_id)

        if was_associated:
            return self.SUCCESSFULLY_ASSOCIATED
        else:
            return self.ALREADY_ASSOCIATED
