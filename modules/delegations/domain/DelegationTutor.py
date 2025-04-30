
class DelegationTutor:
    def __init__(
            self,
            delegation_id: int,
            tutor_id: int,
            role_id: int
    ):
        self.delegation_id = delegation_id
        self.tutor_id = tutor_id
        self.role_id = role_id

        self._validate()

    def _validate(self):
        if not all([self.delegation_id, self.tutor_id, self.role_id]):
            raise ValueError("Todos los IDs son requeridos")

    def __str__(self):
        return f"DelegationTutor({self.delegation_id}, {self.tutor_id}, {self.role_id})"