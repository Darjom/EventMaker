
from modules.permissions.infrastructure.persistence.PermissionMapping import PermissionMapping
from shared.extensions import db


class PermissionService:
    @staticmethod
    def get_or_create(name: str, description: str) -> PermissionMapping:
        perm = PermissionMapping.query.filter_by(name=name).first()
        if not perm:
            perm = PermissionMapping(name=name, description=description)
            db.session.add(perm)
            db.session.flush()  # asigna id sin commitear
        return perm

    @staticmethod
    def all_names() -> set[str]:
        return {p.name for p in PermissionMapping.query.all()}
