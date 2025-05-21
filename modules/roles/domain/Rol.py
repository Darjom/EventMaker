# src/roles/domain/Rol.py
from typing import Optional, List


class Rol:
    """
    Entidad de dominio pura (sin SQLAlchemy).
    """
    def __init__(self, id: Optional[int] = None, name: str = "", description: str = "", permissions: Optional[List[str]] = None):
        self.id = id
        self._name = name
        self._description = description
        self._permissions = permissions or []

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def permissions(self):
        return self._permissions
