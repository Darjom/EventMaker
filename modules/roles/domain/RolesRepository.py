
from  abc import ABC, abstractmethod
from typing import List

from modules.roles.domain.Rol import Rol


class RolesRepository(ABC):

    @abstractmethod
    def save(self, role: Rol) -> None:
        pass

    @abstractmethod
    def find_by_id(self, role_id : int) -> Rol:
        pass

    @abstractmethod
    def find_all(self) -> List[Rol]:
        pass