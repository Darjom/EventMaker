# permissions/domain/PermissionsRepository.py

from abc import ABC, abstractmethod

class PermissionsRepository(ABC):
    @abstractmethod
    def save(self, permission) -> None:
        pass

    @abstractmethod
    def find_by_name(self, name: str):
        pass

    @abstractmethod
    def delete(self, permission) -> None:
        pass