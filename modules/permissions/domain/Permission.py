# permissions/domain/Permission.py
from typing import Optional


class Permission:
    def __init__(self,  id: Optional[int] = None, name: str = "", description: str = ""):
        self.id = id
        self.name = name
        self.description = description

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description

    def __eq__(self, other):
        if not isinstance(other, Permission):
            return False
        return self.name == other.name and self.description == other.description