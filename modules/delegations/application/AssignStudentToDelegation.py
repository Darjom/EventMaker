from ..domain.DelegationRepository import DelegationRepository

class AssignStudentToDelegation:
    def __init__(self, repository: DelegationRepository):
        self.repository = repository

    def execute(self, delegation_id: int, student_id: int) -> bool:
        """
        Assigns a student to a delegation.

        Returns:
            True if the student was newly associated.
            False if the student was already associated.
        """
        return self.repository.assign_student_to_delegation(delegation_id, student_id)
