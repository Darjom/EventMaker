from modules.tutors.domain.TutorRepository import TutorRepository


class GetTutorPermissionsInDelegation:
    def __init__(self, repository: TutorRepository):
        self.__repository = repository

    def execute(self, tutor_id: int, delegation_id: int) :

        permissions = self.__repository.get_delegation_permissions(tutor_id, delegation_id)
        lista =[]
        for permission in permissions:
            lista.append(permission.name)
        return lista