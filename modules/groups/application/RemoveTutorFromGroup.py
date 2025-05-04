from modules.groups.domain.GroupRepository import GroupRepository


class RemoveTutorFromGroup:
    def __init__(self, repository: GroupRepository):
        self.__repository = repository


    def execute(self,tutor_id: int, group_id: int) -> bool:
         resp = self.__repository.remove_tutor_from_group(tutor_id, group_id)

         """
         Returns:
                True if the tutor was removed.
                False if the tutor was not found in the group or if group/tutor doesn't exist.
         """

         return resp