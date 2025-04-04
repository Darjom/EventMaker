from pydantic import BaseModel
from typing import Optional, List

class UserDTO(BaseModel):
    id: Optional[int] = None
    first_name: Optional[str]
    last_name: str
    email: str
    roles: List[str]

    @classmethod
    def from_domain(cls, user):
        return cls(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            roles=user.roles
        )