from ..domain.GroupRepository import GroupRepository


class AssignGroupToTutor:
    def __init__(self, repository: GroupRepository):
        self.repository = repository

    def execute(self, group_id: int, tutor_id: int) -> None:
        """
        Assigns a tutor to an existing group

        Args:
            group_id: ID of the existing group
            tutor_id: ID of the tutor to assign
        """
        self.repository.assign_tutor_to_group(group_id, tutor_id)