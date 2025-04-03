# src/roles/domain/Rol.py
from typing import Optional

class Rol:
    """
    Entidad de dominio pura (sin SQLAlchemy).
    """
    def __init__(self, id: Optional[int] = None, name: str = "", description: str = "", permission: Optional[str] = None):
        self.id = id
        self._name = name
        self._description = description
        self._permission = permission or []


    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    def permission(self):
        return self._permission

    def can_edit(self):
        # Ejemplo de lógica de dominio
        return self._name == "superuser"