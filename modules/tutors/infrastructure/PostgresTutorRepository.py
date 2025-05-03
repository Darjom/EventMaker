from typing import List

from modules.delegations.infrastructure.persistence.DelegationTutorMapping import DelegationTutorMapping
from modules.permissions.domain.Permission import Permission
from modules.permissions.infrastructure.persistence.PermissionMapping import PermissionMapping
from modules.roles.infrastructure.persistence.RolMapping import RolMapping, roles_permissions
from modules.tutors.domain.Tutor import Tutor
from modules.tutors.domain.TutorRepository import TutorRepository
from modules.user.infrastructure.persistence.UserMapping import UserMapping
from shared.extensions import db

class PostgresTutorRepository(TutorRepository):

    def save(self, tutor: Tutor) -> None:
        tutor_mapping = UserMapping.from_domain(tutor)
        db.session.add(tutor_mapping)
        db.session.commit()
        return tutor_mapping.to_domain()

    def add_roles_to_user(self, tutor_id: int, role_ids: List[int]) -> None:
        print("user ", tutor_id)
        tutor_mapping = db.session.query(UserMapping).get(tutor_id)
        if not tutor_mapping:
            raise ValueError(f"Usuario con ID {tutor_id} no encontrado")

        roles = db.session.query(RolMapping).filter(RolMapping.id.in_(role_ids)).all()
        found_ids = {role.id for role in roles}
        missing = set(role_ids) - found_ids
        if missing:
            raise ValueError(f"Roles no encontrados: {missing}")

        tutor_mapping.roles.extend(roles)
        db.session.commit()

    def find_by_email(self, email: str):
        tutor_mapping = db.session.query(UserMapping).filter_by(email=email).first()
        if tutor_mapping:
            return tutor_mapping.to_domain()
        return None

    def find_by_id(self, id: int):
        tutor_mapping = db.session.query(UserMapping).filter_by(id=id).first()
        if tutor_mapping:
            return tutor_mapping.to_domain()
        return None
    
    def find_by_ci(self, ci: int):
        tutor_mapping = db.session.query(UserMapping).filter_by(ci=ci).first()
        if tutor_mapping:
            return tutor_mapping.to_domain()
        return None

    def get_delegation_permissions(self, tutor_id: int, delegation_id: int) -> List[Permission]:
        """
        Obtiene los permisos de un tutor en una delegación específica

        Args:
            tutor_id (int): ID del tutor
            delegation_id (int): ID de la delegación

        Returns:
            List[Permission]: Lista de objetos Permission con todos sus atributos
        """
        # Obtener los permisos con todos sus campos
        permissions = (
            db.session.query(PermissionMapping)
            .select_from(DelegationTutorMapping)
            .join(RolMapping, DelegationTutorMapping.role_id == RolMapping.id)
            .join(roles_permissions, RolMapping.id == roles_permissions.c.role_id)
            .join(PermissionMapping, roles_permissions.c.permission_id == PermissionMapping.id)
            .filter(
                DelegationTutorMapping.tutor_id == tutor_id,
                DelegationTutorMapping.delegation_id == delegation_id
            )
            .distinct()
            .all()
        )
        # Convertir a objetos de dominio con todos los atributos
        return [p.to_domain() for p in permissions]
