from modules.user.application.dtos.UserDTO import UserDTO
from modules.user.domain.UserRepository import UserRepository


class GetUserById:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, user_id: int) -> UserDTO | None:
        user = self.repository.find_by_id(user_id)
        if user is None:
            return None
        return UserDTO.from_domain(user)