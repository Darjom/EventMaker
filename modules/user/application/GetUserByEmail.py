from modules.user.application.dtos.UserDTO import UserDTO
from modules.user.domain.UserRepository import UserRepository


class GetUserByEmail:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, user_email: str) -> UserDTO | None:
        user = self.repository.find_by_email(email=user_email)
        if user is None:
            return None
        return UserDTO.from_domain(user)