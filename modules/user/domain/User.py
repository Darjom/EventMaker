from typing import Optional, List
from datetime import datetime



class User:
    def __init__(
        self,
        id: Optional[int] = None,
        first_name: Optional[str] = None,
        last_name: str = "",
        email: str = "",
        password: str = "",
        active: bool = True,
        confirmed_at: Optional[datetime] = None,
        fs_uniquifier: Optional[str] = None,
        roles: Optional[List[str]] = None,
        ci=None,
        expedito_ci=None,
        fecha_nacimiento=None

    # Lista de nombres de roles
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.active = active
        self.confirmed_at = confirmed_at
        self.fs_uniquifier = fs_uniquifier
        self.roles = roles or []
        self.ci = ci
        self.expedito_ci = expedito_ci
        self.fecha_nacimiento = fecha_nacimiento

    def has_role(self, role_name: str) -> bool:
        """Verifica si el usuario tiene un rol específico."""
        return role_name in self.roles
