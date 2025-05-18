from ..domain.GroupRepository import GroupRepository


class AssignGroupToStudent:
    def __init__(self, repository: GroupRepository):
        self.repository = repository

    def execute(self, group_id: int, student_id: int) -> None:
        """
        Assigns a student to an existing group

        Args:
            group_id: ID of the existing group
            student_id: ID of the tutor to assign
        """
        self.repository.assign_student_to_group(group_id, student_id)
