
from  abc import ABC, abstractmethod
from typing import List, Optional

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

    @abstractmethod
    def find_by_name(self, role_name: str) -> Optional[Rol]:
        pass
