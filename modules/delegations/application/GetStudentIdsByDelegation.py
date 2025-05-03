from modules.delegations.domain.DelegationRepository import DelegationRepository
from modules.students.application.GetStudentsByListIds import GetStudentsByListIds
from modules.students.domain.StudentRepository import StudentRepository


class GetStudentIdsByDelegation:
    def __init__(self, delegation_repository: DelegationRepository, student_repository: StudentRepository):
        self.__delegation_repository = delegation_repository
        self.__student_repository = student_repository

    def execute(self, delegation_id: int):
        list_ids = self.__delegation_repository.get_student_ids_by_delegation_id(delegation_id)
        students = GetStudentsByListIds(self.__student_repository).execute(list_ids)
        return students
