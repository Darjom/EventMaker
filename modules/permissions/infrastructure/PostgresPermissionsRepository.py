# permissions/infrastructure/PostgresPermissionsRepository.py
from modules.permissions.domain.Permission import Permission
from modules.permissions.domain.PermissionsRepository import PermissionsRepository
from modules.permissions.infrastructure.persistence.PermissionMapping import PermissionMapping


class PostgresPermissionsRepository(PermissionsRepository):
    def __init__(self, db_session):
        self.db_session = db_session

    def save(self, permission: Permission) -> None:
        permission_mapping = PermissionMapping.from_domain(permission)
        self.db_session.add(permission_mapping)
        self.db_session.commit()

    def find_by_name(self, name: str) -> Permission:
        permission_mapping = self.db_session.query(PermissionMapping).filter_by(name=name).first()
        if permission_mapping:
            return permission_mapping.to_domain()
        return None

    def delete(self, permission: Permission) -> None:
        permission_mapping = self.db_session.query(PermissionMapping).filter_by(name=permission.name).first()
        if permission_mapping:
            self.db_session.delete(permission_mapping)
            self.db_session.commit()
