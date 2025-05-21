from typing import List

from werkzeug.security import generate_password_hash

from modules.user.domain.User import User
from datetime import datetime
from modules.user.domain.UserRepository import UserRepository
from modules.roles.application.RoleQueryService import RoleQueryService
from .dtos.UserDTO import UserDTO

class UserCreator:
    def __init__(self, user_repo: UserRepository, role_query_service: RoleQueryService):
        self.user_repo = user_repo
        self.role_query_service = role_query_service

    def execute(
        self,
        role_ids: List[int],  # Lista de IDs de roles
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        ci: str,
        expedito_ci: str | None = None,
        fecha_nacimiento: datetime | None = None

    ) -> UserDTO:
        # Validar campos requeridos
        if not first_name.strip():
            raise ValueError("El campo 'first_name' es requerido")
        if not email.strip():
            raise ValueError("El campo 'email' es requerido")
        if not password.strip():
            raise ValueError("El campo 'password' es requerido")

        # Validar existencia de roles
        for role_id in role_ids:
            if not self.role_query_service.execute(role_id):
                raise ValueError(f"Rol con ID {role_id} no existe")

        # Crear entidad User
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=generate_password_hash(password),  # Deberías hashear la contraseña aquí
            roles=[],  # Los roles se asignan después de crear el usuario
            ci=ci,
            expedito_ci=expedito_ci,
            fecha_nacimiento=fecha_nacimiento
        )

        # Persistir usuario
        saved_user = self.user_repo.save(user)

        # Asignar roles al usuario
        self.user_repo.add_roles_to_user(
            user_id=saved_user.id,
            role_ids=role_ids
        )

        # Obtener usuario actualizado con roles
        user_with_roles = self.user_repo.find_by_id(saved_user.id)
        return UserDTO.from_domain(user_with_roles)