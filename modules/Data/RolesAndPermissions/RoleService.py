from modules.roles.infrastructure.persistence.RolMapping import RolMapping
from shared.extensions import db


class RoleService:
    @staticmethod
    def get_or_create(name: str, description: str = "") -> RolMapping:
        role = RolMapping.query.filter_by(name=name).first()
        if not role:
            role = RolMapping(name=name, description=description)
            db.session.add(role)
            db.session.flush()
        return role

    @staticmethod
    def assign_permission(role: RolMapping, permission):
        if permission not in role.permissions:
            role.permissions.append(permission)
